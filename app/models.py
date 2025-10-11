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

from django.db import models

class FeederSetting(models.Model):
    percentage = models.FloatField(default=0)  
    point_value = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Calculate point value from percentage
        if self.percentage > 100:
            self.percentage = 100
        elif self.percentage < 0:
            self.percentage = 0
            
        # Point Value = (Percentage / 100) × 3750
        self.point_value = int((self.percentage / 100) * 3750)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.percentage}% = {self.point_value} points"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

