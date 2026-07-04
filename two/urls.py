from django.urls import path
from . import views

urlpatterns = [
    path('ind', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('set-password/', views.set_password, name='set_password'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('api/login/', views.api_offer, name='api'),
    path('upload/', views.upload, name = 'upload'),
    path('ticket_list/', views.ticket_list, name = 'ticket_list'),
    path('update/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
    path('delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),

    path("customers/", views.customer_list, name="customer_list"),
    path("customers/upload/", views.customer_upload, name="customer_upload"),
    path("customers/update/<int:id>/", views.customer_update, name="customer_update"),
    path("customers/delete/<int:id>/", views.customer_delete, name="customer_delete"),


    path('agents/', views.agent_list, name='agent_list'),
  path('agents/upload/', views.agent_upload, name='agent_upload'),
path('agents/update/<int:agent_id>/', views.update_agent, name='update_agent'),
path('agents/delete/<int:agent_id>/', views.delete_agent, name='delete_agent'),
path('dash',views.dashboard,name='dashboard'),
path('',views.tickets,name='tickets'),


]