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
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import LoanApproval, Payment

def pay_emi(request,id):

    loan = LoanApproval.objects.get(id=id)

    paid_count = Payment.objects.filter(
        loan=loan.loan
    ).count()

    if paid_count >= loan.duration:
        return render(request, 'loan_completed.html', {'loan': loan})

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

from django.shortcuts import render
from .models import LoanApproval, Payment

def emi_payment(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/login/')

    loans = LoanApproval.objects.filter(
        loan__user_id=user_id
    )

    loans_data = []

    for loan in loans:
        paid = Payment.objects.filter(loan=loan.loan).count()
        remaining = loan.duration - paid

        loans_data.append({
            'loan': loan,
            'paid': paid,
            'remaining': remaining
        })

    return render(request, 'emi_payment.html', {'loans_data': loans_data})
  
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


from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

def download_receipt(request,id):

    payment = Payment.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="EMI_Receipt.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    # ---------- Header ----------
    p.setFont("Helvetica-Bold",16)
    p.drawString(200,800,"EasyLoan Finance Pvt Ltd")

    p.setFont("Helvetica",10)
    p.drawString(220,785,"Loan Payment Receipt")

    # Line
    p.setStrokeColor(colors.black)
    p.line(50,770,550,770)

    # ---------- Receipt Box ----------
    p.setStrokeColor(colors.grey)
    p.rect(50,500,500,240, stroke=1, fill=0)

    # ---------- Title ----------
    p.setFont("Helvetica-Bold",14)
    p.drawString(200,730,"EMI PAYMENT RECEIPT")

    # ---------- Customer Details ----------
    p.setFont("Helvetica-Bold",12)
    p.drawString(70,700,"Customer Details")

    p.setFont("Helvetica",11)
    p.drawString(70,675,f"Customer Name : {payment.loan.user.full_name}")
    p.drawString(70,655,f"Loan Amount : ₹ {payment.loan.loan_amount}")
    p.drawString(70,635,f"EMI Number : {payment.emi_number}")

    # ---------- Payment Details ----------
    p.setFont("Helvetica-Bold",12)
    p.drawString(70,600,"Payment Details")

    p.setFont("Helvetica",11)
    p.drawString(70,575,f"Paid Amount : ₹ {payment.amount}")
    p.drawString(70,555,f"Payment Method : {payment.payment_method}")
    p.drawString(70,535,f"Payment Date : {payment.payment_date}")

    # ---------- Status ----------
    p.setFont("Helvetica-Bold",12)
    p.setFillColor(colors.green)
    p.drawString(70,510,"Status : Payment Successful")

    p.setFillColor(colors.black)

    # ---------- Footer Box ----------
    p.setStrokeColor(colors.grey)
    p.rect(50,400,500,70, stroke=1, fill=0)

    p.setFont("Helvetica",10)
    p.drawString(70,440,"This is a system generated receipt and does not require signature.")
    p.drawString(70,420,"Thank you for choosing EasyLoan Finance.")

    # ---------- Footer ----------
    p.line(50,380,550,380)

    p.setFont("Helvetica",9)
    p.drawString(200,360,"EasyLoan Finance Pvt Ltd")
    p.drawString(190,345,"Customer Support : support@easyloan.com")

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
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import inch

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

    # ---------- Title ----------
    title = Paragraph(
        "<b>EasyLoan Finance Pvt Ltd</b>",
        ParagraphStyle(
            'Company',
            parent=styles['Heading1'],
            alignment=TA_CENTER,
            textColor=colors.black
        )
    )

    story.append(title)
    story.append(Spacer(1, 10))

    subtitle = Paragraph(
        "<b>Loan Closure Certificate</b>",
        ParagraphStyle(
            'Title',
            parent=styles['Heading2'],
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
    )

    story.append(subtitle)
    story.append(Spacer(1, 30))


    # ---------- Certificate Text ----------
    text = f"""
    This is to certify that <b>{loan.loan.user.full_name}</b> has successfully 
    completed the repayment of the loan provided by <b>EasyLoan Finance Pvt Ltd</b>.

    All EMI payments related to the below loan account have been successfully completed.
    """

    story.append(Paragraph(text, styles["Normal"]))
    story.append(Spacer(1, 25))


    # ---------- Loan Details Table ----------
    data = [
        ["Customer Name", loan.loan.user.full_name],
        ["Loan Amount", f"₹ {loan.approved_amount}"],
        ["Interest Rate", f"{loan.interest_rate}%"],
        ["Loan Duration", f"{loan.duration} Months"],
        ["Loan Status", "Closed"]
    ]

    table = Table(data, colWidths=[200, 250])

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

        ('BACKGROUND',(0,0),(0,-1),colors.lightgrey),
        ('TEXTCOLOR',(0,0),(0,-1),colors.black),

        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),10),
        ('BOTTOMPADDING',(0,0),(-1,-1),10),
    ]))

    story.append(table)
    story.append(Spacer(1, 40))


    # ---------- Closing Text ----------
    closing = """
    This certificate is issued upon successful repayment of all dues. 
    The loan account is now officially closed with no pending balance.
    """

    story.append(Paragraph(closing, styles["Normal"]))
    story.append(Spacer(1, 60))


    # ---------- Signature Section ----------
    signature_table = Table([
        ["", ""],
        ["Authorized Signature", "Company Seal"]
    ], colWidths=[250, 250])

    signature_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('LINEABOVE',(0,0),(0,0),1,colors.black),
        ('LINEABOVE',(1,0),(1,0),1,colors.black),
    ]))

    story.append(signature_table)


    # ---------- Footer ----------
    story.append(Spacer(1, 40))

    footer = Paragraph(
        "EasyLoan Finance Pvt Ltd | Customer Support : support@easyloan.com",
        ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            alignment=TA_CENTER,
            textColor=colors.grey
        )
    )

    story.append(footer)

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


