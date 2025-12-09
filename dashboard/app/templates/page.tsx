'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Grid,
  List,
  Search,
  Filter,
  Star,
  Play,
  Heart,
  Download,
  Sparkles,
  TrendingUp,
  Clock,
  Users,
  Zap,
  Eye,
  Copy,
  ChevronRight,
  Flame,
  Crown,
  Award,
  Palette,
  Music,
  Film,
  MessageCircle,
  Bookmark,
  Share2,
  LayoutGrid,
  SlidersHorizontal,
  ArrowRight,
} from 'lucide-react'
import Sidebar from '@/components/layout/Sidebar'
import Header from '@/components/layout/Header'
import Button from '@/components/ui/Button'

const categories = [
  { id: 'all', name: 'All Templates', count: 156, icon: LayoutGrid },
  { id: 'trending', name: 'Trending', count: 24, icon: Flame, gradient: 'from-orange-500 to-red-500' },
  { id: 'new', name: 'New', count: 18, icon: Sparkles, gradient: 'from-violet-500 to-fuchsia-500' },
  { id: 'motivation', name: 'Motivation', count: 32, icon: Zap },
  { id: 'education', name: 'Education', count: 28, icon: Award },
  { id: 'lifestyle', name: 'Lifestyle', count: 22, icon: Heart },
  { id: 'business', name: 'Business', count: 16, icon: Crown },
  { id: 'entertainment', name: 'Entertainment', count: 16, icon: Film },
]

const templates = [
  {
    id: '1',
    name: 'Motivational Quote',
    category: 'motivation',
    duration: '15s',
    uses: 124000,
    likes: 8920,
    views: 456000,
    trending: true,
    new: false,
    premium: false,
    preview: 'https://images.unsplash.com/photo-1504805572947-34fad45aed93?w=400&h=700&fit=crop',
    colors: ['#8B5CF6', '#EC4899'],
    author: 'Taj Creative',
    rating: 4.9,
  },
  {
    id: '2',
    name: 'Product Showcase',
    category: 'business',
    duration: '30s',
    uses: 89000,
    likes: 6540,
    views: 234000,
    trending: true,
    new: true,
    premium: true,
    preview: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=700&fit=crop',
    colors: ['#06B6D4', '#10B981'],
    author: 'Pro Templates',
    rating: 4.8,
  },
  {
    id: '3',
    name: 'Tutorial Intro',
    category: 'education',
    duration: '10s',
    uses: 156000,
    likes: 12400,
    views: 567000,
    trending: false,
    new: false,
    premium: false,
    preview: 'https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=400&h=700&fit=crop',
    colors: ['#F59E0B', '#EF4444'],
    author: 'EduCreators',
    rating: 4.7,
  },
  {
    id: '4',
    name: 'Day in My Life',
    category: 'lifestyle',
    duration: '60s',
    uses: 67000,
    likes: 4450,
    views: 189000,
    trending: false,
    new: true,
    premium: false,
    preview: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=700&fit=crop',
    colors: ['#EC4899', '#8B5CF6'],
    author: 'LifeStyle Pro',
    rating: 4.6,
  },
  {
    id: '5',
    name: 'Breaking News',
    category: 'entertainment',
    duration: '20s',
    uses: 45000,
    likes: 3200,
    views: 123000,
    trending: false,
    new: false,
    premium: true,
    preview: 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=700&fit=crop',
    colors: ['#EF4444', '#F59E0B'],
    author: 'NewsRoom',
    rating: 4.5,
  },
  {
    id: '6',
    name: 'Countdown Timer',
    category: 'business',
    duration: '15s',
    uses: 98000,
    likes: 7800,
    views: 345000,
    trending: true,
    new: false,
    premium: false,
    preview: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=400&h=700&fit=crop',
    colors: ['#3B82F6', '#8B5CF6'],
    author: 'TimerPro',
    rating: 4.9,
  },
  {
    id: '7',
    name: 'Recipe Quick',
    category: 'lifestyle',
    duration: '45s',
    uses: 112000,
    likes: 9200,
    views: 456000,
    trending: false,
    new: false,
    premium: false,
    preview: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=700&fit=crop',
    colors: ['#10B981', '#06B6D4'],
    author: 'FoodieVids',
    rating: 4.8,
  },
  {
    id: '8',
    name: 'Fitness Challenge',
    category: 'motivation',
    duration: '30s',
    uses: 76000,
    likes: 5600,
    views: 234000,
    trending: true,
    new: true,
    premium: true,
    preview: 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=700&fit=crop',
    colors: ['#F97316', '#EF4444'],
    author: 'FitPro',
    rating: 4.9,
  },
  {
    id: '9',
    name: 'Travel Vlog',
    category: 'lifestyle',
    duration: '60s',
    uses: 89000,
    likes: 7800,
    views: 345000,
    trending: true,
    new: false,
    premium: false,
    preview: 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=400&h=700&fit=crop',
    colors: ['#0EA5E9', '#6366F1'],
    author: 'Wanderlust',
    rating: 4.7,
  },
  {
    id: '10',
    name: 'Tech Review',
    category: 'education',
    duration: '45s',
    uses: 67000,
    likes: 4500,
    views: 189000,
    trending: false,
    new: true,
    premium: false,
    preview: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=700&fit=crop',
    colors: ['#8B5CF6', '#06B6D4'],
    author: 'TechZone',
    rating: 4.6,
  },
]

