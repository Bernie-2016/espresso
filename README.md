## Espresso: It's way better than drip.™

Espresso is a Django drip email module, based on Zapier's  [django-drip](https://github.com/zapier/django-drip). It's meant to be more flexible and modular. Whereas django-drip is tightly coupled to Django's [`contrib.auth.User`](https://docs.djangoproject.com/es/1.9/topics/auth/default/), Espresso can be configured to setup rules for any Django model.

Espresso also adds support for HTML and plaintext templates to wrap your messages, making use of Django's excellent [template system](https://docs.djangoproject.com/es/1.9/topics/templates/).

### Installation
1. Clone this repo
2. `mkvirtualenv espresso`
3. `pip install -r requirements.txt`
4. Add `'espresso'` to your `INSTALLED_APPS`.
5. Go make some coffee, let's get to work.

### Sample Configuration

1. For demonstration purposes, let's assume you have a few models setup:

        from django.db import models
dr
        class Person(models.Model):
            email = models.EmailField()
            first_name = models.CharField()
            last_name = models.CharField()

        class Event(models.Model):
            name = models.CharField()
            start_date = models.DateTimeField()
            # etc

        class EventAttendee(model.Model):
            attendee = models.ForeignKey(Person, related_name='rsvps')
            event = models.ForeignKey(Event, related_name='attendees')

2. Now, let's setup a drip class for the model you want to query. Add a `drip_emails.py` to your app:

        import espresso
        from .models import EventAttendee # this is your model

        class EventAttendeeDripType(espresso.DripBase):
        
            @classmethod
            def get_email_context(cls, item):
                return {
                    'attendee': item.person,
                    'email_address': item.person.email,
                    'event': item.event,
                    'rsvp': item
                }

            class Meta:
                model = EventAttendee
                verbose_name = 'Event Attendees'

  Set the `model` to the class you want to query, then author a `get_email_context` method. `item` will be an instance of your chosen model. `email_address` will dictate who to send the email to, and any other variables defined will be available for use in the email templates.
  
3. Lastly, you have the option of adding HTML wrappers to use throughout your different drips. To set those up, add a stock HTML template in any templates directory — call this `'stock.html'`:
  
      `<p><img src="/my-logo.png" /></p>`
      `{{ email_content }}`
  
  Then, add a dictionary to your `settings.py`:
  
      DRIP_TEMPLATES = (
        (None, 'None'),
        ('stock.html', 'Stock Email Template'),
      )

4. Alright, let's go to the admin (`./manage.py runserver` + `open http://localhost:8000/admin/`). Create a new Drip Campaign. Most of the fields are fairly self-explanatory, but a few I want to talk about:
    1. **Target** — this is where you choose the drip class you made above. Note that Django will look in all of your `INSTALLED_APPS` for a `drip_emails.py` file, for Drip types to load up. (You'll see it's `verbose_name` in the dropdown)
    2. **Targeting Rules** — this is a query builder, built around Django's [field lookups](https://docs.djangoproject.com/en/1.9/ref/models/querysets/#id4) for querysets.
    3. **Body HTML Template** — here, you can put the `{{ variables }}` to work, as you specified them in the `get_email_context` method you created. [Django filters and template tags](https://docs.djangoproject.com/en/1.9/ref/templates/builtins/) also work here. If you do choose a template, your `Body` / message will be swapped into it, using the `{{ email_content }}` variable.
    
5. Set a campaign live by marking it Enabled, and then add a cron job to run `python manage.py send_drip`. You're off to the races!

### Other helpful points & hints:
1. Espresso (like `drip-emails`) will prune and de-dupe items, per campaign. This also means each item in your queryset will also receive (at maximum) 1 drip email. You can overwrite the `prune` method to change this behavior.
2. If you are using external data sources that you need to map to Django models, I highly recommend looking at [Django's `inspectdb`](https://docs.djangoproject.com/en/1.9/howto/legacy-databases/).
3. [Django filters and template tags](https://docs.djangoproject.com/en/1.9/ref/templates/builtins/) will be your friend here. You can also write [custom template tags or filters](https://docs.djangoproject.com/es/1.9/howto/custom-template-tags/) to do your bididng and empower your authors.
4. Espresso will automatically generate a plaintext version to send along too. You're welcome.

### TODO
1. Finish "Send Me a Sample" so authors can preview their work.
2. For future use, clean up repo to be a Django module rather than a project.

### History

Espresso was built by [Jon Culver](http://jonculver.com) for [Bernie 2016](http://berniesanders.com). There were many cases of data being imported from other systems (people, events, RSVPs, etc.) where, we wanted automated followup, but the data would not necessarily be tied to Django Users. A few coffees later, Espresso was born. It aims to be flexible, configurable, and Django-friendly.