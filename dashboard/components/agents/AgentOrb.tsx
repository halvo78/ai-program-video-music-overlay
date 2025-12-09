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
} from 'lucide-react'

interface AgentOrbProps {
  type: string
  name: string
  status: 'idle' | 'running' | 'completed' | 'error'
  progress?: number
  size?: 'sm' | 'md' | 'lg'
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

const agentColors: Record<string, string> = {
  video_generation: '#8B5CF6',
  music_generation: '#EC4899',
  image_generation: '#06B6D4',
  voice_speech: '#10B981',
  content_analysis: '#F59E0B',
  editing: '#EF4444',
  optimization: '#3B82F6',
  analytics: '#6366F1',
  safety: '#14B8A6',
  social_media: '#F97316',
}

export default function AgentOrb({ type, name, status, progress = 0, size = 'md' }: AgentOrbProps) {
  const Icon = agentIcons[type] || FileText
  const color = agentColors[type] || '#6B7280'

  const sizes = {
    sm: { container: 'w-16 h-16', icon: 'w-6 h-6', ring: 64 },
    md: { container: 'w-24 h-24', icon: 'w-8 h-8', ring: 96 },
    lg: { container: 'w-32 h-32', icon: 'w-10 h-10', ring: 128 },
  }

  const { container, icon, ring } = sizes[size]
  const radius = (ring - 6) / 2
  const circumference = radius * 2 * Math.PI
  const offset = circumference - (progress / 100) * circumference

  return (
    <motion.div
      className="relative flex flex-col items-center"
      whileHover={{ scale: 1.05 }}
    >
      {/* Outer glow */}
      {status === 'running' && (
        <motion.div
          className={`absolute ${container} rounded-full`}
          style={{ backgroundColor: color, opacity: 0.2 }}
          animate={{ scale: [1, 1.3, 1], opacity: [0.2, 0.4, 0.2] }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      )}

      {/* Progress ring */}
      <div className={`relative ${container}`}>
        <svg width={ring} height={ring} className="absolute inset-0 transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={ring / 2}
            cy={ring / 2}
            r={radius}
            fill="none"
            stroke="rgba(255,255,255,0.1)"
            strokeWidth={3}
          />
          {/* Progress circle */}
          {status === 'running' && (
            <motion.circle
              cx={ring / 2}
              cy={ring / 2}
              r={radius}
              fill="none"
              stroke={color}
              strokeWidth={3}
              strokeLinecap="round"
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset: offset }}
              transition={{ duration: 0.5 }}
              style={{ strokeDasharray: circumference }}
            />
          )}
          {status === 'completed' && (
            <circle
              cx={ring / 2}
              cy={ring / 2}
              r={radius}
              fill="none"
              stroke="#10B981"
              strokeWidth={3}
            />
          )}
        </svg>

        {/* Inner orb */}
        <motion.div
          className={`absolute inset-2 rounded-full flex items-center justify-center`}
          style={{
            background: status === 'running'
              ? `linear-gradient(135deg, ${color}40, ${color}20)`
              : status === 'completed'
              ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.4), rgba(16, 185, 129, 0.2))'
              : 'linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05))',
            border: `1px solid ${status === 'running' ? color : status === 'completed' ? '#10B981' : 'rgba(255,255,255,0.1)'}`,
          }}
          animate={status === 'running' ? {
            boxShadow: [
              `0 0 20px ${color}40`,
              `0 0 40px ${color}60`,
              `0 0 20px ${color}40`,
            ]
          } : {}}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <Icon
            className={icon}
            style={{
              color: status === 'running' ? color : status === 'completed' ? '#10B981' : '#6B7280'
            }}
          />
        </motion.div>
      </div>

      {/* Label */}
      <p className="mt-2 text-xs font-medium text-center">{name}</p>
      <p className={`text-xs ${
        status === 'running' ? 'text-primary' :
        status === 'completed' ? 'text-success' :
        'text-muted-foreground'
      }`}>
        {status === 'running' ? `${progress}%` : status}
      </p>
    </motion.div>
  )
}
