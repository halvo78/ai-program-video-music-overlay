'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  FolderOpen,
  Grid,
  List,
  Filter,
  Search,
  Download,
  Share2,
  Trash2,
  Play,
  Clock,
  CheckCircle2,
  Video,
  MoreVertical,
  Eye,
  Heart,
  MessageCircle,
  TrendingUp,
  Calendar,
  Upload,
  Plus,
  Sparkles,
  Film,
  Music,
  Image,
  SlidersHorizontal,
  ChevronDown,
  ExternalLink,
  Copy,
  Edit3,
  Star,
  Bookmark,
  BarChart3,
} from 'lucide-react'
import Sidebar from '@/components/layout/Sidebar'
import Header from '@/components/layout/Header'
import Button from '@/components/ui/Button'

const mockVideos = [
  {
    id: '1',
    title: 'Motivational Morning Routine',
    platform: 'tiktok',
    status: 'completed',
    duration: 30,
    createdAt: '2024-01-15T10:30:00',
    thumbnail: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=700&fit=crop',
    views: 124500,
    likes: 8900,
    comments: 234,
    starred: true,
  },
  {
    id: '2',
    title: 'Quick Cooking Tips',
    platform: 'instagram_reels',
    status: 'completed',
    duration: 45,
    createdAt: '2024-01-14T15:20:00',
    thumbnail: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=700&fit=crop',
    views: 89200,
    likes: 5600,
    comments: 178,
    starred: false,
  },
  {
    id: '3',
    title: 'AI Explained Simply',
    platform: 'youtube_shorts',
    status: 'processing',
    duration: 60,
    createdAt: '2024-01-14T09:15:00',
    thumbnail: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=700&fit=crop',
    views: 0,
    likes: 0,
    comments: 0,
    starred: false,
    progress: 67,
  },
  {
    id: '4',
    title: 'Travel Sunset Vibes',
    platform: 'tiktok',
    status: 'completed',
    duration: 30,
    createdAt: '2024-01-13T18:45:00',
    thumbnail: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=700&fit=crop',
    views: 256000,
    likes: 18700,
    comments: 892,
    starred: true,
  },
  {
    id: '5',
    title: 'Fitness Motivation',
    platform: 'instagram_reels',
    status: 'completed',
    duration: 30,
    createdAt: '2024-01-12T07:30:00',
    thumbnail: 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=700&fit=crop',
    views: 67800,
    likes: 4200,
    comments: 156,
    starred: false,
  },
  {
    id: '6',
    title: 'Product Showcase',
    platform: 'twitter',
    status: 'error',
    duration: 45,
    createdAt: '2024-01-11T14:00:00',
    thumbnail: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=700&fit=crop',
    views: 0,
    likes: 0,
    comments: 0,
    starred: false,
    errorMessage: 'Export failed: Invalid format',
  },
  {
    id: '7',
    title: 'Tech Review Highlights',
    platform: 'youtube_shorts',
    status: 'completed',
    duration: 58,
    createdAt: '2024-01-10T11:20:00',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=400&h=700&fit=crop',
    views: 189000,
    likes: 12400,
    comments: 567,
    starred: true,
  },
  {
    id: '8',
    title: 'Dance Challenge',
    platform: 'tiktok',
    status: 'completed',
    duration: 15,
    createdAt: '2024-01-09T16:45:00',
    thumbnail: 'https://images.unsplash.com/photo-1547153760-18fc86324498?w=400&h=700&fit=crop',
    views: 892000,
    likes: 67800,
    comments: 2340,
    starred: true,
  },
]

const platformConfig: Record<string, { gradient: string; name: string; icon: string }> = {
  tiktok: { gradient: 'from-[#00F2EA] to-[#FF0050]', name: 'TikTok', icon: '🎵' },
  instagram_reels: { gradient: 'from-[#F58529] via-[#DD2A7B] to-[#8134AF]', name: 'Reels', icon: '📸' },
  youtube_shorts: { gradient: 'from-[#FF0000] to-[#CC0000]', name: 'Shorts', icon: '▶️' },
  twitter: { gradient: 'from-[#1DA1F2] to-[#0D8BD9]', name: 'X/Twitter', icon: '𝕏' },
}

