'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Share2,
  TrendingUp,
  TrendingDown,
  Users,
  Eye,
  Heart,
  MessageCircle,
  Send,
  Calendar,
  Clock,
  Plus,
  Filter,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
  MoreVertical,
  Sparkles,
  Zap,
  BarChart3,
  Globe,
  Play,
  Image,
  Video,
  Link,
  Hash,
  ArrowUpRight,
  ArrowDownRight,
  ChevronRight,
  Star,
  Award,
  Flame,
  Target,
  Bot,
} from 'lucide-react'
import Sidebar from '@/components/layout/Sidebar'
import Header from '@/components/layout/Header'
import Card, { CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import Button from '@/components/ui/Button'

// Platform configuration
const platforms = [
  {
    id: 'tiktok',
    name: 'TikTok',
    icon: '🎵',
    gradient: 'from-[#00F2EA] to-[#FF0050]',
    bgGradient: 'from-[#00F2EA]/20 to-[#FF0050]/20',
    connected: true,
    followers: 125000,
    engagement: 8.7,
    posts: 47,
    views: 1200000,
    growth: 28,
  },
  {
    id: 'instagram',
    name: 'Instagram',
    icon: '📸',
    gradient: 'from-[#F58529] via-[#DD2A7B] to-[#8134AF]',
    bgGradient: 'from-[#F58529]/20 to-[#8134AF]/20',
    connected: true,
    followers: 89000,
    engagement: 6.2,
    posts: 32,
    views: 680000,
    growth: 15,
  },
  {
    id: 'youtube',
    name: 'YouTube',
    icon: '▶️',
    gradient: 'from-[#FF0000] to-[#CC0000]',
    bgGradient: 'from-[#FF0000]/20 to-[#CC0000]/20',
    connected: true,
    followers: 45200,
    engagement: 9.1,
    posts: 24,
    views: 420000,
    growth: 22,
  },
  {
    id: 'twitter',
    name: 'Twitter/X',
    icon: '𝕏',
    gradient: 'from-[#1DA1F2] to-[#0D8BD9]',
    bgGradient: 'from-[#1DA1F2]/20 to-[#0D8BD9]/20',
    connected: true,
    followers: 32100,
    engagement: 4.8,
    posts: 89,
    views: 100000,
    growth: 8,
  },
  {
    id: 'facebook',
    name: 'Facebook',
    icon: '👤',
    gradient: 'from-[#1877F2] to-[#0D65D9]',
    bgGradient: 'from-[#1877F2]/20 to-[#0D65D9]/20',
    connected: false,
    followers: 0,
    engagement: 0,
    posts: 0,
    views: 0,
    growth: 0,
  },
]

// Scheduled posts data
const scheduledPosts = [
  {
    id: '1',
    title: 'Morning Motivation Tips',
    platforms: ['tiktok', 'instagram'],
    scheduledFor: '2024-01-16T09:00:00',
    status: 'scheduled',
    thumbnail: 'https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=100&h=100&fit=crop',
    type: 'video',
  },
  {
    id: '2',
    title: 'Quick Recipe: 5-Min Breakfast',
    platforms: ['youtube', 'tiktok'],
    scheduledFor: '2024-01-16T12:30:00',
    status: 'scheduled',
    thumbnail: 'https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=100&h=100&fit=crop',
    type: 'video',
  },
  {
    id: '3',
    title: 'AI Tools You Need in 2024',
    platforms: ['twitter', 'instagram'],
    scheduledFor: '2024-01-16T15:00:00',
    status: 'scheduled',
    thumbnail: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=100&h=100&fit=crop',
    type: 'video',
  },
  {
    id: '4',
    title: 'Behind the Scenes',
    platforms: ['instagram'],
    scheduledFor: '2024-01-16T18:00:00',
    status: 'draft',
    thumbnail: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop',
    type: 'image',
  },
]

// Recent activity data
const recentActivity = [
  { type: 'publish', platform: 'tiktok', title: 'Dance Challenge Video', time: '2 hours ago', icon: '🎵' },
  { type: 'engagement', platform: 'instagram', title: '+1.2K likes on "Morning Routine"', time: '4 hours ago', icon: '📸' },
  { type: 'milestone', platform: 'youtube', title: 'Reached 45K subscribers!', time: '6 hours ago', icon: '🎉' },
  { type: 'comment', platform: 'twitter', title: '24 new replies', time: '8 hours ago', icon: '💬' },
]

// Trending hashtags
const trendingHashtags = [
  { tag: '#AIContent', posts: '2.4M', growth: 45 },
  { tag: '#ShortForm', posts: '1.8M', growth: 32 },
  { tag: '#ContentCreator', posts: '5.2M', growth: 18 },
  { tag: '#ViralVideo', posts: '3.1M', growth: 28 },
  { tag: '#TechTok', posts: '890K', growth: 52 },
]

// Platform card component
function PlatformCard({ platform, isSelected, onSelect }: any) {
  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
    return num.toString()
  }

  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={() => onSelect(platform.id)}
      className={`relative overflow-hidden p-5 rounded-2xl cursor-pointer transition-all ${
        isSelected
          ? 'ring-2 ring-violet-500 bg-white/10'
          : platform.connected
          ? 'bg-white/5 hover:bg-white/10'
          : 'bg-white/[0.02] opacity-60'
      } border border-white/10`}
    >
      {/* Background gradient */}
      <div className={`absolute inset-0 bg-gradient-to-br ${platform.bgGradient} opacity-30`} />

      <div className="relative">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center bg-gradient-to-br ${platform.gradient}`}>
              <span className="text-2xl">{platform.icon}</span>
            </div>
            <div>
              <h3 className="font-semibold">{platform.name}</h3>
              {platform.connected ? (
                <p className="text-xs text-emerald-400 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                  Connected
                </p>
              ) : (
                <p className="text-xs text-white/40">Not connected</p>
              )}
            </div>
          </div>
          {platform.connected && (
            <div className={`flex items-center gap-1 text-xs font-medium ${
              platform.growth >= 0 ? 'text-emerald-400' : 'text-red-400'
            }`}>
              {platform.growth >= 0 ? (
                <TrendingUp className="w-3 h-3" />
              ) : (
                <TrendingDown className="w-3 h-3" />
              )}
              {platform.growth}%
            </div>
          )}
        </div>

        {/* Stats */}
        {platform.connected ? (
          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 rounded-xl bg-white/5">
              <p className="text-lg font-bold">{formatNumber(platform.followers)}</p>
              <p className="text-xs text-white/50">Followers</p>
            </div>
            <div className="p-3 rounded-xl bg-white/5">
              <p className="text-lg font-bold">{platform.engagement}%</p>
              <p className="text-xs text-white/50">Engagement</p>
            </div>
          </div>
        ) : (
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`w-full py-3 rounded-xl font-semibold text-sm bg-gradient-to-r ${platform.gradient}`}
          >
            Connect Account
          </motion.button>
        )}
      </div>
    </motion.div>
  )
}

// Scheduled post card
function ScheduledPostCard({ post }: any) {
  const getPlatformIcon = (id: string) => {
    return platforms.find(p => p.id === id)?.icon || '📱'
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <motion.div
      whileHover={{ scale: 1.01 }}
      className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
    >
      {/* Thumbnail */}
      <div className="w-16 h-16 rounded-xl overflow-hidden bg-gray-800 flex-shrink-0 relative">
        {post.thumbnail ? (
          <img src={post.thumbnail} alt={post.title} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            {post.type === 'video' ? <Video className="w-6 h-6 text-white/40" /> : <Image className="w-6 h-6 text-white/40" />}
          </div>
        )}
        <div className="absolute bottom-1 right-1 w-5 h-5 rounded bg-black/60 flex items-center justify-center">
          {post.type === 'video' ? <Play className="w-3 h-3" /> : <Image className="w-3 h-3" />}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <h4 className="font-medium truncate mb-1">{post.title}</h4>
        <div className="flex items-center gap-2 text-xs text-white/50">
          <Clock className="w-3 h-3" />
          {formatDate(post.scheduledFor)}
        </div>
      </div>

      {/* Platforms */}
      <div className="flex -space-x-2">
        {post.platforms.map((p: string) => (
          <div
            key={p}
            className="w-8 h-8 rounded-full bg-gray-800 border-2 border-gray-900 flex items-center justify-center text-sm"
          >
            {getPlatformIcon(p)}
          </div>
        ))}
      </div>

      {/* Status */}
      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
        post.status === 'scheduled'
          ? 'bg-violet-500/20 text-violet-400'
          : 'bg-amber-500/20 text-amber-400'
      }`}>
        {post.status}
      </span>

      {/* Actions */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        className="p-2 rounded-lg hover:bg-white/10"
      >
        <MoreVertical className="w-4 h-4 text-white/40" />
      </motion.button>
    </motion.div>
  )
}

