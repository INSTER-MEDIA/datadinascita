import { useQuery } from '@tanstack/react-query'
import { authApi } from '@/lib/api'
import { User, Mail, Calendar } from 'lucide-react'
import { format } from 'date-fns'

export default function Profile() {
  const { data: user, isLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: authApi.getProfile,
  })

  if (isLoading) {
    return <div className="text-gray-600">Loading...</div>
  }

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
        <p className="text-gray-600 mt-2">Manage your account settings</p>
      </div>

      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Account Information</h2>

        <div className="space-y-4">
          <div className="flex items-start space-x-3">
            <Mail className="h-5 w-5 text-gray-400 mt-0.5" />
            <div>
              <p className="text-sm text-gray-600">Email</p>
              <p className="font-medium text-gray-900">{user?.email}</p>
            </div>
          </div>

          <div className="flex items-start space-x-3">
            <User className="h-5 w-5 text-gray-400 mt-0.5" />
            <div>
              <p className="text-sm text-gray-600">Username</p>
              <p className="font-medium text-gray-900">{user?.username}</p>
            </div>
          </div>

          {user?.first_name && (
            <div className="flex items-start space-x-3">
              <User className="h-5 w-5 text-gray-400 mt-0.5" />
              <div>
                <p className="text-sm text-gray-600">Name</p>
                <p className="font-medium text-gray-900">
                  {user.first_name} {user.last_name}
                </p>
              </div>
            </div>
          )}

          <div className="flex items-start space-x-3">
            <Calendar className="h-5 w-5 text-gray-400 mt-0.5" />
            <div>
              <p className="text-sm text-gray-600">Member since</p>
              <p className="font-medium text-gray-900">
                {user?.date_joined && format(new Date(user.date_joined), 'MMMM d, yyyy')}
              </p>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t">
          <button className="btn btn-primary">Edit Profile</button>
        </div>
      </div>
    </div>
  )
}
