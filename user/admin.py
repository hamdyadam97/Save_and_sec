from django.contrib import admin
from user.models import Section, Employee, Job, CompanyWork, Blog,CompanyLicense


# Register your models here.

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('key', 'title_ar', 'title_en')
    search_fields = ('key',)


admin.site.register(Employee)
admin.site.register(Job)

admin.site.register(CompanyWork)
admin.site.register(Blog)
admin.site.register(CompanyLicense)
