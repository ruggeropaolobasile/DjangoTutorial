param(
    [string]$Owner = "ruggeropaolobasile",
    [int]$ProjectNumber = 1,
    [string]$Profile = "autonomous",
    [int]$MaxItems = 0,
    [int]$MaxAttemptsPerItem = 2,
    [switch]$SkipPreflight,
    [switch]$CommitOnDone
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
    $root = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($root)) {
        throw "Current directory is not a git repository."
    }

    return $root.Trim()
}

function Assert-CleanWorktree {
    param(
        [string]$RepoRoot,
        [string]$Message
    )

    $status = git -C $RepoRoot status --porcelain
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to read git status."
    }

    if (-not [string]::IsNullOrWhiteSpace(($status | Out-String))) {
        throw $Message
    }
}

function Get-RequiredCommand {
    param(
        [string]$Name
    )

    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if (-not $command) {
        throw "Required command '$Name' was not found in PATH."
    }

    return $command
}

function Get-ProjectData {
    param(
        [string]$Owner,
        [int]$ProjectNumber
    )

    $projectJson = gh project view $ProjectNumber --owner $Owner --format json
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to read project metadata."
    }

    $fieldsJson = gh project field-list $ProjectNumber --owner $Owner --format json
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to read project fields."
    }

    $itemsJson = gh project item-list $ProjectNumber --owner $Owner --limit 100 --format json
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to read project items."
    }

    return @{
        Project = $projectJson | ConvertFrom-Json
        Fields = $fieldsJson | ConvertFrom-Json
        Items = $itemsJson | ConvertFrom-Json
    }
}

function Get-FieldMap {
    param(
        [object]$ProjectData,
        [object]$FieldsData
    )

    if (-not $ProjectData.id) {
        throw "Project id not found in project metadata."
    }

    $statusField = $FieldsData.fields | Where-Object { $_.name -eq "Status" }
    if (-not $statusField) {
        throw "Project field 'Status' not found."
    }

    $optionMap = @{}
    foreach ($option in $statusField.options) {
        $optionMap[$option.name] = $option.id
    }

    return @{
        ProjectId = $ProjectData.id
        StatusFieldId = $statusField.id
        StatusOptions = $optionMap
    }
}

