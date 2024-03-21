from django.urls import path
from . import views

urlpatterns = [
    # path("", views.starting_page, name='starting-page'),
    path("",views.StartingPageView.as_view(), name='starting-page'),
    # path("posts", views.posts, name='posts-page'),
    path("posts",views.AllPostView.as_view(), name='posts-page'),
    path("newpost",views.NewPostView.as_view(), name='new-post'),
    # path("posts/<slug:slug>", views.post_detail, name='post-detail-page')
    path("posts/<slug:slug>", views.PostDetailView.as_view(), name='post-detail-page'),
    path("read-later",views.ReadLaterView.as_view(),name="read-later")
]
