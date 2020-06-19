from django import forms

class ImageForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = 'image'