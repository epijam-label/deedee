"""
Forms for Core
"""

from django import forms


class EmailCaptureForm(forms.Form):
    """
    Form to capture email.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )

    def write_email(self, download_card):
        """
        Writes the email onto the download card.
        """
        download_card.recipient_email = self.cleaned_data["email"]
        download_card.save()
