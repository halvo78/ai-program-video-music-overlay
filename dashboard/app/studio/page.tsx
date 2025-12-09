'use client'

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume2,
  VolumeX,
  Maximize,
  Minimize,
  Settings,
  Download,
  Share2,
  Undo,
  Redo,
  Scissors,
  Type,
  Image,
  Music,
  Layers,
  Wand2,
  Sparkles,
  Clock,
  Grid,
  ZoomIn,
  ZoomOut,
  ChevronLeft,
  ChevronRight,
  ChevronDown,
  Plus,
  Trash2,
  Copy,
  Move,
  RotateCcw,
  Save,
  Upload,
  Film,
  Mic,
  Palette,
  SlidersHorizontal,
  Eye,
  EyeOff,
  Lock,
  Unlock,
  Magnet,
  Ratio,
  Monitor,
  Smartphone,
  Square,
  Bot,
  Cpu,
  Zap,
  Sun,
  Moon,
  Droplets,
  Flame,
  Wind,
  Cloud,
  Heart,
  Star,
  MessageCircle,
  Hash,
  AtSign,
  Smile,
  Camera,
  Video,
  Aperture,
  Focus,
  Contrast,
  CircleDot,
  GripVertical,
  MoreHorizontal,
  Check,
  X,
  AlertCircle,
  Info,
  ArrowRight,
  LayoutGrid,
  List,
  Filter,
  Search,
  FolderOpen,
  FileVideo,
  FileAudio,
  FileImage,
  MessageSquare,
  Volume1,
  Rewind,
  FastForward,
} from 'lucide-react'
import Sidebar from '@/components/layout/Sidebar'
import Button from '@/components/ui/Button'

// Enhanced Timeline Track with waveform visualization
function TimelineTrack({
  name,
  icon: Icon,
  color,
  clips,
  locked,
  visible,
  muted,
  onToggleLock,
  onToggleVisible,
  onToggleMute,
  isSelected,
  onSelect,
}: any) {
  return (
    <motion.div
      className={`flex items-stretch border-b border-white/5 transition-colors ${isSelected ? 'bg-white/5' : 'hover:bg-white/[0.02]'}`}
      onClick={onSelect}
    >
      {/* Track header */}
      <div className="w-56 flex-shrink-0 p-2 bg-gray-900/30 border-r border-white/5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <motion.div
              whileHover={{ scale: 1.1 }}
              className="w-8 h-8 rounded-lg flex items-center justify-center cursor-grab active:cursor-grabbing"
              style={{ backgroundColor: `${color}20`, border: `1px solid ${color}40` }}
            >
              <Icon className="w-4 h-4" style={{ color }} />
            </motion.div>
            <div>
              <span className="text-sm font-medium block">{name}</span>
              <span className="text-[10px] text-white/40">{clips.length} clips</span>
            </div>
          </div>
          <div className="flex items-center gap-0.5">
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={(e) => { e.stopPropagation(); onToggleMute?.(); }}
              className={`p-1.5 rounded-lg transition-colors ${muted ? 'bg-red-500/20 text-red-400' : 'hover:bg-white/10'}`}
            >
              {muted ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5" />}
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={(e) => { e.stopPropagation(); onToggleVisible?.(); }}
              className={`p-1.5 rounded-lg transition-colors ${!visible ? 'bg-white/5 text-white/30' : 'hover:bg-white/10'}`}
            >
              {visible ? <Eye className="w-3.5 h-3.5" /> : <EyeOff className="w-3.5 h-3.5" />}
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={(e) => { e.stopPropagation(); onToggleLock?.(); }}
              className={`p-1.5 rounded-lg transition-colors ${locked ? 'bg-amber-500/20 text-amber-400' : 'hover:bg-white/10'}`}
            >
              {locked ? <Lock className="w-3.5 h-3.5" /> : <Unlock className="w-3.5 h-3.5" />}
            </motion.button>
          </div>
        </div>
      </div>

      {/* Track content with clips */}
      <div className="flex-1 relative h-16 bg-gray-900/20">
        {/* Waveform background for audio tracks */}
        {(name === 'Music' || name === 'Voice') && (
          <div className="absolute inset-0 flex items-center opacity-20">
            {[...Array(100)].map((_, i) => (
              <div
                key={i}
                className="flex-1 mx-px rounded-full"
                style={{
                  height: `${Math.random() * 60 + 20}%`,
                  backgroundColor: color,
                }}
              />
            ))}
          </div>
        )}

        {clips.map((clip: any, i: number) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="absolute top-1.5 bottom-1.5 rounded-xl cursor-pointer group overflow-hidden"
            style={{
              left: `${clip.start}%`,
              width: `${clip.duration}%`,
              background: `linear-gradient(135deg, ${color}40, ${color}20)`,
              border: `1px solid ${color}50`,
            }}
            whileHover={{ scale: 1.01, y: -1 }}
          >
            {/* Clip thumbnail strip */}
            {clip.thumbnail && (
              <div className="absolute inset-0 opacity-30">
                <img src={clip.thumbnail} alt="" className="h-full object-cover" />
              </div>
            )}

            {/* Clip info */}
            <div className="relative px-3 py-1.5 flex items-center gap-2">
              <div className="w-5 h-5 rounded bg-black/30 flex items-center justify-center">
                <Icon className="w-3 h-3" style={{ color }} />
              </div>
              <span className="text-xs font-medium truncate">{clip.name}</span>
            </div>

            {/* Resize handles */}
            <div className="absolute left-0 top-0 bottom-0 w-2 cursor-ew-resize opacity-0 group-hover:opacity-100 bg-white/30 rounded-l-xl" />
            <div className="absolute right-0 top-0 bottom-0 w-2 cursor-ew-resize opacity-0 group-hover:opacity-100 bg-white/30 rounded-r-xl" />

            {/* Selection indicator */}
            <motion.div
              className="absolute inset-0 border-2 rounded-xl opacity-0 group-hover:opacity-100 pointer-events-none"
              style={{ borderColor: color }}
            />
          </motion.div>
        ))}
      </div>
    </motion.div>
  )
}

