from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count

from django_comments_xtd.api.views import CommentCreate
from rest_framework.response import Response
from django_comments.signals import comment_was_posted
from django_comments_xtd import views as comments_views
from django_comments_xtd import django_comments
from django_comments import get_form
from django_comments_xtd.models import XtdComment

import razorpay
from razorpay.errors import SignatureVerificationError

from django.conf import settings
from .models import (Blog, Video, Like, VideoCategory,
                     BlogLikeIntermediate, Course, Section,
                     PaymentCustomer, PaymentDetail)
from .utils import send_email, get_object_or_none
from .forms import VideoUploadForm

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
        liked = True if self.request.user.is_authenticated and \
                        blog.likes.filter(user=self.request.user,
                                          liked=True).exists() else False
        context.update(blog=blog,
                       recommended_blogs=recommended_blogs,
                       like_counter=blog.liked_count,
                       liked=liked)
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

class AjaxCommentDetailView(View):
    '''
        Returns sub comment detail after reply
        Always show the comment action menu as we show the latest one!
    '''

    def get(self, request, *args, **kwargs):
        context = {}
        result = {}
        print(args)
        print(kwargs)
        parent_comment_id = kwargs.get('pk', 0)
        object_id = kwargs.get('object_pk', 0)
        if parent_comment_id:
            template_name = 'comments/includes/sub_comment_detail.html'
            context.update(comment=XtdComment.objects.filter(parent_id=parent_comment_id).latest('id'),
                           comment_id=parent_comment_id,
                           include_action_menu=True)
            #result.update(status='success',
            #             new_comment=render_to_string(template_name, context))
        if object_id:
            template_name = 'comments/includes/comment_detail.html'
            context.update(item={'comment': XtdComment.objects.filter(object_pk=object_id).latest('id')},
                           #Change this in future for other than blog objects for the sub comments form
                           blog=Blog.objects.get(id=object_id))

        result.update(status='success',
                      new_comment=render_to_string(template_name, context, request=request))
        return JsonResponse(result)

class MyVideosView(FormView):
    template_name = 'core/my_videos.html'
    form_class = VideoUploadForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(page='videos',
                       my_videos=Video.objects.filter(user=self.request.user).order_by('-updated_date'))
        return context

    """def get(self, request):
        template_name = 'core/my_videos.html'
        return render(request, template_name, self.get_context_data())"""

    def form_invalid(self, form):
        print(form.errors, "ERRORS!!")
        return HttpResponseRedirect(reverse('my-videos'))

    def form_valid(self, form):
        print("VALID #####")
        youtube_video_base_url = 'https://www.youtube.com'
        form = form.save(commit=False)
        form.user = self.request.user
        if form.url.find('?v=') == -1:
            video_id = form.url.rsplit('/', 1)[1]
            url = "{}/watch?v={}".format(youtube_video_base_url,
                                         video_id)
            form.url = url
        form.save()
        print("SAVED ......")
        return HttpResponseRedirect(reverse('my-videos'))


class VideoListView(TemplateView):
    template_name = 'core/video_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video_list = Video.objects.order_by('-updated_date')
        most_viewed_video_list = Video.objects.order_by('?')[:4]
        data = self.request.GET
        if data.get('category', ''):
            context.update(filtered_category=data['category'])
            video_list = video_list.filter(category__name__istartswith=data['category']).order_by('-updated_date')
        context.update(video_list=video_list,
                       most_viewed_video_list=most_viewed_video_list,
                       categories=VideoCategory.objects.all().values_list('name', flat=True))
        print(context, "context")
        return context

class BlogManageLikeView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, **kwargs):
        result = {}
        blog = Blog.objects.get(id=kwargs['blog_id'])
        like_obj = blog.likes.filter(user=request.user)
        if like_obj.exists():
            like_obj = like_obj[0]
            new_action = False if like_obj.liked else True
            like_obj.liked = new_action
            like_obj.save()
            #result.update(liked=new_action)
        else:
            like_obj = Like(user=self.request.user,
                            liked=True)
            #result.update(liked=True)
            like_obj.save()
            BlogLikeIntermediate(blog=blog, like=like_obj).save()
        result.update(status='success',
                      like_counter=blog.liked_count,
                      liked=like_obj.liked)
        return JsonResponse(result)

