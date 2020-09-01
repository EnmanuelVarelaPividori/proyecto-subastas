from django.contrib import admin
from .models import Auction, Comments, User, Bid, Category, Watchlist
# Register your models here.

admin.site.register(Comments)
admin.site.register(Auction)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Watchlist)