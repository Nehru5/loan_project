from django.shortcuts import render

def home(request):
    return render(request,'home.html')
  
from django.shortcuts import render,redirect
from .models import *


def register(request):

    if request.method == "POST":

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')

        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        username = request.POST.get('username')
        password = request.POST.get('password')

        profile_image = request.FILES.get('profile_image')
        signature = request.FILES.get('signature')

        aadhaar_number = request.POST.get('aadhaar_number')
        aadhaar_image = request.FILES.get('aadhaar_image')

        pan_number = request.POST.get('pan_number')
        pan_image = request.FILES.get('pan_image')

        bank_name = request.POST.get('bank_name')
        account_number = request.POST.get('account_number')
        ifsc = request.POST.get('ifsc')

        occupation = request.POST.get('occupation')
        company = request.POST.get('company')
        salary = request.POST.get('salary')
        experience = request.POST.get('experience')

        AccountHolder.objects.create(

            full_name=full_name,
            email=email,
            phone=phone,
            date_of_birth=dob,

            address=address,
            city=city,
            state=state,
            pincode=pincode,

            username=username,
            password=password,

            profile_image=profile_image,
            signature=signature,

            aadhaar_number=aadhaar_number,
            aadhaar_image=aadhaar_image,

            pan_number=pan_number,
            pan_image=pan_image,

            bank_name=bank_name,
            account_number=account_number,
            ifsc_code=ifsc,

            occupation=occupation,
            company_name=company,
            monthly_salary=salary,
            experience=experience
        )

        return redirect('/login/')

    return render(request,'register.html')
  
  
def login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = AccountHolder.objects.filter(username=username,password=password)

        if user.exists():

            request.session['user_id'] = user[0].id

            return redirect('/dashboard/')

        else:
            return render(request,'login.html',{'error':'Invalid Credentials'})

    return render(request,'login.html')
  

