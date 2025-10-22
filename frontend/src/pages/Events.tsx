import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { eventsApi } from '@/lib/api'
import { Plus, Search } from 'lucide-react'
import { format } from 'date-fns'

export default function Events() {
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)

  const { data, isLoading } = useQuery({
    queryKey: ['events', page, search],
    queryFn: () => eventsApi.list({ page, search }),
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Events</h1>
          <p className="text-gray-600 mt-2">Track anniversaries, holidays, and special occasions</p>
        </div>
        <button className="btn btn-primary flex items-center">
          <Plus className="h-4 w-4 mr-2" />
          Add Event
        </button>
      </div>

      {/* Search */}
      <div className="card">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search events..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input pl-10"
          />
        </div>
      </div>

      {/* Events List */}
      <div className="card">
        {isLoading ? (
          <p className="text-gray-600">Loading...</p>
        ) : data && data.results.length > 0 ? (
          <div className="space-y-4">
            {data.results.map((event) => (
              <div
                key={event.id}
                className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">{event.name}</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {event.type.charAt(0).toUpperCase() + event.type.slice(1)} •{' '}
                      {format(new Date(event.date), 'MMMM d, yyyy')}
                      {event.recurs_annually && ' • Recurring'}
                    </p>
                    {event.notes && (
                      <p className="text-sm text-gray-500 mt-2">{event.notes}</p>
                    )}
                  </div>
                  <div className="text-right">
                    {event.days_until_next !== null && (
                      <p className="text-sm font-medium text-primary-600">
                        {event.days_until_next === 0 ? 'Today!' :
                         event.days_until_next === 1 ? 'Tomorrow' :
                         `In ${event.days_until_next} days`}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-600">No events found</p>
            <button className="btn btn-primary mt-4 flex items-center mx-auto">
              <Plus className="h-4 w-4 mr-2" />
              Create your first event
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
