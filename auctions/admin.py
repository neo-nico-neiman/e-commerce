from django.contrib import admin
from .models import User, WatchList, Listing, Bids, Comments
# Register your models here.

admin.site.register(User)
admin.site.register(WatchList)
admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(Comments)