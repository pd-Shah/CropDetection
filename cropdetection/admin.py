from django.contrib import admin
from . import models


class PhenologyInline(admin.TabularInline):
    model = models.Phenology
    extra = 1


class ShapeFileInline(admin.StackedInline):
    model = models.ShapeFile
    extra = 1


class CalendarInline(admin.TabularInline):
    model = models.Calendar
    extra = 1


class CropInline(admin.TabularInline):
    model = models.Crop
    extra = 1


class BandInline(admin.TabularInline):
    model = models.Band
    extra = 1


class AnalyzeInline(admin.TabularInline):
    inlines = [BandInline, ]
    model = models.Analyze
    extra = 1


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ("Region Information",{'fields': ['name', ]}),
    # ]
    inlines = [CropInline, ShapeFileInline]
    list_filter = ['name', "last_modified_date"]
    list_display = ('name', 'last_modified_date', 'published_recently')


@admin.register(models.Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("region", 'name', 'last_modified_date')
    list_filter = ("region", 'name', 'last_modified_date')


@admin.register(models.Analyze)
class AnalyzeAdmin(admin.ModelAdmin):
    inlines = [BandInline, ]
    list_filter = ('region', 'date')
    list_display = ('region', 'date')


@admin.register(models.Calendar)
class CalendarAdmin(admin.ModelAdmin):
    inlines = [PhenologyInline]
    list_filter = ('name', 'last_modified_date')
    list_display = ('name', 'crop', 'last_modified_date')
