from django.contrib import admin
from .models import User, auction_listing, bid, comment, watchlist

class auctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'starting_bid', 'category')

# Register your models here.
admin.site.register(User)
admin.site.register(auction_listing, auctionAdmin)
admin.site.register(bid)
admin.site.register(comment)
admin.site.register(watchlist)
