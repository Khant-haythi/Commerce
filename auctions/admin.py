from django.contrib import admin
from .models import User,Category,AuctionListing,Bid,Comment,Watchlist
# Register your models here.

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'starting_bid', 'created_by','created_date','active','category')
admin.site.register(AuctionListing, AuctionListingAdmin)

class BidAdmin(admin.ModelAdmin):
    list_display = ( 'listing','bid_amount','created_at')
admin.site.register(Bid, BidAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'comment','created_at')
admin.site.register(Comment, CommentAdmin)

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')
admin.site.register(Watchlist, WatchlistAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
admin.site.register(Category, CategoryAdmin)

