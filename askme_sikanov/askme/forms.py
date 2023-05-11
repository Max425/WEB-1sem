# from django import forms

# from askme.models import Profile


# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(min_length=4, widget=forms.PasswordInput)

#     # def clean_password(self):
#     #     data = self.cleaned_data['password']
#     #     if data == 'wrong':
#     #         raise ValueError('Wrong password!')
#     #     return data

# class RegistrationForm(forms.ModelForm):
#     password_check = forms.CharField(min_length=4, widget=forms.PasswordInput)
    
#     class Meta:
#         model = Profile
#         fields = '__all__'