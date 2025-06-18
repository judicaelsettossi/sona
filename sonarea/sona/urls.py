from django.urls import path
from . import views

app_name = 'sona'

urlpatterns = [
    path('', views.index, name='index'),  # Page d'accueil
    path('commands/', views.commands, name='commands'),
    path('payment', views.payment, name='payment'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('test-email/', views.test_email, name='test_email'),
    path('test-sendgrid/', views.test_sendgrid_email, name='test_sendgrid'),
] 