from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user, allowed_users
from .models import *
from .forms import ProjectForm, ContactForm, CreateUserForm
# Create your views here.


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def index(request):
    projects = Project.objects.all().order_by('-intial_date')
    context = {
        'projects': projects,
    }
    return render(request, 'pages/index.html', context)


@unauthenticated_user
def register(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # associate user with admin group upon registration
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='admin')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'pages/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrenct')
    context = {}
    return render(request, 'pages/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def calculate(subtotal, no_of_signs, sign_permit, engineering, other_fees, discount, cash_discount):
    total = subtotal + (sign_permit * no_of_signs) + engineering + other_fees
    if discount > 0:
        total -= total * discount
    elif cash_discount > 0:
        total -= cash_discount
    else:
        return total
    return total


def calculatePercentage(deposit_percentage):
    completion_percentage = 100 - deposit_percentage

    return completion_percentage


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def addProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form_copy = request.POST.copy()
        # get data used to calculate total

        number_of_signs = int(form_copy['number_of_signs'])
        sign_permit = int(form_copy['sign_permit'])
        engineering = int(form_copy['engineering'])
        other_fees = int(form_copy['other_fees'])
        # project can have discount OR cash discount
        discount = (float(form_copy['discount']) * .01)
        cash_discount = int(form_copy['cash_discount'])
        # total after discount applied
        discount_total = int(form_copy['discount_total'])
        deposit_amount = int(form_copy['deposit_amount'])
        completion_amount = int(form_copy['completion_amount'])
        # calculate percentage
        deposit_percentage = int(form_copy['deposit_percentage'])
        form_copy['completion_percentage'] = 100 - deposit_percentage
        # calculate total sign price as subtotal

        # calculate subtotal given sign price
        sum = 0
        for i in range(number_of_signs):
            i += 1
            sign_order = 'mysign-' + str(i)
            sum += int(form_copy[sign_order])
        form_copy['subtotal'] = sum
        subtotal = int(form_copy['subtotal'])

        # if discount %, discount total = disocunt * subtotal
        # if cash discount, discount total = subtotal - cash discount
        if discount:
            form_copy['discount_total'] = discount * subtotal
        elif cash_discount:
            form_copy['discount_total'] = cash_discount

        # calculate total price
        # form_copy['final_total'] = subtotal
        form_copy['final_total'] = calculate(
            subtotal, number_of_signs, sign_permit, engineering, other_fees, discount, cash_discount)

        form_copy['deposit_amount'] = (form_copy['final_total'] - (form_copy['final_total'] *
                                                                   form_copy['completion_percentage'] * .01))

        form_copy['completion_amount'] = (form_copy['final_total'] -
                                          form_copy['deposit_amount'])

        print('Sum..........', sum)
        form = ProjectForm(form_copy)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'pages/add_project_form.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def addContact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'pages/add_contact_form.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    contact = Contact.objects.get(client=project.contact_id)
    print(project)
    print(contact)
    context = {'project': project, 'contact': contact}

    return render(request, 'pages/project.html', context)


def contact(request, pk):
    contact = Contact.objects.get(client=pk)
    context = {'contact': contact}
    return render(request, 'pages/contact.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    print('Project...', project)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'pages/add_project_form.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('/')
    context = {'project': project}
    return render(request, 'pages/delete.html', context)
