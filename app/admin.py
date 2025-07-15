# admin.py
from django.contrib import admin
from .models import *

@admin.register(AutoFeederData)
class AutoFeederData(admin.ModelAdmin):
    list_display = ('id','auto_start_time', 'auto_end_time', 'auto_feed_rate', 'auto_sprinkle_rate','Timestamp')
    search_fields = ('auto_start_time', 'auto_end_time')



@admin.register(ManualFeederData)
class ManualFeederData(admin.ModelAdmin):
    list_display = ('id','manual_start_time', 'manual_end_time', 'manual_feed_rate', 'manual_sprinkle_rate','Timestamp')
    search_fields = ('manual_start_time', 'manual_end_time')


@admin.register(Alert_message_auto)
class Alert_message_auto(admin.ModelAdmin):
    list_display = ('alert','Timestamp')


@admin.register(Alert_message_manual)
class Alert_message_manual(admin.ModelAdmin):
    list_display = ('alert','Timestamp')