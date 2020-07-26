from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('send_mail/', views.SendEmail, name='send_mail'),
    path('submeter/', views.SubmeterProjecto, name='submeter_projecto'),
    path('project/', views.ProjectView.as_view(), name='project_view'),
    path('project/edit/<int:pk>', views.ProjectEdit.as_view(), name='project_view'),
    path('projects/', views.ProjectsView.as_view(), name='project_list'),
    path('project/<int:pk>/', views.ProjectDetail.as_view(), name='project_detail'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('stats/', views.EstatisticasView.as_view(), name='stats'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile_view'),
]
