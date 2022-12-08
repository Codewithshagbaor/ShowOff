from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserManager
from Base.models import User, Categorie, Verification
# Register your models here.
admin.site.register(User)
admin.site.register(Verification)
admin.site.unregister(Group)
@admin.register(Categorie)
class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}
