from django.urls import path
from .user import create_user, get_users, update_user, remove_user
from .auth import login_view
from .blog import get_blogs, get_curr_blog, create_blog, update_blog, remove_blog, create_blog_detail, get_blog_detail
from .category import get_categories, create_category, update_category, remove_category
from .tag import get_tags, create_tag, update_tag, remove_tag
from .blog_tag import create_blog_tag, get_blog_tag, get_blog_by_tag, get_tag_by_blog

urlpatterns = [
    path("login/", login_view),
    path("blog/", create_blog),
    path("blog-update/<str:id>/", update_blog),
    path("blog/<str:id>/", get_curr_blog),
    path("blog-delete/<str:id>/", remove_blog),
    path("blogs/", get_blogs),
    path("users/", get_users),
    path("user/", create_user),
    path("user/<str:id>/", remove_user),
    path("user-update/<str:id>/", update_user),
    path("categories/", get_categories),
    path("category/", create_category),
    path("category/<str:id>/", update_category),
    path("category-delete/<str:id>/", remove_category),
    path("tags/", get_tags),
    path("tag/", create_tag),
    path("tag/<str:id>/", update_tag),
    path("tag-delete/<str:id>/", remove_tag),
    path("blog-tag/", create_blog_tag),
    path("blog-tags/", get_blog_tag),
    path("blog-tag-by-tag/<str:id>/", get_blog_by_tag),
    path("blog-tag-by-blog/<str:id>/", get_tag_by_blog),
    path("blog-detail/<str:id>/", create_blog_detail),
    path("blog-details/<str:id>/", get_blog_detail),
]
