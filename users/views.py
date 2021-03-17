from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileRegisterForm

# Create your views here.
def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        p_reg_form = ProfileRegisterForm(request.POST)
        if form.is_valid() and p_reg_form.is_valid():
          
            username = form.cleaned_data.get('username')
            
            user = form.save()
            group = Group.objects.get(name=form.cleaned_data.get('group'))
            user.groups.add(group)
            user.refresh_from_db()
            p_reg_form = ProfileRegisterForm(request.POST, instance=user.profile)
            p_reg_form.full_clean()
            p_reg_form.save()
            messages.success(request, f'Your account has been created successfully! You can log in!')
            return redirect('login')
    else:

        form = UserRegisterForm()
        p_reg_form = ProfileRegisterForm()

    context = {
        'form': form,
        'p_reg_form': p_reg_form
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance= request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance= request.user.profile)
        if u_form.is_valid() and p_form.is_valid():

            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance= request.user)
        p_form = ProfileUpdateForm(instance= request.user.profile)
    
    context={
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/fancyprofile.html', context)