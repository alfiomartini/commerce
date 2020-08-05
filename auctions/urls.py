from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.list_detail, name='listing'),
    path("whatchlist/list", views.whatchlist, name='whatchlist'),
    path("whatchlist/add/<int:listing_id>", views.whatchlist_add, name='whatch_add'),
    path("whatchlist/del/<int:listing_id>", views.whatchlist_del, name='whatch_del'),
]
