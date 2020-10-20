import datetime
import uuid

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.postgres.fields import JSONField


def band_upload_dir(self, filename):
    return 'CropDetectionApp/Regions/{0}/Analyzes/{1}/Bands/{2}'.format(
                        self.analyze.region.name, self.analyze.id, filename
    )


def analyze_upload_dir(self, filename):
    return 'CropDetectionApp/Regions/{0}/Analyzes/{1}/{2}'.format(
                        self.region.name, self.id, filename
    )


def regions_upload_dir(self, filename):
    return "CropDetectionApp/Regions/{0}/{1}".format(self.name, filename)


def shape_files_upload_dir(self, filename):
    return "CropDetectionApp/Regions/{0}/ShapeFiles/{1}".format(
                        self.region.name, filename
    )


class Region(models.Model):
    name = models.CharField(
                            max_length=300,
                            help_text="Set the region name.",
                            unique=True
    )

    last_modified_date = models.DateTimeField(auto_now=True)
    # dem=models.FileField(upload_to=regions_upload_dir,
    # help_text= "Select the digital elevation model(DEM) file(.tif).")
    # land_cover=models.FileField(upload_to=regions_upload_dir,
    # help_text= "Select the Land Cover file(.tif).")

    def published_recently(self):
        return self.last_modified_date >= (
                                timezone.now() - datetime.timedelta(days=7)
        )

    published_recently.admin_order_field = 'last_modified_date'
    published_recently.boolean = True
    published_recently.short_description = 'Published recently?'

    def __str__(self):
        return str(self.name)


class ShapeFile(models.Model):
    last_modified_date = models.DateTimeField(auto_now=True)
    shape_file = models.FileField(upload_to=shape_files_upload_dir,
                                  help_text="Select the shape file.",
                                  max_length=300)

    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Crop(models.Model):
    last_modified_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=300, help_text="Set the crop name.")
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.region.name)+": "+str(self.name)


class Calendar(models.Model):
    name = models.CharField(max_length=300, help_text="Set the calendar name.")
    crop = models.OneToOneField(Crop, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=1000, blank=True, null=True,
                               help_text="any more comment?")

    def __str__(self):
        return str(
            self.crop.region.name)+": "+str(self.crop.name)+": "+str(self.name)


class Phenology(models.Model):
    last_modified_date = models.DateTimeField(auto_now=True)
    name = models.CharField(
                            max_length=300,
                            help_text="maximum greenness date for example",
    )

    start = models.DateField(help_text="Set the start date.")
    end = models.DateField(help_text="Set the end date.")
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Analyze(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    date = models.DateField()
    result = models.FileField(upload_to=analyze_upload_dir,
                              help_text="Select the result file(.tif).",
                              blank=True,
                              null=True,
                              max_length=300)

    result_image_1 = models.FileField(upload_to=analyze_upload_dir,
                              help_text="",
                              blank=True,
                              null=True,
                              max_length=300)

    result_image_2 = models.FileField(upload_to=analyze_upload_dir,
                              help_text="",
                              blank=True,
                              null=True,
                              max_length=300)

    input_path = models.FileField(
                        upload_to=analyze_upload_dir,
                        help_text="Select input path file directory(.txt).",
                        max_length=300,)

    color_map = JSONField(null=True, )

    def __str__(self):
        return str(self.result)

    def get_result_path(self,):
        return str(settings.MEDIA_URL + str(self.result))

    def get_inputpath_path(self, ):
        return str(settings.MEDIA_ROOT + '/' + str(self.input_path))

    def get_ndvi_path(self, ):
        return str(settings.MEDIA_ROOT + '/' +
                   str(self.band_set.filter(name='2')[0]))

    def get_red_path(self, ):
        return str(settings.MEDIA_ROOT + '/' +
                   str(self.band_set.filter(name='1')[0]))

    def get_green_path(self, ):
        return str(settings.MEDIA_ROOT + '/' +
                   str(self.band_set.filter(name='3')[0]))

    def get_nir_path(self, ):
        return str(settings.MEDIA_ROOT + '/' +
                   str(self.band_set.filter(name='4')[0]))

    def region_name(self, ):
        return str(self.region.name)


class Band(models.Model):
    choices = (("1", "band red"),
               ("2", "ndvi"),
               ("3", "band green"),
               ("4", "near infrared"))

    name = models.CharField(max_length=300,
                            help_text="Select band.",
                            choices=choices)

    band = models.FileField(upload_to=band_upload_dir,
                            help_text="Select band file(.tif).",
                            max_length=300)

    analyze = models.ForeignKey(Analyze, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.band)        
