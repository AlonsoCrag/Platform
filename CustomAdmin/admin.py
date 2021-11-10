from django.contrib.admin import AdminSite

# Register your models here.
class Customized(AdminSite):
    login_template = 'admin_login.html'

site = Customized()
# This can change the default interface in the admin panel#
# You give this instance to:
# from django.contrib import admin
# admin.site = site

# Do this in all your Apps