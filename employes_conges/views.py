from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordResetView
from django.urls import reverse_lazy

from .forms import EmployeeRegistrationForm, LeaveRequestForm
from .models import Employee, LeaveRequest

# Vues d'authentification
def register(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie!')
            return redirect('dashboard')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Vues pour les employés
@login_required
def dashboard(request):
    # Récupérer les congés de l'utilisateur
    user_requests = LeaveRequest.objects.filter(employee=request.user).order_by('-created_at')
    
    # Statistiques des congés
    stats = {
        'total_requests': user_requests.count(),
        'pending_requests': user_requests.filter(status='PENDING').count(),
        'approved_requests': user_requests.filter(status='APPROVED').count(),
        'rejected_requests': user_requests.filter(status='REJECTED').count(),
    }
    
    # Congés à venir
    upcoming_leaves = user_requests.filter(
        start_date__gte=timezone.now().date(),
        status='APPROVED'
    )

    context = {
        'stats': stats,
        'recent_requests': user_requests[:5],
        'upcoming_leaves': upcoming_leaves,
        'leave_requests': user_requests,  # Ajoutez cette ligne pour passer les demandes de congé à la template
    }
    
    return render(request, 'employes_conges/dashboard.html', context)

@login_required
def submit_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            messages.success(request, 'Demande de congé soumise avec succès!')
            return redirect('dashboard')
    else:
        form = LeaveRequestForm()
    return render(request, 'employes_conges/submit_leave.html', {'form': form})

# Vues pour les administrateurs
def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    # Statistiques globales
    all_requests = LeaveRequest.objects.all()
    pending_requests = all_requests.filter(status='PENDING')
    
    stats = {
        'total_employees': Employee.objects.count(),
        'total_requests': all_requests.count(),
        'pending_requests': pending_requests.count(),
        'approved_requests': all_requests.filter(status='APPROVED').count(),
    }
    
    context = {
        'stats': stats,
        'pending_requests': pending_requests,
    }
    
    return render(request, 'employes_conges/admin_dashboard.html', context)

@user_passes_test(is_admin)
def approve_leave(request, leave_id):
    if request.method == 'POST':
        leave_request = get_object_or_404(LeaveRequest, id=leave_id)
        leave_request.status = 'APPROVED'
        leave_request.save()
        messages.success(request, 'Demande de congé approuvée avec succès.')
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def reject_leave(request, leave_id):
    if request.method == 'POST':
        leave_request = get_object_or_404(LeaveRequest, id=leave_id)
        leave_request.status = 'REJECTED'
        leave_request.save()
        messages.success(request, 'Demande de congé rejetée.')
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def manage_employees(request):
    employees = Employee.objects.all()
    return render(request, 'employes_conges/manage_employees.html', {'employees': employees})

@user_passes_test(is_admin)
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employé ajouté avec succès.')
            return redirect('manage_employees')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'employes_conges/add_employee.html', {'form': form})

@user_passes_test(is_admin)
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employé modifié avec succès.')
            return redirect('manage_employees')
    else:
        form = EmployeeRegistrationForm(instance=employee)
    return render(request, 'employes_conges/edit_employee.html', {'form': form})

@user_passes_test(is_admin)
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employé supprimé avec succès.')
        return redirect('manage_employees')
    return render(request, 'employes_conges/delete_employee.html', {'employee': employee})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('dashboard')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')