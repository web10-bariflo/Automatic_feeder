from django.db import models
from django.utils import timezone


class MyUser(models.Model):
    Device_id=models.CharField(max_length=100)                                    
    User_name=models.CharField(max_length=30)
    password = models.CharField(max_length=50, blank=True, null=True)
    Mob=models.BigIntegerField(unique=True)
    Email =models.EmailField()
 

    
    def __str__(self):
        return str(self.User_name)




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


class Alert_message(models.Model):

    alert = models.CharField(max_length=255) 
    Timestamp = models.DateTimeField(auto_now_add=True)



