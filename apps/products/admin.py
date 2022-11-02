from gettext import gettext
from django.contrib import admin
from .models import *
from django.db.models.aggregates import Count
# from operator import not_
from django.http import HttpResponse
from django.core import serializers


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title','slug')
    search_fields = ('title',)
    ordering = ('title',)


def change_activity_state(modeladmin,request,queryset):
    result = queryset.update(is_active=False)
    message = gettext(f'{result} مورد تغییر کرد')
    modeladmin.message_user(request,message)

change_activity_state.short_description = 'فعال/غیرفعال سازی'


def export_json(modeladmin,request,queryset):
    response = HttpResponse(content_type='application/json')
    serializers.serialize('json',queryset,stream=response)
    return response


class ProductGroupInstanceInline(admin.TabularInline):
    model = ProductGroup

@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('title','parent','is_active','count_children','slug')
    list_filter = ('parent',)
    search_fields = ('title',)
    ordering = ('-is_active','-parent','title')
    inlines = [ProductGroupInstanceInline]
    actions = [change_activity_state,export_json]

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductGroupAdmin,self).get_queryset(*args, **kwargs)
        return qs.annotate(childrens=Count('children'))
    
    def count_children(self,obj):
        return obj.childrens
    
    count_children.short_description = 'زیر‌دسته‌ها'
    export_json.short_description = 'خروجی Json'