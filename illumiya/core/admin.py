'''
Add core admin modules!
'''

from django.contrib import admin

from .models import *
from .forms import BlogAdminForm

class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm

admin.site.register(Blog, BlogAdmin)
admin.site.register(Gallery)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(BlogTopic)
admin.site.register(BlogRatingIntermediate)
admin.site.register(BlogLikeIntermediate)