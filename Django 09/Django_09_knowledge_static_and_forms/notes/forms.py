from django import forms


class NoteForm(forms.Form):
    CATEGORY_CHOICES = {
        'backend':'Backend',
        'forms':'Forms',
        'models':'Models',
        'frontend':'Frontend',
    }
    title = forms.CharField(
        label='Ad',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder':'Adı daxil edin'}), required=True)
    content = forms.CharField(
        label='Mətn',
        min_length=20,
        widget=forms.Textarea(attrs={'placeholder':"Qeydin mətni", "rows":"6"}))
    tags = forms.CharField(
        label="Teqlər",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder':'Məsələn: django python'})
    )
    category = forms.ChoiceField(label="Kateqoriya", choices=CATEGORY_CHOICES)

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if title.lower().strip().startswith('test'):
            raise forms.ValidationError("Ad test sözü ilə başlaya bilməz")
        return title



FORBIDDEN_WORDS = ["niga", "niger", "spam", "virus"]


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Name"
    )

    email = forms.EmailField(
        label="Email"
    )

    message = forms.CharField(
        widget=forms.Textarea,
        label="Message"
    )

    def clean_name(self):
        name = self.cleaned_data["name"]

        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(
                    f"The word '{word}' is not allowed."
                )

        return name

    def clean_message(self):
        message = self.cleaned_data["message"]

        for word in FORBIDDEN_WORDS:
            if word in message.lower():
                raise forms.ValidationError(
                    f"The word '{word}' is not allowed."
                )

        return message