import logging
import csv

from google.appengine.ext import blobstore

from django.http import  HttpResponse

from datadinascita.birthdays.utils import *
from datadinascita.birthdays.forms import AddForm

def index(request):
    return render_to_response('index.html', {'auth_url': get_auth_url(request.META['PATH_INFO'])})

def fof(request, query):
	"""404 pages"""
	return render_to_response('404.html', {'query': query})

def search(request):
    return render_to_response('search.html', {})

def list(request):
    check_auth(request)
    people = modify_people(Person.all().filter("owner =", users.get_current_user()))
    return render_to_response('list.html', {'people': people, 'count': len(people), 'auth_url': get_auth_url(request.META['PATH_INFO'])})

def export(request):
    check_auth(request)
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
    check_auth(request)
    try:
        upload_url = blobstore.create_upload_url('/upload_csv/')
    except:
        upload_url = '.'
    return render_to_response('import.html', {'upload_url': upload_url})

def import_failed(request):
    check_auth(request)
    return render_to_response('import_failed.html', {})

def erase(request):
    check_auth(request)
    people = Person.all().filter("owner =", users.get_current_user())
    for person in people:
        person.delete()

    return HttpResponseRedirect('/people')

def add(request):
    check_auth(request)
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
    check_auth(request)
    return render_to_response('index.html', {'query': id})

