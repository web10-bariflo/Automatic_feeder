from django.db import models
from django.utils import timezone


class AutoFeederData(models.Model):
    
    auto_start_time = models.CharField(max_length=255)  
    auto_end_time = models.CharField(max_length=255)  
    auto_feed_rate = models.CharField(max_length=255) 
    auto_sprinkle_rate = models.CharField(max_length=255)  



class ManualFeederData(models.Model):
    
    manual_start_time = models.CharField(max_length=255)  
    manual_end_time = models.CharField(max_length=255)  
    manual_feed_rate = models.CharField(max_length=255) 
    manual_sprinkle_rate = models.CharField(max_length=255)  