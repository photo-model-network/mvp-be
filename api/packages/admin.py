from django.contrib import admin
from .models import (
    Package,
    PackageProvider,
    PackagePolicy,
    PackageOption,
    # PackageTag,
    PackagePicture,
)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    pass


@admin.register(PackageProvider)
class PackageProviderAdmin(admin.ModelAdmin):
    pass


@admin.register(PackagePolicy)
class PackagePolicyAdmin(admin.ModelAdmin):
    pass


@admin.register(PackageOption)
class PackageOptionAdmin(admin.ModelAdmin):
    pass


# @admin.register(PackageTag)
# class PackageTagAdmin(admin.ModelAdmin):
#     pass


@admin.register(PackagePicture)
class PackagePictureAdmin(admin.ModelAdmin):
    pass
