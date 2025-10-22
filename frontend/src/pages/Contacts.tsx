import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { contactsApi } from '@/lib/api'
import toast from 'react-hot-toast'
import { Plus, Search, Download, Upload, Trash2 } from 'lucide-react'
import { format } from 'date-fns'

export default function Contacts() {
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['contacts', page, search],
    queryFn: () => contactsApi.list({ page, search }),
  })

  const deleteMutation = useMutation({
    mutationFn: contactsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['contacts'] })
      toast.success('Contact deleted successfully')
    },
    onError: () => {
      toast.error('Failed to delete contact')
    },
  })

  const handleExport = async () => {
    try {
      const blob = await contactsApi.exportCsv()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `contacts-${format(new Date(), 'yyyy-MM-dd')}.csv`
      link.click()
      toast.success('Contacts exported successfully')
    } catch (error) {
      toast.error('Failed to export contacts')
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Contacts</h1>
          <p className="text-gray-600 mt-2">Manage your birthday contacts</p>
        </div>
        <div className="flex space-x-3">
          <button onClick={handleExport} className="btn btn-secondary flex items-center">
            <Download className="h-4 w-4 mr-2" />
            Export
          </button>
          <button className="btn btn-primary flex items-center">
            <Plus className="h-4 w-4 mr-2" />
            Add Contact
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="card">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search contacts..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input pl-10"
          />
        </div>
      </div>

      {/* Contacts List */}
      <div className="card">
        {isLoading ? (
          <p className="text-gray-600">Loading...</p>
        ) : data && data.results.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Name</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Birthday</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Age</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Days Until</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody>
                {data.results.map((contact) => (
                  <tr key={contact.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4">{contact.name}</td>
                    <td className="py-3 px-4">
                      {contact.birthday ? format(new Date(contact.birthday), 'MMM d, yyyy') : '-'}
                    </td>
                    <td className="py-3 px-4">{contact.upcoming_age || '-'}</td>
                    <td className="py-3 px-4">
                      {contact.days_until_birthday !== null ? (
                        <span className={contact.days_until_birthday <= 7 ? 'text-primary-600 font-medium' : ''}>
                          {contact.days_until_birthday === 0 ? 'Today!' :
                           contact.days_until_birthday === 1 ? 'Tomorrow' :
                           `${contact.days_until_birthday} days`}
                        </span>
                      ) : '-'}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => {
                          if (confirm('Are you sure you want to delete this contact?')) {
                            deleteMutation.mutate(contact.id)
                          }
                        }}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Pagination */}
            {data.count > 20 && (
              <div className="flex justify-between items-center mt-6 pt-6 border-t">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={!data.previous}
                  className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                <span className="text-gray-600">
                  Page {page} of {Math.ceil(data.count / 20)}
                </span>
                <button
                  onClick={() => setPage((p) => p + 1)}
                  disabled={!data.next}
                  className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-600">No contacts found</p>
            <button className="btn btn-primary mt-4 flex items-center mx-auto">
              <Plus className="h-4 w-4 mr-2" />
              Add your first contact
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
