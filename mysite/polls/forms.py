from django import forms


class PollCreateForm(forms.Form):
    question_text = forms.CharField(max_length=200, label="Question")
    choices = forms.CharField(
        label="Choices",
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "placeholder": "One choice per line\nYes\nNo\nMaybe",
            }
        ),
        help_text="Insert at least two choices, one per line.",
    )

    def clean_choices(self):
        raw_value = self.cleaned_data["choices"]
        items = [line.strip() for line in raw_value.splitlines() if line.strip()]

        deduplicated = list(dict.fromkeys(items))
        if len(deduplicated) < 2:
            raise forms.ValidationError("Please provide at least two distinct choices.")

        return deduplicated