// Enhanced Template Card
function TemplateCard({ template, delay }: { template: typeof templates[0]; delay: number }) {
  const [isHovered, setIsHovered] = useState(false)
  const [isLiked, setIsLiked] = useState(false)
  const [isSaved, setIsSaved] = useState(false)

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
    return num.toString()
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ delay, type: 'spring', stiffness: 100 }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="group relative"
    >
      <div className="relative aspect-[9/16] rounded-2xl overflow-hidden bg-gray-900 border border-white/10 hover:border-white/20 transition-all duration-500 shadow-xl hover:shadow-2xl hover:shadow-violet-500/10">
        {/* Background image */}
        <img
          src={template.preview}
          alt={template.name}
          className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        />

        {/* Gradient overlays */}
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/20 to-transparent opacity-80" />
        <div
          className="absolute inset-0 opacity-0 group-hover:opacity-40 transition-opacity duration-500"
          style={{
            background: `linear-gradient(135deg, ${template.colors[0]}40, ${template.colors[1]}40)`,
          }}
        />

        {/* Top badges */}
        <div className="absolute top-3 left-3 right-3 flex items-start justify-between">
          <div className="flex flex-col gap-2">
            {template.trending && (
              <motion.span
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                className="px-2.5 py-1 rounded-lg bg-gradient-to-r from-orange-500 to-red-500 text-[10px] font-bold text-white flex items-center gap-1 shadow-lg"
              >
                <Flame className="w-3 h-3" />
                TRENDING
              </motion.span>
            )}
            {template.new && (
              <motion.span
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.1 }}
                className="px-2.5 py-1 rounded-lg bg-gradient-to-r from-violet-500 to-fuchsia-500 text-[10px] font-bold text-white flex items-center gap-1 shadow-lg"
              >
                <Sparkles className="w-3 h-3" />
                NEW
              </motion.span>
            )}
            {template.premium && (
              <motion.span
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="px-2.5 py-1 rounded-lg bg-gradient-to-r from-amber-500 to-yellow-500 text-[10px] font-bold text-black flex items-center gap-1 shadow-lg"
              >
                <Crown className="w-3 h-3" />
                PRO
              </motion.span>
            )}
          </div>

          {/* Save button */}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={(e) => { e.stopPropagation(); setIsSaved(!isSaved); }}
            className={`w-8 h-8 rounded-full backdrop-blur-md flex items-center justify-center transition-colors ${
              isSaved ? 'bg-violet-500 text-white' : 'bg-black/30 text-white/70 hover:text-white'
            }`}
          >
            <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-current' : ''}`} />
          </motion.button>
        </div>

        {/* Duration badge */}
        <div className="absolute top-3 right-14 px-2.5 py-1 rounded-lg bg-black/50 backdrop-blur-md text-xs font-mono text-white flex items-center gap-1">
          <Clock className="w-3 h-3" />
          {template.duration}
        </div>

        {/* Rating */}
        <div className="absolute bottom-20 left-3 flex items-center gap-1 px-2 py-1 rounded-lg bg-black/50 backdrop-blur-md">
          <Star className="w-3 h-3 text-amber-400 fill-amber-400" />
          <span className="text-xs font-medium">{template.rating}</span>
        </div>

        {/* Hover overlay with actions */}
        <AnimatePresence>
          {isHovered && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center gap-4"
            >
              {/* Play button */}
              <motion.button
                initial={{ scale: 0.5, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.5, opacity: 0 }}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-md border border-white/30 flex items-center justify-center shadow-2xl"
              >
                <Play className="w-7 h-7 text-white ml-1" fill="white" />
              </motion.button>

              {/* Action buttons */}
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                exit={{ y: 20, opacity: 0 }}
                transition={{ delay: 0.1 }}
                className="flex gap-2"
              >
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={(e) => { e.stopPropagation(); setIsLiked(!isLiked); }}
                  className={`px-4 py-2 rounded-xl flex items-center gap-2 text-sm font-medium transition-colors ${
                    isLiked ? 'bg-red-500/20 text-red-400' : 'bg-white/10 text-white hover:bg-white/20'
                  }`}
                >
                  <Heart className={`w-4 h-4 ${isLiked ? 'fill-current' : ''}`} />
                  {formatNumber(template.likes + (isLiked ? 1 : 0))}
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-4 py-2 rounded-xl bg-white/10 text-white hover:bg-white/20 flex items-center gap-2 text-sm font-medium"
                >
                  <Share2 className="w-4 h-4" />
                </motion.button>
              </motion.div>

              {/* Use template button */}
              <motion.button
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                exit={{ y: 20, opacity: 0 }}
                transition={{ delay: 0.2 }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-6 py-3 rounded-xl bg-gradient-to-r from-violet-600 to-fuchsia-600 text-sm font-bold flex items-center gap-2 shadow-lg shadow-violet-500/30"
              >
                <Zap className="w-4 h-4" />
                Use Template
              </motion.button>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Bottom info */}
        <div className="absolute bottom-0 left-0 right-0 p-4">
          <div className="flex items-center justify-between text-xs text-white/70 mb-2">
            <span className="flex items-center gap-1">
              <Users className="w-3 h-3" />
              {formatNumber(template.uses)} uses
            </span>
            <span className="flex items-center gap-1">
              <Eye className="w-3 h-3" />
              {formatNumber(template.views)}
            </span>
          </div>
        </div>
      </div>

      {/* Template info below card */}
      <div className="mt-3 px-1">
        <h3 className="font-semibold text-sm truncate group-hover:text-primary transition-colors">
          {template.name}
        </h3>
        <div className="flex items-center justify-between mt-1">
          <p className="text-xs text-white/50">{template.author}</p>
          <p className="text-xs text-white/40 capitalize">{template.category}</p>
        </div>
      </div>
    </motion.div>
  )
}

