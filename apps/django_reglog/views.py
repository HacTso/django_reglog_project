from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

def index(request):
    print User.objects.all()
    return render(request, 'django_reglog/index.html')

def register(request):
    postData = {
        'username': request.POST['username'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'confirm': request.POST['confirm'],
    }
    print postData
    errors = User.objects.register(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.get(email=postData['email'])[0].id
        request.session['username'] = postData['username']
        return redirect('/')#/success
    else:
        for error in errors:
            messages.info(request, error)
            return redirect('/')

def login(request):
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password'],
    }
    print postData
    errors = User.objects.login(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.get(email=postData['email'])[0].id
        request.session['username'] = User.objects.get(username=postData['username'])
        return redirect('/')#/success
    else:
        for error in errors:
            messages.info(request, error)
            return redirect('/')

# def success(request):
#     context = {'users': User.objects.all().order_by('-created_at')}
#     return render(request, 'loginRegistration2/success.html', context)







