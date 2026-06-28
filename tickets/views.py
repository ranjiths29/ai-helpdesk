from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .ai_helper import classify_ticket

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        return render(request, 'tickets/login.html', {'error': 'Invalid credentials'})
    return render(request, 'tickets/login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def dashboard(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'tickets/dashboard.html', {'tickets': tickets})

@login_required(login_url='/login/')
def submit_ticket(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']

        priority, suggestion = classify_ticket(title, description)

        Ticket.objects.create(
            title=title,
            description=description,
            priority=priority,
            ai_suggestion=suggestion,
            created_by=request.user,
        )
        return redirect('/dashboard/')
    return render(request, 'tickets/submit_ticket.html')