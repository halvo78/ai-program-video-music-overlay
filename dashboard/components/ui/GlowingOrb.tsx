'use client'

import { motion } from 'framer-motion'

interface GlowingOrbProps {
  color?: string
  size?: 'sm' | 'md' | 'lg'
  animated?: boolean
  className?: string
}

export default function GlowingOrb({
  color = '#8B5CF6',
  size = 'md',
  animated = true,
  className = '',
}: GlowingOrbProps) {
  const sizes = {
    sm: 'w-32 h-32',
    md: 'w-64 h-64',
    lg: 'w-96 h-96',
  }

  return (
    <motion.div
      className={`absolute rounded-full blur-3xl pointer-events-none ${sizes[size]} ${className}`}
      style={{ backgroundColor: color, opacity: 0.3 }}
      animate={animated ? {
        scale: [1, 1.2, 1],
        opacity: [0.2, 0.4, 0.2],
      } : undefined}
      transition={{
        duration: 4,
        repeat: Infinity,
        ease: 'easeInOut',
      }}
    />
  )
}
