from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import CompanyLicense, Employee 
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from twilio.rest import Client




from_whatsapp_number = '' 
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

##@shared_task
##def send_periodic_whatsapp():
    ##today = timezone.now().date()
   ## reminder_day = today + timedelta(days=7)

    ##recipients = [
      ##  'whatsapp:+966XXXXXXXXX',
        ##'whatsapp:+966YYYYYYYY',
        ##'whatsapp:+966ZZZZZZZZ'
    ##]

    ##for lic in CompanyLicense.objects.filter(end_date__lte=reminder_day, end_date__gte=today):
      ##  body = f"📌 تنبيه: سجل تجاري '{lic.name}' سينتهي في {lic.end_date}"
        ##send_whatsapp_message(recipients, body)

    ##for emp in Employee.objects.filter(residency_end_date__lte=reminder_day, residency_end_date__gte=today):
      ##  body = f"📌 تنبيه: إقامة الموظف '{emp.name}' ستنتهي في {emp.residency_end_date}"
        ##send_whatsapp_message(recipients, body)

    ##for leave in EmployeeLeave.objects.filter(leave_end_date__lte=reminder_day, leave_end_date__gte=today):
      ##  body = f"📌 تنبيه: إجازة الموظف '{leave.employee.name}' ستنتهي في {leave.leave_end_date}"
        ##send_whatsapp_message(recipients, body)

    ##for rent in RentContract.objects.filter(rent_end_date__lte=reminder_day, rent_end_date__gte=today):
      ##  body = f"📌 تنبيه: عقد إيجار الموقع '{rent.location}' سينتهي في {rent.rent_end_date}"
        ##send_whatsapp_message(recipients, body)


##def send_whatsapp_message(recipients, body):
    ##for number in recipients:
      ##  try:
        ##    message = client.messages.create(
          ##      body=body,
            ##    from_=from_whatsapp_number,
              ##  to=number
            ##)
            ##print(f"✅ WhatsApp sent to {number}: {message.sid}")
        ##except Exception as e:
          ##  print(f"❌ Error sending to {number}: {e}")





@shared_task
def send_periodic_email():
    today = timezone.now().date()
    recipients = ['hamdyadam543@gmail.com', 'mohamedhelmy9974@gmail.com']
    for lic in CompanyLicense.objects.filter(is_active=True):
        if lic.end_date:
            days_left = (lic.end_date - today).days

            if days_left < 0:
                status = "انتهى ويجب التجديد فوراً / Already expired – urgent renewal required"
            elif days_left <= 30:
                status = f"باقي {days_left} يومًا على انتهاء السجل / {days_left} days remaining – please renew soon"
            else:
                continue  # لا حاجة لإرسال بريد إذا السجل لن ينتهي قريبًا

            body_ar = f"""
            اسم السجل: {lic.name_ar}
            رقم السجل: {lic.license_number}
            الرقم الموحد: {lic.unified_number}
            تاريخ الانتهاء: {lic.end_date}
            الحالة: {status}
            """

            body_en = f"""
            License Name: {lic.name_en}
            License Number: {lic.license_number}
            Unified Number: {lic.unified_number}
            Expiry Date: {lic.end_date}
            Status: {status}
            """

            send_expiry_email(
                subject_ar=f"إشعار بانتهاء السجل التجاري: {lic.name_ar}",
                subject_en=f"Commercial License Expiry Notice: {lic.name_en}",
                due_date=lic.end_date,
                recipients=recipients,
                status=status,
                body_ar=body_ar,
                body_en=body_en
            )



def send_expiry_email(subject_ar, subject_en, due_date, recipients, status, body_ar="", body_en=""):
    subject = f"{subject_ar} / {subject_en}"
    context = {
        'subject_ar': subject_ar,
        'subject_en': subject_en,
        'due_date': due_date.strftime('%Y-%m-%d'),
        'status': status,
        'body_ar': body_ar,
        'body_en': body_en,
    }
    print(context,'ssssssssssssssssssssssssssss')
    body = render_to_string('sendmail.html', context)

    try:
        send_email(
            subject=subject,
            email=recipients,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        print("✅ Email sent:", subject)
    except Exception as e:
        print("❌ ERROR SENDING EMAIL:", e)


def send_email(subject, email, body, from_email=settings.DEFAULT_FROM_EMAIL):
    msg = EmailMultiAlternatives()
    msg.from_email = from_email
    msg.subject = subject.strip()
    msg.body = body
    msg.attach_alternative(body, "text/html")
    msg.to = email if isinstance(email, list) else [email]
    msg.send()
