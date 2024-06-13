from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlist",views.create_list,name="create_list"),
    path('listing/<pk>/', views.listing_page, name='listing_page'),
    path('listing/<pk>/place_bid/', views.place_bid, name='place_bid'),
    path('listing/<pk>/add_comment/', views.add_comment, name='add_comment'),
    path('listing/<pk>/add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('listing/<pk>/remove_from_watchlist/', views.remove_from_watchlist, name='remove_from_watchlist'),
     path('listing/<pk>/close_auction/', views.close_auction, name='close_auction'),
]
