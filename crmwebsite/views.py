from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm,RecordForm
from .models import Record

def home(request):
    #check if user is logging in
    records=Record.objects.all()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user =authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,"You have been logged in succssfully")
            return render(request,'home.html')
        else:
            messages.error(request,"There was an error logging in,Please try again")
            return redirect('home')
    else:
        return render(request,'home.html',{'records':records})
def login_user(request):
    pass
def logout_user(request):
    logout(request)
    messages.success(request,"you have been logged out")
    return redirect('home')

def register_user(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"Registartion is successfully done")
            redirect('home')
            
    else:
        form=SignUpForm
        return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form})


def customer_record(request,pk):
    if request.user.is_authenticated:
        #look uo at te record
        customer_record=Record.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record})
    
    else:
        messages.error(request,"You must be logged in to see the records ")
        redirect('home')
        
def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it=Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Record deleted")
        return redirect('home')
    else:
        messages.error(request,"You must be logged in to delete")
        return redirect('home')
    
    
def add_record(request):
    form=RecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method=='POST':
            if form.is_valid():
                add_record=form.save()
                messages.success(request,"Record added successfully")
                return redirect('home')
        return render(request,'add_record.html',{'form':form})
    else:
        messages.error(request,"You must be logged in to add record")
    return redirect('home')

def update_record(request,pk):
    if request.user.is_authenticated:
        current_record=Record.objects.get(id=pk)
        form=RecordForm(request.POST or None,instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record has been updated")
            return redirect('home')
        return render(request,'update_record.html',{'form':form,
                                                    'customer_record':current_record})
    else:
        messages.error(request,"You must be logged in to update record")
        return redirect('home') 
        
        