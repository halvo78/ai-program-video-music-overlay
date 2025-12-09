'use client'

import { useState, useEffect } from 'react'
import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion'
import Link from 'next/link'
import {
  Sparkles,
  Play,
  ArrowRight,
  Check,
  Star,
  Zap,
  Video,
  Music,
  Image,
  Mic,
  Share2,
  BarChart3,
  Shield,
  Clock,
  Users,
  TrendingUp,
  ChevronDown,
  Menu,
  X,
} from 'lucide-react'

// Animated counter component
function AnimatedCounter({ value, suffix = '' }: { value: number; suffix?: string }) {
  const [count, setCount] = useState(0)

  useEffect(() => {
    const duration = 2000
    const steps = 60
    const increment = value / steps
    let current = 0

    const timer = setInterval(() => {
      current += increment
      if (current >= value) {
        setCount(value)
        clearInterval(timer)
      } else {
        setCount(Math.floor(current))
      }
    }, duration / steps)

    return () => clearInterval(timer)
  }, [value])

  return <span>{count.toLocaleString()}{suffix}</span>
}

// Floating 3D card component
function FloatingCard({ children, delay = 0, className = '' }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8, delay }}
      whileHover={{ y: -10, rotateY: 5, rotateX: 5 }}
      className={`relative ${className}`}
      style={{ transformStyle: 'preserve-3d' }}
    >
      {children}
    </motion.div>
  )
}

// Particle background
function ParticleBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {[...Array(50)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-1 h-1 bg-primary/30 rounded-full"
          initial={{
            x: Math.random() * (typeof window !== 'undefined' ? window.innerWidth : 1920),
            y: Math.random() * (typeof window !== 'undefined' ? window.innerHeight : 1080),
          }}
          animate={{
            y: [null, Math.random() * -500],
            opacity: [0, 1, 0],
          }}
          transition={{
            duration: Math.random() * 10 + 10,
            repeat: Infinity,
            delay: Math.random() * 5,
          }}
        />
      ))}
    </div>
  )
}

// Live activity feed
function LiveActivityFeed() {
  const activities = [
    { user: 'Sarah M.', action: 'created a TikTok video', time: '2s ago' },
    { user: 'Alex K.', action: 'generated music track', time: '5s ago' },
    { user: 'Mike R.', action: 'published to YouTube', time: '8s ago' },
    { user: 'Emma L.', action: 'created Instagram Reel', time: '12s ago' },
  ]

  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % activities.length)
    }, 3000)
    return () => clearInterval(timer)
  }, [])

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="inline-flex items-center gap-3 px-4 py-2 bg-white/5 backdrop-blur-sm rounded-full border border-white/10"
    >
      <span className="relative flex h-2 w-2">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-success opacity-75" />
        <span className="relative inline-flex rounded-full h-2 w-2 bg-success" />
      </span>
      <AnimatePresence mode="wait">
        <motion.span
          key={currentIndex}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="text-sm text-white/80"
        >
          <span className="font-medium text-white">{activities[currentIndex].user}</span>
          {' '}{activities[currentIndex].action}
        </motion.span>
      </AnimatePresence>
    </motion.div>
  )
}

