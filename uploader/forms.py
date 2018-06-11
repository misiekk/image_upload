from django import forms


class ImageForm(forms.Form):
    image = forms.ImageField()
    name = forms.CharField(max_length=100)
