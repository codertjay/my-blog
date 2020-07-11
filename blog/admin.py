from django.contrib import admin
from.models import Post,Action
# Register your models here.


class ActionAdmin(admin.TabularInline):
    model = Action

class PostAdminModel(admin.ModelAdmin):
    inlines = [ActionAdmin]


admin.site.register(Post,PostAdminModel)