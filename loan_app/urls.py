from django.urls import path
from . import views

urlpatterns = [

path('',views.home,name='home'),
path('register/',views.register,name='register'),
path('login/',views.login,name='login'),
path('dashboard/',views.dashboard,name='dashboard'),
path('logout/',views.logout,name='logout'),
path('apply-loan/',views.apply_loan,name='apply_loan'),
path('loan-status/',views.loan_status,name='loan_status'),
path('admin-login/',views.admin_login),
path('admin-dashboard/',views.admin_dashboard),
path('admin-logout/',views.admin_logout),
path('all-loans/',views.all_loans),
path('approve-loan/<int:id>',views.approve_loan),
path('reject-loan/<int:id>',views.reject_loan),
path('emi-calculator/',views.emi_calculator,name='emi_calculator'),
# loan_app/urls.py
# urls.py
path('loan-details/<int:id>/', views.loan_details, name='loan_details'),
path('emi-payment/',views.emi_payment),
path('pay-emi/<int:id>',views.pay_emi),
path('payment-history/',views.payment_history),
path('emi-status/',views.emi_status),
path('download-receipt/<int:id>',views.download_receipt),
path('loan-certificate/<int:id>',views.loan_certificate),
path('loan-analytics/',views.loan_analytics),
# existing paths
    path('pending-loans/', views.pending_loans, name='pending_loans'),
    path('approved-loans/', views.approved_loans, name='approved_loans'),
]