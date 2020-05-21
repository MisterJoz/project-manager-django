from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('add_project_form/', views.addProject, name='add_project'),
    path('project/<str:pk>/', views.project, name='project'),
    path('contact/<str:pk>/', views.contact, name='contact'),
    path('update_project_form/<str:pk>/',
         views.updateProject, name='update_project'),
    path('delete/<str:pk>/',
         views.deleteProject, name='delete_project'),
    path('add_contact_form/', views.addContact, name='add_contact'),

]
