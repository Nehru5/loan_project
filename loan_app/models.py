from django.db import models


class AccountHolder(models.Model):

    # Personal Info
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()

    # Address
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    # Account Info
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    # Images
    profile_image = models.ImageField(upload_to='profile_images/')
    signature = models.ImageField(upload_to='signature/')

    # ID Proofs
    aadhaar_number = models.CharField(max_length=20)
    aadhaar_image = models.ImageField(upload_to='aadhaar/')

    pan_number = models.CharField(max_length=20)
    pan_image = models.ImageField(upload_to='pan/')

    # Bank Details
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=20)

    # Employment Info
    occupation = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    monthly_salary = models.IntegerField()
    experience = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
      
class LoanApplication(models.Model):

    user = models.ForeignKey(AccountHolder,on_delete=models.CASCADE)

    loan_type = models.CharField(max_length=50)

    loan_amount = models.IntegerField()

    interest_rate = models.FloatField(null=True,blank=True)

    loan_duration = models.IntegerField()

    purpose = models.TextField()

    status = models.CharField(max_length=20,default='Pending')

    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.loan_type
      
      
class LoanApproval(models.Model):

    loan = models.ForeignKey(LoanApplication,on_delete=models.CASCADE)

    approved_amount = models.IntegerField()

    interest_rate = models.FloatField()

    emi = models.FloatField()

    duration = models.IntegerField()

    approval_date = models.DateTimeField(auto_now_add=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.loan)
      
      
class Payment(models.Model):

    loan = models.ForeignKey(LoanApplication,on_delete=models.CASCADE)

    amount = models.FloatField()

    payment_method = models.CharField(max_length=50)

    payment_date = models.DateTimeField(auto_now_add=True)

    emi_number = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.amount)