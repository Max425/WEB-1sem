from django import forms
from django.contrib.auth.models import User
from askme.models import Profile, Question, Tag


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)
    password_check = forms.CharField(min_length=4, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_check', 'avatar']

    def save(self, commit=True):
        self.cleaned_data.pop('password_check')
        user = super().save(commit)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            avatar = self.cleaned_data["avatar"]
            if avatar:
                profile = Profile.objects.create(user=user, avatar=self.cleaned_data["avatar"])
            else:
                profile = Profile.objects.create(user=user)
            profile.save()
        return user


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'avatar']

    def save(self, commit=True):
        user = super().save(commit)
        profile = user.profile
        profile.avatar=self.cleaned_data["avatar"]
        profile.save()

        return user


class QuestionForm(forms.Form):
    title = forms.CharField(max_length=255, label='Название вопроса')
    text = forms.CharField(widget=forms.Textarea, label='Текст вопроса')
    tag = forms.CharField(max_length=255, label='Теги')

    def save(self, request):
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        tag_list = self.cleaned_data['tag'].split()
        question = Question.objects.create(title=title, text=text, profile=request.user.profile)
        for tag_name in tag_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            question.tag.add(tag)
        return question
    
class AnswerForm(forms.Form):
    text = forms.CharField(label='Your answer', widget=forms.Textarea(attrs={'rows': 4}))