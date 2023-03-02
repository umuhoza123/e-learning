from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .newfields import OrderField
# Create your models here.

class Subject(models.Model):
    title=models.CharField(max_length=250)
    slug=models.CharField(max_length=30,unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


# models for course
class Course(models.Model):
    owner=models.ForeignKey(User,related_name='courses_created',on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE)
    title=models.CharField(max_length=30)
    slug=models.CharField(max_length=30)
    overview=models.TextField()
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created']

    def __str__(self):
        return self.title

#models of module

class Module(models.Model):
    course=models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title=models.CharField(max_length=500)
    description=models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.title}.{self.order}' 
    
class Content(models.Model):
 module = models.ForeignKey(Module,
 related_name='contents',
 on_delete=models.CASCADE)
 content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to={'model_in':('text','video')})
 object_id = models.PositiveIntegerField()
 item = GenericForeignKey('content_type', 'object_id')
 order = OrderField(blank=True, for_fields=['module'])

 class Meta:
    ordering = ['order']
    
# model that contain abstract
class ItemBase(models.Model):
    owner=models.ForeignKey(User,related_name='%(class)s_related',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
class Text (ItemBase):
    content = models.TextField()

class Video (ItemBase):
    url=models.URLField()



  
