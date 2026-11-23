from django import forms
from django.contrib.auth import get_user_model
from .models import WorkerProfile, ContractorProfile

User = get_user_model()

class WorkerRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=60, required=True, label="Full Name")
    password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=6)
    skills = forms.CharField(max_length=255, required=True, help_text="e.g. Electrician, Plumber, Mason")
    languages_known = forms.CharField(max_length=255, required=True, initial="Kannada, Hindi, English")
    expected_daily_wage = forms.DecimalField(max_digits=8, decimal_places=2, initial=750.00, label="Expected Wage per Day (₹)")
    experience_years = forms.DecimalField(max_digits=4, decimal_places=1, initial=2.0, label="Years of Experience")
    locality = forms.CharField(max_length=120, required=True, label="Area / Locality", initial="Indiranagar")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'phone_number', 'locality', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'WORKER'
        user.city = 'Bengaluru'
        if commit:
            user.save()
            WorkerProfile.objects.create(
                user=user,
                skills=self.cleaned_data['skills'],
                languages_known=self.cleaned_data['languages_known'],
                expected_daily_wage=self.cleaned_data['expected_daily_wage'],
                experience_years=self.cleaned_data['experience_years'],
            )
        return user


class ContractorRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=60, required=True, label="Contact Person Name")
    company_name = forms.CharField(max_length=150, required=True, label="Business or Household Name")
    business_type = forms.ChoiceField(
        choices=[
            ('Individual / Household', 'Individual / Household'),
            ('Construction Contractor', 'Construction Contractor'),
            ('Facility Management', 'Facility Management'),
            ('Interior & Renovation', 'Interior & Renovation'),
            ('Small Enterprise', 'Small Enterprise'),
        ]
    )
    password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=6)
    locality = forms.CharField(max_length=120, required=True, label="Area / Locality", initial="Koramangala")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'phone_number', 'locality', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'CONTRACTOR'
        user.city = 'Bengaluru'
        if commit:
            user.save()
            ContractorProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                business_type=self.cleaned_data['business_type'],
            )
        return user