// Video Card Component
function VideoCard({ video, onPlay, onDelete }: any) {
  const [isHovered, setIsHovered] = useState(false)
  const platform = platformConfig[video.platform]

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
    return num.toString()
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className="relative group rounded-2xl overflow-hidden bg-gray-900/50 border border-white/10 hover:border-white/20 transition-all"
    >
      {/* Thumbnail */}
      <div className="relative aspect-[9/16] overflow-hidden">
        <img
          src={video.thumbnail}
          alt={video.title}
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        />

        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />

        {/* Top badges */}
        <div className="absolute top-3 left-3 right-3 flex items-center justify-between">
          <div className={`px-2.5 py-1 rounded-lg text-xs font-semibold text-white bg-gradient-to-r ${platform.gradient} shadow-lg`}>
            {platform.name}
          </div>

          {video.starred && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="w-8 h-8 rounded-full bg-amber-500/20 backdrop-blur-sm flex items-center justify-center"
            >
              <Star className="w-4 h-4 text-amber-400" fill="currentColor" />
            </motion.div>
          )}
        </div>

        {/* Status badge */}
        <div className="absolute top-3 right-3">
          {video.status === 'processing' && (
            <div className="px-2.5 py-1 rounded-lg bg-blue-500/20 backdrop-blur-sm text-blue-400 text-xs font-medium flex items-center gap-1.5">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              >
                <Clock className="w-3 h-3" />
              </motion.div>
              {video.progress}%
            </div>
          )}
          {video.status === 'error' && (
            <div className="px-2.5 py-1 rounded-lg bg-red-500/20 backdrop-blur-sm text-red-400 text-xs font-medium">
              Error
            </div>
          )}
        </div>

        {/* Duration badge */}
        <div className="absolute bottom-3 right-3 px-2 py-1 rounded-lg bg-black/60 backdrop-blur-sm text-xs font-mono text-white">
          0:{video.duration.toString().padStart(2, '0')}
        </div>

        {/* Play button overlay */}
        <AnimatePresence>
          {isHovered && video.status === 'completed' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm"
            >
              <motion.button
                initial={{ scale: 0.5 }}
                animate={{ scale: 1 }}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => onPlay?.(video)}
                className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-md border border-white/30 flex items-center justify-center shadow-2xl"
              >
                <Play className="w-7 h-7 text-white ml-1" fill="white" />
              </motion.button>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Processing overlay */}
        {video.status === 'processing' && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/50">
            <div className="text-center">
              <div className="relative w-20 h-20 mx-auto mb-3">
                <svg className="w-full h-full -rotate-90">
                  <circle
                    cx="40"
                    cy="40"
                    r="36"
                    fill="none"
                    stroke="rgba(255,255,255,0.1)"
                    strokeWidth="4"
                  />
                  <motion.circle
                    cx="40"
                    cy="40"
                    r="36"
                    fill="none"
                    stroke="url(#gradient)"
                    strokeWidth="4"
                    strokeLinecap="round"
                    strokeDasharray={226}
                    strokeDashoffset={226 - (226 * video.progress) / 100}
                    initial={{ strokeDashoffset: 226 }}
                    animate={{ strokeDashoffset: 226 - (226 * video.progress) / 100 }}
                  />
                  <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#8B5CF6" />
                      <stop offset="100%" stopColor="#EC4899" />
                    </linearGradient>
                  </defs>
                </svg>
                <span className="absolute inset-0 flex items-center justify-center text-lg font-bold">
                  {video.progress}%
                </span>
              </div>
              <p className="text-sm text-white/70">Processing...</p>
            </div>
          </div>
        )}
      </div>

      {/* Info section */}
      <div className="p-4">
        <h3 className="font-semibold text-sm mb-2 truncate group-hover:text-primary transition-colors">
          {video.title}
        </h3>

        {/* Stats */}
        {video.status === 'completed' && (
          <div className="flex items-center gap-4 text-xs text-white/50 mb-3">
            <span className="flex items-center gap-1">
              <Eye className="w-3.5 h-3.5" />
              {formatNumber(video.views)}
            </span>
            <span className="flex items-center gap-1">
              <Heart className="w-3.5 h-3.5" />
              {formatNumber(video.likes)}
            </span>
            <span className="flex items-center gap-1">
              <MessageCircle className="w-3.5 h-3.5" />
              {formatNumber(video.comments)}
            </span>
          </div>
        )}

        {/* Date & Actions */}
        <div className="flex items-center justify-between">
          <span className="text-xs text-white/40 flex items-center gap-1">
            <Calendar className="w-3 h-3" />
            {formatDate(video.createdAt)}
          </span>

          <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="p-1.5 rounded-lg hover:bg-white/10 transition-colors"
            >
              <Download className="w-4 h-4 text-white/60" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="p-1.5 rounded-lg hover:bg-white/10 transition-colors"
            >
              <Share2 className="w-4 h-4 text-white/60" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="p-1.5 rounded-lg hover:bg-white/10 transition-colors"
            >
              <Edit3 className="w-4 h-4 text-white/60" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => onDelete?.(video)}
              className="p-1.5 rounded-lg hover:bg-red-500/20 transition-colors"
            >
              <Trash2 className="w-4 h-4 text-red-400" />
            </motion.button>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

