from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


@require_http_methods(["POST"])
def login_view(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
    
	user = authenticate(request, username=username, password=password)
    
	if user is not None:
		login(request, user)
		return redirect('flights:home')
	else:
		return redirect('flights:home')


@require_http_methods(["POST"])
def signup_view(request):
	username = request.POST.get('username')
	email = request.POST.get('email')
	password = request.POST.get('password')
	password2 = request.POST.get('password2')
    
	if password != password2:
		return redirect('flights:home')
    
	if User.objects.filter(username=username).exists():
		return redirect('flights:home')
    
	if User.objects.filter(email=email).exists():
		return redirect('flights:home')
    
	user = User.objects.create_user(username=username, email=email, password=password)
	login(request, user)
	return redirect('flights:home')


def logout_view(request):
	"""خروج از اکانت"""
	logout(request)
	return redirect('flights:home')
