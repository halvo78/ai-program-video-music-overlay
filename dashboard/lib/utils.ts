import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDuration(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

export function formatDate(date: Date | string): string {
  const d = new Date(date)
  return d.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function getAgentColor(agentType: string): string {
  const colors: Record<string, string> = {
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
  return colors[agentType] || '#6B7280'
}

export function getPlatformColor(platform: string): string {
  const colors: Record<string, string> = {
    tiktok: 'linear-gradient(135deg, #00F2EA, #FF0050)',
    instagram_reels: 'linear-gradient(135deg, #F58529, #DD2A7B, #8134AF)',
    youtube_shorts: '#FF0000',
    twitter: '#1DA1F2',
  }
  return colors[platform] || '#6B7280'
}
