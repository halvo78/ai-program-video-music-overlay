'use client'

import { motion } from 'framer-motion'

interface AnimatedGradientProps {
  className?: string
  colors?: string[]
}

export default function AnimatedGradient({
  className = '',
  colors = ['#8B5CF6', '#EC4899', '#06B6D4'],
}: AnimatedGradientProps) {
  return (
    <motion.div
      className={`absolute inset-0 ${className}`}
      style={{
        background: `linear-gradient(135deg, ${colors.join(', ')})`,
        backgroundSize: '400% 400%',
      }}
      animate={{
        backgroundPosition: ['0% 0%', '100% 100%', '0% 0%'],
      }}
      transition={{
        duration: 10,
        repeat: Infinity,
        ease: 'linear',
      }}
    />
  )
}
