'use client'

import { motion } from 'framer-motion'
import {
  Bell,
  Search,
  User,
  Settings,
  Moon,
  Sun,
  Wifi,
  WifiOff,
} from 'lucide-react'
import { useState, useEffect } from 'react'

interface HeaderProps {
  title?: string
  subtitle?: string
}

export default function Header({ title = 'Dashboard', subtitle }: HeaderProps) {
  const [isOnline, setIsOnline] = useState(true)
  const [notifications, setNotifications] = useState(3)

  useEffect(() => {
    // Check API health
    const checkHealth = async () => {
      try {
        const res = await fetch('http://localhost:8000/health')
        setIsOnline(res.ok)
      } catch {
        setIsOnline(false)
      }
    }

    checkHealth()
    const interval = setInterval(checkHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <header className="sticky top-0 z-40 w-full">
      <div className="glass-card border-0 border-b border-white/5 rounded-none">
        <div className="flex items-center justify-between h-16 px-6">
          {/* Left - Title */}
          <div className="flex items-center gap-4">
            <div>
              <motion.h1
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-xl font-display font-bold"
              >
                {title}
              </motion.h1>
              {subtitle && (
                <p className="text-sm text-muted-foreground">{subtitle}</p>
              )}
            </div>
          </div>

          {/* Center - Search */}
          <div className="flex-1 max-w-xl mx-8">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
              <input
                type="text"
                placeholder="Search videos, agents, workflows..."
                className="w-full bg-white/5 border border-white/10 rounded-xl py-2.5 pl-11 pr-4
                  text-sm placeholder:text-muted focus:outline-none focus:border-primary/50
                  focus:ring-2 focus:ring-primary/20 transition-all duration-200"
              />
              <kbd className="absolute right-4 top-1/2 -translate-y-1/2 px-2 py-0.5
                bg-white/5 border border-white/10 rounded text-xs text-muted">
                ⌘K
              </kbd>
            </div>
          </div>

          {/* Right - Actions */}
          <div className="flex items-center gap-3">
            {/* Connection Status */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className={`
                flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium
                ${isOnline
                  ? 'bg-success/10 text-success'
                  : 'bg-error/10 text-error'
                }
              `}
            >
              {isOnline ? (
                <>
                  <Wifi className="w-3 h-3" />
                  <span>Connected</span>
                </>
              ) : (
                <>
                  <WifiOff className="w-3 h-3" />
                  <span>Offline</span>
                </>
              )}
            </motion.div>

            {/* Notifications */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="relative p-2 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
            >
              <Bell className="w-5 h-5" />
              {notifications > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-secondary text-white
                  text-xs font-bold rounded-full flex items-center justify-center">
                  {notifications}
                </span>
              )}
            </motion.button>

            {/* Settings */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
            >
              <Settings className="w-5 h-5" />
            </motion.button>

            {/* Profile */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center gap-3 p-1.5 pr-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary
                flex items-center justify-center">
                <User className="w-4 h-4 text-white" />
              </div>
              <span className="text-sm font-medium">Creator</span>
            </motion.button>
          </div>
        </div>
      </div>
    </header>
  )
}
