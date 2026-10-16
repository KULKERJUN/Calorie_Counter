from django.shortcuts import render,redirect,get_object_or_404
from calorie_app.models import *
from calorie_app.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.contrib import messages
# Create your views here.

def login_view(request):
    form_data = AuthenticationForm()
    if request.method == 'POST':
        form_data = AuthenticationForm(request, data = request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            if user:
                login(request,user)
                return redirect('dashboard_view')

    context = {
        'title':'LOGIN',
        'form_title':'Please Login with your credentials!',
        'form_btn':'LOGIN',
        'form_data':form_data,
    }
    return render(request,'master/baseform.html',context)

def register_view(request):

    form_data = RegistrationForm()
    if request.method == 'POST':
        form_data = RegistrationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login_view')
        
    context = {
        'title':'REGISTER',
        'form_title':'Please Register with your credentials!',
        'form_btn':'REGISTER',
        'form_data':form_data,
    }
    return render(request,'master/baseform.html',context)

@login_required
def dashboard_view(request):
    current_user = request.user
    try:
        profile_data = current_user.user_profile
        bmr = request.user.user_profile.bmr

    except:
        profile_data = None
        bmr = 0
        messages.warning(request,'Please Update Your Profile First.')
        return redirect('profile_update_view')
    
    data = ConsumeCalorieModel.objects.filter(user = request.user).aggregate(total_calorie= Sum('consumed_calorie'))
    total_consumed_calorie = data['total_calorie'] or 0
    less_or_more = bmr - total_consumed_calorie
    context = {
        'bmr':round(bmr,3),
        'total_consume_calorie':round(total_consumed_calorie,2),
        'less_or_more':round(less_or_more,2),
    }
    return render(request,'dashboard.html',context)

@login_required
def profile_view(request):
    return render(request,'profile.html')

#important
@login_required
def profile_update_view(request):

    current_user = request.user
    try:
        profile_data = current_user.user_profile
    except:
        profile_data = None

    form_data = UpdateProfileForm(instance=profile_data)
    if request.method == 'POST':
        form_data = UpdateProfileForm(request.POST,request.FILES,instance=profile_data)
        if form_data.is_valid():
            form_data = form_data.save(commit=False)
            form_data.user = current_user
            form_data.save()
            return redirect('profile_view')
        
    context = {
        'title':'Profile Update Page',
        'form_title':'Please Update with your credentials!',
        'form_btn':'Update',
        'form_data':form_data,
    }

    return render(request,'master/baseform.html',context)

@login_required
def calorie_consumed_list_view(request):
    try:
        bmr = request.user.user_profile.bmr

    except:
        bmr = 0
        messages.warning(request,'Please Update Your Profile First.')
        return redirect('profile_update_view')

    
    consumed_calorie = ConsumeCalorieModel.objects.filter(user = request.user)

    #SEARCHING
    search_data = request.GET.get('search_value')
    if search_data:
        consumed_calorie = ConsumeCalorieModel.objects.filter(
            Q(user = request.user) &
            Q(item_name__icontains = search_data))
    
    context = {
        'consumed_calorie':consumed_calorie,
    }
    return render(request,'calorie_list.html',context)

@login_required
def add_consumed_calorie_view(request):
    form_data = ConsumedCalorieForm()
    if request.method == 'POST':
        form_data = ConsumedCalorieForm(request.POST)
        if form_data.is_valid():
            form_data = form_data.save(commit=False)
            form_data.user = request.user
            form_data.save()
            return redirect('calorie_consumed_list_view')

    context = {'title':'Add Consumed Calorie',
            'form_title':'Add your consumed calories!',
            'form_btn':'Add',
            'form_data':form_data,}
    return render(request,'master/baseform.html',context)

@login_required
def edit_consumed_calorie_view(request, id):
    data = get_object_or_404(ConsumeCalorieModel, id = id)
    form_data = ConsumedCalorieForm(instance=data)
    if request.method == 'POST':
        form_data = ConsumedCalorieForm(request.POST,instance=data)
        if form_data.is_valid():
            form_data = form_data.save(commit=False)
            form_data.user = request.user
            form_data.save()
            return redirect('calorie_consumed_list_view')

    context = {'title':'Edit Consumed Calorie',
            'form_title':'Edit your consumed calories!',
            'form_btn':'Update',
            'form_data':form_data,}
    return render(request,'master/baseform.html',context)

@login_required
def delete_consumed_calorie_view(request, id):
    get_object_or_404(ConsumeCalorieModel, id = id).delete()
    return redirect('calorie_consumed_list_view')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')