// Featured Template Card (larger)
function FeaturedTemplateCard({ template }: { template: typeof templates[0] }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.02 }}
      className="relative h-80 rounded-3xl overflow-hidden group cursor-pointer"
    >
      <img
        src={template.preview}
        alt={template.name}
        className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent" />
      <div
        className="absolute inset-0 opacity-30 group-hover:opacity-50 transition-opacity"
        style={{
          background: `linear-gradient(135deg, ${template.colors[0]}60, ${template.colors[1]}60)`,
        }}
      />

      <div className="absolute inset-0 p-6 flex flex-col justify-between">
        <div className="flex items-start justify-between">
          <div className="flex gap-2">
            {template.trending && (
              <span className="px-3 py-1.5 rounded-xl bg-gradient-to-r from-orange-500 to-red-500 text-xs font-bold text-white flex items-center gap-1.5">
                <Flame className="w-3.5 h-3.5" />
                TRENDING
              </span>
            )}
            {template.premium && (
              <span className="px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-500 to-yellow-500 text-xs font-bold text-black flex items-center gap-1.5">
                <Crown className="w-3.5 h-3.5" />
                PRO
              </span>
            )}
          </div>
          <div className="flex items-center gap-1 px-3 py-1.5 rounded-xl bg-black/50 backdrop-blur-md">
            <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
            <span className="text-sm font-semibold">{template.rating}</span>
          </div>
        </div>

        <div>
          <h3 className="text-2xl font-bold mb-2">{template.name}</h3>
          <p className="text-white/70 text-sm mb-4">by {template.author}</p>
          <div className="flex items-center gap-4 text-sm text-white/60 mb-4">
            <span className="flex items-center gap-1">
              <Users className="w-4 h-4" />
              {(template.uses / 1000).toFixed(0)}K uses
            </span>
            <span className="flex items-center gap-1">
              <Eye className="w-4 h-4" />
              {(template.views / 1000).toFixed(0)}K views
            </span>
            <span className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              {template.duration}
            </span>
          </div>
          <motion.button
            whileHover={{ scale: 1.02, x: 5 }}
            whileTap={{ scale: 0.98 }}
            className="px-6 py-3 rounded-xl bg-white text-black font-bold flex items-center gap-2 group/btn"
          >
            Use Template
            <ArrowRight className="w-4 h-4 transition-transform group-hover/btn:translate-x-1" />
          </motion.button>
        </div>
      </div>
    </motion.div>
  )
}

