'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  LayoutDashboard,
  Sparkles,
  Bot,
  FolderOpen,
  Share2,
  BarChart3,
  Settings,
  ChevronLeft,
  ChevronRight,
  Video,
  Zap,
  Shield,
  Rocket,
} from 'lucide-react'

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', href: '/' },
  { icon: Sparkles, label: 'Create Video', href: '/create' },
  { icon: Video, label: 'Studio', href: '/studio' },
  { icon: Bot, label: 'AI Agents', href: '/agents' },
  { icon: FolderOpen, label: 'Gallery', href: '/gallery' },
  { icon: Zap, label: 'Templates', href: '/templates' },
  { icon: Share2, label: 'Social Hub', href: '/social' },
  { icon: BarChart3, label: 'Analytics', href: '/analytics' },
  { icon: Shield, label: 'Commission', href: '/commissioning' },
  { icon: Rocket, label: 'Landing', href: '/landing' },
  { icon: Settings, label: 'Settings', href: '/settings' },
]

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const pathname = usePathname()

  return (
    <motion.aside
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className={`
        relative flex flex-col h-screen
        bg-gradient-to-b from-gray-900/95 to-gray-950/95
        backdrop-blur-xl
        border-r border-white/5
        transition-all duration-300 ease-out
        ${isCollapsed ? 'w-20' : 'w-72'}
      `}
    >
      {/* Logo */}
      <div className="p-6 flex items-center gap-4">
        <motion.div
          whileHover={{ scale: 1.05, rotate: 5 }}
          className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary via-secondary to-accent flex items-center justify-center shadow-glow-primary"
        >
          <Video className="w-6 h-6 text-white" />
        </motion.div>
        <AnimatePresence>
          {!isCollapsed && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.2 }}
            >
              <h1 className="font-display font-bold text-xl gradient-text">Taj Chat</h1>
              <p className="text-xs text-muted-foreground">AI Video Studio</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Quick Create Button */}
      <div className="px-4 mb-4">
        <Link href="/create">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => {
              // #region agent log
              fetch('http://127.0.0.1:7242/ingest/462ff03d-fc78-405b-9cfc-573374f4fd13', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  sessionId: 'debug-session',
                  runId: 'run1',
                  hypothesisId: 'B',
                  location: 'components/layout/Sidebar.tsx:quick-create',
                  message: 'Quick create button clicked',
                  data: { href: '/create' },
                  timestamp: Date.now(),
                }),
              }).catch(() => {})
              // #endregion agent log
            }}
            className={`
              w-full flex items-center justify-center gap-2
              bg-gradient-to-r from-primary to-secondary
              text-white font-semibold
              rounded-xl transition-all duration-200
              shadow-lg shadow-primary/25 hover:shadow-primary/40
              ${isCollapsed ? 'p-3' : 'py-3 px-4'}
            `}
          >
            <Zap className="w-5 h-5" />
            {!isCollapsed && <span>Create Video</span>}
          </motion.button>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-2 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link key={item.href} href={item.href}>
              <motion.div
                onClick={() => {
                  // #region agent log
                  fetch('http://127.0.0.1:7242/ingest/462ff03d-fc78-405b-9cfc-573374f4fd13', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                      sessionId: 'debug-session',
                      runId: 'run1',
                      hypothesisId: 'A',
                      location: 'components/layout/Sidebar.tsx:nav-item',
                      message: 'Nav item click',
                      data: { href: item.href, label: item.label },
                      timestamp: Date.now(),
                    }),
                  }).catch(() => {})
                  // #endregion agent log
                }}
                whileHover={{ x: 4 }}
                className={`
                  relative flex items-center gap-3 px-4 py-3 rounded-xl
                  transition-all duration-200 cursor-pointer
                  ${isActive
                    ? 'bg-gradient-to-r from-primary/20 to-secondary/10 text-white'
                    : 'text-muted-foreground hover:text-white hover:bg-white/5'
                  }
                `}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeNav"
                    className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-gradient-to-b from-primary to-secondary rounded-r-full"
                  />
                )}
                <item.icon className={`w-5 h-5 ${isActive ? 'text-primary' : ''}`} />
                <AnimatePresence>
                  {!isCollapsed && (
                    <motion.span
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="text-sm font-medium"
                    >
                      {item.label}
                    </motion.span>
                  )}
                </AnimatePresence>
              </motion.div>
            </Link>
          )
        })}
      </nav>

      {/* System Status */}
      <AnimatePresence>
        {!isCollapsed && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="p-4 mx-4 mb-4 rounded-2xl bg-gradient-to-br from-success/10 via-primary/5 to-accent/10 border border-white/5"
          >
            <div className="flex items-center gap-2 mb-2">
              <span className="status-orb active" />
              <span className="text-sm font-medium text-success">System Online</span>
            </div>
            <p className="text-xs text-muted-foreground">
              10 Agents Ready • All APIs Connected
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Collapse Toggle */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute -right-3 top-1/2 transform -translate-y-1/2
          w-6 h-6 rounded-full bg-gray-800 border border-white/10
          flex items-center justify-center
          hover:bg-gray-700 hover:border-primary/50 transition-all duration-200
          shadow-lg"
      >
        {isCollapsed ? (
          <ChevronRight className="w-3 h-3" />
        ) : (
          <ChevronLeft className="w-3 h-3" />
        )}
      </motion.button>
    </motion.aside>
  )
}
