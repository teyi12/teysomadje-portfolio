from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Your name"),
            }
        ),
    )

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "you@example.com",
            }
        ),
    )

    message = forms.CharField(
        label=_("Message"),
        max_length=5000,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": _("Tell me about your project..."),
            }
        ),
    )

    website = forms.CharField(
        required=False,
        label=_("Leave this field empty"),
        widget=forms.HiddenInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
            }
        ),
    )