// Stats Card
function StatsCard({ icon: Icon, label, value, change, color, delay }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="p-5 rounded-2xl bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10"
    >
      <div className="flex items-center justify-between mb-3">
        <div
          className="w-10 h-10 rounded-xl flex items-center justify-center"
          style={{ backgroundColor: `${color}20` }}
        >
          <Icon className="w-5 h-5" style={{ color }} />
        </div>
        {change && (
          <span className={`text-xs font-medium px-2 py-1 rounded-full ${
            change.startsWith('+') ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'
          }`}>
            {change}
          </span>
        )}
      </div>
      <p className="text-2xl font-bold mb-1">{value}</p>
      <p className="text-sm text-white/50">{label}</p>
    </motion.div>
  )
}

export default function GalleryPage() {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [filter, setFilter] = useState('all')
  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState('newest')

  const filteredVideos = mockVideos.filter(video => {
    if (filter !== 'all' && video.status !== filter) return false
    if (search && !video.title.toLowerCase().includes(search.toLowerCase())) return false
    return true
  }).sort((a, b) => {
    if (sortBy === 'newest') return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    if (sortBy === 'views') return (b.views || 0) - (a.views || 0)
    if (sortBy === 'likes') return (b.likes || 0) - (a.likes || 0)
    return 0
  })

  const totalViews = mockVideos.reduce((sum, v) => sum + (v.views || 0), 0)
  const totalLikes = mockVideos.reduce((sum, v) => sum + (v.likes || 0), 0)
  const completedVideos = mockVideos.filter(v => v.status === 'completed').length

  return (
    <div className="flex min-h-screen bg-[#0a0a0f]">
      <Sidebar />

      <main className="flex-1 overflow-auto">
        <Header title="Gallery" subtitle="Your generated videos and assets" />

        <div className="p-6 space-y-6">
          {/* Hero Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-fuchsia-500/10 via-violet-500/5 to-cyan-500/10 border border-white/10 p-8"
          >
            {/* Background effects */}
            <div className="absolute inset-0">
              <div className="absolute top-0 left-1/4 w-96 h-96 bg-fuchsia-500/20 rounded-full blur-3xl" />
              <div className="absolute bottom-0 right-1/4 w-64 h-64 bg-cyan-500/20 rounded-full blur-3xl" />
            </div>

            <div className="relative grid grid-cols-2 md:grid-cols-4 gap-6">
              <StatsCard icon={Video} label="Total Videos" value={mockVideos.length} change="+12%" color="#8B5CF6" delay={0} />
              <StatsCard icon={Eye} label="Total Views" value={`${(totalViews / 1000000).toFixed(1)}M`} change="+24%" color="#06B6D4" delay={0.05} />
              <StatsCard icon={Heart} label="Total Likes" value={`${(totalLikes / 1000).toFixed(0)}K`} change="+18%" color="#EC4899" delay={0.1} />
              <StatsCard icon={CheckCircle2} label="Completed" value={completedVideos} color="#10B981" delay={0.15} />
            </div>
          </motion.div>

          {/* Toolbar */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="flex flex-col lg:flex-row gap-4 items-center justify-between p-4 rounded-2xl bg-white/5 border border-white/10"
          >
            <div className="flex items-center gap-4 flex-wrap">
              {/* View toggle */}
              <div className="flex items-center gap-1 p-1 rounded-xl bg-white/5">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setViewMode('grid')}
                  className={`p-2.5 rounded-lg transition-all ${viewMode === 'grid' ? 'bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white' : 'text-white/50 hover:text-white'}`}
                >
                  <Grid className="w-4 h-4" />
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setViewMode('list')}
                  className={`p-2.5 rounded-lg transition-all ${viewMode === 'list' ? 'bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white' : 'text-white/50 hover:text-white'}`}
                >
                  <List className="w-4 h-4" />
                </motion.button>
              </div>

              {/* Status filter */}
              <div className="flex gap-1 p-1 rounded-xl bg-white/5">
                {[
                  { key: 'all', label: 'All' },
                  { key: 'completed', label: 'Completed' },
                  { key: 'processing', label: 'Processing' },
                  { key: 'error', label: 'Error' },
                ].map((status) => (
                  <motion.button
                    key={status.key}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => setFilter(status.key)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      filter === status.key
                        ? 'bg-white/10 text-white'
                        : 'text-white/50 hover:text-white'
                    }`}
                  >
                    {status.label}
                  </motion.button>
                ))}
              </div>
            </div>

            <div className="flex items-center gap-3">
              {/* Sort dropdown */}
              <div className="relative">
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="appearance-none px-4 py-2.5 pr-10 bg-white/5 border border-white/10 rounded-xl text-sm focus:outline-none focus:border-violet-500/50 cursor-pointer"
                >
                  <option value="newest">Newest First</option>
                  <option value="views">Most Views</option>
                  <option value="likes">Most Likes</option>
                </select>
                <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40 pointer-events-none" />
              </div>

              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/30" />
                <input
                  type="text"
                  placeholder="Search videos..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="pl-10 pr-4 py-2.5 w-64 bg-white/5 border border-white/10 rounded-xl text-sm placeholder:text-white/30 focus:outline-none focus:border-violet-500/50 transition-colors"
                />
              </div>

              {/* Upload button */}
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-5 py-2.5 bg-gradient-to-r from-violet-600 to-fuchsia-600 rounded-xl text-sm font-semibold flex items-center gap-2 shadow-lg shadow-violet-500/25"
              >
                <Upload className="w-4 h-4" />
                Upload
              </motion.button>
            </div>
          </motion.div>

          {/* Video Grid */}
          <AnimatePresence mode="popLayout">
            {viewMode === 'grid' ? (
              <motion.div
                layout
                className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"
              >
                {filteredVideos.map((video, i) => (
                  <motion.div
                    key={video.id}
                    layout
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    transition={{ delay: 0.03 * i }}
                  >
                    <VideoCard video={video} />
                  </motion.div>
                ))}
              </motion.div>
            ) : (
              <motion.div
                layout
                className="rounded-2xl overflow-hidden border border-white/10 bg-white/5"
              >
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-white/10 bg-white/5">
                      <th className="text-left p-4 text-xs font-semibold text-white/60 uppercase tracking-wider">Video</th>
                      <th className="text-left p-4 text-xs font-semibold text-white/60 uppercase tracking-wider">Platform</th>
                      <th className="text-left p-4 text-xs font-semibold text-white/60 uppercase tracking-wider">Status</th>
                      <th className="text-left p-4 text-xs font-semibold text-white/60 uppercase tracking-wider">Views</th>
                      <th className="text-left p-4 text-xs font-semibold text-white/60 uppercase tracking-wider">Engagement</th>
                      <th className="text-left p-4 text-xs font-semibold text-white/60 uppercase tracking-wider">Created</th>
                      <th className="text-right p-4 text-xs font-semibold text-white/60 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredVideos.map((video, i) => {
                      const platform = platformConfig[video.platform]
                      return (
                        <motion.tr
                          key={video.id}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: 0.03 * i }}
                          className="border-b border-white/5 hover:bg-white/5 transition-colors group"
                        >
                          <td className="p-4">
                            <div className="flex items-center gap-4">
                              <div className="w-16 h-24 rounded-xl overflow-hidden bg-gray-800 flex-shrink-0">
                                <img src={video.thumbnail} alt="" className="w-full h-full object-cover" />
                              </div>
                              <div>
                                <p className="font-medium mb-1">{video.title}</p>
                                <p className="text-xs text-white/40">0:{video.duration.toString().padStart(2, '0')}</p>
                              </div>
                            </div>
                          </td>
                          <td className="p-4">
                            <span className={`px-3 py-1.5 rounded-lg text-xs font-semibold text-white bg-gradient-to-r ${platform.gradient}`}>
                              {platform.name}
                            </span>
                          </td>
                          <td className="p-4">
                            <span className={`px-3 py-1.5 rounded-lg text-xs font-medium ${
                              video.status === 'completed' ? 'bg-emerald-500/20 text-emerald-400' :
                              video.status === 'processing' ? 'bg-blue-500/20 text-blue-400' :
                              'bg-red-500/20 text-red-400'
                            }`}>
                              {video.status === 'processing' ? `${video.progress}%` : video.status}
                            </span>
                          </td>
                          <td className="p-4">
                            <span className="font-medium">
                              {video.views >= 1000 ? `${(video.views / 1000).toFixed(1)}K` : video.views}
                            </span>
                          </td>
                          <td className="p-4">
                            <div className="flex items-center gap-4 text-sm text-white/60">
                              <span className="flex items-center gap-1">
                                <Heart className="w-4 h-4" />
                                {video.likes >= 1000 ? `${(video.likes / 1000).toFixed(1)}K` : video.likes}
                              </span>
                              <span className="flex items-center gap-1">
                                <MessageCircle className="w-4 h-4" />
                                {video.comments}
                              </span>
                            </div>
                          </td>
                          <td className="p-4 text-white/50">
                            {new Date(video.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                          </td>
                          <td className="p-4">
                            <div className="flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                              <motion.button whileHover={{ scale: 1.1 }} className="p-2 rounded-lg hover:bg-white/10">
                                <Play className="w-4 h-4" />
                              </motion.button>
                              <motion.button whileHover={{ scale: 1.1 }} className="p-2 rounded-lg hover:bg-white/10">
                                <Download className="w-4 h-4" />
                              </motion.button>
                              <motion.button whileHover={{ scale: 1.1 }} className="p-2 rounded-lg hover:bg-white/10">
                                <Share2 className="w-4 h-4" />
                              </motion.button>
                              <motion.button whileHover={{ scale: 1.1 }} className="p-2 rounded-lg hover:bg-red-500/20">
                                <Trash2 className="w-4 h-4 text-red-400" />
                              </motion.button>
                            </div>
                          </td>
                        </motion.tr>
                      )
                    })}
                  </tbody>
                </table>
              </motion.div>
            )}
          </AnimatePresence>

          {filteredVideos.length === 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center py-16"
            >
              <div className="w-20 h-20 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4">
                <FolderOpen className="w-10 h-10 text-white/30" />
              </div>
              <p className="text-white/50 text-lg">No videos found</p>
              <p className="text-white/30 text-sm mt-1">Try adjusting your search or filter criteria</p>
            </motion.div>
          )}
        </div>
      </main>
    </div>
  )
}
