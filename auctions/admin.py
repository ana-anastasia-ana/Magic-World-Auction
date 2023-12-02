from django.contrib import admin
from .models import User, Category, Listing, Watchlist, Comment, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Category)

class WatchlistInline(admin.TabularInline):
    model = Watchlist.listings.through
    extra = 0

class BidInline(admin.TabularInline):
    model = Bid
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'current_bid', 'is_active', 'creator', 'created_at', 'winner')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'creator__username', 'winner__username')
    ordering = ('-created_at',)
    actions = ['close_auctions']

    def close_auctions(self, request, queryset):
        # Close selected auctions and update the is_active field
        queryset.update(is_active=False)

    close_auctions.short_description = "Close selected auctions"

admin.site.register(Listing, ListingAdmin)

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'listings_count']

    def listings_count(self, obj):
        return obj.listings.count()

    listings_count.short_description = 'Listings Count'

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['listing', 'get_bidder_username', 'amount', 'created_at']

    def get_bidder_username(self, obj):
        return obj.bidder.username

    get_bidder_username.short_description = 'Bidder'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['listing', 'user', 'message', 'created_at']
