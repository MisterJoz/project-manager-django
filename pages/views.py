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


def calculateTaxAmount(amount, tax):
    tax_amount = float(tax) * float(amount)
    return tax_amount


def calculatePercentage(deposit_percentage):
    completion_percentage = 100 - deposit_percentage

    return completion_percentage


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def addProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form_copy = request.POST
        # get data used to calculate total
        #  .....
        mutable = request.POST._mutable
        request.POST._mutable = True

# ......
        number_of_signs = int(form_copy['number_of_signs'])
        sign_permit = float(form_copy['sign_permit'])
        engineering = float(form_copy['engineering'])
        other_fees = float(form_copy['other_fees'])
        # project can have discount OR cash discount
        discount = (float(form_copy['discount']) * .01)
        cash_discount = float(form_copy['cash_discount'])
        # total after discount applied
        discount_total = float(form_copy['discount_total'])
        deposit_amount = float(form_copy['deposit_amount'])
        completion_amount = float(form_copy['completion_amount'])
        # calculate percentage
        deposit_percentage = float(form_copy['deposit_percentage'])
        form_copy['completion_percentage'] = round(100 - deposit_percentage, 2)
        # request.POST['completion_percentage'] = 100 - deposit_percentage

        # calculate total sign price as subtotal
        # calculate subtotal given sign price
        sum = 0
        for i in range(number_of_signs):
            i += 1
            sign_order = 'mysign-' + str(i)
            sum += int(form_copy[sign_order])
            print(sum)
        form_copy['subtotal'] = sum
        subtotal = float(form_copy['subtotal'])

        # if discount %, discount total = disocunt * subtotal
        # if cash discount, discount total = subtotal - cash discount
        if discount:
            form_copy['discount_total'] = discount * subtotal
        elif cash_discount:
            form_copy['discount_total'] = cash_discount

        # calculate total price
        total = calculate(
            subtotal, number_of_signs, sign_permit, engineering, other_fees, discount, cash_discount)
        # tax amount
        form_copy['tax_amount'] = calculateTaxAmount(
            total, form_copy['tax'])
        # add tax to total
        form_copy['final_total'] = total + form_copy['tax_amount']

        # calculate tax amount

        form_copy['deposit_amount'] = round((form_copy['final_total'] - (form_copy['final_total'] *
                                                                         form_copy['completion_percentage'] * .01)), 2)

        form_copy['completion_amount'] = (form_copy['final_total'] -
                                          form_copy['deposit_amount'])

        form = ProjectForm(form_copy)
        if form.is_valid():
            request.POST._mutable = mutable
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

    context = {'project': project, 'contact': contact}

    return render(request, 'pages/project.html', context)

# contact form


def contact(request, pk):
    contact = Contact.objects.get(client=pk)
    context = {'contact': contact}
    return render(request, 'pages/contact.html', context)
# update contact form


def updateContact(request, pk):
    # project = Project.objects.get(id=pk)
    contact = Contact.objects.get(client=pk)
    form = ContactForm(instance=contact)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        # 'project': project,
        'contact': contact,
        'form': form,
    }
    return render(request, 'pages/add_contact_form.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        mutable = request.POST._mutable
        request.POST._mutable = True

        number_of_signs = int(request.POST['number_of_signs'])
        sign_permit = float(request.POST['sign_permit'])
        engineering = float(request.POST['engineering'])
        other_fees = float(request.POST['other_fees'])
        # project can have discount OR cash discount
        discount = (float(request.POST['discount']) * .01)
        cash_discount = float(request.POST['cash_discount'])
        # total after discount applied
        discount_total = float(request.POST['discount_total'])
        deposit_amount = float(request.POST['deposit_amount'])
        completion_amount = float(request.POST['completion_amount'])
        # calculate percentage
        deposit_percentage = float(request.POST['deposit_percentage'])
        request.POST['completion_percentage'] = round(
            100 - deposit_percentage, 2)
        # request.POST['completion_percentage'] = 100 - deposit_percentage

        # calculate total sign price as subtotal
        # calculate subtotal given sign price
        sum = 0
        for i in range(number_of_signs):
            i += 1
            sign_order = 'mysign-' + str(i)
            sum += int(request.POST[sign_order])
            print(sum)
        request.POST['subtotal'] = sum
        subtotal = float(request.POST['subtotal'])

        # if discount %, discount total = disocunt * subtotal
        # if cash discount, discount total = subtotal - cash discount
        if discount:
            request.POST['discount_total'] = discount * subtotal
        elif cash_discount:
            request.POST['discount_total'] = cash_discount

        # calculate total price
        # request.POST['final_total'] = subtotal
        request.POST['final_total'] = calculate(
            subtotal, number_of_signs, sign_permit, engineering, other_fees, discount, cash_discount)

        # calculate tax
        # calculate total price
        total = calculate(
            subtotal, number_of_signs, sign_permit, engineering, other_fees, discount, cash_discount)
        # tax amount
        request.POST['tax_amount'] = calculateTaxAmount(
            total, request.POST['tax'])
        # add tax to total
        request.POST['final_total'] = total + request.POST['tax_amount']

        request.POST['deposit_amount'] = round((request.POST['final_total'] - (request.POST['final_total'] *
                                                                               request.POST['completion_percentage'] * .01)), 2)
        print('Deposit Amount...', request.POST['deposit_amount'])

        request.POST['completion_amount'] = (request.POST['final_total'] -
                                             request.POST['deposit_amount'])

        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            request.POST._mutable = mutable
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

    context = {
        'project': project
    }
    return render(request, 'pages/delete.html', context)
