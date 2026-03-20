from django.shortcuts import render,redirect
from django.conf import settings
from .models import doctor,patient,appointment
from django.core.mail import send_mail
from google_calendar import create_event
from datetime import datetime, timedelta
import pytz
import resend
import os
# Create your views here.

resend.api_key = os.getenv("RESEND_API_KEY")

def index(request):
    return render(request,'index.html')

def doc_signup(request):
    if request.method=="POST":
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        prof_photo=request.FILES.get('prof_photo')
        exp=request.POST['exp']
        qualification=request.POST['qualification']
        password=request.POST['password']

        s1=doctor(name=name,phone=phone,email=email,prof_photo=prof_photo,exp=exp,qualification=qualification,password=password)
        s1.save()

        return render(request,"index.html")


    return render(request,'doc_signup.html')

def pat_signup(request):
    if request.method=="POST":
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        password=request.POST['password']

        p1=patient(name=name,phone=phone,email=email,password=password)
        p1.save()

        return render(request,"pat_login.html")
    return render(request,'pat_signup.html')

def pat_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        p1 = patient.objects.filter(email=email, password=password).first()

        if p1:
            request.session['patient_id'] = p1.id
            request.session['name'] = p1.name
            return redirect('/pat_dash/')
        else:
            return render(request,'pat_login.html',{'msg':'Invalid Email or Password'})

    return render(request,'pat_login.html')


def doc_login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']

        try:
            d1=doctor.objects.get(email=email,password=password)

            request.session['doctor_id']=d1.id
            return redirect('/doc_dash/')

        except:
            return render(request,'doc_login.html',{'msg':'Invalid Email or Password'})

    return render(request,'doc_login.html')

def pat_dash(request):
    return render(request,'pat_dash.html')

def view_doctors(request):
    docs = doctor.objects.all()
    return render(request,"view_doctors.html",{'docs':docs})

def book_appointment(request, doc_id):

    doc = doctor.objects.get(id=doc_id)
    slots = ["10:00 AM","11:00 AM","12:00 PM","2:00 PM","3:00 PM"]

    if request.method == "POST":

        date = request.POST.get("date")
        slot = request.POST.get("slot")

        pat_id = request.session.get('patient_id')
        pat = patient.objects.get(id=pat_id)

        if appointment.objects.filter(doctor=doc, date=date, slot=slot).exists():

            return render(request,"book.html",{
                "doc":doc,
                "slots":slots,
                "msg":"Slot already booked"
            })

        appt = appointment.objects.create(
            doctor=doc,
            patient=pat,
            date=date,
            slot=slot
        )

        send_appointment_email(pat, doc, date, slot)

        ist = pytz.timezone("Asia/Kolkata")
        start_time = datetime.strptime(f"{date} {slot}", "%Y-%m-%d %I:%M %p")
        start_time = ist.localize(start_time)

        end_time = start_time + timedelta(minutes=30)

        create_event(
            summary="Doctor Appointment",
            description=f"Patient: {pat.name}, Doctor: Dr. {doc.name}",
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat()
        )



        return render(request,"book.html",{
            "doc":doc,
            "slots":slots,
            "msg":"Appointment Booked Successfully"
        })

    return render(request,"book.html",{"doc":doc,"slots":slots})

resend.api_key = os.getenv("RESEND_API_KEY")

def send_appointment_email(pat, doc, date, slot):
    try:
        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": pat.email,
            "subject": "Appointment Confirmation",
            "html": f"""
                <h3>Hello {pat.name},</h3>
                <p>Your appointment is confirmed.</p>

                <b>Doctor:</b> Dr. {doc.name}<br>
                <b>Date:</b> {date}<br>
                <b>Time:</b> {slot}
            """
        })
        print("Email sent:", response)   # 👈 ADD THIS
    except Exception as e:
        print("Email error:", e)

def my_appointments(request):
    pat_id = request.session.get('patient_id')
    pat = patient.objects.get(id=pat_id)
    apps = appointment.objects.filter(patient=pat)

    return render(request,"my_appointments.html",{"apps":apps})

def doc_dash(request):
    doc_id = request.session.get('doctor_id')
    doc = doctor.objects.get(id=doc_id)
    apps = appointment.objects.filter(doctor=doc)
    return render(request,"doc_dash.html",{"apps":apps})
