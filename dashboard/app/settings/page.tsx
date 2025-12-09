'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Settings,
  User,
  Key,
  Bell,
  Palette,
  Globe,
  Shield,
  Database,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Save,
  ExternalLink,
  ChevronRight,
  Moon,
  Sun,
  Monitor,
  Zap,
  Lock,
  Eye,
  EyeOff,
  Copy,
  Check,
  AlertCircle,
  Info,
  Sparkles,
  Bot,
  Cpu,
  Cloud,
  Wifi,
  WifiOff,
  Camera,
  Upload,
  Mail,
  Phone,
  MapPin,
  Link,
  Twitter,
  Youtube,
  Instagram,
  Facebook,
  Server,
} from 'lucide-react'
import Sidebar from '@/components/layout/Sidebar'
import Header from '@/components/layout/Header'
import Button from '@/components/ui/Button'
import { api } from '@/lib/api'

const settingsSections = [
  { id: 'profile', label: 'Creator Profile', icon: User, description: 'Your personal information' },
  { id: 'api', label: 'API Keys', icon: Key, description: 'AI provider connections' },
  { id: 'notifications', label: 'Notifications', icon: Bell, description: 'Alert preferences' },
  { id: 'appearance', label: 'Appearance', icon: Palette, description: 'Theme and display' },
  { id: 'integrations', label: 'Integrations', icon: Globe, description: 'Social media connections' },
  { id: 'security', label: 'Security', icon: Shield, description: 'Privacy and security' },
]

