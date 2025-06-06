from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail

from ...models import CompanyLicense, Employee, EmployeeLeave, RentContract

class Command(BaseCommand):
    help = "إرسال تنبيهات عند اقتراب انتهاء المواعيد"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        reminder_day = today + timedelta(days=7)

        
        recipients = ['hamdyadam543@gmail.com']  

        # ✅ 1. السجل التجاري
        for lic in CompanyLicense.objects.filter(end_date__lte=reminder_day, end_date__gte=today):
            print('sssssssssssssssssssssssssssssssssssssssssssssssssss')
            self.send_email(
                subject_ar=f"انتهاء السجل التجاري: {lic.name}",
                subject_en=f"Commercial License Expiry: {lic.name}",
                due_date=lic.end_date,
                recipients=recipients
            )

       
        for emp in Employee.objects.filter(end_date__lte=reminder_day, end_date__gte=today):
            self.send_email(
                subject_ar=f"انتهاء إقامة الموظف: {emp.name}",
                subject_en=f"Employee Residency Expiry: {emp.name}",
                due_date=emp.residency_end_date,
                recipients=recipients
            )

       
        for leave in EmployeeLeave.objects.filter(end_date__lte=reminder_day, end_date__gte=today):
            self.send_email(
                subject_ar=f"نهاية إجازة الموظف: {leave.employee.name}",
                subject_en=f"Employee Leave Ending: {leave.employee.name}",
                due_date=leave.leave_end_date,
                recipients=recipients
            )

       
        for rent in RentContract.objects.filter(end_date__lte=reminder_day, end_date__gte=today):
            self.send_email(
                subject_ar=f"انتهاء عقد الإيجار: {rent.location}",
                subject_en=f"Rent Contract Expiry: {rent.location}",
                due_date=rent.rent_end_date,
                recipients=recipients
            )

    def send_email(self, subject_ar, subject_en, due_date, recipients):
        subject = f"{subject_ar} / {subject_en}"
        message = (
            f"🔔 تنبيه: الموعد هو {due_date}\n"
            f"🔔 Reminder: The due date is {due_date}"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email='muhammadsaad199719@gmail.com',  # غيّرها إلى بريد الإرسال
            recipient_list=recipients,
            fail_silently=False,
        )
