from django.views.generic.base import TemplateView, View
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site

from django_comments_xtd.api.views import CommentCreate
from rest_framework.response import Response
from django_comments.signals import comment_was_posted
from django_comments_xtd import views as comments_views
from django_comments_xtd import django_comments
from django_comments import get_form


from django.conf import settings
from .models import Blog
from .utils import send_email

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(home_page=True)
        return context

class BlogListView(TemplateView):
    template_name = 'core/blog_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = []
        page = int(self.request.GET.get('page', 1))
        blog_list = Blog.objects.all().order_by('-id')
        exclude_ids = []
        add_blog_row_counter = []
        end_blog_row_counter = []

        if page == 1 and blog_list.exists():
            DEFAULT_PAGE_SIZE = 18
            top_rate_blogs = sorted(blog_list, key=lambda i: i.get_rating, reverse=True)
            exclude_ids.append(top_rate_blogs[0].id)
            blogs.append(top_rate_blogs[0])
            top_views_blog = blog_list.exclude(id__in=exclude_ids).order_by('-views')
            top_views_ids = top_views_blog.values_list('id', flat=True)
            exclude_ids.extend(top_views_ids[:3])
            blogs.extend(list(top_views_blog[:3]))
            popular_blog_ids = top_views_ids[3:5]
            exclude_ids.extend(popular_blog_ids)
            other_blogs = blog_list.exclude(id__in=exclude_ids)
            blogs.extend(list(other_blogs[:2]))
            if popular_blog_ids:
                blogs.extend(list(Blog.objects.filter(id__in=popular_blog_ids)))
            # Need to optimize it to not change the list
            blogs.extend(list(other_blogs[2:]))
            top_viewed_loop_counter = [2, 3, 4]
            add_blog_row_counter = [1, 5, 8, 11, 15]
            end_blog_row_counter = [4, 7, 10, 14, 18]
            context.update(top_viewed_loop_counter=top_viewed_loop_counter)
        else:
            DEFAULT_PAGE_SIZE = 20
            blogs = blog_list
            add_blog_row_counter = [1, 5, 9, 13, 17]
            end_blog_row_counter = [4, 8, 12, 16, 18]
        paginator = Paginator(blogs, DEFAULT_PAGE_SIZE)
        #print(blog_list, "blog_list")
        blogs = paginator.get_page(page)
        blog_list = blogs.object_list
        print(blogs, blogs.object_list, "BLLL")
        context.update(blogs=paginator.get_page(page),
                       blog_list=blog_list,
                       add_blog_row_counter=add_blog_row_counter,
                       end_blog_row_counter=end_blog_row_counter)
        print(context, "context")
        return context

class BlogDetailView(TemplateView):
    template_name = 'core/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = Blog.objects.get(id=kwargs['pk'])
        blog.views += 1
        blog.save()
        """data = {'name': self.request.user.get_full_name().title(),
                'email': self.request.user.email,
                'object': blog}
        comment_form = get_form()(blog, data)"""
        recommended_blogs = Blog.objects.all().exclude(id=blog.id).order_by('?')[:10]
        context.update(blog=blog,
                       recommended_blogs=recommended_blogs)
                       #comment_form=comment_form)
        return context

class ContactView(View):
    '''
    Send contact mail to admin!
    '''

    def post(self, request, *ar, **kwargs):
        data = request.POST
        result = {"status": "success"}
        subject = 'Illumiya: New contactus message'
        to_email = settings.ADMIN_EMAIL
        html_template_name = 'email/contact_us.html'
        context = {'contact_name': data['name'],
                   'contact_email': data['email'],
                   'contact_message': data['message']}
        send_email(subject,
                   to_email,
                   html_template_name,
                   context)
        return JsonResponse(result)

class CreateCommentView(View):

    def post(self, request, *args, **kwargs):
        #serializer_class = serializers.WriteCommentSerializer
        result = {}
        data = request.POST
        blog = Blog.objects.get(id=4)
        self.form = get_form()(blog, data=data)
        #self.form = django_comments.get_form()(blog)
        print(self.form, "FORM")
        if self.form.is_valid():
            #self.form = form(blog)
            pass
        else:
            print(self.form.errors)

        site = get_current_site(request)
        resp = {
            'code': -1,
            'comment': self.form.get_comment_object(site_id=site.id)
        }
        resp['comment'].ip_address = request.META.get("REMOTE_ADDR", None)

        if request.user.is_authenticated:
            resp['comment'].user = request.user

        if (
                not settings.COMMENTS_XTD_CONFIRM_EMAIL or
                request.user.is_authenticated
        ):
            if not comments_views._comment_exists(resp['comment']):
                new_comment = comments_views._create_comment(resp['comment'])
                resp['comment'].xtd_comment = new_comment
                confirmation_received.send(sender=TmpXtdComment,
                                           comment=resp['comment'],
                                           request=request)
                comment_was_posted.send(sender=new_comment.__class__,
                                        comment=new_comment,
                                        request=request)
                if resp['comment'].is_public:
                    resp['code'] = 201
                    #views.notify_comment_followers(new_comment)
                else:
                    resp['code'] = 202
        return JsonResponse(result)
