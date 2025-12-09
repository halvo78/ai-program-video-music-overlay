'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Eye,
  Heart,
  MessageCircle,
  Share2,
  Clock,
  Video,
  Music,
  Image,
  Users,
  Calendar,
  ArrowUpRight,
  ArrowDownRight,
  Globe,
  Sparkles,
  Target,
  Zap,
  Activity,
  PieChart,
  LineChart,
  AreaChart,
  ChevronRight,
  Download,
  Filter,
  RefreshCw,
} from 'lucide-react'
import Sidebar from '@/components/layout/Sidebar'
import Header from '@/components/layout/Header'
import Button from '@/components/ui/Button'

// Mini chart component for sparklines
function MiniChart({ data, color, trend }: { data: number[]; color: string; trend: 'up' | 'down' }) {
  const max = Math.max(...data)
  const min = Math.min(...data)
  const range = max - min || 1

  return (
    <div className="flex items-end gap-0.5 h-8">
      {data.map((value, i) => (
        <motion.div
          key={i}
          initial={{ height: 0 }}
          animate={{ height: `${((value - min) / range) * 100}%` }}
          transition={{ delay: i * 0.05, duration: 0.3 }}
          className="flex-1 rounded-sm min-h-[2px]"
          style={{
            backgroundColor: color,
            opacity: 0.3 + (i / data.length) * 0.7
          }}
        />
      ))}
    </div>
  )
}

// Animated counter component
function AnimatedNumber({ value, suffix = '', prefix = '' }: { value: number; suffix?: string; prefix?: string }) {
  return (
    <motion.span
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      {prefix}{value.toLocaleString()}{suffix}
    </motion.span>
  )
}

// Stats card with enhanced visuals
function StatsCard({ icon: Icon, label, value, change, trend, color, chartData, delay }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      whileHover={{ y: -2, scale: 1.01 }}
      className="relative overflow-hidden rounded-2xl p-5 bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 group"
    >
      {/* Background glow */}
      <div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-xl"
        style={{ background: `radial-gradient(circle at center, ${color}15, transparent 70%)` }}
      />

      <div className="relative">
        <div className="flex items-start justify-between mb-4">
          <div
            className="w-12 h-12 rounded-xl flex items-center justify-center"
            style={{ backgroundColor: `${color}15` }}
          >
            <Icon className="w-6 h-6" style={{ color }} />
          </div>
          <div className={`flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold ${
            trend === 'up' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'
          }`}>
            {trend === 'up' ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
            {change}
          </div>
        </div>

        <p className="text-3xl font-bold mb-1">{value}</p>
        <p className="text-sm text-white/50 mb-3">{label}</p>

        {chartData && (
          <MiniChart data={chartData} color={color} trend={trend} />
        )}
      </div>
    </motion.div>
  )
}

// Platform card with visual bar
function PlatformCard({ platform, views, growth, color, icon, maxViews, delay }: any) {
  const percentage = (views / maxViews) * 100

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay }}
      whileHover={{ scale: 1.01 }}
      className="p-4 rounded-2xl bg-white/5 border border-white/10 hover:border-white/20 transition-all"
    >
      <div className="flex items-center gap-4 mb-3">
        <div
          className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
          style={{ background: `linear-gradient(135deg, ${color.split(' ')[0].replace('from-[', '').replace(']', '')}30, ${color.split(' ').pop()?.replace('to-[', '').replace(']', '')}30)` }}
        >
          {icon}
        </div>
        <div className="flex-1">
          <p className="font-semibold">{platform}</p>
          <p className="text-sm text-white/50">{(views / 1000000).toFixed(1)}M views</p>
        </div>
        <div className="text-right">
          <span className="text-emerald-400 text-sm font-semibold flex items-center gap-1">
            <ArrowUpRight className="w-4 h-4" />
            +{growth}%
          </span>
        </div>
      </div>

      <div className="h-2 bg-white/10 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, delay: delay + 0.2 }}
          className={`h-full rounded-full bg-gradient-to-r ${color}`}
        />
      </div>
    </motion.div>
  )
}