// API Key card component
function APIKeyCard({ provider, connected, icon, gradient, onRefresh }: any) {
  const [showKey, setShowKey] = useState(false)
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <motion.div
      whileHover={{ y: -2 }}
      className={`relative overflow-hidden p-5 rounded-2xl border transition-all ${
        connected
          ? 'bg-emerald-500/5 border-emerald-500/20'
          : 'bg-white/5 border-white/10 hover:border-white/20'
      }`}
    >
      {/* Background gradient */}
      {connected && (
        <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-5`} />
      )}

      <div className="relative flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
            connected ? `bg-gradient-to-br ${gradient}` : 'bg-white/10'
          }`}>
            {icon ? (
              <span className="text-2xl">{icon}</span>
            ) : (
              <Key className={`w-6 h-6 ${connected ? 'text-white' : 'text-white/50'}`} />
            )}
          </div>
          <div>
            <p className="font-semibold capitalize">{provider.replace('_', ' ')}</p>
            <p className="text-xs text-white/50">
              {connected ? 'API key configured' : 'Not configured'}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {connected ? (
            <>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setShowKey(!showKey)}
                className="p-2 rounded-lg hover:bg-white/10 transition-colors"
              >
                {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={handleCopy}
                className="p-2 rounded-lg hover:bg-white/10 transition-colors"
              >
                {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              </motion.button>
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            </>
          ) : (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="px-4 py-2 bg-white/10 hover:bg-white/15 rounded-xl text-sm font-medium transition-colors"
            >
              Configure
            </motion.button>
          )}
        </div>
      </div>

      {/* Key preview */}
      <AnimatePresence>
        {showKey && connected && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="mt-4 pt-4 border-t border-white/10"
          >
            <code className="text-xs text-white/60 font-mono">
              sk-****************************{provider.slice(0, 4)}
            </code>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

// Social platform card
function SocialPlatformCard({ platform, connected, icon, gradient, followers }: any) {
  return (
    <motion.div
      whileHover={{ y: -2 }}
      className={`relative overflow-hidden p-5 rounded-2xl border transition-all ${
        connected
          ? 'bg-white/5 border-white/20'
          : 'bg-white/[0.02] border-white/10'
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center bg-gradient-to-br ${gradient}`}>
            <span className="text-2xl">{icon}</span>
          </div>
          <div>
            <p className="font-semibold capitalize">{platform}</p>
            {connected ? (
              <p className="text-xs text-emerald-400">{followers} followers</p>
            ) : (
              <p className="text-xs text-white/40">Not connected</p>
            )}
          </div>
        </div>

        {connected ? (
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-medium">
              Connected
            </span>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 rounded-lg hover:bg-white/10"
            >
              <Settings className="w-4 h-4 text-white/50" />
            </motion.button>
          </div>
        ) : (
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="px-5 py-2.5 bg-gradient-to-r from-violet-600 to-fuchsia-600 rounded-xl text-sm font-semibold shadow-lg shadow-violet-500/20"
          >
            Connect
          </motion.button>
        )}
      </div>
    </motion.div>
  )
}

// Toggle switch component
function ToggleSwitch({ enabled, onChange, label, description }: any) {
  return (
    <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/10">
      <div>
        <p className="font-medium">{label}</p>
        <p className="text-xs text-white/50">{description}</p>
      </div>
      <motion.button
        onClick={() => onChange(!enabled)}
        className={`relative w-12 h-6 rounded-full transition-colors ${
          enabled ? 'bg-gradient-to-r from-violet-600 to-fuchsia-600' : 'bg-white/20'
        }`}
      >
        <motion.div
          className="absolute top-1 w-4 h-4 bg-white rounded-full shadow-lg"
          animate={{ left: enabled ? 28 : 4 }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
        />
      </motion.button>
    </div>
  )
}

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState('profile')
  const [apiStatus, setApiStatus] = useState<Record<string, boolean>>({})
  const [socialStatus, setSocialStatus] = useState<Record<string, boolean>>({})
  const [isLoading, setIsLoading] = useState(true)
  const [theme, setTheme] = useState('dark')
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    marketing: false,
    updates: true,
  })

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const status = await api.getStatus()
        setApiStatus(status.ai_providers || {})
        setSocialStatus(status.social_media || {})
      } catch (error) {
        console.error('Failed to fetch status:', error)
      } finally {
        setIsLoading(false)
      }
    }
    fetchStatus()
  }, [])

  const refreshStatus = async () => {
    setIsLoading(true)
    try {
      const status = await api.getStatus()
      setApiStatus(status.ai_providers || {})
      setSocialStatus(status.social_media || {})
    } catch (error) {
      console.error('Failed to refresh status:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const connectedCount = Object.values(apiStatus).filter(Boolean).length

  return (
    <div className="flex min-h-screen bg-[#0a0a0f]">
      <Sidebar />

      <main className="flex-1 overflow-auto">
        <Header title="Settings" subtitle="Configure your Taj Chat experience" />

        <div className="p-6">
          <div className="flex gap-6">
            {/* Sidebar Navigation */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="w-72 flex-shrink-0"
            >
              <div className="sticky top-6 space-y-4">
                {/* Quick Status */}
                <div className="p-4 rounded-2xl bg-gradient-to-br from-violet-500/10 to-fuchsia-500/10 border border-violet-500/20">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-fuchsia-600 flex items-center justify-center">
                      <Zap className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <p className="font-semibold">Connected</p>
                      <p className="text-xs text-white/50">{connectedCount} services active</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    {[...Array(5)].map((_, i) => (
                      <div
                        key={i}
                        className={`flex-1 h-1.5 rounded-full ${
                          i < connectedCount ? 'bg-emerald-500' : 'bg-white/10'
                        }`}
                      />
                    ))}
                  </div>
                </div>

                {/* Navigation */}
                <div className="p-2 rounded-2xl bg-white/5 border border-white/10">
                  <nav className="space-y-1">
                    {settingsSections.map((section, i) => {
                      const Icon = section.icon
                      return (
                        <motion.button
                          key={section.id}
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: i * 0.05 }}
                          onClick={() => setActiveSection(section.id)}
                          className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-all ${
                            activeSection === section.id
                              ? 'bg-gradient-to-r from-violet-600/20 to-fuchsia-600/20 text-white border border-violet-500/30'
                              : 'text-white/60 hover:text-white hover:bg-white/5'
                          }`}
                        >
                          <Icon className={`w-5 h-5 ${activeSection === section.id ? 'text-violet-400' : ''}`} />
                          <div className="flex-1">
                            <span className="font-medium block">{section.label}</span>
                            <span className="text-xs text-white/40">{section.description}</span>
                          </div>
                          {activeSection === section.id && (
                            <ChevronRight className="w-4 h-4 text-violet-400" />
                          )}
                        </motion.button>
                      )
                    })}
                  </nav>
                </div>
              </div>
            </motion.div>

            {/* Content */}
            <div className="flex-1 space-y-6">
              <AnimatePresence mode="wait">
                {/* Profile Section */}
                {activeSection === 'profile' && (
                  <motion.div
                    key="profile"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="space-y-6"
                  >
                    {/* Profile Header */}
                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                      <div className="flex items-start gap-6">
                        <div className="relative">
                          <div className="w-24 h-24 rounded-2xl bg-gradient-to-br from-violet-500 to-fuchsia-600 flex items-center justify-center text-3xl font-bold">
                            TC
                          </div>
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            className="absolute -bottom-2 -right-2 w-8 h-8 rounded-full bg-violet-600 flex items-center justify-center shadow-lg"
                          >
                            <Camera className="w-4 h-4" />
                          </motion.button>
                        </div>
                        <div className="flex-1">
                          <h3 className="text-xl font-bold mb-1">Taj Creator</h3>
                          <p className="text-white/50 text-sm mb-4">Premium Creator Account</p>
                          <div className="flex gap-3">
                            <span className="px-3 py-1 rounded-full bg-violet-500/20 text-violet-400 text-xs font-medium">
                              Pro Plan
                            </span>
                            <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-medium">
                              Verified
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Profile Form */}
                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                      <h4 className="font-semibold mb-4">Personal Information</h4>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="text-sm text-white/60 mb-2 block">Display Name</label>
                          <input
                            type="text"
                            defaultValue="Taj Creator"
                            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm focus:outline-none focus:border-violet-500/50 transition-colors"
                          />
                        </div>
                        <div>
                          <label className="text-sm text-white/60 mb-2 block">Username</label>
                          <input
                            type="text"
                            defaultValue="@tajcreator"
                            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm focus:outline-none focus:border-violet-500/50 transition-colors"
                          />
                        </div>
                        <div>
                          <label className="text-sm text-white/60 mb-2 block">Email</label>
                          <input
                            type="email"
                            defaultValue="creator@tajchat.ai"
                            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm focus:outline-none focus:border-violet-500/50 transition-colors"
                          />
                        </div>
                        <div>
                          <label className="text-sm text-white/60 mb-2 block">Phone</label>
                          <input
                            type="tel"
                            defaultValue="+1 (555) 123-4567"
                            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm focus:outline-none focus:border-violet-500/50 transition-colors"
                          />
                        </div>
                        <div className="md:col-span-2">
                          <label className="text-sm text-white/60 mb-2 block">Bio</label>
                          <textarea
                            rows={3}
                            defaultValue="Creating viral content with AI. 🚀"
                            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm focus:outline-none focus:border-violet-500/50 transition-colors resize-none"
                          />
                        </div>
                      </div>
                      <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="mt-6 px-6 py-3 bg-gradient-to-r from-violet-600 to-fuchsia-600 rounded-xl font-semibold flex items-center gap-2 shadow-lg shadow-violet-500/20"
                      >
                        <Save className="w-4 h-4" />
                        Save Changes
                      </motion.button>
                    </div>
                  </motion.div>
                )}

                {/* API Keys Section */}
                {activeSection === 'api' && (
                  <motion.div
                    key="api"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="space-y-6"
                  >
                    {/* AI Providers */}
                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                      <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center gap-3">
                          <div className="p-2 rounded-xl bg-violet-500/20">
                            <Bot className="w-5 h-5 text-violet-400" />
                          </div>
                          <div>
                            <h4 className="font-semibold">AI Providers</h4>
                            <p className="text-xs text-white/50">Configure your AI model access</p>
                          </div>
                        </div>
                        <motion.button
                          whileHover={{ scale: 1.05, rotate: 180 }}
                          whileTap={{ scale: 0.95 }}
                          onClick={refreshStatus}
                          disabled={isLoading}
                          className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
                        >
                          <RefreshCw className={`w-5 h-5 ${isLoading ? 'animate-spin' : ''}`} />
                        </motion.button>
                      </div>

                      <div className="grid md:grid-cols-2 gap-4">
                        {[
                          { provider: 'openai', icon: '🤖', gradient: 'from-emerald-500 to-teal-600' },
                          { provider: 'anthropic', icon: '🧠', gradient: 'from-orange-500 to-red-600' },
                          { provider: 'together', icon: '⚡', gradient: 'from-blue-500 to-indigo-600' },
                          { provider: 'huggingface', icon: '🤗', gradient: 'from-yellow-500 to-orange-600' },
                          { provider: 'replicate', icon: '🔄', gradient: 'from-purple-500 to-pink-600' },
                          { provider: 'flux', icon: '🎨', gradient: 'from-cyan-500 to-blue-600' },
                        ].map((item) => (
                          <APIKeyCard
                            key={item.provider}
                            provider={item.provider}
                            connected={apiStatus[item.provider]}
                            icon={item.icon}
                            gradient={item.gradient}
                          />
                        ))}
                      </div>

                      <p className="text-xs text-white/40 mt-4 flex items-center gap-2">
                        <Info className="w-4 h-4" />
                        API keys are loaded from <code className="px-1.5 py-0.5 bg-white/10 rounded">C:/dev/infra/credentials/</code>
                      </p>
                    </div>

                    {/* Backend Status */}
                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                      <div className="flex items-center gap-3 mb-6">
                        <div className="p-2 rounded-xl bg-cyan-500/20">
                          <Server className="w-5 h-5 text-cyan-400" />
                        </div>
                        <div>
                          <h4 className="font-semibold">Backend Services</h4>
                          <p className="text-xs text-white/50">System infrastructure status</p>
                        </div>
                      </div>

                      <div className="space-y-3">
                        {[
                          { name: 'FastAPI Backend', url: 'http://localhost:8000', status: 'online', icon: Cpu },
                          { name: 'PostgreSQL (Neon)', url: 'Connected via DATABASE_URL', status: 'online', icon: Database },
                          { name: 'Redis Cache', url: 'localhost:6379', status: 'online', icon: Zap },
                        ].map((service) => (
                          <div key={service.name} className="flex items-center justify-between p-4 rounded-xl bg-white/5">
                            <div className="flex items-center gap-3">
                              <service.icon className="w-5 h-5 text-white/60" />
                              <div>
                                <p className="font-medium">{service.name}</p>
                                <p className="text-xs text-white/40">{service.url}</p>
                              </div>
                            </div>
                            <div className="flex items-center gap-3">
                              <span className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${
                                service.status === 'online'
                                  ? 'bg-emerald-500/20 text-emerald-400'
                                  : 'bg-red-500/20 text-red-400'
                              }`}>
                                <span className={`w-2 h-2 rounded-full ${
                                  service.status === 'online' ? 'bg-emerald-400' : 'bg-red-400'
                                } animate-pulse`} />
                                {service.status}
                              </span>
                              <motion.button
                                whileHover={{ scale: 1.1 }}
                                className="p-2 rounded-lg hover:bg-white/10"
                              >
                                <ExternalLink className="w-4 h-4 text-white/40" />
                              </motion.button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}

                {/* Appearance Section */}
                {activeSection === 'appearance' && (
                  <motion.div
                    key="appearance"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="space-y-6"
                  >
                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                      <h4 className="font-semibold mb-6">Theme</h4>
                      <div className="grid grid-cols-3 gap-4">
                        {[
                          { id: 'dark', icon: Moon, label: 'Dark', gradient: 'from-gray-700 to-gray-900' },
                          { id: 'light', icon: Sun, label: 'Light', gradient: 'from-gray-100 to-gray-300' },
                          { id: 'system', icon: Monitor, label: 'System', gradient: 'from-violet-500 to-fuchsia-500' },
                        ].map((t) => (
                          <motion.button
                            key={t.id}
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={() => setTheme(t.id)}
                            className={`p-6 rounded-2xl border text-center transition-all ${
                              theme === t.id
                                ? 'border-violet-500 bg-violet-500/10'
                                : 'border-white/10 bg-white/5 hover:bg-white/10'
                            }`}
                          >
                            <div className={`w-12 h-12 rounded-xl mx-auto mb-3 flex items-center justify-center bg-gradient-to-br ${t.gradient}`}>
                              <t.icon className={`w-6 h-6 ${t.id === 'light' ? 'text-gray-800' : 'text-white'}`} />
                            </div>
                            <span className="font-medium">{t.label}</span>
                          </motion.button>
                        ))}
                      </div>
                    </div>

                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                      <h4 className="font-semibold mb-6">Accent Color</h4>
                      <div className="flex gap-4">
                        {[
                          { color: '#8B5CF6', name: 'Violet' },
                          { color: '#EC4899', name: 'Pink' },
                          { color: '#06B6D4', name: 'Cyan' },
                          { color: '#10B981', name: 'Emerald' },
                          { color: '#F59E0B', name: 'Amber' },
                          { color: '#EF4444', name: 'Red' },
                        ].map((c) => (
                          <motion.button
                            key={c.color}
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            className={`w-12 h-12 rounded-xl transition-all ${
                              c.color === '#8B5CF6' ? 'ring-2 ring-white ring-offset-2 ring-offset-[#0a0a0f]' : ''
                            }`}
                            style={{ backgroundColor: c.color }}
                            title={c.name}
                          />
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}

                {/* Notifications Section */}
                {activeSection === 'notifications' && (
                  <motion.div
                    key="notifications"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="space-y-6"
                  >
                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                      <h4 className="font-semibold mb-6">Notification Preferences</h4>
                      <div className="space-y-3">
                        <ToggleSwitch
                          enabled={notifications.email}
                          onChange={(v: boolean) => setNotifications(n => ({ ...n, email: v }))}
                          label="Email Notifications"
                          description="Receive updates via email"
                        />
                        <ToggleSwitch
                          enabled={notifications.push}
                          onChange={(v: boolean) => setNotifications(n => ({ ...n, push: v }))}
                          label="Push Notifications"
                          description="Browser push notifications"
                        />
                        <ToggleSwitch
                          enabled={notifications.updates}
                          onChange={(v: boolean) => setNotifications(n => ({ ...n, updates: v }))}
                          label="Product Updates"
                          description="New features and improvements"
                        />
                        <ToggleSwitch
                          enabled={notifications.marketing}
                          onChange={(v: boolean) => setNotifications(n => ({ ...n, marketing: v }))}
                          label="Marketing"
                          description="Promotional content and offers"
                        />
                      </div>
                    </div>
                  </motion.div>
                )}

                {/* Integrations Section */}
                {activeSection === 'integrations' && (
                  <motion.div
                    key="integrations"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="space-y-6"
                  >
                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                      <div className="flex items-center gap-3 mb-6">
                        <div className="p-2 rounded-xl bg-fuchsia-500/20">
                          <Globe className="w-5 h-5 text-fuchsia-400" />
                        </div>
                        <div>
                          <h4 className="font-semibold">Social Media</h4>
                          <p className="text-xs text-white/50">Connect your social accounts</p>
                        </div>
                      </div>

                      <div className="grid md:grid-cols-2 gap-4">
                        {[
                          { platform: 'TikTok', icon: '🎵', gradient: 'from-[#00F2EA] to-[#FF0050]', connected: true, followers: '125K' },
                          { platform: 'Instagram', icon: '📸', gradient: 'from-[#F58529] to-[#8134AF]', connected: true, followers: '89K' },
                          { platform: 'YouTube', icon: '▶️', gradient: 'from-[#FF0000] to-[#CC0000]', connected: true, followers: '45K' },
                          { platform: 'Twitter/X', icon: '𝕏', gradient: 'from-[#1DA1F2] to-[#0D8BD9]', connected: false, followers: '0' },
                          { platform: 'Facebook', icon: '👤', gradient: 'from-[#1877F2] to-[#0D65D9]', connected: false, followers: '0' },
                          { platform: 'LinkedIn', icon: '💼', gradient: 'from-[#0A66C2] to-[#004182]', connected: false, followers: '0' },
                        ].map((item) => (
                          <SocialPlatformCard key={item.platform} {...item} />
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}

                {/* Security Section */}
                {activeSection === 'security' && (
                  <motion.div
                    key="security"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="space-y-6"
                  >
                    <div className="p-6 rounded-2xl bg-white/5 border border-white/10">
                      <h4 className="font-semibold mb-6">Security Settings</h4>
                      <div className="space-y-4">
                        <div className="flex items-center justify-between p-4 rounded-xl bg-white/5">
                          <div className="flex items-center gap-3">
                            <Lock className="w-5 h-5 text-white/60" />
                            <div>
                              <p className="font-medium">Two-Factor Authentication</p>
                              <p className="text-xs text-white/40">Add an extra layer of security</p>
                            </div>
                          </div>
                          <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-medium">
                            Enabled
                          </span>
                        </div>
                        <div className="flex items-center justify-between p-4 rounded-xl bg-white/5">
                          <div className="flex items-center gap-3">
                            <Key className="w-5 h-5 text-white/60" />
                            <div>
                              <p className="font-medium">Password</p>
                              <p className="text-xs text-white/40">Last changed 30 days ago</p>
                            </div>
                          </div>
                          <motion.button
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            className="px-4 py-2 bg-white/10 hover:bg-white/15 rounded-xl text-sm font-medium transition-colors"
                          >
                            Change
                          </motion.button>
                        </div>
                        <div className="flex items-center justify-between p-4 rounded-xl bg-white/5">
                          <div className="flex items-center gap-3">
                            <Shield className="w-5 h-5 text-white/60" />
                            <div>
                              <p className="font-medium">Active Sessions</p>
                              <p className="text-xs text-white/40">2 devices currently logged in</p>
                            </div>
                          </div>
                          <motion.button
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            className="px-4 py-2 bg-white/10 hover:bg-white/15 rounded-xl text-sm font-medium transition-colors"
                          >
                            Manage
                          </motion.button>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
