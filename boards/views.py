from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import *

@login_required(login_url='login')
def home(request):
    posts=Post.objects.all()
    context={'posts':posts}
    return render(request, 'boards/home.html',context)

def register(request):
    form=CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='standard')
            user.groups.add(group)
            messages.success(request, 'Account was created for '+username)
            return redirect('login')
    
    context={'form':form}
    return render(request, 'boards/register.html', context)

    

def loginUser(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'boards/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def feed(request):
    posts=Post.objects.all().filter(user=request.user)
    print(request.user)
    context={'posts':posts}
    return render(request,'boards/userContent.html',context)


@login_required(login_url='login')
def viewPost(request, pk):
    try:
        post=Post.objects.get(id=pk, user=request.user)
    except:
        try:
            post=Post.objects.get(id=pk,underWork=True)
        except:
            return redirect('home')
    context={'post':post}
    return render(request,'boards/post.html',context)


@login_required(login_url='login')
def addPost(request):
    if request.method=='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        user1=request.user
        category=request.POST.get('category')
        Post.objects.create(
            user=user1,
            title=title,
            description=description,
            category=category
        )
        return redirect('feed')
        

    return render(request,'boards/addPost.html')


@login_required(login_url='login')
def updatePost(request,pk):
    try:
        post=Post.objects.get(id=pk,user=request.user,underWork=False)
    except:
        return redirect('home')
    if request.method=='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        user1=request.user
        category=request.POST.get('category')
        post.title=title
        post.description=description
        post.category=category
        post.save()
        return redirect('feed')
    context={'post':post}
    return render(request,'boards/update.html',context)


@login_required(login_url='login')
def deletePost(request, pk):
    try:
        post=Post.objects.get(id=pk,user=request.user,underWork=False)
    except:
        return redirect('home')
    post.delete()
    return redirect('feed')