// Video performance row
function VideoRow({ rank, title, views, engagement, platform, thumbnail, delay }: any) {
  const platformColors: Record<string, string> = {
    tiktok: 'from-[#00F2EA] to-[#FF0050]',
    instagram_reels: 'from-[#F58529] to-[#8134AF]',
    youtube_shorts: 'from-[#FF0000] to-[#CC0000]',
    twitter: 'from-[#1DA1F2] to-[#0D8BD9]',
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay }}
      whileHover={{ scale: 1.01, x: 4 }}
      className="flex items-center gap-4 p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-all cursor-pointer group"
    >
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold ${
        rank <= 3 ? 'bg-gradient-to-br from-amber-500 to-orange-600 text-white' : 'bg-white/10 text-white/60'
      }`}>
        {rank}
      </div>

      <div className="w-14 h-20 rounded-lg overflow-hidden bg-gray-800 flex-shrink-0">
        <img src={thumbnail} alt="" className="w-full h-full object-cover" />
      </div>

      <div className="flex-1 min-w-0">
        <p className="font-medium truncate group-hover:text-primary transition-colors">{title}</p>
        <span className={`inline-block px-2 py-0.5 mt-1 rounded text-[10px] font-semibold text-white bg-gradient-to-r ${platformColors[platform]}`}>
          {platform.replace('_', ' ').toUpperCase()}
        </span>
      </div>

      <div className="text-right">
        <p className="font-bold text-lg">{(views / 1000).toFixed(0)}K</p>
        <p className="text-xs text-emerald-400">{engagement}% eng</p>
      </div>

      <ChevronRight className="w-5 h-5 text-white/30 group-hover:text-white/60 transition-colors" />
    </motion.div>
  )
}

const overviewStats = [
  {
    label: 'Total Views',
    value: '2.4M',
    change: '+24%',
    trend: 'up',
    icon: Eye,
    color: '#8B5CF6',
    chartData: [30, 45, 35, 50, 49, 60, 70, 65, 80, 75, 90, 100]
  },
  {
    label: 'Engagement Rate',
    value: '8.7%',
    change: '+12%',
    trend: 'up',
    icon: Heart,
    color: '#EC4899',
    chartData: [20, 35, 40, 45, 50, 48, 55, 60, 58, 65, 70, 75]
  },
  {
    label: 'Avg. Watch Time',
    value: '24s',
    change: '-3%',
    trend: 'down',
    icon: Clock,
    color: '#06B6D4',
    chartData: [50, 48, 45, 47, 44, 42, 45, 43, 40, 42, 38, 36]
  },
  {
    label: 'Total Shares',
    value: '12.4K',
    change: '+18%',
    trend: 'up',
    icon: Share2,
    color: '#10B981',
    chartData: [15, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80]
  },
]

const contentStats = [
  { label: 'Videos Created', value: 147, icon: Video, color: '#8B5CF6', change: '+12' },
  { label: 'Music Tracks', value: 89, icon: Music, color: '#EC4899', change: '+8' },
  { label: 'Images Generated', value: 423, icon: Image, color: '#06B6D4', change: '+34' },
  { label: 'Total Audience', value: '45.2K', icon: Users, color: '#10B981', change: '+2.1K' },
]

const topVideos = [
  { title: 'Morning Motivation Tips', views: 124000, engagement: 8.9, platform: 'tiktok', thumbnail: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=100&h=150&fit=crop' },
  { title: 'Quick Cooking Hacks', views: 89000, engagement: 7.2, platform: 'instagram_reels', thumbnail: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=100&h=150&fit=crop' },
  { title: 'AI Explained in 60s', views: 67000, engagement: 9.1, platform: 'youtube_shorts', thumbnail: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=100&h=150&fit=crop' },
  { title: 'Sunset Vibes Compilation', views: 54000, engagement: 6.8, platform: 'tiktok', thumbnail: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=150&fit=crop' },
  { title: 'Productivity Tips', views: 43000, engagement: 7.5, platform: 'twitter', thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=100&h=150&fit=crop' },
]

const platformPerformance = [
  { platform: 'TikTok', views: 1200000, growth: 28, color: 'from-[#00F2EA] to-[#FF0050]', icon: '🎵' },
  { platform: 'Instagram Reels', views: 680000, growth: 15, color: 'from-[#F58529] to-[#8134AF]', icon: '📸' },
  { platform: 'YouTube Shorts', views: 420000, growth: 22, color: 'from-[#FF0000] to-[#CC0000]', icon: '▶️' },
  { platform: 'Twitter/X', views: 100000, growth: 8, color: 'from-[#1DA1F2] to-[#0D8BD9]', icon: '𝕏' },
]

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState('30D')

  const maxViews = Math.max(...platformPerformance.map(p => p.views))

  return (
    <div className="flex min-h-screen bg-[#0a0a0f]">
      <Sidebar />

      <main className="flex-1 overflow-auto">
        <Header title="Analytics" subtitle="Track your content performance" />

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

            <div className="relative flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 rounded-2xl bg-gradient-to-br from-violet-500 to-fuchsia-600 shadow-lg shadow-violet-500/30">
                    <BarChart3 className="w-8 h-8 text-white" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold">Performance Overview</h2>
                    <p className="text-white/60">Your content is performing great!</p>
                  </div>
                </div>

                <div className="flex items-center gap-6 text-sm">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse" />
                    <span className="text-white/70">Live tracking enabled</span>
                  </div>
                  <div className="text-white/50">
                    Last updated: Just now
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                {/* Time range selector */}
                <div className="flex gap-1 p-1 rounded-xl bg-white/5">
                  {['7D', '30D', '90D', 'ALL'].map((range) => (
                    <motion.button
                      key={range}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setTimeRange(range)}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        timeRange === range
                          ? 'bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white shadow-lg'
                          : 'text-white/60 hover:text-white'
                      }`}
                    >
                      {range}
                    </motion.button>
                  ))}
                </div>

                <motion.button
                  whileHover={{ scale: 1.05, rotate: 180 }}
                  whileTap={{ scale: 0.95 }}
                  className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
                >
                  <RefreshCw className="w-5 h-5 text-white/60" />
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="px-5 py-2.5 bg-white/10 hover:bg-white/15 rounded-xl font-medium flex items-center gap-2 transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Export
                </motion.button>
              </div>
            </div>
          </motion.div>

          {/* Overview Stats */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {overviewStats.map((stat, i) => (
              <StatsCard key={stat.label} {...stat} delay={0.05 * i} />
            ))}
          </div>

          {/* Content Stats */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {contentStats.map((stat, i) => {
              const Icon = stat.icon
              return (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 + 0.05 * i }}
                  whileHover={{ y: -2 }}
                  className="p-4 rounded-2xl bg-white/5 border border-white/10 hover:border-white/20 transition-all"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className="w-12 h-12 rounded-xl flex items-center justify-center"
                      style={{ backgroundColor: `${stat.color}15` }}
                    >
                      <Icon className="w-6 h-6" style={{ color: stat.color }} />
                    </div>
                    <div>
                      <p className="text-2xl font-bold">{stat.value}</p>
                      <p className="text-xs text-white/50">{stat.label}</p>
                    </div>
                    <span className="ml-auto text-xs text-emerald-400 font-medium">
                      {stat.change}
                    </span>
                  </div>
                </motion.div>
              )
            })}
          </div>

          <div className="grid lg:grid-cols-2 gap-6">
            {/* Platform Performance */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="rounded-2xl bg-white/5 border border-white/10 p-6"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-xl bg-violet-500/20">
                    <Globe className="w-5 h-5 text-violet-400" />
                  </div>
                  <h3 className="font-semibold">Platform Performance</h3>
                </div>
                <motion.button
                  whileHover={{ x: 3 }}
                  className="text-sm text-white/50 hover:text-white flex items-center gap-1"
                >
                  View All <ChevronRight className="w-4 h-4" />
                </motion.button>
              </div>

              <div className="space-y-3">
                {platformPerformance.map((platform, i) => (
                  <PlatformCard
                    key={platform.platform}
                    {...platform}
                    maxViews={maxViews}
                    delay={0.35 + 0.05 * i}
                  />
                ))}
              </div>
            </motion.div>

            {/* Top Performing Videos */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="rounded-2xl bg-white/5 border border-white/10 p-6"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-xl bg-fuchsia-500/20">
                    <TrendingUp className="w-5 h-5 text-fuchsia-400" />
                  </div>
                  <h3 className="font-semibold">Top Performing Videos</h3>
                </div>
                <motion.button
                  whileHover={{ x: 3 }}
                  className="text-sm text-white/50 hover:text-white flex items-center gap-1"
                >
                  View All <ChevronRight className="w-4 h-4" />
                </motion.button>
              </div>

              <div className="space-y-2">
                {topVideos.map((video, i) => (
                  <VideoRow
                    key={video.title}
                    rank={i + 1}
                    {...video}
                    delay={0.45 + 0.05 * i}
                  />
                ))}
              </div>
            </motion.div>
          </div>

          {/* Chart Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="rounded-2xl bg-white/5 border border-white/10 p-6"
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-xl bg-cyan-500/20">
                  <AreaChart className="w-5 h-5 text-cyan-400" />
                </div>
                <h3 className="font-semibold">Views Over Time</h3>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-sm">
                  <div className="w-3 h-3 rounded-full bg-violet-500" />
                  <span className="text-white/60">Views</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <div className="w-3 h-3 rounded-full bg-cyan-500" />
                  <span className="text-white/60">Engagement</span>
                </div>
              </div>
            </div>

            {/* Chart visualization */}
            <div className="h-64 relative">
              {/* Grid lines */}
              <div className="absolute inset-0 flex flex-col justify-between">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="border-b border-white/5" />
                ))}
              </div>

              {/* Chart bars */}
              <div className="absolute inset-0 flex items-end justify-between gap-2 pt-4 pb-8">
                {[65, 78, 72, 85, 90, 82, 95, 88, 92, 100, 85, 78, 95, 88, 92, 85, 90, 95, 88, 100, 92, 85, 95, 90, 88, 92, 85, 95, 100, 92].map((value, i) => (
                  <motion.div
                    key={i}
                    initial={{ height: 0 }}
                    animate={{ height: `${value}%` }}
                    transition={{ delay: 0.6 + i * 0.02, duration: 0.5 }}
                    className="flex-1 rounded-t-lg bg-gradient-to-t from-violet-600/80 to-violet-400/80 relative group cursor-pointer"
                  >
                    {/* Hover tooltip */}
                    <div className="absolute -top-10 left-1/2 -translate-x-1/2 px-2 py-1 bg-gray-900 border border-white/10 rounded-lg text-xs opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                      {Math.round(value * 24)}K views
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* X-axis labels */}
              <div className="absolute bottom-0 left-0 right-0 flex justify-between text-xs text-white/40">
                <span>Dec 1</span>
                <span>Dec 8</span>
                <span>Dec 15</span>
                <span>Dec 22</span>
                <span>Dec 30</span>
              </div>
            </div>
          </motion.div>

          {/* AI Insights */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="rounded-2xl bg-gradient-to-br from-violet-500/10 to-fuchsia-500/10 border border-violet-500/20 p-6"
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 rounded-xl bg-violet-500/20">
                <Sparkles className="w-5 h-5 text-violet-400" />
              </div>
              <h3 className="font-semibold">AI Insights</h3>
              <span className="px-2 py-0.5 rounded-full bg-violet-500/20 text-violet-400 text-xs font-medium">
                3 New
              </span>
            </div>

            <div className="grid md:grid-cols-3 gap-4">
              {[
                {
                  title: 'Best Posting Time',
                  value: '6-8 PM EST',
                  description: 'Your audience is most active during evening hours',
                  icon: Clock,
                  color: '#8B5CF6'
                },
                {
                  title: 'Trending Topic',
                  value: 'AI Technology',
                  description: 'Content about AI gets 3x more engagement',
                  icon: TrendingUp,
                  color: '#EC4899'
                },
                {
                  title: 'Recommended Length',
                  value: '15-30 seconds',
                  description: 'Shorter videos perform better on your channels',
                  icon: Video,
                  color: '#06B6D4'
                },
              ].map((insight, i) => (
                <motion.div
                  key={insight.title}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 + i * 0.1 }}
                  className="p-4 rounded-xl bg-white/5 border border-white/10"
                >
                  <div className="flex items-center gap-2 mb-2">
                    <insight.icon className="w-4 h-4" style={{ color: insight.color }} />
                    <span className="text-sm text-white/60">{insight.title}</span>
                  </div>
                  <p className="text-lg font-bold mb-1">{insight.value}</p>
                  <p className="text-xs text-white/40">{insight.description}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  )
}
