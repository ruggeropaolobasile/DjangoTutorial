$ErrorActionPreference = "Stop"

$targets = Get-CimInstance Win32_Process | Where-Object {
    $_.Name -eq "chrome.exe" -and $_.CommandLine -like "*ms-playwright\\mcp-chrome*"
}

if (-not $targets) {
    Write-Host "No Playwright Chrome automation process found."
    exit 0
}

$count = 0
foreach ($proc in $targets) {
    try {
        Stop-Process -Id $proc.ProcessId -Force -ErrorAction Stop
        $count++
    } catch {
        # Ignore races when child processes exit while iterating.
    }
}

Write-Host "Stopped $count Playwright Chrome process(es)."
