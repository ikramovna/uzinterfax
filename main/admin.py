from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from main.models import ZoneModel, NewsModel, TagModel, CategoryModel


# --------------------------
# Define Resource classes
# --------------------------
class ZoneResource(resources.ModelResource):
    class Meta:
        model = ZoneModel


class NewsResource(resources.ModelResource):
    class Meta:
        model = NewsModel


class CategoryResource(resources.ModelResource):
    class Meta:
        model = CategoryModel


class TagResource(resources.ModelResource):
    class Meta:
        model = TagModel


# -------------------------
# Define Admin classes
# -------------------------
class ZoneAdmin(ImportExportModelAdmin):
    resource_class = ZoneResource


class NewsAdmin(ImportExportModelAdmin):
    resource_class = NewsResource


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource


class TagAdmin(ImportExportModelAdmin):
    resource_class = TagResource


# ----------------------------------
# Register models with custom admins
# ----------------------------------
admin.site.register(ZoneModel, ZoneAdmin)
admin.site.register(NewsModel, NewsAdmin)
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(TagModel, TagAdmin)
