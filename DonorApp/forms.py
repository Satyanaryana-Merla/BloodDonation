"""Importing modules"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from DonorApp.models import BloodDonorDetailsmodel
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Define a custom user creation form


class CustomUserCreationForm(UserCreationForm):
    # role = forms.ChoiceField(choices=[
    #     # ('BD', 'Blood Donor'),
    #     ('HP', 'Hospital'),
    #     ('CP', 'Company'),
    # ])
    email = forms.EmailField(required=True, help_text=_('Required. Enter a valid email address.'))
    # groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.groups.set(self.cleaned_data['groups'])
        return user


# GENDER = (("Male", "Male"),
#           ("Female", "Female"),
#           ("Others", "Others"))

# # BLOODGROUP = (("A Positive"),
# #               ("A Negative", "A Negative"),
# #               ("A Unknown", "A Unknown"),
# #               ("B Positive", "B Positive"),
# #               ("B Negative", "B Negative"),
# #               ("B Unknown", "B Unknown"),
# #               ("AB Positive", "AB Positive"),
# #               ("AB Negative", "AB Negative"),
# #               ("AB Unknown", "AB Unknown"),
# #               ("O Positive", "O Positive"),
# #               ("O Negative", "O Negative"),
# #               ("O Unknown", "O Unknown"),
# #               ("Unknown", "Unknown"))


# class BloodDonorDetails(forms.Form):
#     """BloodDonorDetails"""
#     fullname = forms.CharField(max_length=100)
#     gender = forms.ChoiceField(choices=GENDER)
#     blood_group = forms.CharField(max_length=100)  # type: ignore
#     state = forms.CharField(max_length=100)
#     city = forms.CharField(max_length=100)
#     mobilenumber = forms.CharField(max_length=100)
#     last_time_blood_donated = forms.CharField(max_length=100)


class BloodDonorDetails(forms.ModelForm):
    """BloodDonorDetails"""
    class Meta:
        """Meta"""
        model = BloodDonorDetailsmodel
        fields = ('fullname',
                  'gender',
                  "email",
                  "mobilenumber",
                  'blood_group',
                  'state',
                  'city',
                  "Home_address",
                  "office_address",
                  "occupation",
                  'last_time_blood_donated',
                  "did_you_ever_donate_blood_before",
                  "Are_you_currently_taking_any_medications",
                  "Do_you_have_any_disease",
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['blood_group'].required = True


class CustomUserForm(CustomUserCreationForm):
    role = forms.ChoiceField(choices=[
        # ('BD', 'Blood Donor'),
        ('HP', 'Hospital'),
        ('CP', 'Company'),
    ])

    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('role',)
