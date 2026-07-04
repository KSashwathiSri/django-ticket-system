import pytest
from two.models import Tickets,Customer,Agent
from django.db import models
from pytest_django.asserts import assertTemplateUsed
from django.urls import reverse
pytestmark=pytest.mark.django_db
from two.models import Customer

def test_upload():
    ticket=Tickets.objects.create(
        CustomerId=1,
        Subject='laptop issue',
        Description='laptop broken',
        Status='yes',
        Priority='yes',
    )
    assert ticket.Status=='yes'

def test_ticket_list():
    ticket=Tickets.objects.create(
        CustomerId=1,
        Subject='mouse issue',
        Description='mouse broken',
        Status='no',
        Priority='yes',
    )
    data = Tickets.objects.get(Ticketid=ticket.Ticketid)
    assert data.Subject == "mouse issue"

def test_update_ticket():
    ticket=Tickets.objects.create(
        CustomerId=1,
        Subject='key issue',
        Description='key broken',
        Status='yes',
        Priority='no',
    )
    ticket.Status = "Closed"
    ticket.save()
    assert ticket.Status == "Closed"

def test_delete_ticket():
    ticket=Tickets.objects.create(
        CustomerId=1,
        Subject='ipad issue',
        Description='ipad broken',
        Status='no',
        Priority='no',
    )
    ticket.delete()
    assert Tickets.objects.count() == 0

def test_customer_list():
    customer=Customer.objects.create(
        CustomerId=1,
        Name='jay',
        Email='jay@gmail.com',
        Phone='1234',
        Address='af1',
        AccountStatus='s',
    )
    data = Customer.objects.get(CustomerId=customer.CustomerId)
    assert data.Name == "jay"

def test_customer_upload():
    customer=Customer.objects.create(
        CustomerId=1,
        Name='cay',
        Email='cay@gmail.com',
        Phone='1934',
        Address='vf1',
        AccountStatus='n',
    )
    assert customer.Name=='cay'

def test_customer_update():
    customer=Customer.objects.create(
        CustomerId=1,
        Name='kay',
        Email='kay@gmail.com',
        Phone='10074',
        Address='mf1',
        AccountStatus='s',
    )
    customer.Phone = "1345"
    customer.save()
    assert customer.Phone== "1345"

def test_customer_delete():
    customer=Customer.objects.create(
        CustomerId=1,
        Name='pay',
        Email='pay@gmail.com',
        Phone='1264',
        Address='ef1',
        AccountStatus='s',
    )
    customer.delete()
    assert Customer.objects.count() == 0

def test_agent_list():
    agent=Agent.objects.create(
        AgentId = 1,
        Name='bay',
        Email ='bay@gmail.com',
        Skillset ='s',
        Availability='s',
    )
    data = Agent.objects.get(AgentId=agent.AgentId)

    assert data.Name == "bay"

def test_agent_upload():
    agent=Agent.objects.create(
        AgentId = 1,
        Name='bay',
        Email ='bay@gmail.com',
        Skillset ='s',
        Availability='s',
    )
    assert agent.Name=='bay'

def test_agent_update():
    agent=Agent.objects.create(
        AgentId = 1,
        Name='bay',
        Email ='bay@gmail.com',
        Skillset ='n',
        Availability='s',
    )
    agent.Skillset = "n"
    agent.save()
    assert agent.Skillset== "n"

def test_agent_delete():
    agent=Agent.objects.create(
        AgentId = 1,
        Name='bay',
        Email ='bay@gmail.com',
        Skillset ='s',
        Availability='s',
    )
    agent.delete()
    assert Agent.objects.count() == 0



def test_create_customer(client):
    response = client.post("/customers/upload/", {
        "CustomerId": 1,
        "Name": "John",
        "Email": "john@gmail.com",
        "Phone": "9876543210",
        "Address": "ABC Street",
        "AccountStatus": "s"
    })
    assert response.status_code == 302

def test_duplicate_email(client):
    Customer.objects.create(
        CustomerId=1,
        Name="John",
        Email="john@gmail.com",
        Phone="9999999999",
        Address="ABC Street",
        AccountStatus="s"
    )
    response = client.post("/customers/upload/", {
        "CustomerId": 2,
        "Name": "Alex",
        "Email": "john@gmail.com",
        "Phone": "8888888888",
        "Address": "XYZ Street",
        "AccountStatus": "s"
    })

    assert response.status_code in [200, 302]

def test_customer_without_email(client):
    response = client.post("/customers/upload/", {
        "CustomerId": 1,
        "Name": "John",
        "Phone": "9876543210",
        "Address": "ABC Street",
        "AccountStatus": "s"
    })
    assert response.status_code == 200

def test_delete_invalid_customer():
    with pytest.raises(Customer.DoesNotExist):
        Customer.objects.get(CustomerId=500)