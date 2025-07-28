from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/add_event/', views.event_create, name='event_create'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
]
