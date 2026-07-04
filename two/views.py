from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import OTPVerification
import random
from django.http import JsonResponse
from .models import Tickets
from .forms import Booking
from .models import Customer
from .forms import CustomerForm
from .models import Agent
from .forms import AgentForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = str(random.randint(100000, 999999))
        OTPVerification.objects.update_or_create(
            email=email,
            defaults={"otp": otp}
        )
        send_mail(
            "OTP Verification",
            f"Your OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        request.session["signup_email"] = email
        return redirect("verify_otp")
    return render(request, "two/signup.html")


def verify_otp(request):
    email = request.session.get("signup_email")
    if not email:
        return redirect("signup")
    if request.method == "POST":
        otp = request.POST.get("otp")
        try:
            record = OTPVerification.objects.get(email=email)
            if record.otp == otp:
                return redirect("set_password")
            else:
                messages.error(request, "Invalid OTP")
        except OTPVerification.DoesNotExist:
            messages.error(request, "OTP verification failed")
    return render(request, "two/verify_otp.html")


def set_password(request):
    email = request.session.get("signup_email")
    if not email:
        return redirect("signup")
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("set_password")
        username = email.split("@")[0]
        if User.objects.filter(username=username).exists():
            username = username + str(random.randint(1000, 9999))
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        OTPVerification.objects.filter(email=email).delete()
        messages.success(request, "Account created successfully")
        return redirect("login")
    return render(request, "two/set_password.html")


def login_view(request):

    if request.method == "POST":

        email = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.filter(email=email).first()

            if user_obj is None:
                messages.error(request, "Email not registered")
                return render(request, "two/login.html")

            user = authenticate(request,username=user_obj.username,password=password
)

            if user is not None:
                login(request, user)
                return redirect("home")

            messages.error(request, "Invalid Password")

        except User.DoesNotExist:
            messages.error(request, "Email not registered")

    return render(request, "two/login.html")


def home(request):

    # if not request.user.is_authenticated:
    #     return redirect("login")

    return render(request, "two/home.html")


def logout_view(request):

    logout(request)

    return redirect("login")

def index(request):
    return render(request, 'two/index.html')    

@csrf_exempt
def upload(request):
    if request.method == "POST":
        upload_form = Booking(request.POST, request.FILES)

        if upload_form.is_valid():
            upload_form.save()
            return HttpResponse("Ticket Added Successfully")
        else:
            print(upload_form.errors)    
            return HttpResponse(upload_form.errors)

    else:
        upload_form = Booking()

    return render(request, "two/upload.html", {"upload_form": upload_form})

def ticket_list(request):
    tickets=Tickets.objects.all()
    return render(request, 'two/ticket_list.html',{'tickets': tickets})

def update_ticket(request, ticket_id):
    ticket_id = int(ticket_id)
    try:
        ticket_sel = Tickets.objects.get(Ticketid=ticket_id)
    except Tickets.DoesNotExist:
        return redirect('ticket_list')
    upload_form = Booking(request.POST or None, instance=ticket_sel)
    if upload_form.is_valid():
        upload_form.save()
        return redirect('ticket_list')
    return render(request, 'two/upload.html',{'upload_form': upload_form})

def delete_ticket(request, ticket_id):
    ticket_id = int(ticket_id)
    try:
        ticket_sel = Tickets.objects.get(Ticketid=ticket_id)
    except Tickets.DoesNotExist:
        return redirect('ticket_list')
    ticket_sel.delete()
    return redirect('ticket_list')

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "two/customer_list.html", {"customers": customers})

@csrf_exempt
def customer_upload(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        form = CustomerForm()

    return render(request, "two/customer_upload.html", {"form": form})

@csrf_exempt
def customer_update(request, id):
    customer = Customer.objects.get(CustomerId=id)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer)

    return render(request, "two/customer_upload.html", {"form": form})


def customer_delete(request, id):
    try:
        customer = Customer.objects.get(CustomerId=id)
    except Customer.DoesNotExist:
        return redirect("customer_list")

    customer.delete()
    return redirect("customer_list")


def agent_list(request):
    agents = Agent.objects.all()
    return render(request, "two/agent_list.html", {"agents": agents})

@csrf_exempt
def agent_upload(request):
    if request.method == "POST":
        form = AgentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agent_list')
    else:
        form = AgentForm()

    return render(request, 'two/agent_upload.html', {'form': form})

@csrf_exempt
def update_agent(request, agent_id):
    try:
        agent = Agent.objects.get(AgentId=agent_id)
    except Agent.DoesNotExist:
        return redirect('agent_list')

    form = AgentForm(request.POST or None, instance=agent)

    if form.is_valid():
        form.save()
        return redirect('agent_list')

    return render(request, 'two/agent_upload.html', {'form': form})

@csrf_exempt
def delete_agent(request, agent_id):
    try:
        agent = Agent.objects.get(AgentId=agent_id)
    except Agent.DoesNotExist:
        return redirect('agent_list')

    agent.delete()
    return redirect('agent_list')   





def api_offer(request):
    if request.method=='GET':
        username = request.GET.get("username")
        password = request.GET.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return JsonResponse({'message': ' login done.'})
            return JsonResponse({'success': True}, status=200)
        else:
           return JsonResponse({'success': False,'message': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'message': ' only GET method is allowed.'},status= 405)


def dashboard(request):
    return render(request,'dashboard.html')   

def tickets(request):
    return render(request,'tickets.html')   

from django.shortcuts import render
from .models import Tickets, Customer, Agent

def dashboard(request):
    # Fetch all ticket records from your Tickets model
    all_tickets = Tickets.objects.all()
    # Filter and count using your exact status text options
    context = {
        # Fetching latest 10 tickets for the dashboard table
        # select_related avoids hitting the DB repeatedly for Customer/Agent names
        'tickets': all_tickets.select_related('customer_id', 'assigned').order_by('-id')[:10],
        'total_tickets_count': all_tickets.count(),
        'open_tickets_count': all_tickets.filter(status__iexact='Open').count(),
        'resolved_tickets_count': all_tickets.filter(status__iexact='Resolved').count(),
        'pending_tickets_count': all_tickets.filter(status__iexact='Pending').count(),
    }
    return render(request, 'dashboard.html', context)

def tickets(request):
    # Fetch all records to supply the cards display list
    all_tickets = Tickets.objects.all()
    return render(request, 'tickets.html', {'tickets': all_tickets})  