function Get-NextTodoItem {
    param(
        [object]$ItemsData
    )

    $priorityRank = @{
        "P0" = 0
        "P1" = 1
        "P2" = 2
    }
    $sizeRank = @{
        "XS" = 0
        "S" = 1
        "M" = 2
        "L" = 3
        "XL" = 4
    }

    return $ItemsData.items |
        Where-Object { $_.status -eq "Todo" } |
        Sort-Object `
            @{ Expression = { $priorityRank[$_.priority] } ; Ascending = $true }, `
            @{ Expression = { $sizeRank[$_.size] } ; Ascending = $true }, `
            @{ Expression = { $_.title } ; Ascending = $true } |
        Select-Object -First 1
}

function Set-ProjectItemStatus {
    param(
        [string]$ItemId,
        [string]$Status,
        [hashtable]$FieldMap
    )

    $statusOptionId = $FieldMap.StatusOptions[$Status]
    if (-not $statusOptionId) {
        throw "Status option '$Status' not found in project metadata."
    }

    gh project item-edit `
        --id $ItemId `
        --project-id $FieldMap.ProjectId `
        --field-id $FieldMap.StatusFieldId `
        --single-select-option-id $statusOptionId | Out-Null

    if ($LASTEXITCODE -ne 0) {
        throw "Unable to set status '$Status' on item '$ItemId'."
    }
}

function Invoke-Preflight {
    param(
        [string]$RepoRoot
    )

    $preflightScript = Join-Path $RepoRoot "scripts\preflight.ps1"
    if (-not (Test-Path $preflightScript)) {
        throw "Preflight script not found at $preflightScript."
    }

    & $preflightScript
    if ($LASTEXITCODE -ne 0) {
        throw "Preflight failed."
    }
}

function Get-CommitMessagePrefix {
    param(
        [string]$Title
    )

    $lower = $Title.ToLowerInvariant()
    if ($lower.StartsWith("fix") -or $lower.Contains("stabilize") -or $lower.Contains("verify")) {
        return "fix"
    }

    if ($lower.StartsWith("chore") -or $lower.Contains("docs") -or $lower.Contains("project")) {
        return "chore"
    }

    return "feat"
}

function New-TaskPrompt {
    param(
        [object]$Item,
        [int]$Attempt,
        [string]$RecoveryNotes
    )

    $body = ""
    if ($Item.content -and $Item.content.body) {
        $body = $Item.content.body.Trim()
    }

    $recoverySection = ""
    if (-not [string]::IsNullOrWhiteSpace($RecoveryNotes)) {
        $recoverySection = @"
Recovery from previous attempt:
$RecoveryNotes

"@
    }

    return @"
Segui AGENTS.md e i playbook pertinenti in agent-docs/.

Task dal backlog canonico GitHub Project:
Title: $($Item.title)
Priority: $($Item.priority)
Size: $($Item.size)
Attempt: $Attempt/$MaxAttemptsPerItem

$recoverySection
Issue body / acceptance context:
$body

Vincoli operativi:
- usa il clone e il branch gia attivi; non cambiare branch
- applica il loop modifica -> verifica -> fix -> riverifica
- esegui i check minimi richiesti dai file AGENTS applicabili
- mantieni cambi piccoli e mirati
- se il task e bloccato da decisioni mancanti, non forzare workaround deboli

Output finale obbligatorio:
- rispondi SOLO con JSON valido conforme allo schema fornito
- status deve essere uno tra: done, blocked, needs_input, failed
- summary deve spiegare in una frase cosa e successo
- tests_run deve elencare i controlli eseguiti
- notes puo contenere blocker, rischi residui o il motivo del fallimento
"@
}

Get-RequiredCommand -Name "git" | Out-Null
Get-RequiredCommand -Name "gh" | Out-Null
Get-RequiredCommand -Name "codex" | Out-Null

$repoRoot = Get-RepoRoot
Assert-CleanWorktree -RepoRoot $repoRoot -Message "Working tree is not clean. Commit or stash changes before starting the autonomous session."

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$schemaPath = Join-Path $scriptDir "autonomous-session.schema.json"
if (-not (Test-Path $schemaPath)) {
    throw "Schema file not found at $schemaPath."
}

$processed = 0

while ($true) {
    if ($MaxItems -gt 0 -and $processed -ge $MaxItems) {
        Write-Host "Reached MaxItems=$MaxItems. Stopping." -ForegroundColor Yellow
        break
    }

    Assert-CleanWorktree -RepoRoot $repoRoot -Message "Working tree became dirty before picking the next item. Stop, review changes, then resume."

    $projectData = Get-ProjectData -Owner $Owner -ProjectNumber $ProjectNumber
    $fieldMap = Get-FieldMap -ProjectData $projectData.Project -FieldsData $projectData.Fields
    $item = Get-NextTodoItem -ItemsData $projectData.Items

    if (-not $item) {
        Write-Host "No Todo items left in project $ProjectNumber." -ForegroundColor Green
        break
    }

    Write-Host "Picked item: $($item.title) [$($item.priority)/$($item.size)]" -ForegroundColor Cyan
    Set-ProjectItemStatus -ItemId $item.id -Status "In progress" -FieldMap $fieldMap

    $attempt = 1
    $recoveryNotes = ""
    $completed = $false
    $restoreTodoOnError = $true

    try {
        while ($attempt -le $MaxAttemptsPerItem -and -not $completed) {
            $outputFile = Join-Path $env:TEMP ("codex-autonomous-output-{0}.json" -f ([guid]::NewGuid().ToString("N")))
            $prompt = New-TaskPrompt -Item $item -Attempt $attempt -RecoveryNotes $recoveryNotes

            $prompt | codex exec --cd $repoRoot -p $Profile --output-schema $schemaPath -o $outputFile -
            $codexExitCode = $LASTEXITCODE

            if ($codexExitCode -ne 0) {
                throw "codex exec failed for item '$($item.title)' with exit code $codexExitCode."
            }

            $result = Get-Content $outputFile -Raw | ConvertFrom-Json
            Remove-Item $outputFile -ErrorAction SilentlyContinue

            Write-Host "Codex status: $($result.status) - $($result.summary)" -ForegroundColor DarkCyan

            switch ($result.status) {
                "done" {
                    if (-not $SkipPreflight) {
                        try {
                            Invoke-Preflight -RepoRoot $repoRoot
                        }
                        catch {
                            $recoveryNotes = "Preflight failed after attempt $attempt. Fix the root cause and rerun. Error: $($_.Exception.Message)"
                            $attempt += 1
                            continue
                        }
                    }

                    if ($CommitOnDone) {
                        $worktreeStatus = git -C $repoRoot status --porcelain
                        if ($LASTEXITCODE -ne 0) {
                            throw "Unable to read git status after task completion."
                        }

                        if (-not [string]::IsNullOrWhiteSpace(($worktreeStatus | Out-String))) {
                            $prefix = Get-CommitMessagePrefix -Title $item.title
                            git -C $repoRoot add -A
                            if ($LASTEXITCODE -ne 0) {
                                throw "git add failed after task completion."
                            }

                            git -C $repoRoot commit -m "${prefix}: $($item.title)"
                            if ($LASTEXITCODE -ne 0) {
                                throw "git commit failed after task completion."
                            }
                        }
                    }

                    Set-ProjectItemStatus -ItemId $item.id -Status "Done" -FieldMap $fieldMap
                    $restoreTodoOnError = $false
                    $processed += 1
                    $completed = $true
                }
                "blocked" {
                    Set-ProjectItemStatus -ItemId $item.id -Status "Todo" -FieldMap $fieldMap
                    $restoreTodoOnError = $false
                    $processed += 1
                    $completed = $true
                }
                "needs_input" {
                    Set-ProjectItemStatus -ItemId $item.id -Status "Todo" -FieldMap $fieldMap
                    $restoreTodoOnError = $false
                    Write-Host "Task requires user input. Stopping loop." -ForegroundColor Yellow
                    return
                }
                "failed" {
                    if ($attempt -ge $MaxAttemptsPerItem) {
                        throw "Task '$($item.title)' failed after $attempt attempt(s). Notes: $($result.notes)"
                    }

                    $recoveryNotes = "Previous attempt reported failed. Summary: $($result.summary)`nNotes: $($result.notes)"
                    $attempt += 1
                }
                default {
                    throw "Unknown task status '$($result.status)'."
                }
            }
        }

        if (-not $completed) {
            throw "Task '$($item.title)' did not reach a terminal state."
        }
    }
    catch {
        if ($restoreTodoOnError) {
            Set-ProjectItemStatus -ItemId $item.id -Status "Todo" -FieldMap $fieldMap
        }

        throw
    }
}
