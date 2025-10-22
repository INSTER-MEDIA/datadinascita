import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { authApi } from '@/lib/api'
import toast from 'react-hot-toast'
import { Cake, Calendar, User, LogOut, Menu } from 'lucide-react'
import { useState } from 'react'

export default function Layout() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleLogout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        await authApi.logout(refreshToken)
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      logout()
      navigate('/login')
      toast.success('Logged out successfully')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <Cake className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">DataDiNascita</span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              <Link
                to="/"
                className="text-gray-700 hover:text-primary-600 transition-colors"
              >
                Dashboard
              </Link>
              <Link
                to="/contacts"
                className="text-gray-700 hover:text-primary-600 transition-colors"
              >
                Contacts
              </Link>
              <Link
                to="/events"
                className="text-gray-700 hover:text-primary-600 transition-colors"
              >
                Events
              </Link>
            </nav>

            {/* User Menu */}
            <div className="hidden md:flex items-center space-x-4">
              <Link to="/profile" className="flex items-center space-x-2 text-gray-700 hover:text-primary-600">
                <User className="h-5 w-5" />
                <span>{user?.email}</span>
              </Link>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 text-gray-700 hover:text-red-600 transition-colors"
              >
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </div>

            {/* Mobile menu button */}
            <button
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <Menu className="h-6 w-6" />
            </button>
          </div>

          {/* Mobile menu */}
          {mobileMenuOpen && (
            <div className="md:hidden py-4 space-y-2">
              <Link
                to="/"
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded"
                onClick={() => setMobileMenuOpen(false)}
              >
                Dashboard
              </Link>
              <Link
                to="/contacts"
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded"
                onClick={() => setMobileMenuOpen(false)}
              >
                Contacts
              </Link>
              <Link
                to="/events"
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded"
                onClick={() => setMobileMenuOpen(false)}
              >
                Events
              </Link>
              <Link
                to="/profile"
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded"
                onClick={() => setMobileMenuOpen(false)}
              >
                Profile
              </Link>
              <button
                onClick={() => {
                  handleLogout()
                  setMobileMenuOpen(false)
                }}
                className="block w-full text-left px-4 py-2 text-red-600 hover:bg-gray-100 rounded"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-600 text-sm">
            © 2025 DataDiNascita - Never forget a birthday again!
          </p>
        </div>
      </footer>
    </div>
  )
}