export default function TemplatesPage() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [search, setSearch] = useState('')

  const filteredTemplates = templates.filter(template => {
    if (selectedCategory !== 'all' && selectedCategory !== 'trending' && selectedCategory !== 'new') {
      if (template.category !== selectedCategory) return false
    }
    if (selectedCategory === 'trending' && !template.trending) return false
    if (selectedCategory === 'new' && !template.new) return false
    if (search && !template.name.toLowerCase().includes(search.toLowerCase())) return false
    return true
  })

  const featuredTemplates = templates.filter(t => t.trending).slice(0, 2)

  return (
    <div className="flex min-h-screen bg-[#0a0a0f]">
      <Sidebar />

      <main className="flex-1 overflow-auto">
        <Header title="Templates" subtitle="Start with a professional template" />

        <div className="p-6 space-y-8">
          {/* Hero Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-violet-500/10 via-fuchsia-500/5 to-cyan-500/10 border border-white/10 p-8"
          >
            {/* Background effects */}
            <div className="absolute inset-0">
              <div className="absolute top-0 right-0 w-96 h-96 bg-violet-500/20 rounded-full blur-3xl" />
              <div className="absolute bottom-0 left-0 w-64 h-64 bg-fuchsia-500/20 rounded-full blur-3xl" />
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
            </div>

            <div className="relative z-10 flex flex-col lg:flex-row items-center gap-8">
              <div className="flex-1">
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex items-center gap-2 mb-4"
                >
                  <span className="px-3 py-1 rounded-full bg-violet-500/20 text-violet-400 text-sm font-medium flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4" />
                    156 Templates Available
                  </span>
                </motion.div>

                <h1 className="text-4xl lg:text-5xl font-bold mb-4">
                  <span className="bg-gradient-to-r from-white via-violet-200 to-white bg-clip-text text-transparent">
                    Professional Templates
                  </span>
                </h1>
                <p className="text-white/60 text-lg mb-6 max-w-lg">
                  Choose from our curated collection of stunning templates designed by experts.
                  Customize them with AI to match your brand perfectly.
                </p>
                <div className="flex flex-wrap gap-3">
                  <motion.button
                    whileHover={{ scale: 1.02, boxShadow: '0 20px 40px rgba(139, 92, 246, 0.3)' }}
                    whileTap={{ scale: 0.98 }}
                    className="px-6 py-3 bg-gradient-to-r from-violet-600 to-fuchsia-600 rounded-xl font-semibold flex items-center gap-2 shadow-lg shadow-violet-500/25"
                  >
                    <Sparkles className="w-5 h-5" />
                    Browse All
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className="px-6 py-3 bg-white/10 hover:bg-white/15 rounded-xl font-semibold flex items-center gap-2 transition-colors"
                  >
                    <Zap className="w-5 h-5" />
                    AI Suggest
                  </motion.button>
                </div>
              </div>

              {/* Featured templates preview */}
              <div className="hidden lg:grid grid-cols-2 gap-4 w-96">
                {featuredTemplates.map((template, i) => (
                  <motion.div
                    key={template.id}
                    initial={{ opacity: 0, y: 20, rotate: i === 0 ? -5 : 5 }}
                    animate={{ opacity: 1, y: 0, rotate: i === 0 ? -3 : 3 }}
                    transition={{ delay: 0.2 + i * 0.1 }}
                    whileHover={{ scale: 1.05, rotate: 0 }}
                    className="aspect-[9/16] rounded-2xl overflow-hidden shadow-2xl"
                  >
                    <img
                      src={template.preview}
                      alt={template.name}
                      className="w-full h-full object-cover"
                    />
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Featured Section */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <Flame className="w-5 h-5 text-orange-500" />
                Featured Templates
              </h2>
              <motion.button
                whileHover={{ x: 5 }}
                className="text-sm text-white/60 hover:text-white flex items-center gap-1"
              >
                View All
                <ChevronRight className="w-4 h-4" />
              </motion.button>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              {featuredTemplates.map((template) => (
                <FeaturedTemplateCard key={template.id} template={template} />
              ))}
            </div>
          </div>

          {/* Category Pills & Filters */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between"
          >
            {/* Categories */}
            <div className="flex flex-wrap gap-2">
              {categories.map((category) => (
                <motion.button
                  key={category.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center gap-2 ${
                    selectedCategory === category.id
                      ? category.gradient
                        ? `bg-gradient-to-r ${category.gradient} text-white shadow-lg`
                        : 'bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white shadow-lg shadow-violet-500/25'
                      : 'bg-white/5 hover:bg-white/10 text-white/60 hover:text-white'
                  }`}
                >
                  {category.icon && <category.icon className="w-4 h-4" />}
                  {category.name}
                  <span className="opacity-70 text-xs">({category.count})</span>
                </motion.button>
              ))}
            </div>

            {/* Search and view toggle */}
            <div className="flex items-center gap-3">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/30" />
                <input
                  type="text"
                  placeholder="Search templates..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="pl-10 pr-4 py-2.5 w-64 bg-white/5 border border-white/10 rounded-xl text-sm placeholder:text-white/30 focus:outline-none focus:border-violet-500/50 transition-colors"
                />
              </div>
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
            </div>
          </motion.div>

          {/* Templates Grid */}
          <AnimatePresence mode="popLayout">
            <motion.div
              layout
              className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4"
            >
              {filteredTemplates.map((template, i) => (
                <TemplateCard key={template.id} template={template} delay={0.03 * i} />
              ))}
            </motion.div>
          </AnimatePresence>

          {filteredTemplates.length === 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center py-16"
            >
              <div className="w-20 h-20 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4">
                <Sparkles className="w-10 h-10 text-white/30" />
              </div>
              <p className="text-white/50 text-lg">No templates found</p>
              <p className="text-white/30 text-sm mt-1">Try adjusting your search or filter criteria</p>
            </motion.div>
          )}
        </div>
      </main>
    </div>
  )
}
