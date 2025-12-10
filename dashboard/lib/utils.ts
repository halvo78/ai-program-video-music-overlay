import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getAgentColor(agentType: string): string {
  const colorMap: Record<string, string> = {
    content_analysis: '#8B5CF6',
    video_generation: '#EC4899',
    music_generation: '#06B6D4',
    image_generation: '#10B981',
    voice_speech: '#F59E0B',
    editing: '#6366F1',
    optimization: '#EAB308',
    analytics: '#3B82F6',
    safety: '#EF4444',
    social_media: '#D946EF',
  }
  return colorMap[agentType] || '#6B7280'
}
