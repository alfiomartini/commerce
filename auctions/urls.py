from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.list_detail, name='listing'),
    path('listing/new', views.create_listing, name='create_listing'),
    path("whatchlist/list", views.whatchlist, name='whatchlist'),
    path("whatchlist/add/<int:listing_id>",
         views.whatchlist_add, name='whatch_add'),
    path("whatchlist/del/<int:listing_id>",
         views.whatchlist_del, name='whatch_del'),
    path('comment/add/<int:listing_id>', views.add_comment, name='add_comment'),
    path('bid/place/<int:listing_id>', views.place_bid, name='place_bid'),
    path('bid/close/<int:listing_id>', views.close_auction, name='close_auction'),
    path('category', views.categories, name='categories'),
    path('category/<int:category_id>',
         views.category_listings, name='listings_in_cat'),
    path('readme', views.readme, name='readme')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# this will help to access your media folder.
