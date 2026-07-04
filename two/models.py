from django.db import models
from django.contrib.auth.models import User

class OTPVerification(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return self.email

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    account_status = models.CharField(max_length=50)

    def __str__(self):
        return self.name        

class Agent(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    skill = models.CharField(max_length=255)
    availability = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Tickets(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=255)
    description = models.CharField(max_length=60)
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    assigned = models.ForeignKey(Agent, on_delete=models.RESTRICT, null=True, blank=True)
    created_At = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"T{self.id} - {self.subject}"