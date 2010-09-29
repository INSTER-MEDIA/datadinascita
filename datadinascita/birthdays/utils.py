__author__ = 'oleg@kossoy.com'

from datetime import datetime

from google.appengine.api import users

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from datadinascita.birthdays.models import Person

def get_auth_url(back):
    user = users.get_current_user()
    if user:
        auth_url = users.create_logout_url(back)
    else:
        auth_url = users.create_login_url(back)

    return auth_url

def check_auth(req):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url(req.META['PATH_INFO']))

def show_new_person(form, request):
    people = modify_people(Person.all().filter("owner =", users.get_current_user()))
    return render_to_response('add.html',
                              {'form': form, 'people': people, 'count': len(people),
                               'auth_url': get_auth_url(request.META['PATH_INFO'])})

def modify_people(people):
    pp = []
    for person in people:
        today = datetime.date(datetime.today())
        this_year_birthday = datetime.date(datetime(today.year, person.birthday.month, person.birthday.day))

        if this_year_birthday > today:
            bd_year = today.year
        else:
            bd_year = today.year + 1

        next_bd_date = datetime(bd_year, person.birthday.month, person.birthday.day)
        next_bd = datetime.date(next_bd_date) - today

        person.age = int(round((datetime.date(next_bd_date) - person.birthday).days / 365.25))
        person.next_bd = next_bd.days
        pp.append(person)

    return sorted(pp, key=lambda ps: ps.next_bd)




  