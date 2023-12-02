from django.urls import path
from . import views
from .views import close_auction

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.createListing, name="create_listing"),
    path('view_listing/<int:listing_id>/', views.viewListing, name='view_listing'),
    path('add_to_watchlist/<int:listing_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:listing_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('addComment/<int:listing_id>/', views.addComment, name="addComment"),
    path('place_bid/<int:listing_id>/', views.place_bid, name='place_bid'),    
    path('close_auction/<int:listing_id>/', views.close_auction, name='close_auction'),
]
