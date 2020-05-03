from django.urls import path

from .link_views import link_collection, link_element, linkStats, checkLinkPassword, ReportLink
from .user_views import UserSignup, UserLogin, GetUser, ChangePassword, DeleteAccount

urlpatterns = [
    # link routes
    path('links/', link_collection.as_view(), name="link_collection"),
    path('links/<str:url_id>/', link_element.as_view(), name="link_element"),
    path('links/<str:url_id>/stats/', linkStats, name="stats"),
    path('links/<str:url_id>/protected/', checkLinkPassword),
    path('report/', ReportLink),

    # user routes
    path('signup/', UserSignup, name="signup"),
    path('login/', UserLogin, name="login"),
    path('user/', GetUser, name="user"),
    path('change-password/', ChangePassword),
    path('delete-account/', DeleteAccount)
]