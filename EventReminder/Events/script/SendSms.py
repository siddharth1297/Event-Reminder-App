from twilio.rest import Client
"""put account_sid auth_token, Twillio number at from_"""

def SendSms(user, event):
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    message_body = "Hii " + str(user.username) + "\nyou have " + event.events + ' at ' + str(event.event_time)
    try:
        message = client.messages.create(
            body=message_body,
            from_=",
            to='+91'+str(user.phone)
        )

        print(message.sid)
    except:
        return
