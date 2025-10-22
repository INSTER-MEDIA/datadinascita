import { useQuery } from '@tanstack/react-query'
import { contactsApi, eventsApi } from '@/lib/api'
import { format } from 'date-fns'
import { Cake, Calendar, Users, TrendingUp } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const { data: upcomingBirthdays, isLoading: birthdaysLoading } = useQuery({
    queryKey: ['upcomingBirthdays'],
    queryFn: () => contactsApi.upcomingBirthdays(30),
  })

  const { data: upcomingEvents, isLoading: eventsLoading } = useQuery({
    queryKey: ['upcomingEvents'],
    queryFn: () => eventsApi.upcomingEvents(30),
  })

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome back! Here's what's coming up.</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Upcoming (30 days)</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {upcomingBirthdays?.length || 0}
              </p>
            </div>
            <Cake className="h-12 w-12 text-primary-600" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Events (30 days)</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {upcomingEvents?.length || 0}
              </p>
            </div>
            <Calendar className="h-12 w-12 text-primary-600" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">This Week</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {upcomingBirthdays?.filter((c) => c.days_until_birthday !== null && c.days_until_birthday <= 7).length || 0}
              </p>
            </div>
            <TrendingUp className="h-12 w-12 text-primary-600" />
          </div>
        </div>
      </div>

      {/* Upcoming Birthdays */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900">Upcoming Birthdays</h2>
          <Link to="/contacts" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
            View all contacts →
          </Link>
        </div>

        {birthdaysLoading ? (
          <p className="text-gray-600">Loading...</p>
        ) : upcomingBirthdays && upcomingBirthdays.length > 0 ? (
          <div className="space-y-4">
            {upcomingBirthdays.slice(0, 5).map((contact) => (
              <div
                key={contact.id}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <div className="h-12 w-12 rounded-full bg-primary-100 flex items-center justify-center">
                    <Cake className="h-6 w-6 text-primary-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{contact.name}</p>
                    <p className="text-sm text-gray-600">
                      {contact.next_birthday && format(new Date(contact.next_birthday), 'MMMM d, yyyy')}
                      {contact.upcoming_age && ` • Turning ${contact.upcoming_age}`}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-primary-600">
                    {contact.days_until_birthday === 0 ? 'Today!' :
                     contact.days_until_birthday === 1 ? 'Tomorrow' :
                     `In ${contact.days_until_birthday} days`}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <Cake className="h-12 w-12 text-gray-400 mx-auto mb-3" />
            <p className="text-gray-600">No upcoming birthdays in the next 30 days</p>
            <Link to="/contacts" className="text-primary-600 hover:text-primary-700 text-sm font-medium mt-2 inline-block">
              Add your first contact
            </Link>
          </div>
        )}
      </div>

      {/* Upcoming Events */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900">Upcoming Events</h2>
          <Link to="/events" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
            View all events →
          </Link>
        </div>

        {eventsLoading ? (
          <p className="text-gray-600">Loading...</p>
        ) : upcomingEvents && upcomingEvents.length > 0 ? (
          <div className="space-y-4">
            {upcomingEvents.slice(0, 5).map((event) => (
              <div
                key={event.id}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <div className="h-12 w-12 rounded-full bg-primary-100 flex items-center justify-center">
                    <Calendar className="h-6 w-6 text-primary-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{event.name}</p>
                    <p className="text-sm text-gray-600">
                      {event.type.charAt(0).toUpperCase() + event.type.slice(1)} •{' '}
                      {event.next_occurrence && format(new Date(event.next_occurrence), 'MMMM d, yyyy')}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-primary-600">
                    {event.days_until_next === 0 ? 'Today!' :
                     event.days_until_next === 1 ? 'Tomorrow' :
                     `In ${event.days_until_next} days`}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-3" />
            <p className="text-gray-600">No upcoming events in the next 30 days</p>
            <Link to="/events" className="text-primary-600 hover:text-primary-700 text-sm font-medium mt-2 inline-block">
              Create your first event
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}