// Enhanced Asset Card with real images
function AssetCard({ name, type, duration, thumbnail, isSelected, onClick }: any) {
  return (
    <motion.div
      whileHover={{ scale: 1.03, y: -2 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={`relative rounded-xl overflow-hidden cursor-pointer group ${
        isSelected ? 'ring-2 ring-primary ring-offset-2 ring-offset-gray-900' : ''
      }`}
      draggable
    >
      {/* Thumbnail */}
      <div className="aspect-video relative overflow-hidden bg-gray-800">
        {thumbnail ? (
          <img src={thumbnail} alt={name} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-gray-800 to-gray-900">
            {type === 'video' && <FileVideo className="w-8 h-8 text-violet-400/50" />}
            {type === 'audio' && <FileAudio className="w-8 h-8 text-cyan-400/50" />}
            {type === 'image' && <FileImage className="w-8 h-8 text-pink-400/50" />}
          </div>
        )}

        {/* Overlay gradient */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

        {/* Duration badge */}
        {duration && (
          <div className="absolute bottom-2 right-2 px-2 py-0.5 bg-black/70 backdrop-blur-sm rounded-md text-[10px] font-mono">
            {duration}
          </div>
        )}

        {/* Play overlay */}
        <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
          <motion.div
            whileHover={{ scale: 1.1 }}
            className="w-10 h-10 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center"
          >
            <Play className="w-4 h-4 text-white ml-0.5" fill="white" />
          </motion.div>
        </div>

        {/* Type indicator */}
        <div className="absolute top-2 left-2">
          <div className={`w-6 h-6 rounded-lg flex items-center justify-center backdrop-blur-sm ${
            type === 'video' ? 'bg-violet-500/30' : type === 'audio' ? 'bg-cyan-500/30' : 'bg-pink-500/30'
          }`}>
            {type === 'video' && <Film className="w-3 h-3 text-violet-300" />}
            {type === 'audio' && <Music className="w-3 h-3 text-cyan-300" />}
            {type === 'image' && <Image className="w-3 h-3 text-pink-300" />}
          </div>
        </div>
      </div>

      {/* Info */}
      <div className="p-2 bg-gray-900/50">
        <p className="text-xs font-medium truncate">{name}</p>
      </div>
    </motion.div>
  )
}

// Effect card with preview
function EffectCard({ name, icon: Icon, gradient, preview, isActive }: any) {
  return (
    <motion.div
      whileHover={{ scale: 1.05, y: -2 }}
      whileTap={{ scale: 0.95 }}
      className={`relative p-3 rounded-xl cursor-pointer overflow-hidden group ${
        isActive ? 'ring-2 ring-primary' : ''
      }`}
    >
      {/* Background gradient */}
      <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-20 group-hover:opacity-40 transition-opacity`} />

      {/* Content */}
      <div className="relative text-center">
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${gradient} flex items-center justify-center mx-auto mb-2 shadow-lg`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <p className="text-xs font-medium">{name}</p>
      </div>

      {/* Active indicator */}
      {isActive && (
        <div className="absolute top-1 right-1 w-2 h-2 rounded-full bg-primary" />
      )}
    </motion.div>
  )
}

// AI Feature card
function AIFeatureCard({ name, icon: Icon, description, gradient, onClick }: any) {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className="relative p-4 rounded-xl cursor-pointer overflow-hidden group border border-white/10 hover:border-white/20 transition-colors"
    >
      <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-10 group-hover:opacity-20 transition-opacity`} />

      <div className="relative flex items-start gap-3">
        <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${gradient} flex items-center justify-center flex-shrink-0`}>
          <Icon className="w-5 h-5 text-white" />
        </div>
        <div>
          <p className="text-sm font-medium mb-0.5">{name}</p>
          <p className="text-xs text-white/50">{description}</p>
        </div>
      </div>

      <motion.div
        className="absolute right-3 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity"
        whileHover={{ x: 3 }}
      >
        <ArrowRight className="w-4 h-4 text-white/50" />
      </motion.div>
    </motion.div>
  )
}

// Property slider with label
function PropertySlider({ label, value, min, max, unit, color, onChange }: any) {
  const percentage = ((value - min) / (max - min)) * 100

  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between">
        <span className="text-xs text-white/60">{label}</span>
        <span className="text-xs font-mono text-white/80">{value}{unit}</span>
      </div>
      <div className="relative h-2 bg-white/10 rounded-full overflow-hidden">
        <motion.div
          className="absolute inset-y-0 left-0 rounded-full"
          style={{
            width: `${percentage}%`,
            background: `linear-gradient(90deg, ${color}80, ${color})`,
          }}
          layoutId={`slider-${label}`}
        />
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
      </div>
    </div>
  )
}

