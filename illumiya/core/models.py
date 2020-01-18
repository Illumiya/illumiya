'''
Add all core models here!
'''

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

from django.conf import settings
from ckeditor.fields import RichTextField


class VideoCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % self.name

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    @property
    def liked_count(self):
        return self.likes.filter(liked=True).count()

    def get_absolute_url(self):
        return "/blog/detail/{0}/".format(self.id)

class BlogRatingIntermediate(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)

class BlogLikeIntermediate(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    #ranking = models.IntegerField(default=100)

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    url = models.URLField(null=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.title

    @property
    def get_video_thumbnail(self):
        if self.url.find('?v=') >= 0:
            video_id = self.url.split('?v=')[1]
        else:
            video_id = self.url.rsplit('/', 1)[1]
        print(self.url, "self.url")
        print(video_id, "video_id")
        image = "https://img.youtube.com/vi/{}/0.jpg".format(video_id)
        return image

class CourseCategory(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)

    def __str__(self):
        if self.parent:
            return "{}-{}".format(self.parent.name, self.name)
        else:
            return "{}".format(self.name)

class Section(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    video = models.FileField(upload_to='section/videos/y/m/d/',
                             null=True,
                             blank=True)
    notes = models.TextField(null=True,
                             blank=True)
    order = models.IntegerField(default=1)
    #game = models.ForeignKey(Game)
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)

    def __str__(self):
        return "%s" % self.title

class Course(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, related_name='course_category')
    sub_category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, related_name='course_sub_category')
    section = models.ManyToManyField('Section', through='CourseSection')
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.name

class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.course, self.section)

class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    is_completed = models.BooleanField()
    section_completed = models.ForeignKey(Section,
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True,
                                          related_name='user_course_section_completed')
    section_reading = models.ForeignKey(Section,
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        blank=True,
                                        related_name='user_course_section_reading')

    def __str__(self):
        return "{} - {}".format(self.user, self.course)

class PaymentCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.user)

class PaymentDetail(models.Model):
    payment_customer = models.ForeignKey(PaymentCustomer, on_delete=models.CASCADE)
    plan_id = models.CharField(max_length=200)
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200)
    payment_signature = models.CharField(max_length=200)
    subscription_id = models.CharField(max_length=200)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.payment_customer)