from django.db import models
from django.contrib.auth import get_user_model as user_model
User = user_model()
from django.db.models.signals import post_save
from django.dispatch import receiver 
from apps.supervisor.models import Department
from apps.manager.models import ManagerProfile

# Create your models here.
class ReporteeProfile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.IntegerField(blank=True, null= True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to = 'profilepics/', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.first_name 


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  
        if instance.is_reportee:  
            ReporteeProfile.objects.create(user=instance) 
            
        else:
            pass
    


