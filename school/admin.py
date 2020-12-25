from django.contrib import admin
from school.models import School,Book,BookExtra
# Register your models here.
admin.site.register(School)
admin.site.register(Book)
admin.site.register(BookExtra)
