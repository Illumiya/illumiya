'''
Add the core forms here!
'''

from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Blog

class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        exclude = ('created_date',)

