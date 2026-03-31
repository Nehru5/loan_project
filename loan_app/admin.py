from django.contrib import admin
from .models import *


admin.site.register(AccountHolder)
admin.site.register(LoanApplication)
admin.site.register(LoanApproval)
admin.site.register(Payment)