from django import forms
from .models import Job, Review

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'category', 'description', 'required_skill',
            'city', 'location', 'pay_offered', 'pay_type',
            'duration', 'workers_required', 'contact_phone', 'contact_person', 'start_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Need 2 Painters for 2BHK Apartment'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe job scope, tools provided/required, timing, etc.'}),
            'required_skill': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Wall putty, primer coating'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'value': 'Bengaluru'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Indiranagar 100ft Road'}),
            'pay_offered': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '850.00'}),
            'pay_type': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1 Day (9 AM - 6 PM)'}),
            'workers_required': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 9876543210'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Site supervisor or employer name'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your honest review & experience...'}),
        }
