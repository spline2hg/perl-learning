

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from .models import *

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm_password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email','user_type']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords dont match')
        return password2

    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email']

class LearnerProfileForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    banner_image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'hidden'}),
        required=False
    )

    class Meta:
        model = LearnerProfile
        fields = ['profile_image','banner_image','interests', 'age', 'location','linkedin_url', 'github_url', 'website', 'bio', 'phone','best_describe']

        widgets = {
            'experience': forms.NumberInput(attrs={'min': 0, 'class': 'form-field'}),
            'bio': forms.Textarea(attrs={'rows': 2, 'cols': 50, 'class': 'form-field'}),

        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].widget.attrs.update({'class': 'hidden'})
        self.fields['banner_image'].widget.attrs.update({'class': 'hidden'})


class EducatorProfileForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    banner_image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'hidden'}),
        required=False
    )

    class Meta:
        model = EducatorProfile
        # fields = ['profile_image','banner_image','subjects', 'qualification', 'experience', 'linkedin_url', 'github_url']
        fields = ['profile_image', 'banner_image', 'subjects', 'qualification', 'experience', 'location','linkedin_url', 'github_url', 'website', 'bio', 'phone','best_describe']

        widgets = {
            # 'qualification': forms.Textarea(attrs={'rows': 2, 'cols': 30}),  # Adjust rows and cols
            # 'experience': forms.NumberInput(attrs={'min': 0}),
            # 'bio': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
            'experience': forms.NumberInput(attrs={'min': 0, 'class': 'form-field'}),
            'bio': forms.Textarea(attrs={'rows': 2, 'cols': 50, 'class': 'form-field'}),
            # 'profile_image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
            # 'banner_image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].widget.attrs.update({'class': 'hidden'})
        self.fields['banner_image'].widget.attrs.update({'class': 'hidden'})

# class CreateMeetingForm(forms.ModelForm):
#     class Meta:
#         model = Classroom
#         fields = '__all__'


# class CreateMeetingForm(forms.ModelForm):
#     class Meta:
#         model = Classroom
#         fields = '__all__'
