from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Store, User, Customer

@receiver(post_save, sender=User)#user modelinde instance oluşturulduğunda ve kaydedildiğinden hemen sonra çalış
def create_store(sender, instance, created, **kwargs):
    if created:
        print(instance.is_store)
        if instance.is_store:
            Store.objects.create(user=instance)
        elif instance.is_customer:
            Customer.objects.create(user=instance)
        
    