from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Profile
from .forms import ProfileForm,CustomUserCreationForm

# Create your views here.


def follow(request,user_id):
    people=get_object_or_404(get_user_model(),id=user_id)
    if request.user in people.followers.all():
        people.followers.remove(request.user)
    else:
        people.followers.add(request.user)
    return redirect('accounts:people',people.username)

def password(request):
    if request.method=='POST':
        password_change_form=PasswordChangeForm(request.user,request.POST)
        if password_change_form.is_valid():
            user=password_change_form.save()
            update_session_auth_hash(request,user)
            return redirect('people.html',request.user.username)
    else:
        password_change_form=PasswordChangeForm(request.user)
    return render(request,'password.html',{'password_change_form':password_change_form})

def delete(request):
    if request.method=='POST':
        request.user.delete()
        return redirect('posts:list')
    return render(request,'delete.html')

def update(request):
    if request.method=='POST':
        user_change_form=CustomUserChangeForm(request.POST,instace=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('accounts:people',request.user.username)
    else:
        user_change_form=CustomUserChangeForm(instance=request.user)
        return render(request,'update.html',{'user_change_form':user_change_form})

def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method=='POST':
        signup_form=CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user=signup_form.save()
            Profile.objects.create(user=user)
            auth_login(request,user)
            return redirect('posts:list')
    else:
        signup_form=UserCreationForm()
    return render(request,'signup.html',{'signup_form':signup_form})

def profile_update(request):
    try:
        profile=Profile.objects.get(user=request.user.id)
    except Profile.DoesNotExist:
        profile=Profile.objects.create(user=request.user,nickname='none')
    if request.method=='POST':
        profile_form =ProfileForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
        return redirect('accounts:people',request.user.username)
    else:
        profile_form=ProfileForm(instance=profile)
    return render(request,'profile_update.html',{'profile_form':profile_form})

def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
        return redirect('posts:list')
    else:
        login_form=AuthenticationForm()
    return render(request,'login.html',{'login_form':login_form})

def logout(request):
    auth_logout(request)
    return redirect('posts:list')

def people(request,username):
    people=get_object_or_404(get_user_model(),username=username)
    return render(request,'people.html',{'people':people})