// Activity item
function ActivityItem({ activity }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors"
    >
      <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-lg">
        {activity.icon}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate">{activity.title}</p>
        <p className="text-xs text-white/40">{activity.time}</p>
      </div>
      <ChevronRight className="w-4 h-4 text-white/20" />
    </motion.div>
  )
}

// Animated counter
function AnimatedCounter({ value, suffix = '' }: { value: number; suffix?: string }) {
  const [displayValue, setDisplayValue] = useState(0)

  useState(() => {
    const duration = 1500
    const steps = 60
    const increment = value / steps
    let current = 0
    const timer = setInterval(() => {
      current += increment
      if (current >= value) {
        setDisplayValue(value)
        clearInterval(timer)
      } else {
        setDisplayValue(Math.floor(current))
      }
    }, duration / steps)
    return () => clearInterval(timer)
  })

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
    return num.toString()
  }

  return <span>{formatNumber(displayValue)}{suffix}</span>
}

export default function SocialHubPage() {
  const [selectedPlatform, setSelectedPlatform] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'overview' | 'schedule' | 'analytics'>('overview')

  const connectedPlatforms = platforms.filter(p => p.connected)
  const totalFollowers = connectedPlatforms.reduce((sum, p) => sum + p.followers, 0)
  const totalViews = connectedPlatforms.reduce((sum, p) => sum + p.views, 0)
  const avgEngagement = connectedPlatforms.reduce((sum, p) => sum + p.engagement, 0) / connectedPlatforms.length

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
    return num.toString()
  }

  return (
    <div className="flex min-h-screen bg-[#0a0a0f]">
      <Sidebar />

      <main className="flex-1 overflow-auto">
        <Header title="Social Hub" subtitle="Manage your social media presence" />

        <div className="p-6 space-y-6">
          {/* Hero Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-violet-600/20 via-fuchsia-600/10 to-cyan-600/20 border border-white/10 p-8"
          >
            {/* Animated background */}
            <div className="absolute inset-0">
              <motion.div
                className="absolute w-96 h-96 rounded-full bg-violet-500/20 blur-3xl"
                animate={{
                  x: [0, 100, 0],
                  y: [0, -50, 0],
                }}
                transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
                style={{ top: '-20%', left: '10%' }}
              />
              <motion.div
                className="absolute w-96 h-96 rounded-full bg-fuchsia-500/20 blur-3xl"
                animate={{
                  x: [0, -80, 0],
                  y: [0, 60, 0],
                }}
                transition={{ duration: 12, repeat: Infinity, ease: 'easeInOut' }}
                style={{ bottom: '-20%', right: '10%' }}
              />
            </div>

            <div className="relative z-10">
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h1 className="text-3xl font-display font-bold mb-2">
                    Social Command Center
                  </h1>
                  <p className="text-white/60">
                    {connectedPlatforms.length} platforms connected • {scheduledPosts.length} posts scheduled
                  </p>
                </div>
                <div className="flex gap-3">
                  <Button variant="secondary" leftIcon={<Calendar className="w-4 h-4" />}>
                    Schedule Post
                  </Button>
                  <Button variant="gradient" leftIcon={<Plus className="w-4 h-4" />}>
                    Create & Publish
                  </Button>
                </div>
              </div>

              {/* Overview Stats */}
              <div className="grid grid-cols-4 gap-4">
                {[
                  { label: 'Total Followers', value: totalFollowers, icon: Users, color: 'violet', growth: '+18%' },
                  { label: 'Total Views', value: totalViews, icon: Eye, color: 'fuchsia', growth: '+24%' },
                  { label: 'Avg. Engagement', value: avgEngagement, icon: Heart, suffix: '%', color: 'cyan', growth: '+12%' },
                  { label: 'Posts This Week', value: 24, icon: Send, color: 'emerald', growth: '+8' },
                ].map((stat, i) => (
                  <motion.div
                    key={stat.label}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 * i }}
                    className="p-5 rounded-2xl bg-white/5 backdrop-blur-sm border border-white/10"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className={`w-10 h-10 rounded-xl bg-${stat.color}-500/20 flex items-center justify-center`}>
                        <stat.icon className={`w-5 h-5 text-${stat.color}-400`} />
                      </div>
                      <span className="text-xs text-emerald-400 font-medium">{stat.growth}</span>
                    </div>
                    <p className="text-2xl font-bold mb-1">
                      {stat.suffix ? stat.value.toFixed(1) + stat.suffix : formatNumber(stat.value)}
                    </p>
                    <p className="text-xs text-white/50">{stat.label}</p>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Platform Cards */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Connected Platforms</h2>
              <Button variant="ghost" size="sm" leftIcon={<Plus className="w-4 h-4" />}>
                Add Platform
              </Button>
            </div>
            <div className="grid md:grid-cols-3 lg:grid-cols-5 gap-4">
              {platforms.map((platform, i) => (
                <motion.div
                  key={platform.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.05 * i }}
                >
                  <PlatformCard
                    platform={platform}
                    isSelected={selectedPlatform === platform.id}
                    onSelect={setSelectedPlatform}
                  />
                </motion.div>
              ))}
            </div>
          </div>

          {/* Main Content Grid */}
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Scheduled Posts */}
            <div className="lg:col-span-2">
              <Card variant="glass">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Calendar className="w-5 h-5 text-violet-400" />
                    Scheduled Posts
                  </CardTitle>
                  <div className="flex gap-2">
                    <Button variant="ghost" size="sm">Today</Button>
                    <Button variant="primary" size="sm">This Week</Button>
                    <Button variant="ghost" size="sm">All</Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {scheduledPosts.map((post, i) => (
                      <motion.div
                        key={post.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.05 * i }}
                      >
                        <ScheduledPostCard post={post} />
                      </motion.div>
                    ))}
                  </div>
                  <motion.button
                    whileHover={{ scale: 1.01 }}
                    className="w-full mt-4 p-4 rounded-xl border-2 border-dashed border-white/10 hover:border-violet-500/30 text-white/50 hover:text-white/80 transition-all flex items-center justify-center gap-2"
                  >
                    <Plus className="w-5 h-5" />
                    Schedule New Post
                  </motion.button>
                </CardContent>
              </Card>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Recent Activity */}
              <Card variant="glass">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Zap className="w-5 h-5 text-amber-400" />
                    Recent Activity
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-1">
                    {recentActivity.map((activity, i) => (
                      <ActivityItem key={i} activity={activity} />
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Trending Hashtags */}
              <Card variant="glass">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Hash className="w-5 h-5 text-cyan-400" />
                    Trending Hashtags
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {trendingHashtags.map((hashtag, i) => (
                      <motion.div
                        key={hashtag.tag}
                        initial={{ opacity: 0, x: 10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.05 * i }}
                        className="flex items-center justify-between p-3 rounded-xl bg-white/5 hover:bg-white/10 cursor-pointer transition-colors"
                      >
                        <div>
                          <p className="font-medium text-cyan-400">{hashtag.tag}</p>
                          <p className="text-xs text-white/40">{hashtag.posts} posts</p>
                        </div>
                        <div className="flex items-center gap-1 text-xs text-emerald-400">
                          <TrendingUp className="w-3 h-3" />
                          +{hashtag.growth}%
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* AI Suggestions */}
              <Card variant="glass" className="bg-gradient-to-br from-violet-500/10 to-fuchsia-500/10">
                <CardContent className="p-5">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-fuchsia-600 flex items-center justify-center">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h4 className="font-semibold">AI Suggestions</h4>
                      <p className="text-xs text-white/50">Optimize your reach</p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="p-3 rounded-xl bg-white/5 text-sm">
                      <p className="text-white/80">🕐 Best time to post on TikTok today:</p>
                      <p className="font-semibold text-violet-400">2:00 PM - 4:00 PM</p>
                    </div>
                    <div className="p-3 rounded-xl bg-white/5 text-sm">
                      <p className="text-white/80">📈 Trending audio you should use:</p>
                      <p className="font-semibold text-fuchsia-400">"Aesthetic Vibes" - 2.4M uses</p>
                    </div>
                  </div>
                  <Button variant="secondary" size="sm" className="w-full mt-4">
                    View All Suggestions
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Performance Chart Placeholder */}
          <Card variant="glass">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-violet-400" />
                Cross-Platform Performance
              </CardTitle>
              <div className="flex gap-2">
                {['7D', '30D', '90D', 'All'].map((period) => (
                  <Button
                    key={period}
                    variant={period === '30D' ? 'primary' : 'ghost'}
                    size="sm"
                  >
                    {period}
                  </Button>
                ))}
              </div>
            </CardHeader>
            <CardContent>
              <div className="h-64 flex items-center justify-center bg-white/5 rounded-xl">
                <div className="text-center">
                  <BarChart3 className="w-12 h-12 text-white/20 mx-auto mb-3" />
                  <p className="text-white/40">Performance chart visualization</p>
                  <p className="text-xs text-white/20">Connect analytics to see real-time data</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
