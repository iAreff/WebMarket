from django.db.models import (Model, CharField, SlugField, ImageField, TextField, BooleanField, DateField,
                              PositiveIntegerField,
                              ForeignKey, ManyToManyField, CASCADE)
from django.utils import timezone
from utils import FileUploader

class Brand(Model):
    title = CharField(max_length=100,verbose_name='عنوان برند')
    uploader_instance = FileUploader('images','brand')
    image = ImageField(upload_to=uploader_instance.upload_image,verbose_name='تصویر برند')
    slug = SlugField(max_length=200,null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند‌ها'
        db_table = 'table_brand'


class ProductGroup(Model):
    title = CharField(max_length=100,verbose_name='عنوان گروه محصولات')
    uploader_instance = FileUploader('images','product_group')
    image = ImageField(upload_to=uploader_instance.upload_image,verbose_name='تصویر گروه محصولات')
    description = TextField(blank=True,null=True,verbose_name='توضیحات گروه محصولات')
    is_active = BooleanField(default=True,blank=True,verbose_name='وضعیت: فعال/غیرفعال')
    parent = ForeignKey('ProductGroup', verbose_name='والد گروه محصولات', on_delete=CASCADE,blank=True,null=True,related_name='children')
    slug = SlugField(max_length=200,null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'گروه محصولات'
        verbose_name_plural = 'گروه محصولات'
        db_table = 'table_product_group'


class Feature(Model):
    title = CharField(max_length=30,verbose_name='عنوان ویژگی')
    product_group = ManyToManyField(ProductGroup, verbose_name='گروه محصولات',related_name='features',db_table = 'table_product_group_feature')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی‌ها'
        db_table = 'table_feature'


class Product(Model):
    title = CharField(max_length=300,verbose_name='عنوان محصول')
    description = TextField(blank=True,null=True,verbose_name='توضیحات محصول')
    uploader_instance = FileUploader('images','product_main_image')
    image = ImageField(upload_to=uploader_instance.upload_image,verbose_name='تصویر محصول')
    price = PositiveIntegerField(default=0,verbose_name='قیمت محصول')
    product_group = ManyToManyField(ProductGroup, verbose_name='گروه محصولات',related_name='products',db_table='table_product_product_group')
    brand = ForeignKey(Brand,verbose_name='برند محصول',on_delete=CASCADE,null=True,related_name='products')
    is_active = BooleanField(default=True,blank=True,verbose_name='وضعیت: فعال/غیرفعال')
    slug = SlugField(max_length=200,null=True)
    register_date = DateField(auto_now_add=True,verbose_name='تاریخ درج')
    publish_date = DateField(default=timezone.now,verbose_name='تاریخ انتشار')
    update_date = DateField(auto_now=True,verbose_name='تاریخ بروزرسانی')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        db_table = 'table_product'
        

class ProductFeature(Model):
    product = ForeignKey(Product,on_delete=CASCADE,verbose_name = 'محصول')
    feature = ForeignKey(Feature,on_delete=CASCADE,verbose_name = 'ویژگی')
    detail = CharField(max_length=100,verbose_name = 'جزئیات')
    
    def __str__(self):
        return f'{self.product} - {self.feature} : {self.detail}'
    
    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی‌های محصولات'
        db_table = 'table_product_feature'


class ProductImages(Model):
    product = ForeignKey(Product,on_delete=CASCADE,verbose_name = 'محصول')
    uploader_instance = FileUploader('images','product_images')
    image = ImageField(upload_to=uploader_instance.upload_image,verbose_name='تصاویر محصول')
    
    class Meta:
        verbose_name = 'تصاویر محصول'
        verbose_name_plural = 'تصاویر محصولات'
        db_table = 'table_product_images'