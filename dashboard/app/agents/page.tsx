'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Bot,
  RefreshCw,
  Filter,
  Search,
  Cpu,
  Zap,
  Activity,
  CheckCircle2,
  XCircle,
  Clock,
  Play,
  Pause,
  Settings,
  MoreHorizontal,
  TrendingUp,
  Sparkles,
  Brain,
  Wand2,
  Music,
  Image,
  Mic,
  Video,
  Film,
  Share2,
  Shield,
  BarChart3,
  Layers,
  Eye,
  ChevronRight,
  Terminal,
  Code,
  Database,
  Network,
  Workflow,
  CircuitBoard,
} from 'lucide-react'
import Sidebar from '@/components/layout/Sidebar'
import Header from '@/components/layout/Header'
import Button from '@/components/ui/Button'
import { api } from '@/lib/api'

// Agent type icons and colors
const agentConfig: Record<string, { icon: any; gradient: string; color: string; bgImage?: string }> = {
  content_analysis: {
    icon: Brain,
    gradient: 'from-violet-500 to-purple-600',
    color: '#8B5CF6',
    bgImage: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=200&fit=crop&q=80'
  },
  video_generation: {
    icon: Film,
    gradient: 'from-pink-500 to-rose-600',
    color: '#EC4899',
    bgImage: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=400&h=200&fit=crop&q=80'
  },
  music_generation: {
    icon: Music,
    gradient: 'from-cyan-500 to-blue-600',
    color: '#06B6D4',
    bgImage: 'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400&h=200&fit=crop&q=80'
  },
  image_generation: {
    icon: Image,
    gradient: 'from-emerald-500 to-teal-600',
    color: '#10B981',
    bgImage: 'https://images.unsplash.com/photo-1547826039-bfc35e0f1ea8?w=400&h=200&fit=crop&q=80'
  },
  voice_speech: {
    icon: Mic,
    gradient: 'from-amber-500 to-orange-600',
    color: '#F59E0B',
    bgImage: 'https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=400&h=200&fit=crop&q=80'
  },
  editing: {
    icon: Layers,
    gradient: 'from-indigo-500 to-violet-600',
    color: '#6366F1',
    bgImage: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=400&h=200&fit=crop&q=80'
  },
  optimization: {
    icon: Zap,
    gradient: 'from-yellow-500 to-amber-600',
    color: '#EAB308',
    bgImage: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=200&fit=crop&q=80'
  },
  analytics: {
    icon: BarChart3,
    gradient: 'from-blue-500 to-indigo-600',
    color: '#3B82F6',
    bgImage: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=200&fit=crop&q=80'
  },
  safety: {
    icon: Shield,
    gradient: 'from-red-500 to-rose-600',
    color: '#EF4444',
    bgImage: 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=400&h=200&fit=crop&q=80'
  },
  social_media: {
    icon: Share2,
    gradient: 'from-fuchsia-500 to-pink-600',
    color: '#D946EF',
    bgImage: 'https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=400&h=200&fit=crop&q=80'
  },
}

