from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

from .models import Profile, Project, Project_Avaliacao


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.user.username)


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
    )


class RegisterForm(forms.Form):
    CHOICES = (('1', 'Interno',), ('0', 'Externo',))
    user_type = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-check-input',
            })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mx-1',
                'placeholder': 'Username'
            })
    )
    first_name = forms.CharField(
        label="Nome",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mx-1',
                'placeholder': 'Nome'
            })
    )
    last_name = forms.CharField(
        label="Apelido",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mx-1',
                'placeholder': 'Apelido'
            })
    )
    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            })
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'area_de_interesse', 'descricao', 'profissao', 'empresa', 'gender', 'status']

    age = forms.IntegerField(
        label="Idade",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control mx-1',
                'placeholder': 'Idade'
            }),
        required=False
    )
    area_de_interesse = forms.CharField(
        label="Area de Interesse",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Area de Interesse'
            }),
        required=False
    )
    descricao = forms.CharField(
        label="Descrição",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Descrição'
            }),
        required=False
    )
    profissao = forms.CharField(
        label="Profissão",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Profissão'
            }),
        required=False
    )
    empresa = forms.CharField(
        label="Empresa",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Empresa'
            }),
        required=False
    )
    genderChoices = (('1', 'Male',), ('0', 'Female',))
    gender = forms.ChoiceField(
        choices=genderChoices,
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-check-input',
                'placeholder': 'Gender'
            }),
        required=False
    )
    statusChoices = (('1', 'Interno',), ('0', 'Externo',))
    status = forms.ChoiceField(
        choices=statusChoices,
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-check-input',
                'placeholder': 'Status'
            })
    )

    morada = forms.CharField(
        label="Morada",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Rua da Bananas nº4 ...'
            })
    )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name_text', 'empresa', 'descricao', 'responsavel']

    name_text = forms.CharField(
        label="Nome",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mx-1',
                'placeholder': 'Nome'
            })
    )
    empresa = forms.CharField(
        label="Empresa",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mx-1',
                'placeholder': 'Empresa'
            })
    )
    descricao = forms.CharField(
        label="Descricao",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mx-1',
                'placeholder': 'Descricao'
            })
    )

    users = forms.CharField(
        label="Users",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mx-1',
                'placeholder': 'Users Atribuidos'
            })
    )

    responsavel = MyModelChoiceField(queryset=Profile.objects.all(), empty_label="(Choose field)", to_field_name="user")

