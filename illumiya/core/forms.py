'''
Add the core forms here!
'''

from django import forms
from django.utils.translation import ugettext_lazy as _

from django_comments_xtd.forms import XtdCommentForm
from django_comments_xtd.models import TmpXtdComment
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Blog, Video

class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        exclude = ('created_date',)


class CommentCustomForm(XtdCommentForm):
    name = forms.CharField(max_length=100,
                           widget=forms.HiddenInput())
    email = forms.EmailField(max_length=100,
                            widget=forms.HiddenInput())
    #followup = forms.BooleanField(widget=forms.HiddenInput())
    url = forms.CharField(max_length=100,
                           widget=forms.HiddenInput())

    def get_comment_create_data(self, site_id=None):
        data = super(CommentCustomForm, self).get_comment_create_data(site_id)
        #data.update({'title': self.cleaned_data['title']})
        return data

class VideoUploadForm(forms.ModelForm):
    url = forms.URLField(widget=forms.TextInput(attrs={'placeholder': '(Paste your video link here )'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 6}))

    class Meta:
        model = Video
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
