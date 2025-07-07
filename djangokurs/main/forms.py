from django import forms
from .models import *


class kursForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'images', 'isActive', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'isActive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            
        }


def validate_video(value):
    if not value.name.endswith(('.mp4', '.mov', '.avi', '.mkv')):
        raise forms.ValidationError("Sadece video dosyaları yükleyebilirsiniz.")

class VideoUploadForm(forms.Form):
    videos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=False,
        validators=[validate_video]
    )