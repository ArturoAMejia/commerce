from django.contrib import admin
from .models import * 
# Register your models here.

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(ListingBid)
admin.site.register(ListingComment)
admin.site.register(WatchList)