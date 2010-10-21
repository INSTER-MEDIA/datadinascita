import csv

from google.appengine.ext import blobstore

from django.http import  HttpResponse, HttpResponseRedirect

from datadinascita.birthdays.utils import *
from datadinascita.birthdays.forms import AddForm
from datadinascita.birthdays.models import Contact, Event

def index(request):
    return render_to_response('index.html', {'auth_url': get_auth_url(request.META['PATH_INFO'])})

def fof(request, query):
    """404 pages"""
    return render_to_response('404.html', {'query': query})

def search(request):
    return render_to_response('search.html', {})

def people(request):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url(request.META['PATH_INFO']))

    people = modify_people(Person.all().filter("owner =", users.get_current_user()))
    return render_to_response('people.html', {'people': people, 'count': len(people),
                                              'auth_url': get_auth_url(request.META['PATH_INFO'])})

def export(request):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url(request.META['PATH_INFO']))

    people = modify_people(Person.all().filter("owner =", users.get_current_user()))
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=birthdays.csv'

    # Create the CSV writer using the HttpResponse as the "file"
    writer = csv.writer(response)
    for person in people:
        writer.writerow(["%s/%s/%s" % (person.birthday.month, person.birthday.day, person.birthday.year),
                         person.name.encode('utf-8')])
    return response


def csv_upload(request):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url(request.META['PATH_INFO']))

    try:
        upload_url = blobstore.create_upload_url('/upload_csv/')
    except:
        upload_url = '.'
    return render_to_response('import.html', {'upload_url': upload_url})

def import_failed(request):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url(request.META['PATH_INFO']))

    return render_to_response('import_failed.html', {})

def erase(request):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url(request.META['PATH_INFO']))

    people = Person.all().filter("owner =", users.get_current_user())
    for person in people:
        person.delete()

    return HttpResponseRedirect('/people')

def add(request):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url(request.META['PATH_INFO']))

    if request.method == 'POST':
        form = AddForm(request.POST)

        if form.is_valid():
            try:
                name = form.clean_data['name']
                birthday = form.clean_birthday()
                p = Person(name=name)
                p.owner = users.get_current_user()
                p.birthday = datetime.date(datetime.strptime(birthday, "%m/%d/%Y"))
            except:
                return show_new_person(form)

            a = p.put()
            logging.info(a)
        else:
            return show_new_person(form)

        return HttpResponseRedirect('/people')
    else:
        form = AddForm()

    return show_new_person(form, request)

def edit(request, id):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url(request.META['PATH_INFO']))

    return render_to_response('index.html', {'query': id})

def list(request):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url(request.META['PATH_INFO']))

    people = Contact.all()

    return render_to_response('list.html', {'people': people})

def new(request):
    if not users.get_current_user():
        return HttpResponseRedirect(users.create_login_url(request.META['PATH_INFO']))

    params = {}

    if request.method == 'POST':

        event_date = datetime.date(
                datetime.strptime(
                        request.POST.get('date', ''),
                        "%Y-%m-%d"
                        )
                )

        e = Event.all().filter(
                "type =", request.POST.get('type', '')).filter(
                "date =", event_date
                ).fetch(1)

        if not e:
            e = Event(
                    type=request.POST.get('type', ''),
                    name=request.POST.get('type', ''),
                    date=event_date
                    )
            e.put()
        else:
            e = e[0]

        contact = Contact(
                name=request.POST.get('fullName', ''),
                owner=users.get_current_user(),
                event=e
                )
        contact.put()

        return HttpResponseRedirect('/')

    return render_to_response('new.html', {'params': params})