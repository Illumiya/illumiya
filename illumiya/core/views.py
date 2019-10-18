from django.views.generic.base import TemplateView
from django.core.paginator import Paginator

from .models import Blog

class HomeView(TemplateView):
    template_name = 'index.html'

class BlogListView(TemplateView):
    template_name = 'core/blog_list.html'

    def get_context_data(self, **kwargs):
        DEFAULT_PAGE_SIZE = 20
        context = super().get_context_data(**kwargs)
        blog_list = Blog.objects.all().order_by('-id')
        paginator = Paginator(blog_list, DEFAULT_PAGE_SIZE)
        page = self.request.GET.get('page', 1)
        print(blog_list, "blog_list")
        context.update(blogs=paginator.get_page(page))
        return context

class BlogDetailView(TemplateView):
    template_name = 'core/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = Blog.objects.get(id=kwargs['pk'])
        recommended_blogs = Blog.objects.all().exclude(id=blog.id).order_by('?')[:10]
        context.update(blog=blog,
                       recommended_blogs=recommended_blogs)
        return context
