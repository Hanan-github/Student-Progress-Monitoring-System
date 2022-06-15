from django.db import models

# #create your models here
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'message from ' + self.name + ' - ' + self.email
    