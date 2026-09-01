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
                "autocomplete": "name",
            }
        ),
    )

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "you@example.com",
                "autocomplete": "email",
                "inputmode": "email",
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
                "autocomplete": "off",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.is_bound:
            return

        for field_name in ("name", "email", "message"):
            if field_name not in self.errors:
                continue

            widget = self.fields[field_name].widget
            widget.attrs["aria-invalid"] = "true"
            widget.attrs["aria-describedby"] = f"id_{field_name}-error"

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
