'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import {
  Play,
  Video,
  Music,
  Bot,
  Globe,
  Star,
  ArrowRight,
  Check,
  ChevronDown,
  ChevronRight,
  Award,
  Wand2,
  Mic,
  Type,
  Share2,
  Sparkles,
  PlayCircle,
  Copy,
  Menu,
  X,
  Image,
  Zap,
  Users,
  TrendingUp,
  Clock,
  Eye,
  Heart,
  Flame,
  Crown,
  Film,
  Palette,
  Volume2,
  MessageSquare,
  Download,
  Instagram,
  Youtube,
  Twitter,
  Facebook,
  Linkedin,
  Mail,
  Phone,
  MapPin,
  Shield,
  Headphones,
  BookOpen,
  HelpCircle,
  FileText,
  Layers,
  Target,
  BarChart3,
  Smartphone,
  Monitor,
  Scissors,
  Languages,
  Subtitles,
} from 'lucide-react';

// ============ MEGA MENU NAVIGATION ============
const MegaMenu = () => {
  const [activeMenu, setActiveMenu] = useState<string | null>(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const menuItems = {
    'AI Features': {
      sections: [
        {
          title: 'Video Generation',
          items: [
            { name: 'AI Video Generator', desc: 'Create videos from text prompts', icon: Video, href: '/create' },
            { name: 'Text to Video', desc: 'Transform scripts into videos', icon: Type, href: '/create' },
            { name: 'URL to Video', desc: 'Convert articles to video', icon: Globe, href: '/create' },
            { name: 'Image to Video', desc: 'Animate your images', icon: Image, href: '/create' },
          ]
        },
        {
          title: 'Audio & Voice',
          items: [
            { name: 'AI Music Generator', desc: 'Create custom soundtracks', icon: Music, href: '/create' },
            { name: 'Voice Cloning', desc: '100+ AI voices in 50+ languages', icon: Mic, href: '/create' },
            { name: 'Text to Speech', desc: 'Natural voiceovers', icon: Volume2, href: '/create' },
            { name: 'Auto Captions', desc: 'AI-powered subtitles', icon: Subtitles, href: '/create' },
          ]
        },
        {
          title: 'Smart Editing',
          items: [
            { name: 'AI Avatars', desc: 'Digital spokespersons', icon: Bot, href: '/create' },
            { name: 'Background Remover', desc: 'One-click removal', icon: Scissors, href: '/studio' },
            { name: 'Smart Crop', desc: 'Auto-resize for platforms', icon: Target, href: '/studio' },
            { name: 'Virality Score', desc: 'AI-powered predictions', icon: TrendingUp, href: '/analytics' },
          ]
        }
      ]
    },
    'Platforms': {
      sections: [
        {
          title: 'Social Media',
          items: [
            { name: 'TikTok', desc: 'Short-form vertical videos', icon: Smartphone, href: '/create?platform=tiktok' },
            { name: 'Instagram Reels', desc: 'Stories & Reels creator', icon: Instagram, href: '/create?platform=instagram' },
            { name: 'YouTube Shorts', desc: 'Vertical YouTube content', icon: Youtube, href: '/create?platform=youtube' },
            { name: 'Twitter/X', desc: 'Viral video content', icon: Twitter, href: '/create?platform=twitter' },
          ]
        },
        {
          title: 'Long-form',
          items: [
            { name: 'YouTube', desc: 'Full-length videos', icon: Youtube, href: '/create?platform=youtube-long' },
            { name: 'Facebook', desc: 'Social video content', icon: Facebook, href: '/create?platform=facebook' },
            { name: 'LinkedIn', desc: 'Professional videos', icon: Linkedin, href: '/create?platform=linkedin' },
            { name: 'Website Embed', desc: 'Custom player embed', icon: Monitor, href: '/create?platform=web' },
          ]
        }
      ]
    },
    'Resources': {
      sections: [
        {
          title: 'Learn',
          items: [
            { name: 'Tutorials', desc: 'Step-by-step guides', icon: BookOpen, href: '#' },
            { name: 'Blog', desc: 'Tips & best practices', icon: FileText, href: '#' },
            { name: 'Help Center', desc: 'FAQs and support', icon: HelpCircle, href: '#' },
            { name: 'Community', desc: 'Join creators worldwide', icon: Users, href: '#' },
          ]
        },
        {
          title: 'Tools',
          items: [
            { name: 'Templates', desc: '500+ pro templates', icon: Layers, href: '/templates' },
            { name: 'Brand Kit', desc: 'Consistent branding', icon: Palette, href: '/settings' },
            { name: 'API Access', desc: 'Developer tools', icon: Zap, href: '#' },
            { name: 'Integrations', desc: 'Connect your tools', icon: Share2, href: '#' },
          ]
        }
      ]
    }
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-black/95 backdrop-blur-xl border-b border-white/10">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-violet-500 to-fuchsia-500 rounded-xl flex items-center justify-center shadow-lg shadow-violet-500/25">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-white">Taj Chat</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden lg:flex items-center gap-1">
            {Object.entries(menuItems).map(([key, value]) => (
              <div
                key={key}
                className="relative"
                onMouseEnter={() => setActiveMenu(key)}
                onMouseLeave={() => setActiveMenu(null)}
              >
                <button className="flex items-center gap-1 px-4 py-2 text-white/80 hover:text-white font-medium transition-colors">
                  {key}
                  <ChevronDown className={`w-4 h-4 transition-transform ${activeMenu === key ? 'rotate-180' : ''}`} />
                </button>

                <AnimatePresence>
                  {activeMenu === key && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 10 }}
                      className="absolute top-full left-0 mt-2 bg-gray-900 rounded-2xl border border-white/10 shadow-2xl shadow-black/50 overflow-hidden"
                      style={{ minWidth: value.sections.length > 2 ? '700px' : '500px' }}
                    >
                      <div className="p-6 grid gap-8" style={{ gridTemplateColumns: `repeat(${value.sections.length}, 1fr)` }}>
                        {value.sections.map((section, idx) => (
                          <div key={idx}>
                            <h4 className="text-xs font-semibold text-white/40 uppercase tracking-wider mb-4">{section.title}</h4>
                            <div className="space-y-1">
                              {section.items.map((item, i) => (
                                <Link
                                  key={i}
                                  href={item.href}
                                  className="flex items-start gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors group"
                                >
                                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-violet-500/20 to-fuchsia-500/20 flex items-center justify-center group-hover:from-violet-500/30 group-hover:to-fuchsia-500/30 transition-colors">
                                    <item.icon className="w-5 h-5 text-violet-400" />
                                  </div>
                                  <div>
                                    <p className="text-sm font-medium text-white group-hover:text-violet-300 transition-colors">{item.name}</p>
                                    <p className="text-xs text-white/50">{item.desc}</p>
                                  </div>
                                </Link>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ))}

            <Link href="/pricing" className="px-4 py-2 text-white/80 hover:text-white font-medium transition-colors">
              Pricing
            </Link>
          </div>

          {/* Right Side */}
          <div className="flex items-center gap-4">
            <Link href="/settings" className="hidden md:block text-white/80 hover:text-white font-medium transition-colors">
              Login
            </Link>
            <Link
              href="/create"
              className="px-5 py-2.5 bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-violet-500/25 transition-all"
            >
              Try Free
            </Link>
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="lg:hidden p-2 rounded-lg hover:bg-white/10 transition-colors"
            >
              {isMobileMenuOpen ? <X className="w-6 h-6 text-white" /> : <Menu className="w-6 h-6 text-white" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="lg:hidden bg-gray-900 border-t border-white/10"
          >
            <div className="p-6 space-y-4">
              {Object.entries(menuItems).map(([key, value]) => (
                <div key={key} className="space-y-2">
                  <p className="text-sm font-semibold text-white/60">{key}</p>
                  {value.sections.map((section, idx) => (
                    <div key={idx} className="space-y-1 pl-4">
                      {section.items.map((item, i) => (
                        <Link
                          key={i}
                          href={item.href}
                          className="flex items-center gap-3 py-2 text-white/80 hover:text-white"
                          onClick={() => setIsMobileMenuOpen(false)}
                        >
                          <item.icon className="w-4 h-4" />
                          {item.name}
                        </Link>
                      ))}
                    </div>
                  ))}
                </div>
              ))}
              <div className="pt-4 border-t border-white/10">
                <Link
                  href="/pricing"
                  className="block py-2 text-white/80 hover:text-white"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Pricing
                </Link>
                <Link
                  href="/settings"
                  className="block py-2 text-white/80 hover:text-white"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Login
                </Link>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

// ============ HERO SECTION ============
const HeroSection = () => {
  const [currentPrompt, setCurrentPrompt] = useState(0);
  const prompts = [
    "Create a 30-second ad for a coffee shop with cozy vibes...",
    "Make a TikTok about morning routines with trendy music...",
    "Generate a product showcase for wireless earbuds...",
    "Create a motivational video with inspiring quotes...",
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentPrompt((prev) => (prev + 1) % prompts.length);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <section className="relative min-h-screen pt-32 pb-20 overflow-hidden bg-black">
      {/* Background Effects */}
      <div className="absolute inset-0">
        <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-violet-500/20 rounded-full blur-[120px]" />
        <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-fuchsia-500/20 rounded-full blur-[120px]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-cyan-500/10 rounded-full blur-[150px]" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6">
        {/* Trust Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex justify-center mb-8"
        >
          <div className="flex items-center gap-4 px-6 py-3 bg-white/5 backdrop-blur-sm rounded-full border border-white/10">
            <div className="flex items-center gap-2">
              <Award className="w-5 h-5 text-amber-400" />
              <span className="text-sm font-medium text-white/80">Product of the Year</span>
            </div>
            <div className="w-px h-4 bg-white/20" />
            <div className="flex items-center gap-2">
              <div className="flex -space-x-1">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-4 h-4 fill-amber-400 text-amber-400" />
                ))}
              </div>
              <span className="text-sm font-medium text-white/80">4.9/5 (10K+ reviews)</span>
            </div>
          </div>
        </motion.div>

        {/* Main Headline */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-center mb-8"
        >
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-black tracking-tight leading-none mb-4">
            <span className="block text-white">Create Videos</span>
            <span className="block bg-gradient-to-r from-violet-400 via-fuchsia-400 to-cyan-400 bg-clip-text text-transparent">
              Without Limits
            </span>
          </h1>
          <p className="text-xl md:text-2xl text-white/60 max-w-3xl mx-auto leading-relaxed">
            Turn any idea into videos. Ads, explainers, stories, anything you can imagine.
            Our <span className="text-white font-semibold">10 AI agents</span> create publish-ready content in minutes.
          </p>
        </motion.div>

        {/* Prompt Input */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="max-w-3xl mx-auto mb-8"
        >
          <div className="relative bg-white/5 backdrop-blur-xl rounded-2xl border border-white/10 overflow-hidden">
            <div className="absolute top-4 left-6 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-xs text-white/40">10 AI Agents Ready</span>
            </div>
            <textarea
              placeholder={prompts[currentPrompt]}
              className="w-full h-32 pt-12 px-6 pb-20 bg-transparent text-white placeholder:text-white/40 resize-none focus:outline-none text-lg"
            />
            <div className="absolute bottom-4 left-6 right-6 flex items-center justify-between">
              <div className="flex items-center gap-3">
                {['TikTok', 'Reels', 'Shorts'].map((platform) => (
                  <button
                    key={platform}
                    className="px-3 py-1.5 text-xs font-medium rounded-lg bg-white/10 text-white/70 hover:bg-white/20 hover:text-white transition-colors"
                  >
                    {platform}
                  </button>
                ))}
              </div>
              <Link
                href="/create"
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-violet-500/25 transition-all"
              >
                <Wand2 className="w-5 h-5" />
                Generate
              </Link>
            </div>
          </div>
          <p className="text-center text-sm text-white/40 mt-4">
            No credit card required • 5 free videos per month • Cancel anytime
          </p>
        </motion.div>
      </div>
    </section>
  );
};

// ============ VIDEO GALLERY SECTION ============
const VideoGallerySection = ({ title, subtitle, videos, category }: any) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  const scrollLeft = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: -400, behavior: 'smooth' });
    }
  };

  const scrollRight = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: 400, behavior: 'smooth' });
    }
  };

  return (
    <section className="py-16 bg-black">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2">{title}</h2>
            {subtitle && <p className="text-white/60">{subtitle}</p>}
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={scrollLeft}
              className="p-3 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 transition-colors"
            >
              <ChevronRight className="w-5 h-5 text-white rotate-180" />
            </button>
            <button
              onClick={scrollRight}
              className="p-3 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 transition-colors"
            >
              <ChevronRight className="w-5 h-5 text-white" />
            </button>
          </div>
        </div>

        <div
          ref={scrollRef}
          className="flex gap-4 overflow-x-auto scrollbar-hide pb-4 -mx-6 px-6"
          style={{ scrollSnapType: 'x mandatory' }}
        >
          {videos.map((video: any, index: number) => (
            <VideoCard key={index} video={video} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
};

// ============ VIDEO CARD WITH GENERATE & COPY PROMPT ============
const VideoCard = ({ video, index }: { video: any; index: number }) => {
  const [isHovered, setIsHovered] = useState(false);
  const [copied, setCopied] = useState(false);

  const copyPrompt = () => {
    navigator.clipboard.writeText(video.prompt || video.title);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.05 }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="relative flex-shrink-0 group cursor-pointer"
      style={{ scrollSnapAlign: 'start', width: video.aspect === '16:9' ? '400px' : '225px' }}
    >
      <div className={`relative overflow-hidden rounded-2xl bg-gray-900 border border-white/10 hover:border-violet-500/50 transition-all ${video.aspect === '16:9' ? 'aspect-video' : 'aspect-[9/16]'}`}>
        {/* Thumbnail */}
        <img
          src={video.thumbnail}
          alt={video.title}
          className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
        />

        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/30 to-transparent opacity-80" />

        {/* Category Badge */}
        {video.category && (
          <div className="absolute top-3 left-3 px-3 py-1 rounded-full bg-black/50 backdrop-blur-sm border border-white/10 text-xs font-medium text-white">
            {video.category}
          </div>
        )}

        {/* Duration */}
        {video.duration && (
          <div className="absolute top-3 right-3 px-2 py-1 rounded-lg bg-black/50 backdrop-blur-sm text-xs font-mono text-white">
            {video.duration}
          </div>
        )}

        {/* Hover Actions */}
        <AnimatePresence>
          {isHovered && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center gap-4"
            >
              {/* Play Button */}
              <motion.button
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm border border-white/30 flex items-center justify-center hover:bg-white/30 transition-colors"
              >
                <Play className="w-7 h-7 text-white ml-1" fill="white" />
              </motion.button>

              {/* Action Buttons */}
              <div className="flex gap-2">
                <motion.button
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.1 }}
                  onClick={(e) => { e.stopPropagation(); copyPrompt(); }}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-sm font-medium transition-colors"
                >
                  {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
                  {copied ? 'Copied!' : 'Copy Prompt'}
                </motion.button>
                <Link href={`/create?prompt=${encodeURIComponent(video.prompt || video.title)}`}>
                  <motion.button
                    initial={{ y: 10, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.15 }}
                    className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white text-sm font-medium hover:shadow-lg hover:shadow-violet-500/25 transition-all"
                  >
                    <Wand2 className="w-4 h-4" />
                    Generate
                  </motion.button>
                </Link>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Bottom Info */}
        <div className="absolute bottom-0 left-0 right-0 p-4">
          <h3 className="text-white font-semibold text-sm mb-2 line-clamp-2">{video.title}</h3>
          <div className="flex items-center gap-3 text-white/60 text-xs">
            {video.views && (
              <span className="flex items-center gap-1">
                <Eye className="w-3 h-3" />
                {video.views}
              </span>
            )}
            {video.likes && (
              <span className="flex items-center gap-1">
                <Heart className="w-3 h-3" />
                {video.likes}
              </span>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// ============ FEATURE SHOWCASE (Edit Like You Think) ============
const FeatureShowcase = () => {
  const features = [
    {
      title: 'Replace any image',
      description: 'Swap visuals with AI-generated alternatives',
      progress: 100,
      status: 'Done',
      icon: Image,
    },
    {
      title: 'Mix audio tracks',
      description: 'Balance music, voice, and sound effects',
      progress: 100,
      status: 'Done',
      icon: Music,
    },
    {
      title: 'Translate voiceover',
      description: 'Convert to 50+ languages with voice cloning',
      progress: 85,
      status: 'Processing',
      icon: Languages,
    },
    {
      title: 'Generate captions',
      description: 'Accurate AI-powered subtitles',
      progress: 60,
      status: 'Processing',
      icon: Subtitles,
    },
  ];

  return (
    <section className="py-24 bg-gradient-to-b from-black via-gray-900 to-black">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl md:text-5xl font-bold text-white mb-4"
          >
            Edit like you <span className="bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent">think</span>
          </motion.h2>
          <p className="text-xl text-white/60 max-w-2xl mx-auto">
            Our AI understands your creative intent and executes complex edits automatically
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="relative p-6 rounded-2xl bg-white/5 border border-white/10 hover:border-violet-500/50 transition-colors group"
            >
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-violet-500/20 to-fuchsia-500/20 flex items-center justify-center mb-4 group-hover:from-violet-500/30 group-hover:to-fuchsia-500/30 transition-colors">
                <feature.icon className="w-6 h-6 text-violet-400" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-sm text-white/50 mb-4">{feature.description}</p>

              {/* Progress bar */}
              <div className="relative">
                <div className="h-1 bg-white/10 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    whileInView={{ width: `${feature.progress}%` }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.5 + index * 0.1, duration: 1 }}
                    className={`h-full rounded-full ${feature.progress === 100 ? 'bg-green-500' : 'bg-gradient-to-r from-violet-500 to-fuchsia-500'}`}
                  />
                </div>
                <div className="flex items-center justify-between mt-2">
                  <span className="text-xs text-white/40">{feature.status}</span>
                  <span className="text-xs text-white/60">{feature.progress}%</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

// ============ TESTIMONIALS SECTION ============
const TestimonialsSection = () => {
  const testimonials = [
    {
      quote: "From my first video to a monetized channel, it took less than two months. Taj Chat is incredible.",
      author: "Sarah Chen",
      role: "Content Creator",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop",
      metric: "500K+ subscribers",
    },
    {
      quote: "We replaced our entire video production team with Taj Chat. The quality is indistinguishable from human-made content.",
      author: "Michael Torres",
      role: "Marketing Director",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop",
      metric: "10x faster production",
    },
    {
      quote: "The AI music generator alone is worth the subscription. I've never had to worry about copyright again.",
      author: "Emily Johnson",
      role: "YouTuber",
      avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop",
      metric: "2M+ views/month",
    },
  ];

  return (
    <section className="py-24 bg-black">
      <div className="max-w-7xl mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            HOME FOR <span className="bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent">BOLD IDEAS</span>
          </h2>
          <p className="text-xl text-white/60">
            Join thousands of creators making their mark with AI-powered video
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="relative p-8 rounded-2xl bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10"
            >
              <div className="flex items-center gap-4 mb-6">
                <img
                  src={testimonial.avatar}
                  alt={testimonial.author}
                  className="w-14 h-14 rounded-full object-cover border-2 border-violet-500/50"
                />
                <div>
                  <p className="text-white font-semibold">{testimonial.author}</p>
                  <p className="text-white/50 text-sm">{testimonial.role}</p>
                </div>
              </div>
              <p className="text-white/80 text-lg leading-relaxed mb-6">"{testimonial.quote}"</p>
              <div className="flex items-center gap-2 text-sm">
                <TrendingUp className="w-4 h-4 text-green-400" />
                <span className="text-green-400 font-semibold">{testimonial.metric}</span>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

// ============ STATS SECTION ============
const StatsSection = () => {
  const stats = [
    { value: '10M+', label: 'Videos Created', icon: Video },
    { value: '150+', label: 'Countries', icon: Globe },
    { value: '10', label: 'AI Agents', icon: Bot },
    { value: '99%', label: 'Satisfaction', icon: Star },
  ];

  return (
    <section className="py-16 bg-gradient-to-r from-violet-900/20 via-fuchsia-900/20 to-cyan-900/20 border-y border-white/10">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="text-center"
            >
              <div className="w-14 h-14 mx-auto mb-4 bg-gradient-to-br from-violet-500/20 to-fuchsia-500/20 rounded-xl flex items-center justify-center">
                <stat.icon className="w-7 h-7 text-violet-400" />
              </div>
              <p className="text-4xl md:text-5xl font-bold text-white mb-2">{stat.value}</p>
              <p className="text-white/60">{stat.label}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

// ============ CTA SECTION ============
const CTASection = () => {
  return (
    <section className="py-24 bg-black">
      <div className="max-w-4xl mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="relative p-12 rounded-3xl bg-gradient-to-br from-violet-600/20 via-fuchsia-600/20 to-cyan-600/20 border border-white/10 text-center overflow-hidden"
        >
          {/* Background glow */}
          <div className="absolute inset-0 bg-gradient-to-r from-violet-500/10 via-fuchsia-500/10 to-cyan-500/10 blur-3xl" />

          <div className="relative z-10">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to create your first video?
            </h2>
            <p className="text-xl text-white/60 mb-8 max-w-2xl mx-auto">
              Join millions of creators using Taj Chat to grow their audience.
              Start free, no credit card required.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/create"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-black font-semibold rounded-xl hover:bg-white/90 transition-colors"
              >
                Start Creating Free
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                href="/gallery"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white/10 text-white font-semibold rounded-xl border border-white/20 hover:bg-white/20 transition-colors"
              >
                <Play className="w-5 h-5" />
                Watch Examples
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

// ============ FOOTER ============
const Footer = () => {
  const footerLinks = {
    'AI Tools': [
      { name: 'AI Video Generator', href: '/create' },
      { name: 'Text to Video', href: '/create' },
      { name: 'AI Music Creator', href: '/create' },
      { name: 'Voice Cloning', href: '/create' },
      { name: 'Auto Captions', href: '/create' },
      { name: 'AI Avatars', href: '/create' },
    ],
    'Platforms': [
      { name: 'TikTok', href: '/create?platform=tiktok' },
      { name: 'Instagram Reels', href: '/create?platform=instagram' },
      { name: 'YouTube Shorts', href: '/create?platform=youtube' },
      { name: 'Twitter/X', href: '/create?platform=twitter' },
      { name: 'Facebook', href: '/create?platform=facebook' },
    ],
    'Resources': [
      { name: 'Templates', href: '/templates' },
      { name: 'Blog', href: '#' },
      { name: 'Tutorials', href: '#' },
      { name: 'Help Center', href: '#' },
      { name: 'API Docs', href: '#' },
    ],
    'Company': [
      { name: 'About', href: '#' },
      { name: 'Careers', href: '#' },
      { name: 'Press', href: '#' },
      { name: 'Contact', href: '#' },
    ],
  };

  return (
    <footer className="bg-gray-950 border-t border-white/10">
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="grid grid-cols-2 md:grid-cols-6 gap-8 mb-12">
          {/* Logo & Description */}
          <div className="col-span-2">
            <Link href="/" className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-br from-violet-500 to-fuchsia-500 rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Taj Chat</span>
            </Link>
            <p className="text-white/50 text-sm mb-6 max-w-xs">
              AI-powered video creation platform. Create stunning videos in minutes with our 10 specialized AI agents.
            </p>
            {/* App Store Buttons */}
            <div className="flex gap-3">
              <button className="flex items-center gap-2 px-4 py-2 bg-white/5 rounded-lg border border-white/10 hover:bg-white/10 transition-colors">
                <Smartphone className="w-5 h-5 text-white/70" />
                <div className="text-left">
                  <p className="text-[10px] text-white/50">Download on</p>
                  <p className="text-xs font-semibold text-white">App Store</p>
                </div>
              </button>
              <button className="flex items-center gap-2 px-4 py-2 bg-white/5 rounded-lg border border-white/10 hover:bg-white/10 transition-colors">
                <Smartphone className="w-5 h-5 text-white/70" />
                <div className="text-left">
                  <p className="text-[10px] text-white/50">Get it on</p>
                  <p className="text-xs font-semibold text-white">Google Play</p>
                </div>
              </button>
            </div>
          </div>

          {/* Links */}
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h4 className="text-sm font-semibold text-white mb-4">{category}</h4>
              <ul className="space-y-3">
                {links.map((link) => (
                  <li key={link.name}>
                    <Link
                      href={link.href}
                      className="text-sm text-white/50 hover:text-white transition-colors"
                    >
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm text-white/40">
            © 2024 Taj Chat. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <Link href="#" className="text-sm text-white/40 hover:text-white transition-colors">Privacy Policy</Link>
            <Link href="#" className="text-sm text-white/40 hover:text-white transition-colors">Terms of Service</Link>
            <Link href="#" className="text-sm text-white/40 hover:text-white transition-colors">Cookie Policy</Link>
          </div>
          <div className="flex items-center gap-4">
            {[Twitter, Instagram, Youtube, Linkedin].map((Icon, i) => (
              <a key={i} href="#" className="text-white/40 hover:text-white transition-colors">
                <Icon className="w-5 h-5" />
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
};

// ============ MAIN PAGE ============
export default function HomePage() {
  // Sample video data for galleries
  const trendingVideos = [
    { thumbnail: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=711&fit=crop', title: 'Product Launch Campaign', category: 'Marketing', duration: '0:32', views: '2.4M', likes: '156K', prompt: 'Create a dynamic product launch video with modern transitions and energetic music', aspect: '9:16' },
    { thumbnail: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400&h=711&fit=crop', title: 'AI Art Creation Tutorial', category: 'Education', duration: '0:45', views: '1.8M', likes: '98K', prompt: 'Make an educational tutorial about AI art generation with step-by-step visuals', aspect: '9:16' },
    { thumbnail: 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&h=711&fit=crop', title: 'Latest Tech Review', category: 'Technology', duration: '0:28', views: '3.2M', likes: '210K', prompt: 'Create a tech review video showcasing the latest smartphone features', aspect: '9:16' },
    { thumbnail: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=711&fit=crop', title: '30-Day Fitness Challenge', category: 'Health', duration: '0:35', views: '4.1M', likes: '340K', prompt: 'Generate a motivational fitness challenge video with workout montages', aspect: '9:16' },
    { thumbnail: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&h=711&fit=crop', title: 'Bali Travel Adventure', category: 'Travel', duration: '0:52', views: '1.2M', likes: '87K', prompt: 'Create a cinematic travel video showcasing Bali beaches and temples', aspect: '9:16' },
    { thumbnail: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=711&fit=crop', title: 'Indie Music Video', category: 'Music', duration: '1:15', views: '5.6M', likes: '420K', prompt: 'Generate an indie music video with artistic visuals and smooth transitions', aspect: '9:16' },
  ];

  const effectsVideos = [
    { thumbnail: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&h=711&fit=crop', title: 'Drip Flip Effect', category: 'Effects', duration: '0:08', views: '890K', prompt: 'Create a video with drip flip transition effect', aspect: '9:16' },
    { thumbnail: 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=400&h=711&fit=crop', title: 'Car Crash Cinematic', category: 'VFX', duration: '0:12', views: '1.2M', prompt: 'Generate a cinematic car crash scene with slow motion', aspect: '9:16' },
    { thumbnail: 'https://images.unsplash.com/photo-1614729939124-032d1e6c9945?w=400&h=711&fit=crop', title: 'Neon Glow Animation', category: 'Effects', duration: '0:15', views: '670K', prompt: 'Create a neon glow animation with cyberpunk aesthetics', aspect: '9:16' },
    { thumbnail: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=711&fit=crop', title: 'Particle Explosion', category: 'VFX', duration: '0:10', views: '450K', prompt: 'Generate a dramatic particle explosion effect', aspect: '9:16' },
  ];

  const adsVideos = [
    { thumbnail: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&h=340&fit=crop', title: 'Premium Headphones Ad', category: 'Product', duration: '0:30', views: '2.1M', prompt: 'Create a premium headphones advertisement with sleek product shots', aspect: '16:9' },
    { thumbnail: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&h=340&fit=crop', title: 'Luxury Watch Commercial', category: 'Luxury', duration: '0:45', views: '1.8M', prompt: 'Generate a luxury watch commercial with elegant cinematography', aspect: '16:9' },
    { thumbnail: 'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=600&h=340&fit=crop', title: 'Sports Car Reveal', category: 'Automotive', duration: '1:00', views: '3.4M', prompt: 'Create a dramatic sports car reveal video with cinematic lighting', aspect: '16:9' },
  ];

  return (
    <div className="min-h-screen bg-black text-white">
      <MegaMenu />
      <HeroSection />

      <VideoGallerySection
        title="Trending"
        subtitle="See what creators are making right now"
        videos={trendingVideos}
        category="trending"
      />

      <VideoGallerySection
        title="Effects & VFX"
        subtitle="Mind-blowing visual effects"
        videos={effectsVideos}
        category="effects"
      />

      <VideoGallerySection
        title="Million Dollar Ads"
        subtitle="Cinematic brand commercials"
        videos={adsVideos}
        category="ads"
      />

      <FeatureShowcase />
      <StatsSection />
      <TestimonialsSection />
      <CTASection />
      <Footer />
    </div>
  );
}
