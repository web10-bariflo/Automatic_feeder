from django.db import models
from django.utils import timezone


class AutoFeederData(models.Model):
    
    auto_start_time = models.CharField(max_length=255)  
    auto_end_time = models.CharField(max_length=255)  
    auto_feed_rate = models.CharField(max_length=255) 
    auto_sprinkle_rate = models.CharField(max_length=255)  
    Timestamp = models.DateTimeField(auto_now_add=True)



class ManualFeederData(models.Model):
    
    manual_start_time = models.CharField(max_length=255)  
    manual_end_time = models.CharField(max_length=255)  
    manual_feed_rate = models.CharField(max_length=255) 
    manual_sprinkle_rate = models.CharField(max_length=255)  
    Timestamp = models.DateTimeField(auto_now_add=True)


class Alert_message_auto(models.Model):

    alert = models.CharField(max_length=255) 
    Timestamp = models.DateTimeField(auto_now_add=True)


class Alert_message_manual(models.Model):
    
    alert = models.CharField(max_length=255) 
    Timestamp = models.DateTimeField(auto_now_add=True)
