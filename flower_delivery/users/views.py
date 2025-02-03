from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    """
    Обрабатывает авторизацию пользователя.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('flower_list')  # Перенаправляем, напр., на каталог
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'users/login.html')

def logout_view(request):
    """
    Разлогинивает текущего пользователя и перенаправляет, напр., в каталог.
    """
    logout(request)
    return redirect('flower_list')  # Или на любую страницу

def register_view(request):
    """
    Регистрация нового пользователя с помощью UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # После успешной регистрации сразу логиним пользователя
            login(request, user)
            return redirect('flower_list')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
from django.shortcuts import render