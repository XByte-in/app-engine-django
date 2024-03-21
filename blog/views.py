
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from datetime import date
from django.views.generic import DetailView
from django.views.generic import ListView,TemplateView
from django.views.generic.edit import FormView,CreateView
from django.views import View

from .models import Post
from .forms import NewPostForm, CommentForm

# all_posts=[
# {
#     "slug":"roam-in-land",
#     "image":"land.png",
#     "author":"qwerty",
#     "date":date(2024,1,3),
#     "title":"Land Roaming",
#     "excerpt":"There is nothing to lookout for in Land, but everything to look out for in those great Lands",
#     "content":"""
#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Consequuntur sint facere facilis nisi aperiam deleniti excepturi illo molestiae quam voluptate deserunt quae, ullam harum! Tenetur rem minima quo cum molestiae!
#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Consequuntur sint facere facilis nisi aperiam deleniti excepturi illo molestiae quam voluptate deserunt quae, ullam harum! Tenetur rem minima quo cum molestiae!
#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Consequuntur sint facere facilis nisi aperiam deleniti excepturi illo molestiae quam voluptate deserunt quae, ullam harum! Tenetur rem minima quo cum molestiae!
#     """
# }
# ]


 # Create your views here.

# all_posts=Post.objects.all()

# def get_date(post):
#     return post['date']
    
# def starting_page(request):
#     # sorted_posts = sorted(all_posts, key=get_date)
#     # latest_post = sorted_posts[-3:]
#     latest_post = all_posts.order_by("-dated")[:3]
#     return render(request, "blog/index.html", {"posts":latest_post})

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    context_object_name ="posts"
    ordering = ['-dated','id']
    def get_queryset(self):
        query_set = super().get_queryset()
        limit_data = query_set[:3]
        return limit_data

# def posts(request):
#     return render(request, "blog/all-posts.html", {"all_posts":all_posts})

class AllPostView(ListView):
    template_name="blog/all-posts.html"
    model = Post
    context_object_name = "all_posts"

# def post_detail(request, slug):
#     # the_post=all_posts[0]
#     # the_post = next(post for post in all_posts if post['slug'] == slug)
#     the_post = get_object_or_404(Post,slug=slug)
#     return render(request, "blog/post-detail.html",{"the_post":the_post})

# class PostDetailView(DetailView):
#     template_name="blog/post-detail.html"
#     model = Post
#     context_object_name = "the_post"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # this_post = self.get_object['slug']
#         context["form"] = CommentForm()
#         return context
    

class NewPostView(CreateView):
    model = Post
    form_class = NewPostForm
    template_name = "blog/newpost.html"
    success_url = "/newpost"


class PostDetailView(View):
    def get(self,request,slug):
        the_post=Post.objects.get(slug=slug)
        comments=the_post.comments.all().order_by("-id")
        form=CommentForm()
        post_ids=request.session.get("later_posts")
        if post_ids is None or len(post_ids)==0:
            marked = False
        else:
            marked = the_post.id in post_ids
        return render(request,"blog/post-detail.html",{"the_post":the_post,"form":form,"comments":comments,"marked":marked})
    
    def post(self,request,slug):
        form=CommentForm(request.POST)
        the_post=Post.objects.get(slug=slug)
        comments=the_post.comments.all().order_by("-id")
        post_ids=request.session.get("later_posts")
        if post_ids is None or len(post_ids)==0:
            marked = False
        else:
            marked = the_post.id in post_ids
        if form.is_valid():
            form_obj=form.save(commit=False)
            form_obj.post=the_post
            form_obj.save()
            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))
        return render(request,"blog/post-detail.html",{"the_post":the_post,"form":form,"comments":comments,"marked":marked})


class ReadLaterView(TemplateView):
    def get(self,request):
        post_ids=request.session.get("later_posts")
        if post_ids is None or len(post_ids)==0:
            no_post=True
            post_list=[]
        else:
            no_post=False
            post_list=Post.objects.filter(id__in=post_ids)
        return render(request,"blog/later.html",{"no_post":no_post,"post_list":post_list})
    
    def post(self,request):
        post_id=int(request.POST["post_id"])
        later_posts=request.session.get("later_posts")
        if later_posts is None:
            later_posts=[]
        if post_id not in later_posts:
            later_posts.append(post_id)
        else:
            later_posts.remove(post_id)
        request.session["later_posts"]=later_posts
        return HttpResponseRedirect("/read-later")
