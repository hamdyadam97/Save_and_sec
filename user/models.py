from django.core.exceptions import ValidationError
from django.db import models
import datetime
# Create your models here.



 
        

class Section(models.Model):
    key = models.CharField(max_length=50, unique=True, verbose_name="المفتاح (مثلاً about, services)")
    title_ar = models.CharField(max_length=200, verbose_name="العنوان (عربي)")
    title_en = models.CharField(max_length=200, verbose_name="العنوان (إنجليزي)")
    description_ar = models.TextField(verbose_name="الوصف (عربي)")
    description_en = models.TextField(verbose_name="الوصف (إنجليزي)")
    image = models.ImageField(upload_to='section/',blank=True,null=True)

    def __str__(self):
        return self.key


class Job(models.Model):
    LEVEL_CHOICES = [
        ('Manager', 'مدير'),
        ('Eng', 'مهندس'),
        ('Tech', 'فني'),
        ('Emp', 'موظف'),
    ]

    title_en = models.CharField(max_length=100)         # Example: Project Manager
    title_ar = models.CharField(max_length=100)         # مثال: مدير مشروع

    description_en = models.TextField()
    description_ar = models.TextField()

    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.title_en} / {self.title_ar}"

    def get_title(self, lang):
        return self.title_ar if lang == 'ar' else self.title_en

    def get_description(self, lang):
        return self.description_ar if lang == 'ar' else self.description_en



class Employee(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    img = models.ImageField(upload_to='emp',blank=True, null=True)
    job = models.ForeignKey('Job', on_delete=models.SET_NULL, null=True)
    date_joined = models.DateField(auto_now_add=True)
    residency_end_date = models.DateField(default=datetime.date(2025, 12, 31))

    def clean(self):
        if self.job and self.job.level == 'Manager':
            existing_manager = Employee.objects.filter(job__level='Manager')
            if self.pk:
                existing_manager = existing_manager.exclude(pk=self.pk)
            if existing_manager.exists():
                raise ValidationError("لا يمكن إضافة أكثر من مدير واحد.")

    def save(self, *args, **kwargs):
        self.full_clean()  # تأكد من تشغيل clean()
        super().save(*args, **kwargs)

    def __str__(self, lang=None):
        return self.name_ar





class CompanyWork(models.Model):
    # اسم الشركة
    company_name_ar = models.CharField(max_length=255)
    company_name_en = models.CharField(max_length=255)

    # عنوان الخدمة
    service_title_ar = models.CharField(max_length=255)
    service_title_en = models.CharField(max_length=255)

    # وصف الخدمة
    service_description_ar = models.TextField()
    service_description_en = models.TextField()

    image = models.ImageField(upload_to='company_works/', null=True, blank=True)
    video = models.FileField(upload_to='company_works/videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name_en

class Blog(models.Model):
    title_en = models.CharField(max_length=200)  # عنوان المقال بالإنجليزية
    title_ar = models.CharField(max_length=200)  # عنوان المقال بالعربية
    content_en = models.TextField()  # محتوى المقال بالإنجليزية
    content_ar = models.TextField()  # محتوى المقال بالعربية
    published_at = models.DateTimeField(auto_now_add=True)  # تاريخ النشر
    image = models.ImageField(upload_to='blog/', null=True, blank=True)

    def __str__(self):
        return self.title_en  # عرض العنوان بالإنجليزية في الـ admin panel



from django.utils.translation import gettext_lazy as _





class CompanyLicense(models.Model):
    name_ar = models.CharField(max_length=255, verbose_name=_("اسم السجل بالعربي"))
    name_en = models.CharField(max_length=255, verbose_name=_("اسم السجل بالإنجليزي"))
    start_date = models.DateField(verbose_name=_("بداية السجل"),null=True )
    end_date = models.DateField(verbose_name=_("نهاية السجل"),null=True)
    file = models.FileField(upload_to='licenses/', null=True, blank=True, verbose_name=_("الملف"))
    unified_number = models.CharField(max_length=100, unique=True, verbose_name=_("رقم الموحد للسجل"))
    license_number = models.CharField(max_length=100, verbose_name=_("رقم السجل"))
    is_active = models.BooleanField(default=True, verbose_name=_("هل مسموع"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("سوفت دليت"))

    renewed_from = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='renewals',
        verbose_name=_("تم تجديده من")
    )

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        # ممكن تعرض الاسم بالعربي لو متوفر، وإلا بالإنجليزي
        return self.name_ar or self.name_en

    class Meta:
        verbose_name = _("السجل التجاري")
        verbose_name_plural = _("السجلات التجارية")