export default function StudioPage() {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(8.5)
  const [duration] = useState(30)
  const [volume, setVolume] = useState(80)
  const [isMuted, setIsMuted] = useState(false)
  const [zoom, setZoom] = useState(100)
  const [activePanel, setActivePanel] = useState<'assets' | 'effects' | 'text' | 'audio' | 'ai'>('assets')
  const [selectedTool, setSelectedTool] = useState<string>('select')
  const [selectedTrack, setSelectedTrack] = useState<number>(0)
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [aspectRatio, setAspectRatio] = useState<'9:16' | '16:9' | '1:1'>('9:16')
  const [showGrid, setShowGrid] = useState(true)

  // Property panel state
  const [brightness, setBrightness] = useState(0)
  const [contrast, setContrast] = useState(0)
  const [saturation, setSaturation] = useState(0)
  const [temperature, setTemperature] = useState(0)
  const [opacity, setOpacity] = useState(100)

  const tracks = [
    {
      name: 'Video',
      icon: Film,
      color: '#8B5CF6',
      clips: [{ name: 'Main Scene', start: 5, duration: 65, thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=200&h=100&fit=crop' }],
      locked: false,
      visible: true,
      muted: false,
    },
    {
      name: 'B-Roll',
      icon: Video,
      color: '#A855F7',
      clips: [
        { name: 'Transition', start: 0, duration: 8, thumbnail: 'https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=200&h=100&fit=crop' },
        { name: 'Outro', start: 70, duration: 30, thumbnail: 'https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=200&h=100&fit=crop' },
      ],
      locked: false,
      visible: true,
      muted: false,
    },
    {
      name: 'Overlay',
      icon: Layers,
      color: '#EC4899',
      clips: [{ name: 'Title Card', start: 10, duration: 25 }],
      locked: false,
      visible: true,
      muted: false,
    },
    {
      name: 'Music',
      icon: Music,
      color: '#06B6D4',
      clips: [{ name: 'Background Beat', start: 0, duration: 100 }],
      locked: false,
      visible: true,
      muted: false,
    },
    {
      name: 'Voice',
      icon: Mic,
      color: '#10B981',
      clips: [{ name: 'Narration', start: 12, duration: 50 }],
      locked: false,
      visible: true,
      muted: false,
    },
    {
      name: 'SFX',
      icon: Volume2,
      color: '#F59E0B',
      clips: [
        { name: 'Whoosh', start: 8, duration: 3 },
        { name: 'Ding', start: 35, duration: 2 },
      ],
      locked: false,
      visible: true,
      muted: false,
    },
  ]

  const assets = [
    { name: 'Hero Shot', type: 'video', duration: '0:15', thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=300&h=200&fit=crop' },
    { name: 'Product Demo', type: 'video', duration: '0:22', thumbnail: 'https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=300&h=200&fit=crop' },
    { name: 'Lifestyle B-Roll', type: 'video', duration: '0:18', thumbnail: 'https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=300&h=200&fit=crop' },
    { name: 'City Timelapse', type: 'video', duration: '0:30', thumbnail: 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=300&h=200&fit=crop' },
    { name: 'Nature Scene', type: 'video', duration: '0:12', thumbnail: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=200&fit=crop' },
    { name: 'Tech Abstract', type: 'video', duration: '0:08', thumbnail: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=300&h=200&fit=crop' },
  ]

  const effects = [
    { name: 'Fade In', icon: Sun, gradient: 'from-amber-500 to-orange-500' },
    { name: 'Fade Out', icon: Moon, gradient: 'from-indigo-500 to-purple-500' },
    { name: 'Zoom In', icon: ZoomIn, gradient: 'from-cyan-500 to-blue-500' },
    { name: 'Zoom Out', icon: ZoomOut, gradient: 'from-teal-500 to-emerald-500' },
    { name: 'Slide Left', icon: ChevronLeft, gradient: 'from-pink-500 to-rose-500' },
    { name: 'Slide Right', icon: ChevronRight, gradient: 'from-violet-500 to-purple-500' },
    { name: 'Blur', icon: Droplets, gradient: 'from-sky-500 to-cyan-500' },
    { name: 'Glow', icon: Sparkles, gradient: 'from-yellow-500 to-amber-500' },
    { name: 'Shake', icon: Wind, gradient: 'from-gray-500 to-slate-500' },
    { name: 'Flash', icon: Zap, gradient: 'from-white to-gray-300' },
    { name: 'Vignette', icon: Aperture, gradient: 'from-gray-700 to-black' },
    { name: 'Film Grain', icon: Grid, gradient: 'from-stone-500 to-stone-700' },
  ]

  const aiFeatures = [
    { name: 'Auto Enhance', icon: Wand2, description: 'AI-powered color and exposure correction', gradient: 'from-violet-500 to-purple-500' },
    { name: 'Background Remove', icon: Scissors, description: 'Remove background with one click', gradient: 'from-pink-500 to-rose-500' },
    { name: 'Smart Crop', icon: Ratio, description: 'Intelligent framing for any aspect ratio', gradient: 'from-cyan-500 to-blue-500' },
    { name: 'Generate Music', icon: Music, description: 'Create custom AI soundtrack', gradient: 'from-emerald-500 to-teal-500' },
    { name: 'Voice Clone', icon: Mic, description: 'Clone and generate voiceovers', gradient: 'from-amber-500 to-orange-500' },
    { name: 'Auto Captions', icon: MessageSquare, description: 'Generate accurate subtitles', gradient: 'from-indigo-500 to-violet-500' },
  ]

  const tools = [
    { id: 'select', icon: Move, name: 'Select', shortcut: 'V' },
    { id: 'cut', icon: Scissors, name: 'Cut', shortcut: 'C' },
    { id: 'text', icon: Type, name: 'Text', shortcut: 'T' },
    { id: 'image', icon: Image, name: 'Image', shortcut: 'I' },
    { id: 'effects', icon: Wand2, name: 'Effects', shortcut: 'E' },
    { id: 'draw', icon: Palette, name: 'Draw', shortcut: 'D' },
  ]

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    const frames = Math.floor((seconds % 1) * 30)
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}:${frames.toString().padStart(2, '0')}`
  }

  // Simulate playback
  useEffect(() => {
    if (isPlaying) {
      const interval = setInterval(() => {
        setCurrentTime(t => t >= duration ? 0 : t + 0.033)
      }, 33)
      return () => clearInterval(interval)
    }
  }, [isPlaying, duration])

  return (
    <div className="flex h-screen bg-[#0a0a0f] overflow-hidden">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        {/* Enhanced Top Toolbar */}
        <div className="h-14 bg-gradient-to-r from-gray-900/95 to-gray-900/90 backdrop-blur-xl border-b border-white/5 flex items-center justify-between px-4">
          <div className="flex items-center gap-1">
            {/* Undo/Redo */}
            <div className="flex items-center mr-2">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 rounded-lg hover:bg-white/10 transition-colors text-white/60 hover:text-white"
              >
                <Undo className="w-4 h-4" />
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 rounded-lg hover:bg-white/10 transition-colors text-white/60 hover:text-white"
              >
                <Redo className="w-4 h-4" />
              </motion.button>
            </div>

            <div className="w-px h-6 bg-white/10" />

            {/* Tools */}
            <div className="flex items-center gap-0.5 ml-2">
              {tools.map((tool) => (
                <motion.button
                  key={tool.id}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setSelectedTool(tool.id)}
                  className={`relative p-2.5 rounded-xl transition-all group ${
                    selectedTool === tool.id
                      ? 'bg-primary/20 text-primary shadow-lg shadow-primary/20'
                      : 'hover:bg-white/10 text-white/60 hover:text-white'
                  }`}
                >
                  <tool.icon className="w-4 h-4" />
                  {/* Tooltip */}
                  <div className="absolute -bottom-10 left-1/2 -translate-x-1/2 px-2 py-1 bg-gray-900 border border-white/10 rounded-lg text-xs opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50 pointer-events-none">
                    {tool.name}
                    <span className="ml-2 text-white/40">{tool.shortcut}</span>
                  </div>
                </motion.button>
              ))}
            </div>

            <div className="w-px h-6 bg-white/10 mx-2" />

            {/* Snap & Grid toggles */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className={`p-2 rounded-lg transition-colors ${showGrid ? 'bg-white/10 text-white' : 'text-white/40 hover:text-white'}`}
              onClick={() => setShowGrid(!showGrid)}
            >
              <Grid className="w-4 h-4" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 rounded-lg hover:bg-white/10 transition-colors text-white/60 hover:text-white"
            >
              <Magnet className="w-4 h-4" />
            </motion.button>
          </div>

          {/* Center - Time display */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-4 py-2 bg-black/30 rounded-xl border border-white/10">
              <Clock className="w-4 h-4 text-primary" />
              <span className="font-mono text-sm tracking-wider">
                <span className="text-white">{formatTime(currentTime)}</span>
                <span className="text-white/40 mx-1">/</span>
                <span className="text-white/60">{formatTime(duration)}</span>
              </span>
            </div>
          </div>

          {/* Right - Actions */}
          <div className="flex items-center gap-2">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-sm font-medium flex items-center gap-2 transition-colors"
            >
              <Save className="w-4 h-4" />
              Save
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-sm font-medium flex items-center gap-2 transition-colors"
            >
              <Download className="w-4 h-4" />
              Export
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02, boxShadow: '0 10px 30px rgba(139, 92, 246, 0.3)' }}
              whileTap={{ scale: 0.98 }}
              className="px-5 py-2 bg-gradient-to-r from-violet-600 to-fuchsia-600 rounded-xl text-sm font-semibold flex items-center gap-2 shadow-lg shadow-violet-500/20"
            >
              <Share2 className="w-4 h-4" />
              Publish
            </motion.button>
          </div>
        </div>

        {/* Main content area */}
        <div className="flex-1 flex overflow-hidden">
          {/* Left panel - Assets/Effects/AI */}
          <div className="w-72 bg-gradient-to-b from-gray-900/80 to-gray-950/80 backdrop-blur-xl border-r border-white/5 flex flex-col">
            {/* Panel tabs */}
            <div className="flex border-b border-white/5">
              {[
                { id: 'assets', icon: FolderOpen, label: 'Assets' },
                { id: 'effects', icon: Sparkles, label: 'Effects' },
                { id: 'text', icon: Type, label: 'Text' },
                { id: 'ai', icon: Bot, label: 'AI' },
              ].map((tab) => (
                <motion.button
                  key={tab.id}
                  whileHover={{ backgroundColor: 'rgba(255,255,255,0.05)' }}
                  onClick={() => setActivePanel(tab.id as any)}
                  className={`flex-1 py-3.5 text-xs font-medium transition-all relative ${
                    activePanel === tab.id
                      ? 'text-white'
                      : 'text-white/40 hover:text-white/70'
                  }`}
                >
                  <tab.icon className="w-4 h-4 mx-auto mb-1" />
                  {tab.label}
                  {activePanel === tab.id && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute bottom-0 left-2 right-2 h-0.5 bg-gradient-to-r from-violet-500 to-fuchsia-500 rounded-full"
                    />
                  )}
                </motion.button>
              ))}
            </div>

            {/* Search bar */}
            <div className="p-3 border-b border-white/5">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/30" />
                <input
                  type="text"
                  placeholder="Search..."
                  className="w-full pl-10 pr-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-sm placeholder:text-white/30 focus:outline-none focus:border-primary/50 transition-colors"
                />
              </div>
            </div>

            {/* Panel content */}
            <div className="flex-1 overflow-y-auto p-3 space-y-3">
              <AnimatePresence mode="wait">
                {activePanel === 'assets' && (
                  <motion.div
                    key="assets"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="space-y-3"
                  >
                    <Button variant="secondary" size="sm" className="w-full" leftIcon={<Upload className="w-4 h-4" />}>
                      Upload Media
                    </Button>
                    <div className="grid grid-cols-2 gap-2">
                      {assets.map((asset, i) => (
                        <AssetCard key={i} {...asset} />
                      ))}
                    </div>
                  </motion.div>
                )}

                {activePanel === 'effects' && (
                  <motion.div
                    key="effects"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="grid grid-cols-3 gap-2"
                  >
                    {effects.map((effect, i) => (
                      <EffectCard key={i} {...effect} />
                    ))}
                  </motion.div>
                )}

                {activePanel === 'text' && (
                  <motion.div
                    key="text"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="space-y-3"
                  >
                    <Button variant="secondary" size="sm" className="w-full" leftIcon={<Plus className="w-4 h-4" />}>
                      Add Text Layer
                    </Button>
                    <div className="space-y-2">
                      {[
                        { name: 'Bold Title', preview: 'IMPACT', style: 'text-2xl font-black' },
                        { name: 'Elegant Subtitle', preview: 'Serif Style', style: 'text-lg font-serif italic' },
                        { name: 'Modern Caption', preview: 'Clean & Simple', style: 'text-sm font-medium' },
                        { name: 'Lower Third', preview: 'Name | Title', style: 'text-sm tracking-wide' },
                        { name: 'Call to Action', preview: 'CLICK HERE →', style: 'text-base font-bold' },
                      ].map((preset) => (
                        <motion.div
                          key={preset.name}
                          whileHover={{ scale: 1.02, x: 4 }}
                          className="p-4 rounded-xl bg-white/5 hover:bg-white/10 cursor-pointer border border-transparent hover:border-white/10 transition-all"
                        >
                          <p className={`${preset.style} text-white mb-1`}>{preset.preview}</p>
                          <p className="text-xs text-white/40">{preset.name}</p>
                        </motion.div>
                      ))}
                    </div>
                  </motion.div>
                )}

                {activePanel === 'ai' && (
                  <motion.div
                    key="ai"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="space-y-2"
                  >
                    {/* AI Status */}
                    <div className="p-3 rounded-xl bg-gradient-to-r from-violet-500/10 to-fuchsia-500/10 border border-violet-500/20 mb-4">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="relative">
                          <Cpu className="w-5 h-5 text-violet-400" />
                          <span className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-emerald-400 rounded-full" />
                        </div>
                        <span className="text-sm font-medium">AI Engine Active</span>
                      </div>
                      <p className="text-xs text-white/50">3 AI agents ready to assist</p>
                    </div>

                    {aiFeatures.map((feature, i) => (
                      <AIFeatureCard key={i} {...feature} />
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          {/* Center - Preview */}
          <div className="flex-1 flex flex-col bg-[#0d0d12]">
            {/* Preview toolbar */}
            <div className="h-10 flex items-center justify-between px-4 border-b border-white/5">
              <div className="flex items-center gap-2">
                {/* Aspect ratio buttons */}
                {[
                  { ratio: '9:16', icon: Smartphone, label: 'Portrait' },
                  { ratio: '16:9', icon: Monitor, label: 'Landscape' },
                  { ratio: '1:1', icon: Square, label: 'Square' },
                ].map((ar) => (
                  <motion.button
                    key={ar.ratio}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setAspectRatio(ar.ratio as any)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-colors ${
                      aspectRatio === ar.ratio
                        ? 'bg-primary/20 text-primary'
                        : 'text-white/40 hover:text-white hover:bg-white/5'
                    }`}
                  >
                    <ar.icon className="w-3.5 h-3.5" />
                    {ar.ratio}
                  </motion.button>
                ))}
              </div>

              <div className="flex items-center gap-2">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setIsFullscreen(!isFullscreen)}
                  className="p-2 rounded-lg hover:bg-white/10 transition-colors text-white/60 hover:text-white"
                >
                  {isFullscreen ? <Minimize className="w-4 h-4" /> : <Maximize className="w-4 h-4" />}
                </motion.button>
              </div>
            </div>

            {/* Preview area */}
            <div className="flex-1 flex items-center justify-center p-6 bg-[radial-gradient(circle_at_center,#1a1a2e_0%,#0d0d12_100%)]">
              <motion.div
                className={`relative bg-gray-900 rounded-2xl overflow-hidden shadow-2xl shadow-black/50 ${
                  aspectRatio === '9:16' ? 'w-full max-w-sm aspect-[9/16]' :
                  aspectRatio === '16:9' ? 'w-full max-w-3xl aspect-video' :
                  'w-full max-w-md aspect-square'
                }`}
                layoutId="preview"
              >
                {/* Video preview with real image */}
                <img
                  src="https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=800&h=1400&fit=crop"
                  alt="Preview"
                  className="absolute inset-0 w-full h-full object-cover"
                />

                {/* Overlay gradient */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-black/30" />

                {/* Title overlay */}
                <motion.div
                  className="absolute top-12 left-0 right-0 text-center px-6"
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <h2 className="text-3xl font-bold text-white drop-shadow-2xl mb-2">
                    Your Amazing Title
                  </h2>
                  <p className="text-white/80 text-sm">Subtitle goes here</p>
                </motion.div>

                {/* CTA at bottom */}
                <motion.div
                  className="absolute bottom-12 left-0 right-0 text-center"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <div className="inline-flex items-center gap-2 px-6 py-3 bg-white/20 backdrop-blur-md rounded-full border border-white/30">
                    <span className="text-white font-semibold">Swipe Up</span>
                    <ChevronRight className="w-4 h-4 text-white" />
                  </div>
                </motion.div>

                {/* Safe zone guides */}
                {showGrid && (
                  <div className="absolute inset-4 border border-dashed border-white/20 rounded-xl pointer-events-none">
                    <div className="absolute inset-0 grid grid-cols-3 grid-rows-3">
                      {[...Array(9)].map((_, i) => (
                        <div key={i} className="border border-white/5" />
                      ))}
                    </div>
                  </div>
                )}

                {/* Playhead indicator */}
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-white/10">
                  <motion.div
                    className="h-full bg-gradient-to-r from-violet-500 to-fuchsia-500"
                    style={{ width: `${(currentTime / duration) * 100}%` }}
                  />
                </div>
              </motion.div>
            </div>

            {/* Enhanced Playback controls */}
            <div className="h-20 bg-gradient-to-t from-gray-900/95 to-gray-900/80 backdrop-blur-xl border-t border-white/5 flex items-center justify-center gap-6 px-6">
              {/* Skip backward */}
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-xl hover:bg-white/10 transition-colors text-white/60 hover:text-white"
              >
                <Rewind className="w-5 h-5" />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-xl hover:bg-white/10 transition-colors text-white/60 hover:text-white"
              >
                <SkipBack className="w-5 h-5" />
              </motion.button>

              {/* Play button */}
              <motion.button
                whileHover={{ scale: 1.1, boxShadow: '0 0 40px rgba(139, 92, 246, 0.5)' }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setIsPlaying(!isPlaying)}
                className="w-14 h-14 rounded-2xl bg-gradient-to-br from-violet-600 to-fuchsia-600 flex items-center justify-center shadow-xl shadow-violet-500/30"
              >
                {isPlaying ? (
                  <Pause className="w-6 h-6 text-white" />
                ) : (
                  <Play className="w-6 h-6 text-white ml-1" fill="white" />
                )}
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-xl hover:bg-white/10 transition-colors text-white/60 hover:text-white"
              >
                <SkipForward className="w-5 h-5" />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-xl hover:bg-white/10 transition-colors text-white/60 hover:text-white"
              >
                <FastForward className="w-5 h-5" />
              </motion.button>

              <div className="w-px h-8 bg-white/10 mx-2" />

              {/* Volume */}
              <div className="flex items-center gap-3">
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => setIsMuted(!isMuted)}
                  className="p-2 rounded-xl hover:bg-white/10 transition-colors text-white/60 hover:text-white"
                >
                  {isMuted ? <VolumeX className="w-5 h-5" /> : volume > 50 ? <Volume2 className="w-5 h-5" /> : <Volume1 className="w-5 h-5" />}
                </motion.button>
                <div className="w-24 h-1.5 bg-white/10 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-gradient-to-r from-violet-500 to-fuchsia-500 rounded-full"
                    style={{ width: isMuted ? '0%' : `${volume}%` }}
                  />
                </div>
              </div>

              <div className="w-px h-8 bg-white/10 mx-2" />

              {/* Zoom */}
              <div className="flex items-center gap-3">
                <ZoomOut className="w-4 h-4 text-white/40" />
                <div className="w-20 h-1.5 bg-white/10 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-white/40 rounded-full"
                    style={{ width: `${((zoom - 50) / 150) * 100}%` }}
                  />
                </div>
                <ZoomIn className="w-4 h-4 text-white/40" />
                <span className="text-xs text-white/40 w-10 font-mono">{zoom}%</span>
              </div>
            </div>
          </div>

          {/* Right panel - Properties */}
          <div className="w-80 bg-gradient-to-b from-gray-900/80 to-gray-950/80 backdrop-blur-xl border-l border-white/5 overflow-y-auto">
            <div className="p-4 border-b border-white/5">
              <h3 className="text-sm font-semibold flex items-center gap-2">
                <SlidersHorizontal className="w-4 h-4 text-primary" />
                Properties
              </h3>
            </div>

            <div className="p-4 space-y-6">
              {/* Transform */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-xs font-medium text-white/60 uppercase tracking-wider">Transform</h4>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    className="p-1 rounded hover:bg-white/10"
                  >
                    <RotateCcw className="w-3 h-3 text-white/40" />
                  </motion.button>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { label: 'X', value: '0', unit: 'px' },
                    { label: 'Y', value: '0', unit: 'px' },
                    { label: 'W', value: '1080', unit: 'px' },
                    { label: 'H', value: '1920', unit: 'px' },
                    { label: 'Rotation', value: '0', unit: '°' },
                    { label: 'Scale', value: '100', unit: '%' },
                  ].map((prop) => (
                    <div key={prop.label} className="flex items-center gap-2">
                      <span className="text-xs text-white/40 w-10">{prop.label}</span>
                      <div className="flex-1 relative">
                        <input
                          type="text"
                          defaultValue={prop.value}
                          className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-xs font-mono focus:outline-none focus:border-primary/50 transition-colors"
                        />
                        <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-white/30">{prop.unit}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Appearance */}
              <div>
                <h4 className="text-xs font-medium text-white/60 uppercase tracking-wider mb-3">Appearance</h4>
                <div className="space-y-4">
                  <PropertySlider
                    label="Opacity"
                    value={opacity}
                    min={0}
                    max={100}
                    unit="%"
                    color="#8B5CF6"
                    onChange={setOpacity}
                  />
                  <div>
                    <span className="text-xs text-white/60">Blend Mode</span>
                    <select className="w-full mt-1.5 px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-xs focus:outline-none focus:border-primary/50 transition-colors cursor-pointer">
                      <option>Normal</option>
                      <option>Multiply</option>
                      <option>Screen</option>
                      <option>Overlay</option>
                      <option>Soft Light</option>
                      <option>Hard Light</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Color Correction */}
              <div>
                <h4 className="text-xs font-medium text-white/60 uppercase tracking-wider mb-3">Color Correction</h4>
                <div className="space-y-4">
                  <PropertySlider
                    label="Brightness"
                    value={brightness}
                    min={-100}
                    max={100}
                    unit=""
                    color="#F59E0B"
                    onChange={setBrightness}
                  />
                  <PropertySlider
                    label="Contrast"
                    value={contrast}
                    min={-100}
                    max={100}
                    unit=""
                    color="#EC4899"
                    onChange={setContrast}
                  />
                  <PropertySlider
                    label="Saturation"
                    value={saturation}
                    min={-100}
                    max={100}
                    unit=""
                    color="#06B6D4"
                    onChange={setSaturation}
                  />
                  <PropertySlider
                    label="Temperature"
                    value={temperature}
                    min={-100}
                    max={100}
                    unit=""
                    color="#F97316"
                    onChange={setTemperature}
                  />
                </div>
              </div>

              {/* AI Quick Actions */}
              <div>
                <h4 className="text-xs font-medium text-white/60 uppercase tracking-wider mb-3">AI Quick Actions</h4>
                <div className="grid grid-cols-2 gap-2">
                  {[
                    { icon: Wand2, label: 'Auto Fix', gradient: 'from-violet-500 to-purple-500' },
                    { icon: Palette, label: 'Color Grade', gradient: 'from-pink-500 to-rose-500' },
                    { icon: Focus, label: 'Stabilize', gradient: 'from-cyan-500 to-blue-500' },
                    { icon: Sparkles, label: 'Enhance', gradient: 'from-amber-500 to-orange-500' },
                  ].map((action) => (
                    <motion.button
                      key={action.label}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      className="p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 transition-all group"
                    >
                      <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${action.gradient} flex items-center justify-center mx-auto mb-2 group-hover:scale-110 transition-transform`}>
                        <action.icon className="w-4 h-4 text-white" />
                      </div>
                      <span className="text-xs font-medium">{action.label}</span>
                    </motion.button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Enhanced Timeline */}
        <div className="h-56 bg-gradient-to-t from-gray-950 to-gray-900/95 border-t border-white/5">
          {/* Timeline header with time markers */}
          <div className="h-8 flex items-center border-b border-white/5 bg-black/20">
            <div className="w-56 flex-shrink-0 px-3 flex items-center justify-between">
              <span className="text-xs font-medium text-white/40">Tracks</span>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-1 rounded hover:bg-white/10"
              >
                <Plus className="w-3.5 h-3.5 text-white/40" />
              </motion.button>
            </div>
            <div className="flex-1 relative">
              {/* Time markers */}
              <div className="flex">
                {[...Array(11)].map((_, i) => (
                  <div key={i} className="flex-1 text-center text-[10px] text-white/30 font-mono">
                    {i * 3}s
                  </div>
                ))}
              </div>
              {/* Playhead */}
              <motion.div
                className="absolute top-0 bottom-0 w-0.5 bg-gradient-to-b from-violet-500 to-fuchsia-500 z-20"
                style={{ left: `${(currentTime / duration) * 100}%` }}
              >
                <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-4 h-4 bg-gradient-to-br from-violet-500 to-fuchsia-500 rounded-full shadow-lg shadow-violet-500/50" />
              </motion.div>
            </div>
          </div>

          {/* Timeline tracks */}
          <div className="overflow-y-auto" style={{ height: 'calc(100% - 32px)' }}>
            {tracks.map((track, i) => (
              <TimelineTrack
                key={i}
                {...track}
                isSelected={selectedTrack === i}
                onSelect={() => setSelectedTrack(i)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
