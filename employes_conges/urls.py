from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .views import CustomLoginView, CustomPasswordResetView

urlpatterns = [
    # URLs d'authentification
    path('register/', views.register, name='register'),
    #path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # URLs employés
    path('', views.dashboard, name='dashboard'),
    path('submit-leave/', views.submit_leave_request, name='submit_leave'),

    # URLs administrateur
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/leave/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('admin-dashboard/leave/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('admin-dashboard/employees/', views.manage_employees, name='manage_employees'),
    path('admin-dashboard/employees/add/', views.add_employee, name='add_employee'),
    path('admin-dashboard/employees/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('admin-dashboard/employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    # Autres vues de reset de mot de passe standard de Django
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]