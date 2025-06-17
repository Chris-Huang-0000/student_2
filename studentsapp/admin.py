from django.contrib import admin
from studentsapp.models import student

# Register your models here.
class studentadmin(admin.ModelAdmin):
    list_display = ['id','name','sex','birthday','email','phone','address']
    list_filter = ('name','sex')
    search_fields = ['name']
    ordering = ('id',) #tuple中如果只有一筆資料存在，必須要加逗號，用以區分是單純的括號;或是tuple
admin.site.register(student,studentadmin)