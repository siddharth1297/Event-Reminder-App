from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=False, unique=True)
    gender_choices = [('M', 'male'),
                      ('F', 'Female')]
    gender = models.CharField(choices=gender_choices, max_length=1, null=False)

    def get_user_name(self):
        a = User.objects.all()
        for i in a:
            if i == self.username:
                return i.username
        return 'usename not found'

    def __str__(self):
        return self.get_user_name()


class ToDo(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    events = models.CharField(max_length=100)
    event_time = models.DateTimeField(null=False)
    sms_time = models.DateTimeField(null=False)
    is_completed = models.BooleanField(default=False)

    def get_user_name(self):
        a = User.objects.all()
        for i in a:
            if i == self.username:
                return i.username
        return 'usename not found'

    def __str__(self):
        return self.get_user_name() + str(self.events)
