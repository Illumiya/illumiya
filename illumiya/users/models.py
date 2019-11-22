from django.db import models
from django.contrib.auth.models import User


USER_TYPE_CHOICES = (
    ('school', 'school'),
    ('student', 'student')
)

COUNTRY_CHOICES = (
    ('IN', 'India'),
    ('UK', 'United Kingdom')
)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=True)
    user_type = models.CharField(max_length=10,
                                 choices=USER_TYPE_CHOICES)
    profile_pic = models.ImageField(upload_to='profile/')
    street = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50,
                            null=True,
                            blank=True)
    state = models.CharField(max_length=50,
                             null=True,
                             blank=True)
    country = models.CharField(max_length=20,
                               choices=COUNTRY_CHOICES,
                               null=True,
                               blank=True)
    mobile_number = models.CharField(max_length=14)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.user)