def dashboard(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/login/')

    user = AccountHolder.objects.get(id=user_id)

    return render(request,'dashboard.html',{'user':user})
  
  
def logout(request):

    del request.session['user_id']

    return redirect('/login/')
  
  
def apply_loan(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/login/')

    user = AccountHolder.objects.get(id=user_id)

    if request.method == "POST":

        loan_type = request.POST.get('loan_type')
        amount = request.POST.get('amount')
        duration = request.POST.get('duration')
        purpose = request.POST.get('purpose')

        LoanApplication.objects.create(

            user=user,
            loan_type=loan_type,
            loan_amount=amount,
            loan_duration=duration,
            purpose=purpose

        )

        return redirect('/loan-status/')

    return render(request,'apply_loan.html')
  
  
def loan_status(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/login/')

    loans = LoanApplication.objects.filter(user_id=user_id)

    return render(request,'loan_status.html',{'loans':loans})
  
  
def admin_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "admin" and password == "admin":

            request.session['admin'] = True

            return redirect('/admin-dashboard/')

    return render(request,'admin_login.html')
  
  
def admin_dashboard(request):

    if not request.session.get('admin'):
        return redirect('/admin-login/')

    total_users = AccountHolder.objects.all().count()
    total_loans = LoanApplication.objects.all().count()
    pending = LoanApplication.objects.filter(status="Pending").count()
    approved = LoanApplication.objects.filter(status="Approved").count()

    context = {

        'total_users':total_users,
        'total_loans':total_loans,
        'pending':pending,
        'approved':approved
    }

    return render(request,'admin_dashboard.html',context)
  
def admin_logout(request):

    del request.session['admin']

    return redirect('/admin-login/')
  
  
  
def all_loans(request):

    if not request.session.get('admin'):
        return redirect('/admin-login/')

    loans = LoanApplication.objects.all()

    return render(request,'all_loans.html',{'loans':loans})
  

import math
from django.shortcuts import render, redirect, get_object_or_404
import math
from .models import LoanApplication, LoanApproval

def approve_loan(request, id):
    # Safely fetch loan or return 404 if not found
    loan = get_object_or_404(LoanApplication, id=id)

    if request.method == "POST":
        try:
            interest = float(request.POST.get('interest'))
            duration = int(request.POST.get('duration'))

            # EMI Calculation
            P = loan.loan_amount
            R = interest / (12 * 100)  # Monthly interest rate
            N = duration

            emi = (P * R * math.pow(1 + R, N)) / (math.pow(1 + R, N) - 1)

            # Create Loan Approval
            LoanApproval.objects.create(
                loan=loan,
                approved_amount=P,
                interest_rate=interest,
                emi=round(emi, 2),
                duration=duration
            )

            # Update loan status
            loan.status = "Approved"
            loan.save()

            return redirect('/all-loans/')

        except Exception as e:
            # Optional: handle form errors
            return render(request, 'approve_loan.html', {'loan': loan, 'error': str(e)})

    return render(request, 'approve_loan.html', {'loan': loan})
  
def reject_loan(request,id):

    loan = LoanApplication.objects.get(id=id)

    loan.status = "Rejected"
    loan.save()

    return redirect('/all-loans/')
  
  
def emi_calculator(request):
    return render(request,'emi_calculator.html')
  
from django.shortcuts import render, get_object_or_404
from .models import LoanApplication, LoanApproval

def loan_details(request, id):
    # get the loan, or 404 if not found
    loan = get_object_or_404(LoanApplication, id=id)
    # if approved, get approval details
    approval = LoanApproval.objects.filter(loan=loan).first()
    return render(request, 'loan_details.html', {'loan': loan, 'approval': approval})
  
  
def emi_payment(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/login/')

    loans = LoanApproval.objects.filter(
        loan__user_id=user_id
    )

    return render(request,'emi_payment.html',{'loans':loans})
  
def pay_emi(request,id):

    loan = LoanApproval.objects.get(id=id)

    paid_count = Payment.objects.filter(
        loan=loan.loan
    ).count()

    next_emi = paid_count + 1

    if request.method == "POST":

        amount = request.POST.get('amount')
        method = request.POST.get('method')

        Payment.objects.create(

            loan=loan.loan,
            amount=amount,
            payment_method=method,
            emi_number=next_emi

        )

        return redirect('/payment-history/')

    return render(request,'pay_emi.html',{'loan':loan,'emi':next_emi})
  
def payment_history(request):

    user_id = request.session.get('user_id')

    payments = Payment.objects.filter(
        loan__user__id=user_id
    )

    return render(request,'payment_history.html',{'payments':payments})
  
def emi_status(request):

    user_id = request.session.get('user_id')

    loans = LoanApproval.objects.filter(
        loan__user_id=user_id
    )

    data = []

    for loan in loans:

        total = loan.duration

        paid = Payment.objects.filter(
            loan=loan.loan
        ).count()

        remaining = total - paid

        data.append({
            'loan':loan,
            'total':total,
            'paid':paid,
            'remaining':remaining
        })

    return render(request,'emi_status.html',{'data':data})
  
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import *


def download_receipt(request,id):

    payment = Payment.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    p.setFont("Helvetica", 14)

    p.drawString(200,800,"Loan EMI Payment Receipt")

    p.setFont("Helvetica", 12)

    p.drawString(100,750,f"Customer Name : {payment.loan.user.full_name}")
    p.drawString(100,720,f"Loan Amount : {payment.loan.loan_amount}")
    p.drawString(100,690,f"EMI Number : {payment.emi_number}")
    p.drawString(100,660,f"Paid Amount : {payment.amount}")
    p.drawString(100,630,f"Payment Method : {payment.payment_method}")
    p.drawString(100,600,f"Payment Date : {payment.payment_date}")

    p.drawString(100,550,"Status : Payment Successful")

    p.drawString(100,500,"Thank you for your payment")

    p.showPage()
    p.save()

    return response
  
  
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch



from django.http import HttpResponse

def loan_certificate(request,id):

    loan = LoanApproval.objects.get(id=id)

    total_emi = loan.duration

    paid_emi = Payment.objects.filter(
        loan=loan.loan
    ).count()

    if paid_emi != total_emi:
        return HttpResponse("Loan not completed yet")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Loan_Certificate.pdf"'

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        "<b>Loan Closure Certificate</b>",
        ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            alignment=TA_CENTER,
            textColor=colors.black
        )
    )

    story.append(title)
    story.append(Spacer(1, 20))

    text = f"""
    This is to certify that <b>{loan.loan.user.full_name}</b> 
    has successfully completed the loan repayment.

    Loan Amount : {loan.approved_amount} <br/>
    Interest Rate : {loan.interest_rate}% <br/>
    Duration : {loan.duration} Months <br/>

    All EMI payments have been successfully completed.
    
    This loan account is now closed.
    """

    story.append(Paragraph(text, styles["Normal"]))
    story.append(Spacer(1, 40))

    story.append(Paragraph("Authorized Signature", styles["Normal"]))

    doc = SimpleDocTemplate(response, pagesize=A4)
    doc.build(story)

    return response
  
  
  
from django.db.models import Sum
import json
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth
import json
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth
import json
from django.contrib.auth.models import User

def loan_analytics(request):

    total_users = User.objects.count()  # Total registered users

    total_loans = LoanApplication.objects.count()
    approved = LoanApproval.objects.count()
    rejected = LoanApplication.objects.filter(status="Rejected").count()
    total_amount = LoanApproval.objects.aggregate(Sum('approved_amount'))['approved_amount__sum'] or 0
    total_emi = Payment.objects.count()

    # Monthly data as before
    monthly_loans = LoanApplication.objects.annotate(
        month=ExtractMonth('applied_date')
    ).values('month').annotate(count=Count('id')).order_by('month')

    monthly_amount = LoanApproval.objects.annotate(
        month=ExtractMonth('approval_date')
    ).values('month').annotate(total=Sum('approved_amount')).order_by('month')

    months = []
    loan_counts = []
    loan_amounts = []

    for m in monthly_loans:
        months.append(m['month'])
        loan_counts.append(m['count'])

    for m in monthly_amount:
        loan_amounts.append(m['total'])

    data = {
        'total_users': total_users,
        'total_loans': total_loans,
        'approved': approved,
        'rejected': rejected,
        'total_amount': total_amount,
        'total_emi': total_emi,
        'months': json.dumps(months),
        'loan_counts': json.dumps(loan_counts),
        'loan_amounts': json.dumps(loan_amounts)
    }

    return render(request, 'loan_analytics.html', {'data': data})


from django.shortcuts import render
from .models import LoanApplication

def pending_loans(request):
    loans = LoanApplication.objects.filter(status='Pending')
    return render(request, 'pending_loans.html', {'loans': loans})


from django.shortcuts import render
from .models import LoanApplication

def approved_loans(request):
    loans = LoanApplication.objects.filter(status='Approved')
    return render(request, 'approved_loans.html', {'loans': loans})