// Enhanced Agent Card Component
function EnhancedAgentCard({ type, name, status, capabilities, progress, lastRun, tasksCompleted, onRun, onStop }: any) {
  const config = agentConfig[type] || { icon: Bot, gradient: 'from-gray-500 to-gray-600', color: '#6B7280' }
  const Icon = config.icon

  const statusConfig = {
    idle: { label: 'Ready', color: 'text-emerald-400', bg: 'bg-emerald-500/20', icon: CheckCircle2 },
    running: { label: 'Running', color: 'text-blue-400', bg: 'bg-blue-500/20', icon: Activity },
    completed: { label: 'Completed', color: 'text-green-400', bg: 'bg-green-500/20', icon: CheckCircle2 },
    error: { label: 'Error', color: 'text-red-400', bg: 'bg-red-500/20', icon: XCircle },
  }

  const currentStatus = statusConfig[status as keyof typeof statusConfig] || statusConfig.idle
  const StatusIcon = currentStatus.icon

  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.01 }}
      className="relative group rounded-2xl overflow-hidden bg-gray-900/50 border border-white/10 hover:border-white/20 transition-all"
    >
      {/* Background image with gradient overlay */}
      <div className="absolute inset-0 opacity-20 group-hover:opacity-30 transition-opacity">
        {config.bgImage && (
          <img src={config.bgImage} alt="" className="w-full h-full object-cover" />
        )}
        <div className={`absolute inset-0 bg-gradient-to-br ${config.gradient} opacity-60`} />
      </div>

      {/* Content */}
      <div className="relative p-5">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <motion.div
              className={`w-12 h-12 rounded-xl bg-gradient-to-br ${config.gradient} flex items-center justify-center shadow-lg`}
              whileHover={{ scale: 1.1, rotate: 5 }}
            >
              <Icon className="w-6 h-6 text-white" />
            </motion.div>
            <div>
              <h3 className="font-semibold text-sm">{name}</h3>
              <span className="text-xs text-white/50">Agent #{type.split('_')[0]}</span>
            </div>
          </div>

          {/* Status badge */}
          <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full ${currentStatus.bg}`}>
            {status === 'running' ? (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              >
                <Activity className={`w-3 h-3 ${currentStatus.color}`} />
              </motion.div>
            ) : (
              <StatusIcon className={`w-3 h-3 ${currentStatus.color}`} />
            )}
            <span className={`text-xs font-medium ${currentStatus.color}`}>{currentStatus.label}</span>
          </div>
        </div>

        {/* Progress bar (when running) */}
        {status === 'running' && progress !== undefined && (
          <div className="mb-4">
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="text-white/60">Progress</span>
              <span className="text-white/80 font-mono">{progress}%</span>
            </div>
            <div className="h-2 bg-white/10 rounded-full overflow-hidden">
              <motion.div
                className={`h-full bg-gradient-to-r ${config.gradient}`}
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
          </div>
        )}

        {/* Capabilities */}
        <div className="mb-4">
          <p className="text-xs text-white/40 mb-2">Capabilities</p>
          <div className="flex flex-wrap gap-1.5">
            {capabilities.slice(0, 3).map((cap: string, i: number) => (
              <span
                key={i}
                className="px-2 py-0.5 text-[10px] rounded-full bg-white/10 text-white/70"
              >
                {cap}
              </span>
            ))}
            {capabilities.length > 3 && (
              <span className="px-2 py-0.5 text-[10px] rounded-full bg-white/5 text-white/40">
                +{capabilities.length - 3} more
              </span>
            )}
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="p-2.5 rounded-xl bg-white/5">
            <p className="text-[10px] text-white/40 mb-0.5">Tasks Completed</p>
            <p className="text-sm font-semibold">{tasksCompleted || 0}</p>
          </div>
          <div className="p-2.5 rounded-xl bg-white/5">
            <p className="text-[10px] text-white/40 mb-0.5">Last Active</p>
            <p className="text-sm font-semibold">{lastRun || 'Never'}</p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          {status === 'running' ? (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={onStop}
              className="flex-1 py-2.5 px-4 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-xl text-sm font-medium flex items-center justify-center gap-2 transition-colors"
            >
              <Pause className="w-4 h-4" />
              Stop
            </motion.button>
          ) : (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={onRun}
              className={`flex-1 py-2.5 px-4 bg-gradient-to-r ${config.gradient} rounded-xl text-sm font-medium flex items-center justify-center gap-2 shadow-lg`}
              style={{ boxShadow: `0 10px 30px ${config.color}30` }}
            >
              <Play className="w-4 h-4" />
              Run Agent
            </motion.button>
          )}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
          >
            <Settings className="w-4 h-4 text-white/60" />
          </motion.button>
        </div>
      </div>

      {/* Running indicator line */}
      {status === 'running' && (
        <motion.div
          className={`absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r ${config.gradient}`}
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 0.3 }}
        />
      )}
    </motion.div>
  )
}

// Stats Card Component
function StatsCard({ icon: Icon, label, value, change, color, delay }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      whileHover={{ y: -2, scale: 1.02 }}
      className="relative overflow-hidden rounded-2xl p-5 bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 group"
    >
      {/* Glow effect */}
      <div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-xl"
        style={{ background: `radial-gradient(circle at center, ${color}20, transparent 70%)` }}
      />

      <div className="relative">
        <div className="flex items-center justify-between mb-3">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center"
            style={{ backgroundColor: `${color}20` }}
          >
            <Icon className="w-5 h-5" style={{ color }} />
          </div>
          {change && (
            <span className={`text-xs font-medium px-2 py-1 rounded-full ${
              change.startsWith('+') ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'
            }`}>
              {change}
            </span>
          )}
        </div>
        <p className="text-3xl font-bold mb-1">{value}</p>
        <p className="text-sm text-white/50">{label}</p>
      </div>
    </motion.div>
  )
}

type AgentStatus = 'idle' | 'running' | 'completed' | 'error';

interface Agent {
  type: string;
  name: string;
  status: AgentStatus;
  capabilities: string[];
  tasksCompleted: number;
  lastRun: string;
  progress?: number;
}

const defaultAgents: Agent[] = [
  {
    type: 'content_analysis',
    name: 'Content Analysis Agent',
    status: 'idle',
    capabilities: ['Script generation', 'SEO optimization', 'Hashtag suggestions', 'Mood detection'],
    tasksCompleted: 1247,
    lastRun: '2m ago',
  },
  {
    type: 'video_generation',
    name: 'Video Generation Agent',
    status: 'running',
    progress: 67,
    capabilities: ['Text-to-video', 'Image animation', 'Multi-scene composition', 'Style transfer'],
    tasksCompleted: 892,
    lastRun: 'Now',
  },
  {
    type: 'music_generation',
    name: 'Music Generation Agent',
    status: 'idle',
    capabilities: ['Text-to-music', 'Beat detection', 'Mood matching', 'Duration control'],
    tasksCompleted: 634,
    lastRun: '5m ago',
  },
  {
    type: 'image_generation',
    name: 'Image Generation Agent',
    status: 'completed',
    capabilities: ['Text-to-image', 'Overlay creation', 'Thumbnail generation', 'Style consistency'],
    tasksCompleted: 2156,
    lastRun: '1m ago',
  },
  {
    type: 'voice_speech',
    name: 'Voice & Speech Agent',
    status: 'idle',
    capabilities: ['Text-to-speech', 'Voice cloning', 'Auto-captioning', 'Emotion control'],
    tasksCompleted: 445,
    lastRun: '8m ago',
  },
  {
    type: 'editing',
    name: 'Editing Agent',
    status: 'running',
    progress: 34,
    capabilities: ['Video compositing', 'Overlay placement', 'Transitions', 'Color grading'],
    tasksCompleted: 1089,
    lastRun: 'Now',
  },
  {
    type: 'optimization',
    name: 'Optimization Agent',
    status: 'idle',
    capabilities: ['Platform encoding', 'Aspect ratio conversion', 'File size optimization'],
    tasksCompleted: 3421,
    lastRun: '3m ago',
  },
  {
    type: 'analytics',
    name: 'Analytics Agent',
    status: 'idle',
    capabilities: ['Performance prediction', 'A/B testing', 'Engagement analysis', 'Trend detection'],
    tasksCompleted: 567,
    lastRun: '12m ago',
  },
  {
    type: 'safety',
    name: 'Safety & Compliance Agent',
    status: 'idle',
    capabilities: ['Content moderation', 'Copyright detection', 'AI labeling', 'Platform compliance'],
    tasksCompleted: 4532,
    lastRun: '1m ago',
  },
  {
    type: 'social_media',
    name: 'Social Media Agent',
    status: 'idle',
    capabilities: ['Multi-platform upload', 'Caption optimization', 'Scheduling', 'Analytics sync'],
    tasksCompleted: 789,
    lastRun: '6m ago',
  },
]

export default function AgentsPage() {
  const [agents, setAgents] = useState(defaultAgents)
  const [isLoading, setIsLoading] = useState(false)
  const [filter, setFilter] = useState('all')
  const [search, setSearch] = useState('')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')

  const refreshAgents = async () => {
    setIsLoading(true)
    try {
      const data = await api.getAgents()
      setAgents(defaultAgents.map(agent => ({
        ...agent,
        status: data[agent.type]?.is_running ? 'running' : 'idle',
      })))
    } catch (error) {
      console.error('Failed to fetch agents:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    refreshAgents()
  }, [])

  const filteredAgents = agents.filter(agent => {
    if (filter !== 'all' && agent.status !== filter) return false
    if (search && !agent.name.toLowerCase().includes(search.toLowerCase())) return false
    return true
  })

  const statusCounts = {
    all: agents.length,
    idle: agents.filter(a => a.status === 'idle').length,
    running: agents.filter(a => a.status === 'running').length,
    completed: agents.filter(a => a.status === 'completed').length,
    error: agents.filter(a => a.status === 'error').length,
  }

  const totalTasksCompleted = agents.reduce((sum, a) => sum + (a.tasksCompleted || 0), 0)

  return (
    <div className="flex min-h-screen bg-[#0a0a0f]">
      <Sidebar />

      <main className="flex-1 overflow-auto">
        <Header title="AI Agents" subtitle="Monitor and manage your 10x specialist agents" />

        <div className="p-6 space-y-6">
          {/* Hero Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-violet-500/10 via-fuchsia-500/5 to-cyan-500/10 border border-white/10 p-8"
          >
            {/* Background effects */}
            <div className="absolute inset-0">
              <div className="absolute top-0 right-0 w-96 h-96 bg-violet-500/20 rounded-full blur-3xl" />
              <div className="absolute bottom-0 left-0 w-64 h-64 bg-cyan-500/20 rounded-full blur-3xl" />
            </div>

            <div className="relative flex items-center justify-between">
              <div>
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-center gap-3 mb-4"
                >
                  <div className="p-3 rounded-2xl bg-gradient-to-br from-violet-500 to-fuchsia-600 shadow-lg shadow-violet-500/30">
                    <CircuitBoard className="w-8 h-8 text-white" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold">AI Agent Swarm</h2>
                    <p className="text-white/60">10 specialist agents working in harmony</p>
                  </div>
                </motion.div>

                <div className="flex items-center gap-6">
                  <div className="flex items-center gap-2">
                    <div className="relative">
                      <div className="w-3 h-3 bg-emerald-500 rounded-full" />
                      <div className="absolute inset-0 w-3 h-3 bg-emerald-500 rounded-full animate-ping" />
                    </div>
                    <span className="text-sm text-white/70">{statusCounts.running} agents active</span>
                  </div>
                  <div className="text-sm text-white/50">
                    {totalTasksCompleted.toLocaleString()} tasks completed
                  </div>
                </div>
              </div>

              <div className="hidden lg:flex items-center gap-4">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="px-6 py-3 bg-white/10 hover:bg-white/15 rounded-xl font-medium flex items-center gap-2 transition-colors"
                >
                  <Terminal className="w-5 h-5" />
                  View Logs
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.02, boxShadow: '0 20px 40px rgba(139, 92, 246, 0.3)' }}
                  whileTap={{ scale: 0.98 }}
                  className="px-6 py-3 bg-gradient-to-r from-violet-600 to-fuchsia-600 rounded-xl font-semibold flex items-center gap-2 shadow-lg shadow-violet-500/25"
                >
                  <Play className="w-5 h-5" />
                  Run All Agents
                </motion.button>
              </div>
            </div>
          </motion.div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <StatsCard icon={Bot} label="Total Agents" value={statusCounts.all} color="#8B5CF6" delay={0} />
            <StatsCard icon={CheckCircle2} label="Ready" value={statusCounts.idle} color="#10B981" delay={0.05} />
            <StatsCard icon={Activity} label="Running" value={statusCounts.running} change="+2" color="#3B82F6" delay={0.1} />
            <StatsCard icon={Sparkles} label="Completed" value={statusCounts.completed} color="#06B6D4" delay={0.15} />
            <StatsCard icon={XCircle} label="Errors" value={statusCounts.error} color="#EF4444" delay={0.2} />
          </div>

          {/* Filters & Search */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="flex flex-col md:flex-row gap-4 items-center justify-between p-4 rounded-2xl bg-white/5 border border-white/10"
          >
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-white/40" />
              <div className="flex gap-1 p-1 rounded-xl bg-white/5">
                {[
                  { key: 'all', label: 'All' },
                  { key: 'idle', label: 'Ready' },
                  { key: 'running', label: 'Running' },
                  { key: 'completed', label: 'Done' },
                  { key: 'error', label: 'Error' },
                ].map((status) => (
                  <motion.button
                    key={status.key}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => setFilter(status.key)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      filter === status.key
                        ? 'bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white shadow-lg'
                        : 'text-white/60 hover:text-white hover:bg-white/5'
                    }`}
                  >
                    {status.label}
                    <span className="ml-1.5 text-xs opacity-70">
                      ({statusCounts[status.key as keyof typeof statusCounts]})
                    </span>
                  </motion.button>
                ))}
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/30" />
                <input
                  type="text"
                  placeholder="Search agents..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="pl-10 pr-4 py-2.5 w-64 bg-white/5 border border-white/10 rounded-xl text-sm placeholder:text-white/30 focus:outline-none focus:border-violet-500/50 transition-colors"
                />
              </div>
              <motion.button
                whileHover={{ scale: 1.05, rotate: 180 }}
                whileTap={{ scale: 0.95 }}
                onClick={refreshAgents}
                disabled={isLoading}
                className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
              >
                <RefreshCw className={`w-5 h-5 text-white/60 ${isLoading ? 'animate-spin' : ''}`} />
              </motion.button>
            </div>
          </motion.div>

          {/* Agent Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            <AnimatePresence mode="popLayout">
              {filteredAgents.map((agent, i) => (
                <motion.div
                  key={agent.type}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ delay: 0.03 * i }}
                  layout
                >
                  <EnhancedAgentCard
                    {...agent}
                    onRun={() => console.log('Run', agent.type)}
                    onStop={() => console.log('Stop', agent.type)}
                  />
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          {filteredAgents.length === 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center py-16"
            >
              <div className="w-20 h-20 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4">
                <Bot className="w-10 h-10 text-white/30" />
              </div>
              <p className="text-white/50 text-lg">No agents match your filters</p>
              <p className="text-white/30 text-sm mt-1">Try adjusting your search or filter criteria</p>
            </motion.div>
          )}
        </div>
      </main>
    </div>
  )
}
