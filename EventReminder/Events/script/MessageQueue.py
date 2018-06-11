'''importing django modules outside django app
https://stackoverflow.com/questions/2180415/using-django-database-layer-outside-of-django
'''
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EventReminder.settings")
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth.models import User
from Events.models import UserProfile, ToDo
from django.utils.timezone import now
from datetime import datetime
import SendSms


def get_user(event_object):
    user_obj = User.objects.get(username=event_object.username)
    user_profile_obj = UserProfile.objects.get(username=user_obj)
    return user_profile_obj

def check_time(todo_object):
    if todo_object.sms_time.date() == now().date():
        if todo_object.sms_time.hour == datetime.now().hour and todo_object.sms_time.minute == datetime.now().minute:
            current_user = get_user(todo_object)
            print('sending message')
            # send_message
            SendSms.SendSms(current_user, todo_object)
            print('sms sent')
            # update is_completed value
            ToDo.objects.filter(events=todo_object.events).update(is_completed=True)

def get_todo_data():
    while True:
        todo_all_object = ToDo.objects.filter(is_completed=False).order_by('sms_time')
        if len(todo_all_object) > 0:
            check_time(todo_all_object[0])

if __name__ == '__main__':
    get_todo_data()