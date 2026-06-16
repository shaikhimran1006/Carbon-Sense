import React from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Leaf, Home, Settings, MessageSquare, TrendingUp, LogOut } from 'lucide-react'

interface LayoutProps {
  children: React.ReactNode
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/simulator', icon: TrendingUp, label: 'Simulator' },
    { path: '/assistant', icon: MessageSquare, label: 'Assistant' },
    { path: '/profile', icon: Settings, label: 'Profile' },
  ]

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="flex">
        <aside className="w-64 bg-white dark:bg-gray-800 shadow-lg h-screen sticky top-0 hidden md:block">
          <div className="p-6">
            <div className="flex items-center gap-3 mb-8">
              <div className="w-10 h-10 bg-green-100 dark:bg-green-900 rounded-xl flex items-center justify-center">
                <Leaf className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <span className="text-xl font-bold text-gray-900 dark:text-white">CarbonSense</span>
            </div>

            <nav className="space-y-2">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400'
                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    <Icon size={20} />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                )
              })}
            </nav>
          </div>

          <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-gray-200 dark:border-gray-700">
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-900 dark:text-white">{user?.name}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">{user?.email}</p>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-3 w-full px-4 py-3 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors"
            >
              <LogOut size={20} />
              <span className="font-medium">Logout</span>
            </button>
          </div>
        </aside>

        <main className="flex-1 p-6">
          <div className="md:hidden mb-6 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Leaf className="w-6 h-6 text-green-600" />
              <span className="font-bold text-gray-900 dark:text-white">CarbonSense</span>
            </div>
            <button onClick={handleLogout} className="text-gray-600 dark:text-gray-400">
              <LogOut size={20} />
            </button>
          </div>
          {children}

          <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 px-4 py-2">
            <div className="flex justify-around">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex flex-col items-center p-2 ${
                      isActive ? 'text-green-600 dark:text-green-400' : 'text-gray-600 dark:text-gray-400'
                    }`}
                  >
                    <Icon size={20} />
                    <span className="text-xs mt-1">{item.label}</span>
                  </Link>
                )
              })}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
