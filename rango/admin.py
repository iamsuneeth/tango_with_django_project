from django.contrib import admin
from models import Category, Page

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):

	prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):

	list_display = ('title','Category','url')


admin.site.register(Category,CategoryAdmin)
admin.site.register(Page, PageAdmin)