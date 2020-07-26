import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .models import Profile, Project, Project_Avaliacao
from .forms import LoginForm, UserForm, ProfileForm, RegisterForm, ProjectForm
from django.contrib.auth import authenticate, login, logout as django_logout

from django.core.mail import send_mail
from django.conf import settings


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/voluntariado/profile/')
    else:
        return HttpResponseRedirect('/voluntariado/login/')


@login_required(login_url='/voluntariado/login/')
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/voluntariado/')


class LoginView(TemplateView):
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        form = LoginForm(request.POST or None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            error = 'Dados incorretos'
            return render(request, self.template_name, {'form': form, 'error': error})


class RegisterView(TemplateView):
    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        register_form = RegisterForm(request.POST or None)
        user_form = UserForm(request.POST or None, instance=User())
        profile_form = ProfileForm(request.POST or None, instance=Profile())
        forms = {'register_form': register_form, 'user_form': user_form, 'profile_form': profile_form}
        return render(request, self.template_name, forms)

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST or None)
        user_form = UserForm(request.POST or None, instance=User())
        profile_form = ProfileForm(request.POST or None, instance=Profile())
        if register_form.is_valid() and user_form.is_valid() and profile_form.is_valid():
            type_user = request.POST.get('user_type', '')
            is_staff = True if type_user == '1' else False
            password = request.POST.get('password', '')

            newUser = user_form.save(commit=False)
            newUser.is_staff = is_staff
            newUser.password = make_password(password, salt=None, hasher='default')
            newUser.save()
            newProfile = profile_form.save(commit=False)
            newProfile.user = newUser
            newProfile.save()
            user = authenticate(request, username=newUser.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
        return redirect('register')


class ProfileEditView(LoginRequiredMixin, TemplateView):
    login_url = '/voluntariado/login/'
    template_name = 'profile_edit.html'

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        return redirect('profile')


class ProjectEdit(LoginRequiredMixin, TemplateView):
    login_url = '/voluntariado/login/'
    template_name = 'project_edit.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.filter(id=kwargs["pk"]).first()
        project_form = ProjectForm(instance=project)
        return render(request, self.template_name, {'form': project_form})

    def post(self, request, *args, **kwargs):
        project = Project(id=kwargs["pk"])
        if request.method == "POST":
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                project.empresa = form.cleaned_data["empresa"]
                project.descricao = form.cleaned_data["descricao"]
                project.responsavel = form.cleaned_data["responsavel"]
                project.users = form.cleaned_data["users"]
                project.name_text = form.cleaned_data["name_text"]
                project.save()
                return redirect('project_list')


class ProfileDetailView(LoginRequiredMixin, TemplateView):
    login_url = '/voluntariado/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'profile_main.html'

    def get(self, request, *args, **kwargs):
        user = Profile.objects.filter(user=request.user.id).first()
        projects = Project.objects.filter(responsavel=request.user.id)
        return render(request, self.template_name, {'user': user, "projects": projects, "userId": request.user.id, "username": request.user.username, "userMail": request.user.email})

class ProjectDetail(LoginRequiredMixin, TemplateView):
    login_url = '/voluntariado/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'project_detail.html'

    def get(self, request, *args, **kwargs):
        project = Project.objects.filter(id=kwargs["pk"]).first()
        can_edit = request.user == project.responsavel.user
        return render(request, self.template_name, {'project': project, "can_edit": can_edit})


class ProjectsView(LoginRequiredMixin, TemplateView):
    login_url = '/voluntariado/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'projects_list.html'

    def get(self, request, *args, **kwargs):
        responsavel = Profile.objects.get(user=request.user.id)
        projects = Project.objects.filter(~Q(responsavel=responsavel))
        return render(request, self.template_name,
                      {"projects": projects, "userId": request.user.id, "username": request.user.username,
                       "userMail": request.user.email})

class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/voluntariado/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=kwargs["pk"])
        return render(request, self.template_name, {"user": profile})


@csrf_exempt
def SendEmail(request):
    body = json.loads(request.body)
    try:
        projectId = body["projectId"]
        project = Project.objects.filter(id=projectId).first()
        responsavel = project.responsavel.user.email
        linkForUserProfile = "http://localhost:8000/voluntariado/profile/{}".format(body["userId"])
        subject = 'Candidatura a projecto {}'.format(body["projectId"])
        message = 'Utilizador {} ({}) ({}) com o ID: {} gostaria de se associar ao projecto {}'.format(body["username"], body["userMail"], linkForUserProfile, body["userId"], body["projectId"])
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [responsavel]
        send_mail(subject, message, email_from, recipient_list)

    except Exception as e:
        return JsonResponse({"error": e}, status=500)

    return JsonResponse({"success": "success"}, status=200)


@csrf_exempt
def SubmeterProjecto(request):
    body = json.loads(request.body)
    try:
        projectId = body["projectId"]
        project = Project.objects.filter(id=projectId).first()
        responsavel = project.responsavel.user.email
        linkForUserProfile = "http://localhost:8000/voluntariado/profile/{}".format(body["userId"])
        subject = 'Projecto {} - Submetido'.format(body["projectId"])
        message = 'Utilizador {} ({}) ({}) com o ID: {} submeteu o projecto {} para avaliação'.format(body["username"], body["userMail"], linkForUserProfile, body["userId"], body["projectId"])
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ["noreplyvoluntariadogdp@gmail.com"]
        send_mail(subject, message, email_from, recipient_list)

    except Exception as e:
        return JsonResponse({"error": e}, status=500)

    return JsonResponse({"success": "success"}, status=200)


class ProjectView(LoginRequiredMixin, TemplateView):
    login_url = '/voluntariado/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'project_main.html'

    def get(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST or None)
        forms = {'project_form': project_form}
        return render(request, self.template_name, forms)

    def post(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST or None, instance=request.user)

        if project_form.is_valid():
            project_name = project_form.cleaned_data["name_text"]
            project_descricao = project_form.cleaned_data["descricao"]
            project_empresa = project_form.cleaned_data["empresa"]
            project_responsavel = project_form.cleaned_data["responsavel"]
            project_users = project_form.cleaned_data["users"]
            project = Project(name_text=project_name, descricao=project_descricao, empresa=project_empresa,
                              responsavel=project_responsavel, users=project_users, aprovado=False, complete=False)
            project.save()

        return HttpResponseRedirect(reverse('project_view'))


class EstatisticasView(LoginRequiredMixin, TemplateView):
    login_url = '/voluntariado/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'estatisticas.html'

    def get(self, request, *args, **kwargs):
        n_projectos = Project.objects.all().count()
        n_users = User.objects.all().count()
        n_complete_projects = Project.objects.filter(complete=False).count()
        n_non_complete_projects = Project.objects.filter(complete=True).count()
        n_projects_with_users = Project.objects.filter(~Q(users="")).count()
        n_non_aproved_projects = Project.objects.filter(aprovado=False).count()
        return render(request, self.template_name, {"n_projectos": n_projectos,"n_users": n_users,
                                                    "n_complete_projects": n_complete_projects,"n_non_complete_projects": n_non_complete_projects,
                                                    "n_projects_with_users": n_projects_with_users,"n_non_aproved_projects": n_non_aproved_projects})