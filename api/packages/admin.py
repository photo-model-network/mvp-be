from django.contrib import admin
from .models import (
    Package,
    PackageProvider,
    PackagePolicy,
    PackageOption,
    PackagePicture,
    PackageTag,
    PackageTaggedItem,
)


class PackageOptionInline(admin.TabularInline):
    model = PackageOption
    extra = 0


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    inlines = [PackageOptionInline]

    list_display = ["id", "provider", "title", "created_at"]


@admin.register(PackageProvider)
class PackageProviderAdmin(admin.ModelAdmin):
    pass


@admin.register(PackagePolicy)
class PackagePolicyAdmin(admin.ModelAdmin):
    pass


@admin.register(PackageOption)
class PackageOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(PackagePicture)
class PackagePictureAdmin(admin.ModelAdmin):
    pass


@admin.register(PackageTag)
class PackageTagAdmin(admin.ModelAdmin):
    pass


@admin.register(PackageTaggedItem)
class PackageTaggedItemAdmin(admin.ModelAdmin):
    pass


from taggit.models import Tag

admin.site.unregister(Tag)
