'use client'

import { motion } from 'framer-motion'
import {
  Video,
  Music,
  Image,
  Mic,
  FileText,
  Scissors,
  Gauge,
  BarChart3,
  Shield,
  Share2,
  Loader2,
  CheckCircle2,
  XCircle,
} from 'lucide-react'
import { cn, getAgentColor } from '@/lib/utils'

interface AgentCardProps {
  type: string
  name: string
  status: 'idle' | 'running' | 'completed' | 'error'
  progress?: number
  capabilities?: string[]
  compact?: boolean
}

const agentIcons: Record<string, any> = {
  video_generation: Video,
  music_generation: Music,
  image_generation: Image,
  voice_speech: Mic,
  content_analysis: FileText,
  editing: Scissors,
  optimization: Gauge,
  analytics: BarChart3,
  safety: Shield,
  social_media: Share2,
}

const statusConfig = {
  idle: { label: 'Ready', color: 'text-muted-foreground', bg: 'bg-white/5' },
  running: { label: 'Processing', color: 'text-primary', bg: 'bg-primary/10' },
  completed: { label: 'Complete', color: 'text-success', bg: 'bg-success/10' },
  error: { label: 'Error', color: 'text-error', bg: 'bg-error/10' },
}

export default function AgentCard({
  type,
  name,
  status,
  progress = 0,
  capabilities = [],
  compact = false,
}: AgentCardProps) {
  const Icon = agentIcons[type] || FileText
  const color = getAgentColor(type)
  const statusInfo = statusConfig[status]

  if (compact) {
    return (
      <motion.div
        whileHover={{ scale: 1.02 }}
        className={cn(
          'relative flex items-center gap-3 p-3 rounded-xl transition-all duration-200',
          'bg-gray-900/60 border border-white/5',
          status === 'running' && 'border-primary/30 shadow-glow-primary',
          status === 'completed' && 'border-success/30',
          status === 'error' && 'border-error/30'
        )}
      >
        <div
          className="w-10 h-10 rounded-xl flex items-center justify-center"
          style={{ backgroundColor: `${color}20` }}
        >
          <Icon className="w-5 h-5" style={{ color }} />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium truncate">{name}</p>
          <p className={cn('text-xs', statusInfo.color)}>{statusInfo.label}</p>
        </div>
        {status === 'running' && (
          <Loader2 className="w-4 h-4 text-primary animate-spin" />
        )}
        {status === 'completed' && (
          <CheckCircle2 className="w-4 h-4 text-success" />
        )}
        {status === 'error' && (
          <XCircle className="w-4 h-4 text-error" />
        )}
      </motion.div>
    )
  }

  return (
    <motion.div
      whileHover={{ y: -4 }}
      className={cn(
        'relative overflow-hidden rounded-2xl transition-all duration-300',
        'bg-gradient-to-br from-gray-900/90 to-gray-800/50',
        'border border-white/5',
        status === 'running' && 'border-primary/30 shadow-glow-primary',
      )}
    >
      {/* Top accent line */}
      <div
        className="absolute top-0 left-0 right-0 h-1"
        style={{
          background: status === 'running'
            ? `linear-gradient(90deg, transparent, ${color}, transparent)`
            : 'transparent'
        }}
      />

      <div className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div
            className="w-12 h-12 rounded-xl flex items-center justify-center"
            style={{ backgroundColor: `${color}15` }}
          >
            <Icon className="w-6 h-6" style={{ color }} />
          </div>
          <div className={cn('px-2.5 py-1 rounded-lg text-xs font-medium', statusInfo.bg, statusInfo.color)}>
            {statusInfo.label}
          </div>
        </div>

        {/* Name */}
        <h3 className="text-base font-semibold mb-1">{name}</h3>
        <p className="text-xs text-muted-foreground mb-4">Agent #{type.split('_')[0]}</p>

        {/* Progress (if running) */}
        {status === 'running' && (
          <div className="mb-4">
            <div className="flex justify-between text-xs mb-1">
              <span className="text-muted-foreground">Progress</span>
              <span className="text-primary">{progress}%</span>
            </div>
            <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                className="h-full rounded-full"
                style={{ background: `linear-gradient(90deg, ${color}, ${color}80)` }}
              />
            </div>
          </div>
        )}

        {/* Capabilities */}
        {capabilities.length > 0 && (
          <div className="flex flex-wrap gap-1.5">
            {capabilities.slice(0, 3).map((cap, i) => (
              <span
                key={i}
                className="px-2 py-0.5 bg-white/5 rounded text-xs text-muted-foreground"
              >
                {cap}
              </span>
            ))}
            {capabilities.length > 3 && (
              <span className="px-2 py-0.5 bg-white/5 rounded text-xs text-muted-foreground">
                +{capabilities.length - 3}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Running animation */}
      {status === 'running' && (
        <motion.div
          initial={{ x: '-100%' }}
          animate={{ x: '100%' }}
          transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
          className="absolute bottom-0 left-0 right-0 h-0.5"
          style={{
            background: `linear-gradient(90deg, transparent, ${color}, transparent)`
          }}
        />
      )}
    </motion.div>
  )
}
