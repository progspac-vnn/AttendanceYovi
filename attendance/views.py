from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
# from django.views.decorators import csrf_exempt
from django.contrib import messages
from app.models import customUser
from django.contrib.auth.decorators import login_required

def base(request):
    return render(request, 'base.html')

def loginpage(request):
    return render(request, 'login.html')

# @csrf_exempt
def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user!=None:
            
            login(request, user)
            
            user_type = user.user_type
            
            if user_type=='1':
                return redirect('hod_home')
                
            elif user_type=='2':
    
                return redirect('staff_home')
                
            elif user_type=='3':
    
                return redirect('student_home')
                
            elif user_type==None:

                print('error: ' + messages.error)
                messages.error(request, 'Email and Password Are Invalid')
                return redirect('loginpage')
            
        else:
            print(9)
            messages.error(request, 'Email and Password Are Invalid')
            return redirect('loginpage')

def doLogout(request):
    logout(request)
    return redirect('loginpage')

@login_required(login_url='/')
def profile(request):
    user = customUser.objects.get(id = request.user.id)
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/')
def profile_update(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        passw = request.POST.get('passw')
        try:
            customuser = customUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            
            if passw != None and passw != "":
                customuser.set_password(passw)
            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic
            
            customuser.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
        except:
            messages.error(request, 'Failed To Update Your Profile')
    return render(request, 'profile.html')