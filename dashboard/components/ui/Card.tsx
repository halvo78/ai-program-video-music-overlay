'use client'

import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'glass' | 'gradient' | 'bordered'
  hover?: boolean
  glow?: 'primary' | 'secondary' | 'accent' | 'success' | 'none'
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'default', hover = false, glow = 'none', children, ...props }, ref) => {
    const variants = {
      default: 'bg-gray-900/80 border border-white/5',
      glass: 'glass-card',
      gradient: 'bg-gradient-to-br from-gray-900/90 to-gray-800/50 border border-white/10',
      bordered: 'bg-gray-900/60 border-2 border-white/10',
    }

    const glowStyles = {
      primary: 'hover:shadow-glow-primary hover:border-primary/30',
      secondary: 'hover:shadow-glow-secondary hover:border-secondary/30',
      accent: 'hover:shadow-glow-accent hover:border-accent/30',
      success: 'hover:shadow-glow-success hover:border-success/30',
      none: '',
    }

    return (
      <div
        ref={ref}
        className={cn(
          'rounded-2xl p-6 transition-all duration-300',
          variants[variant],
          hover && 'cursor-pointer hover:-translate-y-1 hover:scale-[1.01]',
          glowStyles[glow],
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)

Card.displayName = 'Card'

export const CardHeader = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('flex items-center justify-between mb-4', className)} {...props} />
  )
)
CardHeader.displayName = 'CardHeader'

export const CardTitle = forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn('text-lg font-semibold', className)} {...props} />
  )
)
CardTitle.displayName = 'CardTitle'

export const CardDescription = forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn('text-sm text-muted-foreground', className)} {...props} />
  )
)
CardDescription.displayName = 'CardDescription'

export const CardContent = forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('', className)} {...props} />
  )
)
CardContent.displayName = 'CardContent'

export default Card