// Feature card with icon
function FeatureCard({ icon: Icon, title, description, gradient, delay }: any) {
  return (
    <FloatingCard delay={delay}>
      <div className="group relative p-6 rounded-2xl bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 hover:border-primary/30 transition-all duration-500 overflow-hidden">
        {/* Glow effect on hover */}
        <div className={`absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-gradient-to-br ${gradient} blur-xl`} />

        <div className="relative z-10">
          <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${gradient} p-0.5 mb-4`}>
            <div className="w-full h-full rounded-xl bg-background flex items-center justify-center">
              <Icon className="w-6 h-6 text-white" />
            </div>
          </div>
          <h3 className="text-lg font-semibold mb-2">{title}</h3>
          <p className="text-sm text-muted-foreground">{description}</p>
        </div>
      </div>
    </FloatingCard>
  )
}

// Testimonial card
function TestimonialCard({ quote, author, role, avatar, delay }: any) {
  return (
    <FloatingCard delay={delay}>
      <div className="p-6 rounded-2xl bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10">
        <div className="flex gap-1 mb-4">
          {[...Array(5)].map((_, i) => (
            <Star key={i} className="w-4 h-4 fill-yellow-500 text-yellow-500" />
          ))}
        </div>
        <p className="text-white/80 mb-4 italic">"{quote}"</p>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-white font-bold">
            {avatar}
          </div>
          <div>
            <p className="font-medium">{author}</p>
            <p className="text-sm text-muted-foreground">{role}</p>
          </div>
        </div>
      </div>
    </FloatingCard>
  )
}

// Pricing card
function PricingCard({ name, price, period, features, popular, cta, delay }: any) {
  return (
    <FloatingCard delay={delay}>
      <div className={`relative p-8 rounded-3xl ${popular ? 'bg-gradient-to-br from-primary/20 via-secondary/10 to-accent/20 border-2 border-primary/50' : 'bg-white/5 border border-white/10'}`}>
        {popular && (
          <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-gradient-to-r from-primary to-secondary rounded-full text-sm font-medium">
            Most Popular
          </div>
        )}
        <h3 className="text-xl font-bold mb-2">{name}</h3>
        <div className="flex items-baseline gap-1 mb-6">
          <span className="text-4xl font-bold">${price}</span>
          <span className="text-muted-foreground">/{period}</span>
        </div>
        <ul className="space-y-3 mb-8">
          {features.map((feature: string, i: number) => (
            <li key={i} className="flex items-center gap-2 text-sm">
              <Check className="w-4 h-4 text-success" />
              {feature}
            </li>
          ))}
        </ul>
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className={`w-full py-3 rounded-xl font-semibold transition-all ${popular ? 'bg-gradient-to-r from-primary to-secondary text-white shadow-lg shadow-primary/25' : 'bg-white/10 hover:bg-white/20'}`}
        >
          {cta}
        </motion.button>
      </div>
    </FloatingCard>
  )
}

export default function LandingPage() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { scrollYProgress } = useScroll()
  const opacity = useTransform(scrollYProgress, [0, 0.2], [1, 0])
  const scale = useTransform(scrollYProgress, [0, 0.2], [1, 0.95])

  const features = [
    { icon: Video, title: 'AI Video Generation', description: 'Create stunning videos from text prompts using state-of-the-art AI models', gradient: 'from-violet-500 to-purple-500' },
    { icon: Music, title: 'AI Music Creation', description: 'Generate custom soundtracks that perfectly match your video mood', gradient: 'from-pink-500 to-rose-500' },
    { icon: Image, title: 'AI Image Generation', description: 'Create thumbnails, overlays, and visual assets with FLUX Pro', gradient: 'from-cyan-500 to-blue-500' },
    { icon: Mic, title: 'Voice & Speech', description: 'Natural text-to-speech and voice cloning capabilities', gradient: 'from-emerald-500 to-green-500' },
    { icon: Share2, title: 'Social Publishing', description: 'One-click publishing to TikTok, Instagram, YouTube & more', gradient: 'from-orange-500 to-amber-500' },
    { icon: BarChart3, title: 'AI Analytics', description: 'Predict performance and optimize content with AI insights', gradient: 'from-indigo-500 to-violet-500' },
  ]

  const testimonials = [
    { quote: "Taj Chat transformed my content creation workflow. I went from 1 video per week to 10 per day!", author: "Sarah Mitchell", role: "Content Creator", avatar: "SM" },
    { quote: "The AI agents work like magic. It's like having a full production team at my fingertips.", author: "Alex Johnson", role: "Marketing Director", avatar: "AJ" },
    { quote: "Finally, an all-in-one tool that actually delivers on its promises. Game changer!", author: "Mike Roberts", role: "YouTuber, 2M subs", avatar: "MR" },
  ]

  const stats = [
    { value: 1000000, suffix: '+', label: 'Videos Created' },
    { value: 50000, suffix: '+', label: 'Active Creators' },
    { value: 99.9, suffix: '%', label: 'Uptime' },
    { value: 4.9, suffix: '/5', label: 'User Rating' },
  ]

  return (
    <div className="min-h-screen bg-background overflow-hidden">
      {/* Animated background */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(139,92,246,0.15),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_right,rgba(236,72,153,0.1),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,rgba(6,182,212,0.1),transparent_50%)]" />
        <ParticleBackground />
      </div>

      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50">
        <div className="mx-auto max-w-7xl px-6 py-4">
          <div className="flex items-center justify-between backdrop-blur-xl bg-white/5 rounded-2xl px-6 py-3 border border-white/10">
            <Link href="/" className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary via-secondary to-accent flex items-center justify-center">
                <Video className="w-5 h-5 text-white" />
              </div>
              <span className="font-display font-bold text-xl">Taj Chat</span>
            </Link>

            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-sm text-white/70 hover:text-white transition-colors">Features</a>
              <a href="#pricing" className="text-sm text-white/70 hover:text-white transition-colors">Pricing</a>
              <a href="#testimonials" className="text-sm text-white/70 hover:text-white transition-colors">Testimonials</a>
              <Link href="/" className="text-sm text-white/70 hover:text-white transition-colors">Dashboard</Link>
            </div>

            <div className="hidden md:flex items-center gap-3">
              <button className="px-4 py-2 text-sm font-medium text-white/80 hover:text-white transition-colors">
                Sign In
              </button>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-5 py-2 bg-gradient-to-r from-primary to-secondary rounded-xl text-sm font-semibold shadow-lg shadow-primary/25"
              >
                Get Started Free
              </motion.button>
            </div>

            <button
              className="md:hidden p-2"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X /> : <Menu />}
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            style={{ opacity, scale }}
            className="text-center max-w-4xl mx-auto"
          >
            {/* Live activity badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-center mb-8"
            >
              <LiveActivityFeed />
            </motion.div>

            {/* Main headline */}
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-5xl md:text-7xl font-display font-bold mb-6 leading-tight"
            >
              Create{' '}
              <span className="relative">
                <span className="relative z-10 bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
                  Viral Videos
                </span>
                <motion.span
                  className="absolute -inset-1 bg-gradient-to-r from-primary/20 via-secondary/20 to-accent/20 blur-xl"
                  animate={{ opacity: [0.5, 1, 0.5] }}
                  transition={{ duration: 2, repeat: Infinity }}
                />
              </span>
              {' '}in Seconds
            </motion.h1>

            {/* Subheadline */}
            <motion.p
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-xl text-white/60 mb-8 max-w-2xl mx-auto"
            >
              10 specialist AI agents working together to generate stunning short-form videos
              with custom music, overlays, and automatic social media optimization.
            </motion.p>

            {/* CTA buttons */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12"
            >
              <Link href="/create">
                <motion.button
                  whileHover={{ scale: 1.05, boxShadow: '0 20px 40px rgba(139, 92, 246, 0.4)' }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-4 bg-gradient-to-r from-primary via-secondary to-accent rounded-2xl text-lg font-semibold shadow-2xl shadow-primary/30 flex items-center gap-2"
                >
                  <Sparkles className="w-5 h-5" />
                  Start Creating Free
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
              </Link>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl text-lg font-semibold flex items-center gap-2"
              >
                <Play className="w-5 h-5" />
                Watch Demo
              </motion.button>
            </motion.div>

            {/* Trust badges */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="flex flex-wrap items-center justify-center gap-8 text-white/40"
            >
              <span className="text-sm">Trusted by creators at</span>
              <div className="flex items-center gap-6">
                {['TikTok', 'YouTube', 'Instagram', 'Twitter'].map((platform) => (
                  <span key={platform} className="text-sm font-medium">{platform}</span>
                ))}
              </div>
            </motion.div>
          </motion.div>

          {/* Hero visual - Dashboard preview with real images */}
          <motion.div
            initial={{ opacity: 0, y: 100 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="relative mt-20 mx-auto max-w-6xl"
          >
            <div className="relative rounded-3xl overflow-hidden border border-white/10 shadow-2xl shadow-primary/20">
              {/* Glow effects */}
              <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-gradient-to-b from-primary/30 to-transparent rounded-full blur-3xl" />

              {/* Dashboard mockup with real content */}
              <div className="relative bg-gradient-to-br from-gray-900 to-gray-950 p-6 md:p-8">
                <div className="grid grid-cols-12 gap-4">
                  {/* Sidebar mockup */}
                  <div className="col-span-2 space-y-3">
                    <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
                      <Video className="w-5 h-5 text-white" />
                    </div>
                    <div className="space-y-2 mt-6">
                      {['Dashboard', 'Create', 'Studio', 'Agents', 'Gallery', 'Social'].map((item, i) => (
                        <div key={i} className={`h-8 rounded-lg ${i === 0 ? 'bg-primary/20 border border-primary/30' : 'bg-white/5'} flex items-center px-3`}>
                          <span className="text-[10px] text-white/60 truncate">{item}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Main content mockup with real images */}
                  <div className="col-span-10 space-y-4">
                    {/* Header */}
                    <div className="h-12 bg-white/5 rounded-xl flex items-center px-4 justify-between">
                      <span className="text-sm text-white/60">Dashboard</span>
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-secondary" />
                      </div>
                    </div>

                    {/* Stats cards */}
                    <div className="grid grid-cols-4 gap-4">
                      {[
                        { label: 'Videos', value: '147', color: 'from-violet-500/20 to-purple-500/10' },
                        { label: 'Views', value: '2.4M', color: 'from-pink-500/20 to-rose-500/10' },
                        { label: 'Likes', value: '89K', color: 'from-cyan-500/20 to-blue-500/10' },
                        { label: 'Followers', value: '+12K', color: 'from-emerald-500/20 to-green-500/10' },
                      ].map((stat, i) => (
                        <div key={i} className={`h-24 rounded-xl bg-gradient-to-br ${stat.color} border border-white/10 p-4 flex flex-col justify-between`}>
                          <span className="text-[10px] text-white/50">{stat.label}</span>
                          <span className="text-xl font-bold">{stat.value}</span>
                        </div>
                      ))}
                    </div>

                    {/* Video grid with real images */}
                    <div className="grid grid-cols-5 gap-3">
                      {[
                        'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=200&h=350&fit=crop&q=80',
                        'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=200&h=350&fit=crop&q=80',
                        'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=200&h=350&fit=crop&q=80',
                        'https://images.unsplash.com/photo-1507400492013-162706c8c05e?w=200&h=350&fit=crop&q=80',
                        'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=200&h=350&fit=crop&q=80',
                      ].map((img, i) => (
                        <motion.div
                          key={i}
                          className="aspect-[9/16] rounded-xl overflow-hidden relative group"
                          whileHover={{ scale: 1.05, zIndex: 10 }}
                        >
                          <img src={img} alt={`Video ${i + 1}`} className="w-full h-full object-cover" />
                          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                          <div className="absolute bottom-2 left-2 right-2">
                            <div className="flex items-center gap-1 text-[8px] text-white">
                              <span className="bg-black/40 backdrop-blur-sm px-1.5 py-0.5 rounded-full">124K</span>
                            </div>
                          </div>
                          {/* Platform badge */}
                          <div className={`absolute top-1.5 left-1.5 px-1.5 py-0.5 rounded text-[7px] font-medium text-white ${
                            i === 0 ? 'bg-gradient-to-r from-[#00F2EA] to-[#FF0050]' :
                            i === 1 ? 'bg-gradient-to-r from-[#F58529] to-[#8134AF]' :
                            i === 2 ? 'bg-red-600' :
                            i === 3 ? 'bg-gradient-to-r from-[#00F2EA] to-[#FF0050]' :
                            'bg-gradient-to-r from-[#F58529] to-[#8134AF]'
                          }`}>
                            {i === 0 || i === 3 ? 'TikTok' : i === 1 || i === 4 ? 'Insta' : 'YT'}
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Floating elements */}
            <motion.div
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity }}
              className="absolute -right-8 top-20 p-4 rounded-2xl bg-gradient-to-br from-success/20 to-success/5 border border-success/20 backdrop-blur-xl"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-success/20 flex items-center justify-center">
                  <TrendingUp className="w-5 h-5 text-success" />
                </div>
                <div>
                  <p className="text-sm font-medium">Video Published!</p>
                  <p className="text-xs text-white/60">TikTok • 1.2K views</p>
                </div>
              </div>
            </motion.div>

            <motion.div
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 4, repeat: Infinity }}
              className="absolute -left-8 bottom-20 p-4 rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 border border-primary/20 backdrop-blur-xl"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center">
                  <Zap className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <p className="text-sm font-medium">AI Processing</p>
                  <p className="text-xs text-white/60">10 agents active</p>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-6 border-y border-white/5">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="text-center"
              >
                <p className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                  <AnimatedCounter value={stat.value} suffix={stat.suffix} />
                </p>
                <p className="text-white/60 mt-2">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <span className="px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium">
              Powerful Features
            </span>
            <h2 className="text-4xl md:text-5xl font-display font-bold mt-6 mb-4">
              Everything You Need to{' '}
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Go Viral
              </span>
            </h2>
            <p className="text-xl text-white/60 max-w-2xl mx-auto">
              10 specialist AI agents working in parallel to create, edit, and publish
              your content across all major platforms.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, i) => (
              <FeatureCard key={feature.title} {...feature} delay={i * 0.1} />
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-6 bg-gradient-to-b from-transparent via-primary/5 to-transparent">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <span className="px-4 py-2 rounded-full bg-secondary/10 text-secondary text-sm font-medium">
              Simple Process
            </span>
            <h2 className="text-4xl md:text-5xl font-display font-bold mt-6 mb-4">
              Create Videos in{' '}
              <span className="bg-gradient-to-r from-secondary to-accent bg-clip-text text-transparent">
                3 Easy Steps
              </span>
            </h2>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { step: '01', title: 'Describe Your Vision', description: 'Tell our AI what kind of video you want to create. Be as detailed or simple as you like.' },
              { step: '02', title: 'AI Creates Magic', description: '10 specialist agents work together to generate video, music, images, and voiceovers.' },
              { step: '03', title: 'Publish Everywhere', description: 'One-click publishing to TikTok, Instagram, YouTube, and more with optimized formats.' },
            ].map((item, i) => (
              <FloatingCard key={item.step} delay={i * 0.2}>
                <div className="relative p-8 rounded-2xl bg-white/5 border border-white/10 text-center">
                  <span className="text-6xl font-display font-bold text-white/10">{item.step}</span>
                  <h3 className="text-xl font-semibold mt-4 mb-2">{item.title}</h3>
                  <p className="text-white/60">{item.description}</p>
                </div>
              </FloatingCard>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <span className="px-4 py-2 rounded-full bg-accent/10 text-accent text-sm font-medium">
              Testimonials
            </span>
            <h2 className="text-4xl md:text-5xl font-display font-bold mt-6 mb-4">
              Loved by{' '}
              <span className="bg-gradient-to-r from-accent to-success bg-clip-text text-transparent">
                50,000+ Creators
              </span>
            </h2>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6">
            {testimonials.map((testimonial, i) => (
              <TestimonialCard key={testimonial.author} {...testimonial} delay={i * 0.1} />
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <span className="px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium">
              Pricing
            </span>
            <h2 className="text-4xl md:text-5xl font-display font-bold mt-6 mb-4">
              Simple,{' '}
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Transparent Pricing
              </span>
            </h2>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <PricingCard
              name="Starter"
              price="0"
              period="month"
              features={['10 videos/month', '5 AI agents', 'Basic templates', '720p exports', 'Watermark']}
              cta="Get Started"
              delay={0}
            />
            <PricingCard
              name="Pro"
              price="29"
              period="month"
              features={['100 videos/month', 'All 10 AI agents', 'Premium templates', '4K exports', 'No watermark', 'Priority support']}
              popular
              cta="Start Free Trial"
              delay={0.1}
            />
            <PricingCard
              name="Enterprise"
              price="99"
              period="month"
              features={['Unlimited videos', 'Custom AI training', 'API access', 'White-label', 'Dedicated support', 'SLA guarantee']}
              cta="Contact Sales"
              delay={0.2}
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative p-12 rounded-3xl overflow-hidden"
          >
            {/* Background */}
            <div className="absolute inset-0 bg-gradient-to-br from-primary via-secondary to-accent opacity-20" />
            <div className="absolute inset-0 bg-gradient-to-t from-background to-transparent" />

            <div className="relative z-10 text-center">
              <h2 className="text-4xl md:text-5xl font-display font-bold mb-4">
                Ready to Create{' '}
                <span className="bg-gradient-to-r from-white to-white/80 bg-clip-text text-transparent">
                  Amazing Videos?
                </span>
              </h2>
              <p className="text-xl text-white/60 mb-8 max-w-xl mx-auto">
                Join 50,000+ creators who are already using Taj Chat to create viral content.
              </p>
              <Link href="/create">
                <motion.button
                  whileHover={{ scale: 1.05, boxShadow: '0 20px 40px rgba(255, 255, 255, 0.2)' }}
                  whileTap={{ scale: 0.95 }}
                  className="px-10 py-5 bg-white text-background rounded-2xl text-lg font-bold shadow-2xl flex items-center gap-2 mx-auto"
                >
                  <Sparkles className="w-5 h-5" />
                  Start Creating Now
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-white/5">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary via-secondary to-accent flex items-center justify-center">
                <Video className="w-5 h-5 text-white" />
              </div>
              <span className="font-display font-bold text-xl">Taj Chat</span>
            </div>
            <div className="flex items-center gap-8 text-sm text-white/60">
              <a href="#" className="hover:text-white transition-colors">Privacy</a>
              <a href="#" className="hover:text-white transition-colors">Terms</a>
              <a href="#" className="hover:text-white transition-colors">Support</a>
              <a href="#" className="hover:text-white transition-colors">Blog</a>
            </div>
            <p className="text-sm text-white/40">© 2024 Taj Chat. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
