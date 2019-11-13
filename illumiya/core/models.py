'''
Add all core models here!
'''

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

from ckeditor.fields import RichTextField

class BlogTopic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % self.name

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=False)
    rate = models.FloatField()

    def __str__(self):
        return "%s" % self.rate

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=False)
    liked = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.user

class Gallery(models.Model):
    image = models.ImageField(upload_to='blog/')

    def __str__(self):
        return "%s" % self.image

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=True)
    title = models.CharField(max_length=300)
    topic = models.ForeignKey(BlogTopic,
                              on_delete=False,
                              blank=True,
                              null=True)
    content = models.TextField()
    rating = models.ManyToManyField(Rating, through='BlogRatingIntermediate')
    #gallery = models.ManyToManyField(Gallery, through='BlogGalleryIntermediate')
    main_image = models.ImageField(upload_to='blog/%d/%m/%Y/',
                                   blank=True,
                                   null=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(Like, through='BlogLikeIntermediate')
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.title

    @property
    def get_rating(self):
        result = self.rating.aggregate(average_rating=Avg('rate'))
        average_rating = result['average_rating'] if result['average_rating'] else 0
        return average_rating

    def get_absolute_url(self):
        return "/blog/detail/{0}/".format(self.id)

class BlogRatingIntermediate(models.Model):
    blog = models.ForeignKey(Blog, on_delete=True)
    rating = models.ForeignKey(Rating, on_delete=True)

class BlogLikeIntermediate(models.Model):
    blog = models.ForeignKey(Blog, on_delete=True)
    like = models.ForeignKey(Like, on_delete=True)
    #ranking = models.IntegerField(default=100)