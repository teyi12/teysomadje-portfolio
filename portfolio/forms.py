from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your name",
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "you@example.com",
            }
        ),
    )

    message = forms.CharField(
        max_length=5000,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Tell me about your project...",
            }
        ),
    )

    website = forms.CharField(
        required=False,
        label="Leave this field empty",
        widget=forms.HiddenInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
            }
        ),
    )
