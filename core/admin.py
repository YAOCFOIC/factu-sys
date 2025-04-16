from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(InvoiceDetail)
admin.site.register(Backup)
admin.site.register(Report)
admin.site.register(TaxValidation)
admin.site.register(XMLUbl)