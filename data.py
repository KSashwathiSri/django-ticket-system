import random
from django.contrib.auth.models import User
from faker import Faker
from two.models import Customer, Agent, Tickets, OTPVerification

fake = Faker()

# ----------------------------
# Create Agents
# ----------------------------

skills = [
    "Networking",
    "Software",
    "Hardware",
    "Billing",
    "Cloud",
    "Database",
    "Security",
    "Technical Support",
    "Customer Support",
    "Application Support"
]

availability = ["Available", "Busy", "Offline"]

agents = []

for i in range(10):
    agent, created = Agent.objects.get_or_create(
        email=f"agent{i}@example.com",
        defaults={
            "name": fake.name(),
            "skill": random.choice(skills),
            "availability": random.choice(availability)
        }
    )
    agents.append(agent)

# ----------------------------
# Create Users, Customers, OTP
# ----------------------------

statuses = ["Active", "Inactive", "Pending"]

customers = []

for i in range(65):
    username = f"user{i}"
    email = f"user{i}@example.com"

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email
        }
    )

    if created:
        user.set_password("password123")
        user.save()

    customer, created = Customer.objects.get_or_create(
        email=email,
        defaults={
            "user": user,
            "name": fake.name(),
            "phone": fake.phone_number()[:20],
            "address": fake.address(),
            "account_status": random.choice(statuses)
        }
    )

    customers.append(customer)

    OTPVerification.objects.get_or_create(
        email=email,
        defaults={
            "otp": str(random.randint(100000, 999999))
        }
    )

# ----------------------------
# Create Tickets
# ----------------------------

subjects = [
    "Login Issue",
    "Password Reset",
    "Payment Failed",
    "Account Locked",
    "Website Down",
    "App Crash",
    "Refund Request",
    "Billing Issue",
    "Order Delay",
    "Email Not Working"
]

descriptions = [
    "Unable to login",
    "Forgot password",
    "Payment unsuccessful",
    "Need account unlock",
    "Website inaccessible",
    "Application crashes",
    "Refund not received",
    "Incorrect bill",
    "Order delayed",
    "Email issue"
]

priorities = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

ticket_status = [
    "To Do",
    "In Progress",
    "Completed",
    "Rejected"
]

remarks = [
    "Investigating",
    "Resolved successfully",
    "Waiting for customer",
    "Assigned to team",
    "Pending approval",
    "Issue reproduced",
    "Escalated",
    "Fixed"
]

for i in range(65):
    Tickets.objects.create(
        customer_id=random.choice(customers),
        subject=random.choice(subjects),
        description=random.choice(descriptions),
        status=random.choice(ticket_status),
        priority=random.choice(priorities),
        assigned=random.choice(agents),
        remarks=random.choice(remarks)
    )

print("✅ Successfully inserted 65 Customers, 65 OTPs, 65 Tickets and 10 Agents.")