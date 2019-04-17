from django.contrib import admin
from . import models

class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "semester", "year")
    prepopulated_fields = {"slug": ("author",)}

class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "author")

admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Document, DocumentAdmin)
