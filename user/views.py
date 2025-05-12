from django.shortcuts import render
from django.utils.translation import get_language
from .models import Section, Employee, CompanyWork, Blog


def index_view(request):
    lang = get_language()
    sections = Section.objects.all()
    content = {}
    for section in sections:
        content[section.key] = {
            'title': section.title_ar if lang == 'ar' else section.title_en,
            'description': section.description_ar if lang == 'ar' else section.description_en,
            'image':section.image       }
    # Get the manager (if one exists)
    manager = Employee.objects.filter(job__level='Manager').select_related('job').first()
    employees = Employee.objects.exclude(job__level='Manager').select_related('job')
    blogs = Blog.objects.all()
    blogs_data = []
    for blog in blogs:
        blogs_data.append({
            'title': blog.title_ar if lang == 'ar' else blog.title_en,
            'job_title': blog.title_ar if lang == 'ar' else blog.title_en,
            'content': blog.content_ar if lang == 'ar' else blog.content_en,
            'image': blog.image,
            'published_at':blog.published_at
        })

    employees_data = []
    for emp in employees:
        employees_data.append({
            'name': emp.name_ar if lang == 'ar' else emp.name_en,
            'phone': emp.phone,
            'email': emp.email,
            'job_title': emp.job.title_ar if lang == 'ar' else emp.job.title_en,
            'job_description': emp.job.description_ar if lang == 'ar' else emp.job.description_en,
            'image': emp.img,
        })

    if manager:
        manager_data = {
            'name': manager.name_en if lang == 'en' else manager.name_ar,
            'phone': manager.phone,
            'email': manager.email,
            'job_title': manager.job.title_en if lang == 'en' else manager.job.title_ar,
            'job_description': manager.job.description_en if lang == 'en' else manager.job.description_ar,
            'image':manager.img
            # ترجم لو عندك وصفين
        }
    else:
        manager_data = None
    # ✅ استرجاع الأعمال مع الشركات
    works = CompanyWork.objects.all().order_by('-created_at')

    works_data = []
    for work in works:
        print(work.image.url)
        works_data.append({
            'company_name': work.company_name_ar if lang == 'ar' else work.company_name_en,
            'service_title': work.service_title_ar if lang == 'ar' else work.service_title_en,
            'service_description': work.service_description_ar if lang == 'ar' else work.service_description_en,
            'image': work.image if work.image else None,
            'video': work.video if work.video else None,
        })

    return render(request, 'index.html', {
        'sections': content,
        'manager': manager_data,  # Pass manager data to the template
        'employees':employees_data,
        'company_works': works_data,  # ✅ تمرير البيانات للقالب
        "blogs":blogs_data
    })