class CourseDetailView(TemplateView):
    template_name = 'core/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_none(Course, id=kwargs['pk'])
        course_sections = []
        parent_sections = []
        if course:
            parent_sections = course.section.filter(parent__isnull=True)
            #sections = course.section.filter(parent__isnull=False).order_by('id', 'order')
            print(parent_sections, "parent_sections")
        for i in parent_sections:
            #parent = get_object_or_none(Section, id=i['parent'])
            #print(parent, i['parent'])
            course_sections.append({i: i.section_set.all()})
        print(course_sections, "course_sections")
        context.update(course=course,
                       course_sections=course_sections)
        return context


class PayOrderView(View):
    template_name = 'payment/pay_order.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        context = {}
        data = self.request.GET
        client = razorpay.Client(auth=('%s' % settings.RAZOR_PAY_KEY, '%s' % settings.RAZOR_PAY_SECRET))
        plans = client.plan.all()
        #plan_amount =
        plan = data.get('plan', 'Silver')

        payment_detail = PaymentDetail.objects.filter(payment_customer__user__email=self.request.user.email).order_by('-id')

        if payment_detail.exists():
            payment_detail = payment_detail[0]
            subscription_res = client.subscription.fetch(payment_detail.subscription_id)
            if 'status' in subscription_res:
                status = subscription_res['status']
                if status not in ['created', 'authenticated', 'active']:
                    payment_detail.status = False
                    payment_detail.save()
                    context.update(paid=False)

        for i in plans['items']:
            plan_name = i['item']['name']
            if plan_name == plan:
                plan_amount = i['item']['amount']
                order_data = {'amount': plan_amount,
                              'currency': 'INR',
                              'payment_capture': 1,
                              'notes': {'plan': i['id']}}
                order_id = client.order.create(data=order_data)['id']
                context.update(plan=plan,
                               plan_id=i['id'],
                               plan_amount=plan_amount,
                               order_id=order_id,
                               customer_name=self.request.user.get_full_name().title(),
                               #customer_email='ugk@gmail.com')
                               customer_email=self.request.user.email)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def post(self, request, **kwargs):
        result = {'status': 'success'}
        #print(request.POST, "post_Data")
        data = request.POST
        if (data and
            'order_id' in data and
            'payment_id' in data and
            'payment_signature' in data):
            client = razorpay.Client(auth=('%s' % settings.RAZOR_PAY_KEY, '%s' % settings.RAZOR_PAY_SECRET))

            try:
                signature_data = {'razorpay_order_id': data['order_id'],
                                  'razorpay_payment_id': data['payment_id'],
                                  'razorpay_signature': data['payment_signature']}
                signature_res = client.utility.verify_payment_signature(signature_data)
                #print(signature_res, "signature_res signature_res")
                payment_res = client.payment.fetch(data['payment_id'])
                #print(payment_res, "PAYMNENT RESP!")
                payment_customer = get_object_or_none(PaymentCustomer, user__id=self.request.user.id)

                if not payment_customer:
                    customer_data = {'name': self.request.user.get_full_name().title(),
                                     'email': self.request.user.email,
                                     'fail_existing': '0'}
                    res = client.customer.create(customer_data)
                    #print(res, "RESP!")
                    payment_customer = PaymentCustomer(user=self.request.user,
                                                       customer_id=res['id'])
                    payment_customer.save()

                subscription_data = {'plan_id': payment_res['notes']['plan'],
                                     'customer_id': res['id'],
                                     'total_count': 1}
                subscription_res = client.subscription.create(data=subscription_data)
                print(subscription_res, "RES!")
                payment_detail = PaymentDetail(payment_customer=payment_customer,
                                               plan_id=payment_res['notes']['plan'],
                                               order_id=data['order_id'],
                                               payment_id=data['payment_id'],
                                               payment_signature=data['payment_signature'],
                                               subscription_id=subscription_res['id'],
                                               status=True)
                payment_detail.save()

            except SignatureVerificationError:
                #logger.error("The payment signature is not verified!")
                print("SIGNATURE ERROR!")
                result.update(status='error')
        else:
            result.update(status='error')
        return JsonResponse(result)

class PaymentStatusView(TemplateView):
    template_name = 'payment/payment_status.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.GET)
        context.update(status=self.request.GET.get('status', 'error'))
        return context