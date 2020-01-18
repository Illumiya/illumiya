'''
Add core admin modules!
'''

from django.contrib import admin

from .models import *
from .forms import BlogAdminForm, CourseSectionAdminForm

class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm

class CourseSectionAdmin(admin.ModelAdmin):
    form = CourseSectionAdminForm


admin.site.register(Blog, BlogAdmin)
admin.site.register(Gallery)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(BlogTopic)
admin.site.register(BlogRatingIntermediate)
admin.site.register(BlogLikeIntermediate)
admin.site.register(VideoCategory)
admin.site.register(Video)
admin.site.register(CourseCategory)
admin.site.register(Section, CourseSectionAdmin)
admin.site.register(CourseSection)
admin.site.register(Course)
admin.site.register(UserCourse)
admin.site.register(PaymentCustomer)
admin.site.register(PaymentDetail)
