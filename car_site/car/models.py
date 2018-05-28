# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Axisdata(models.Model):
    ticks = models.IntegerField()
    channel = models.IntegerField()
    axisno = models.IntegerField()
    pulse_width = models.IntegerField()
    time_stamp = models.IntegerField()
    sum = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'AxisData'


class Carphoto(models.Model):
    ticks = models.IntegerField()
    carno = models.CharField(db_column='CarNo', max_length=40)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=40)  # Field name made lowercase.
    pathname = models.CharField(db_column='PathName', max_length=500)  # Field name made lowercase.
    typename = models.CharField(db_column='TypeName', max_length=40)  # Field name made lowercase.
    phototype = models.CharField(db_column='PhotoType', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CarPhoto'


class Heartdata(models.Model):
    ticks = models.IntegerField()
    advalue1 = models.IntegerField(db_column='adValue1', blank=True, null=True)  # Field name made lowercase.
    advalue2 = models.IntegerField(db_column='adValue2', blank=True, null=True)  # Field name made lowercase.
    advalue3 = models.IntegerField(db_column='adValue3', blank=True, null=True)  # Field name made lowercase.
    advalue4 = models.IntegerField(db_column='adValue4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HeartData'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
