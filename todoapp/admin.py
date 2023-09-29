from django.contrib import admin

from .models import List, Item

class ItemInLine(admin.TabularInline):
	model = Item
	extra = 3

class ListAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {"fields": ["list_name", "created_date"]}),
	]
	inlines = [ItemInLine]
	list_display = ["list_name", "created_date"]
	# list_filter = ["created_date"]
	search_fields = ["list_name"]

admin.site.register(List, ListAdmin)