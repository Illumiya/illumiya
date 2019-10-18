'''
Add all core models here!
'''

from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=False)
    rate = models.FloatField()

class Gallery(models.Model):
    image = models.ImageField(upload_to='blog/')

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=False)
    title = models.CharField(max_length=300)
    content = models.TextField()
    rating = models.ManyToManyField(Rating, through='BlogRatingIntermediate')
    #gallery = models.ManyToManyField(Gallery, through='BlogGalleryIntermediate')
    main_image = models.ImageField(upload_to='blog/%d/%m/%Y/',
                                   blank=True,
                                   null=True)
    views = models.IntegerField(default=0)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.title

class BlogRatingIntermediate(models.Model):
    blog = models.ForeignKey(Blog, on_delete=False)
    rating = models.ForeignKey(Rating, on_delete=False)

"""class BlogGalleryIntermediate(models.Model):
    blog = models.ForeignKey(Blog, on_delete=False)
    gallery = models.ForeignKey(Gallery, on_delete=False)
    ranking = models.IntegerField(default=100)
"""