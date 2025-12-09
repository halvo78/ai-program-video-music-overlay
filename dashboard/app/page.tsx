'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
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
  Award,
  Wand2,
  Mic,
  Type,
  Share2,
  Sparkles,
  PlayCircle,
  Shield,
  Image as ImageIcon,
} from 'lucide-react';

// Professional gradient text - use sparingly
const GradientText = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <span className={`text-gradient ${className}`}>
    {children}
  </span>
);

// Animated counter
const AnimatedCounter = ({ value, suffix = '' }: { value: number; suffix?: string }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const duration = 2000;
    const steps = 60;
    const increment = value / steps;
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= value) {
        setCount(value);
        clearInterval(timer);
      } else {
        setCount(Math.floor(current));
      }
    }, duration / steps);

    return () => clearInterval(timer);
  }, [value]);

  return <span>{count.toLocaleString()}{suffix}</span>;
};

// Video Text Hero - Professional implementation
const VideoTextHero = () => {
  const videos = [
    'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=1200&h=800&fit=crop&q=80',
    'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1200&h=800&fit=crop&q=80',
    'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=1200&h=800&fit=crop&q=80',
  ];

  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % videos.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative py-12 md:py-16 select-none">
      {/* CREATE - with video/image background clipped to text */}
    <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative"
      >
        <h1
          className="text-[clamp(4rem,12vw,10rem)] font-black tracking-tighter leading-[0.9] text-center uppercase"
          style={{
            backgroundImage: `url(${videos[currentIndex]})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            WebkitBackgroundClip: 'text',
            backgroundClip: 'text',
            color: 'transparent',
            transition: 'background-image 0.8s ease-in-out',
          }}
        >
          CREATE
        </h1>
    </motion.div>

      {/* VIDEOS - professional blue gradient */}
    <motion.div
        initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.1 }}
      >
        <h1 className="text-[clamp(4rem,12vw,10rem)] font-black tracking-tighter leading-[0.9] text-center uppercase text-[#2563EB]">
          VIDEOS
        </h1>
      </motion.div>

      {/* WITHOUT LIMITS - subtle gray */}
    <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <h1 className="text-[clamp(3rem,10vw,8rem)] font-black tracking-tighter leading-[0.95] text-center uppercase text-gray-300">
          WITHOUT LIMITS
        </h1>
      </motion.div>
          </div>
  );
};

// Professional Video Wall - InVideo Style with Hover Video Playback
// REBUILT FROM SCRATCH - Content perfectly matched to titles
const VideoWall = () => {
  // REBUILT FROM SCRATCH - Perfect content matching with video start times
  // Each video starts from the frame shown in the thumbnail
  const videos = [
    {
      // Product Launch Campaign - Product unboxing, marketing reveal
      thumbnail: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=711&fit=crop&q=95&auto=format',
      video: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
      startTime: 5, // Start from 5 seconds (matching thumbnail frame)
      title: 'Product Launch Campaign',
      category: 'Marketing',
      views: '2.4M',
      duration: '0:32',
      platform: 'TikTok'
    },
    {
      // AI Art Creation Tutorial - Digital art, creative AI process
      thumbnail: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400&h=711&fit=crop&q=95&auto=format',
      video: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
      startTime: 8, // Start from 8 seconds
      title: 'AI Art Creation Tutorial',
      category: 'Education',
      views: '1.8M',
      duration: '0:45',
      platform: 'YouTube'
    },
    {
      // Latest Tech Review - Smartphone, gadget review
      thumbnail: 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&h=711&fit=crop&q=95&auto=format',
      video: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
      startTime: 3, // Start from 3 seconds
      title: 'Latest Tech Review',
      category: 'Technology',
      views: '3.2M',
      duration: '0:28',
      platform: 'Instagram'
    },
    {
      // 30-Day Fitness Challenge - Workout, exercise, transformation
      thumbnail: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=711&fit=crop&q=95&auto=format',
      video: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
      startTime: 6, // Start from 6 seconds
      title: '30-Day Fitness Challenge',
      category: 'Health',
      views: '4.1M',
      duration: '0:35',
      platform: 'TikTok'
    },
    {
      // Bali Travel Adventure - Tropical beach, travel destination
      thumbnail: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&h=711&fit=crop&q=95&auto=format',
      video: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
      startTime: 4, // Start from 4 seconds
      title: 'Bali Travel Adventure',
      category: 'Lifestyle',
      views: '1.2M',
      duration: '0:52',
      platform: 'YouTube'
    },
    {
      // Indie Music Video - Music performance, instruments
      thumbnail: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=711&fit=crop&q=95&auto=format',
      video: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4',
      startTime: 7, // Start from 7 seconds
      title: 'Indie Music Video',
      category: 'Entertainment',
      views: '5.6M',
      duration: '1:15',
      platform: 'Instagram'
    },
    {
      // Daily Motivation Boost - Success, achievement, inspiration
      thumbnail: 'https://images.unsplash.com/photo-1504805572947-34fad45aed93?w=400&h=711&fit=crop&q=95&auto=format',
      video: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4',
      startTime: 5, // Start from 5 seconds
      title: 'Daily Motivation Boost',
      category: 'Inspiration',
      views: '2.9M',
      duration: '0:41',
      platform: 'TikTok'
    },
    {
      // Entrepreneur Success Tips - Business meeting, success
      thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=711&fit=crop&q=95&auto=format',
      video: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
      startTime: 10, // Start from 10 seconds
      title: 'Entrepreneur Success Tips',
      category: 'Business',
      views: '1.5M',
      duration: '0:38',
      platform: 'LinkedIn'
    },
  ];

  return (
    <section className="section bg-white">
      <div className="container">
    <motion.div
      initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            See what creators are making
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Join millions creating viral content with Taj Chat
          </p>
    </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {videos.map((video, index) => (
            <VideoCard key={index} video={video} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
};

// Individual Video Card with Hover Playback - InVideo Style
// REBUILT - Handles both video and image-only content perfectly
const VideoCard = ({ video, index }: { video: any; index: number }) => {
  const [isHovered, setIsHovered] = useState(false);
  const [videoLoaded, setVideoLoaded] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [showVideo, setShowVideo] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const hasVideo = video.video !== null && video.video !== undefined;

  useEffect(() => {
    if (hasVideo && videoRef.current) {
      if (isHovered) {
        // Set video to start from thumbnail frame (startTime)
        const startTime = video.startTime || 0;
        videoRef.current.currentTime = startTime;

        // Play video with sound on hover
        videoRef.current.volume = 0.4; // Moderate volume
        const playPromise = videoRef.current.play();

        if (playPromise !== undefined) {
          playPromise
            .then(() => {
              setIsPlaying(true);
              setShowVideo(true);
            })
            .catch((err) => {
              // Autoplay with sound blocked - try muted
              videoRef.current!.muted = true;
              videoRef.current!.play()
                .then(() => {
                  setIsPlaying(true);
                  setShowVideo(true);
                })
                .catch(() => {
                  // Video play failed completely
                  setIsPlaying(false);
                  setShowVideo(false);
                });
            });
        }
      } else {
        // When not hovering, reset to thumbnail frame but don't pause immediately
        // This allows smooth transition back to thumbnail
        const startTime = video.startTime || 0;
        videoRef.current.pause();
        videoRef.current.currentTime = startTime;
        setIsPlaying(false);
        setShowVideo(false);
      }
    }
  }, [isHovered, hasVideo, video.startTime]);

  const handleVideoLoad = () => {
    setVideoLoaded(true);
    // Set initial frame to match thumbnail when video loads
    if (videoRef.current && video.startTime !== undefined) {
      videoRef.current.currentTime = video.startTime;
    }
  };

  const handleVideoError = () => {
    // If video fails to load, just show thumbnail
    setVideoLoaded(false);
    setIsPlaying(false);
    setShowVideo(false);
  };

  const handleVideoCanPlay = () => {
    setVideoLoaded(true);
    // Ensure video starts at thumbnail frame
    if (videoRef.current && video.startTime !== undefined) {
      videoRef.current.currentTime = video.startTime;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.05 }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="relative group cursor-pointer"
      whileHover={{ y: -4 }}
    >
      <div className="relative aspect-[9/16] rounded-2xl overflow-hidden bg-gray-100 border border-gray-200 shadow-sm hover:shadow-2xl transition-all duration-500 group">
        {/* Thumbnail - perfect 9:16 aspect ratio, fills box correctly */}
        <img
          src={video.thumbnail}
          alt={video.title}
          className={`absolute inset-0 w-full h-full transition-all duration-700 ${
            hasVideo && showVideo && isPlaying
              ? 'opacity-0 z-0 scale-100'
              : 'opacity-100 z-10 scale-100 group-hover:scale-105'
          }`}
          style={{
            objectFit: 'cover',
            objectPosition: 'center',
            width: '100%',
            height: '100%',
          }}
          loading="lazy"
        />

        {/* Video element - plays on hover with sound, starts from thumbnail frame */}
        {hasVideo && (
          <video
            ref={videoRef}
            src={video.video}
            onLoadedData={handleVideoLoad}
            onError={handleVideoError}
            onCanPlay={handleVideoCanPlay}
            className={`absolute inset-0 w-full h-full transition-opacity duration-700 ${
              showVideo && isPlaying ? 'opacity-100 z-20' : 'opacity-0 z-0'
            }`}
            style={{
              objectFit: 'cover',
              objectPosition: 'center',
              width: '100%',
              height: '100%',
            }}
            muted={false}
            loop
            playsInline
            preload="metadata"
          />
        )}

        {/* Minimal gradient overlay - InVideo style */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-transparent pointer-events-none" />

        {/* Category badge - top left, clean white pill */}
        <div className="absolute top-3 left-3 px-3 py-1.5 bg-white rounded-full text-gray-900 text-xs font-bold shadow-lg z-10">
          {video.category}
        </div>

        {/* Duration badge - top right, clean design */}
        <div className="absolute top-3 right-3 px-2.5 py-1 bg-black/85 backdrop-blur-sm rounded-lg text-white text-xs font-semibold z-10">
          {video.duration}
        </div>

        {/* Platform indicator - subtle, professional */}
        {video.platform && (
          <div className="absolute top-12 left-3 px-2 py-1 bg-black/60 backdrop-blur-sm rounded-md text-white text-[10px] font-medium z-10">
            {video.platform}
          </div>
        )}

        {/* Info at bottom - clean typography like InVideo */}
        <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black via-black/90 to-transparent z-10">
          <h3 className="text-white font-bold text-sm mb-2 leading-tight line-clamp-2 drop-shadow-lg">{video.title}</h3>
          <div className="flex items-center gap-3 text-white/90 text-xs">
            <span className="flex items-center gap-1.5 font-medium">
              <span className="w-1 h-1 bg-white rounded-full"></span>
              {video.views}
            </span>
        </div>
      </div>

        {/* Subtle hover effect - clean, no Netflix elements */}
        <div className={`absolute inset-0 rounded-2xl transition-all duration-500 pointer-events-none ${
          isHovered ? 'ring-2 ring-white/20' : ''
        }`} />
      </div>
    </motion.div>
  );
};

// Professional Feature Cards
const FeatureShowcase = () => {
  const features = [
    {
      icon: Video,
      title: 'AI Video Generation',
      description: 'Generate stunning videos from text prompts using state-of-the-art AI models.',
      preview: 'https://images.unsplash.com/photo-1536240478700-b869070f9279?w=600&h=400&fit=crop&q=80',
      stats: '10M+ videos created',
    },
    {
      icon: Music,
      title: 'AI Music Creation',
      description: 'Create custom royalty-free music tracks that perfectly match your video.',
      preview: 'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600&h=400&fit=crop&q=80',
      stats: '5M+ tracks generated',
    },
    {
      icon: Mic,
      title: 'Voice Cloning',
      description: 'Clone your voice or choose from 100+ AI voices in 50+ languages.',
      preview: 'https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=600&h=400&fit=crop&q=80',
      stats: '50+ languages',
    },
    {
      icon: Bot,
      title: 'AI Avatars',
      description: 'Create lifelike digital spokespersons that speak any script.',
      preview: 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&h=400&fit=crop&q=80',
      stats: '100+ avatars',
    },
  ];

  return (
    <section className="section">
      <div className="container">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Everything you need to <GradientText>create viral content</GradientText>
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            10 specialized AI agents work together to create stunning videos with
            custom music, captions, and automatic optimization.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
              <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="group relative bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
            >
              <div className="relative h-56 overflow-hidden">
                <img
                  src={feature.preview}
                  alt={feature.title}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
                <div className="absolute bottom-4 left-4 px-3 py-1 bg-white/90 backdrop-blur-sm rounded-full text-gray-900 text-xs font-medium">
                  {feature.stats}
                </div>
              </div>

              <div className="p-8">
                <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-6">
                  <feature.icon className="w-6 h-6 text-blue-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed mb-4">{feature.description}</p>
                <button className="text-blue-600 font-medium flex items-center gap-2 hover:gap-3 transition-all">
                  Learn more
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

// FAQ Item
const FAQItem = ({ question, answer }: { question: string; answer: string }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border-b border-gray-200 last:border-0">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full py-6 flex items-center justify-between text-left"
      >
        <span className="text-lg font-semibold text-gray-900">{question}</span>
        <ChevronDown className={`w-5 h-5 text-gray-500 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      {isOpen && (
              <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: 'auto', opacity: 1 }}
          className="overflow-hidden"
        >
          <p className="pb-6 text-gray-600 leading-relaxed">{answer}</p>
        </motion.div>
      )}
    </div>
  );
};

// Enhanced Dashboard Stats Component
const DashboardStats = () => {
  const stats = [
    { label: 'Videos Created', value: '2,847', change: '+12%', icon: Video, bgColor: 'bg-blue-50', iconColor: 'text-blue-600' },
    { label: 'Total Views', value: '24.7M', change: '+8%', icon: PlayCircle, bgColor: 'bg-green-50', iconColor: 'text-green-600' },
    { label: 'AI Agents Active', value: '10/10', change: '100%', icon: Bot, bgColor: 'bg-purple-50', iconColor: 'text-purple-600' },
    { label: 'Platforms Connected', value: '5/5', change: '100%', icon: Globe, bgColor: 'bg-orange-50', iconColor: 'text-orange-600' },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {stats.map((stat, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
          className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
        >
          <div className="flex items-center justify-between mb-4">
            <div className={`w-12 h-12 rounded-xl ${stat.bgColor} flex items-center justify-center`}>
              <stat.icon className={`w-6 h-6 ${stat.iconColor}`} />
            </div>
            <span className="text-sm font-medium text-green-600">{stat.change}</span>
          </div>
          <h3 className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</h3>
          <p className="text-sm text-gray-600">{stat.label}</p>
        </motion.div>
      ))}
    </div>
  );
};

// Agent Status Grid
const AgentStatusGrid = () => {
  const agents = [
    { name: 'Content Agent', status: 'active', tasks: 3, icon: Type },
    { name: 'Video Agent', status: 'active', tasks: 2, icon: Video },
    { name: 'Music Agent', status: 'idle', tasks: 0, icon: Music },
    { name: 'Image Agent', status: 'active', tasks: 1, icon: ImageIcon },
    { name: 'Voice Agent', status: 'idle', tasks: 0, icon: Mic },
    { name: 'Editing Agent', status: 'active', tasks: 2, icon: Wand2 },
    { name: 'Optimization Agent', status: 'idle', tasks: 0, icon: Sparkles },
    { name: 'Analytics Agent', status: 'active', tasks: 1, icon: Star },
    { name: 'Safety Agent', status: 'active', tasks: 1, icon: Shield },
    { name: 'Social Agent', status: 'idle', tasks: 0, icon: Share2 },
  ];

  return (
    <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm mb-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">AI Agents Status</h2>
          <p className="text-sm text-gray-600 mt-1">10 Core Agents + 50 Dashboard Agents</p>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/dashboard-agents" className="text-purple-600 hover:text-purple-700 font-medium text-sm flex items-center gap-1 bg-purple-50 px-3 py-1.5 rounded-lg">
            <Bot className="w-4 h-4" />
            50 Agents
          </Link>
          <Link href="/agents" className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center gap-1">
            View All <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {agents.map((agent, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.05 }}
            className="relative p-4 rounded-xl border border-gray-200 hover:border-blue-300 transition-colors"
          >
            <div className="flex items-center gap-3 mb-2">
              <agent.icon className="w-5 h-5 text-gray-600" />
              <div className={`w-2 h-2 rounded-full ${
                agent.status === 'active' ? 'bg-green-500' : 'bg-gray-300'
              }`} />
            </div>
            <h3 className="text-sm font-semibold text-gray-900 mb-1">{agent.name}</h3>
            <p className="text-xs text-gray-500">
              {agent.status === 'active' ? `${agent.tasks} tasks` : 'Idle'}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default function HomePage() {
  const [prompt, setPrompt] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Toggle for dashboard vs landing
  const { scrollYProgress } = useScroll();

  // If logged in, show dashboard view
  if (isLoggedIn) {
    return (
      <div className="min-h-screen bg-gray-50">
        {/* Dashboard Navigation */}
        <nav className="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200">
          <div className="container">
            <div className="flex items-center justify-between h-16">
              <Link href="/" className="flex items-center gap-2">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <span className="text-lg font-bold text-gray-900">Taj Chat</span>
              </Link>
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setIsLoggedIn(false)}
                  className="text-sm text-gray-600 hover:text-gray-900"
                >
                  View Landing
                </button>
                <Link href="/create" className="btn-primary">
                  Create Video
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <div className="container py-8">
          {/* Welcome Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Welcome back! 👋</h1>
            <p className="text-gray-600">Here's what's happening with your videos today.</p>
          </motion.div>

          {/* Stats Grid */}
          <DashboardStats />

          {/* Agent Status */}
          <AgentStatusGrid />

          {/* Recent Videos & Quick Actions */}
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Recent Videos */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">Recent Videos</h2>
                  <Link href="/gallery" className="text-blue-600 hover:text-blue-700 font-medium text-sm">
                    View All
                  </Link>
                </div>
                <VideoWall />
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h2>
              <div className="space-y-3">
                <Link href="/create" className="block w-full btn-primary text-center">
                  <Wand2 className="w-5 h-5 inline mr-2" />
                  Create New Video
                </Link>
                <Link href="/studio" className="block w-full btn-secondary text-center">
                  <Video className="w-5 h-5 inline mr-2" />
                  Open Studio
                </Link>
                <Link href="/dashboard-agents" className="block w-full btn-secondary text-center bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700">
                  <Bot className="w-5 h-5 inline mr-2" />
                  Manage 50 Agents
                </Link>
                <Link href="/templates" className="block w-full btn-secondary text-center">
                  <Sparkles className="w-5 h-5 inline mr-2" />
                  Browse Templates
                </Link>
                <Link href="/social" className="block w-full btn-secondary text-center">
                  <Share2 className="w-5 h-5 inline mr-2" />
                  Publish to Social
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Landing page view (existing)
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation - Clean and Professional */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200">
        <div className="container">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
            </div>
              <span className="text-lg font-bold text-gray-900">Taj Chat</span>
            </Link>

            <div className="hidden md:flex items-center gap-8">
              <Link href="/studio" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
                Studio
              </Link>
              <Link href="/templates" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
                Templates
              </Link>
              <Link href="/pricing" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
                Pricing
              </Link>
              <Link href="/gallery" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
                Gallery
              </Link>
            </div>

            <div className="flex items-center gap-4">
              <button
                onClick={() => setIsLoggedIn(true)}
                className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
              >
                Dashboard
              </button>
              <Link href="/settings" className="text-gray-600 hover:text-gray-900 font-medium transition-colors">
                Login
              </Link>
              <Link
                href="/create"
                className="btn-primary"
              >
                Sign up
              </Link>
                  </div>
                  </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen pt-32 pb-20 px-6 overflow-hidden">
        <div className="container">
          {/* Trust Badge */}
                <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-center mb-8"
          >
            <div className="flex items-center gap-6 px-6 py-3 bg-white rounded-full border border-gray-200 shadow-sm">
              <div className="flex items-center gap-2">
                <Award className="w-5 h-5 text-orange-500" />
                <span className="text-sm font-medium text-gray-700">Product of the Year</span>
              </div>
              <div className="w-px h-4 bg-gray-300" />
              <div className="flex items-center gap-2">
                <div className="flex -space-x-1">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  ))}
            </div>
                <span className="text-sm font-medium text-gray-700">4.9/5 (2,847 reviews)</span>
                  </div>
                  </div>
                </motion.div>

          {/* Video Text Hero */}
          <VideoTextHero />

          {/* Subtitle */}
                <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
            className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto text-center leading-relaxed mb-12"
                >
            Turn any idea into viral videos. Ads, explainers, stories, YouTube Shorts, TikToks —
            our <span className="font-semibold text-gray-900">10 AI agents</span> create publish-ready content in minutes.
                </motion.p>

          {/* Prompt Input */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
            className="max-w-3xl mx-auto mb-8"
          >
            <div className="relative bg-white rounded-2xl shadow-lg border border-gray-200">
              <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe your video idea... e.g., 'A 30-second ad for a coffee shop'"
                className="w-full px-6 py-5 pr-40 text-lg rounded-2xl border-0 focus:ring-2 focus:ring-blue-500/20 outline-none"
              />
              <Link
                href="/create"
                className="absolute right-3 top-1/2 -translate-y-1/2 px-6 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-all flex items-center gap-2"
              >
                <Wand2 className="w-5 h-5" />
                Generate
                  </Link>
                    </div>
            <p className="text-center text-sm text-gray-500 mt-3">
              No credit card required • 5 free videos per month • Cancel anytime
            </p>
                </motion.div>
              </div>
      </section>

      {/* Brands Section */}
      <section className="py-12 bg-gray-50 border-y border-gray-200">
        <div className="container">
          <p className="text-center text-gray-500 text-sm mb-8 uppercase tracking-wider">Publish Directly To All Major Platforms</p>
          <div className="flex justify-center items-center gap-12 flex-wrap">
            {['TikTok', 'Instagram', 'YouTube', 'Twitter', 'Facebook', 'Threads'].map((brand, i) => (
                <motion.div
                key={i}
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="text-gray-400 hover:text-gray-600 transition-colors font-medium"
              >
                {brand}
                </motion.div>
            ))}
              </div>
                    </div>
      </section>

      {/* Video Wall */}
      <VideoWall />

      {/* Stats Section */}
      <section className="section bg-gray-900">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { value: 5000000, suffix: '+', label: 'Videos Created', icon: Video },
              { value: 150, suffix: '+', label: 'Countries', icon: Globe },
              { value: 10, suffix: '', label: 'AI Agents', icon: Bot },
              { value: 99, suffix: '%', label: 'Satisfaction', icon: Star },
            ].map((stat, i) => (
                <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="text-center"
              >
                <div className="w-14 h-14 mx-auto mb-4 bg-blue-500/10 rounded-xl flex items-center justify-center">
                  <stat.icon className="w-7 h-7 text-blue-400" />
                  </div>
                <p className="text-4xl md:text-5xl font-bold text-white mb-2">
                  <AnimatedCounter value={stat.value} suffix={stat.suffix} />
                </p>
                <p className="text-gray-400">{stat.label}</p>
              </motion.div>
            ))}
                    </div>
                    </div>
      </section>

      {/* Features */}
      <FeatureShowcase />

      {/* How It Works */}
      <section className="section bg-gray-50">
        <div className="container">
                    <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Create videos in <GradientText>3 simple steps</GradientText>
            </h2>
                </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '01',
                title: 'Describe your idea',
                description: 'Type a simple prompt describing what video you want to create.',
                icon: Type,
                image: 'https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?w=600&h=400&fit=crop&q=80',
              },
              {
                step: '02',
                title: 'AI creates your video',
                description: '10 AI agents work together to generate script, visuals, music, and more.',
                icon: Bot,
                image: 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&h=400&fit=crop&q=80',
              },
              {
                step: '03',
                title: 'Publish everywhere',
                description: 'Export and publish directly to all major social platforms.',
                icon: Share2,
                image: 'https://images.unsplash.com/photo-1611162618071-b39a2ec055fb?w=600&h=400&fit=crop&q=80',
              },
            ].map((item, i) => (
                <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="relative bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
              >
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={item.image}
                    alt={item.title}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  <div className="absolute bottom-4 left-4 text-5xl font-bold text-white/30">
                    {item.step}
                  </div>
                    </div>
                <div className="p-8">
                  <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center mb-6">
                    <item.icon className="w-6 h-6 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-3">{item.title}</h3>
                  <p className="text-gray-600">{item.description}</p>
                  </div>
                </motion.div>
            ))}
                  </div>
                  </div>
      </section>

      {/* Pricing Preview */}
      <section className="section bg-white">
        <div className="container">
                <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              The right plans, <GradientText>for the right price</GradientText>
            </h2>
            <p className="text-xl text-gray-600">
              Start free. Upgrade when you're ready.
            </p>
                </motion.div>

          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {[
              { name: 'Free', price: '$0', features: ['5 videos/month', '720p quality', 'Basic AI features'] },
              { name: 'Creator', price: '$19', features: ['30 videos/month', '1080p quality', 'All AI features', 'Virality Score'], popular: true },
              { name: 'Pro', price: '$49', features: ['100 videos/month', '4K quality', 'All features', 'Brand Kit', 'Priority support'] },
            ].map((plan, i) => (
                <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className={`relative bg-white rounded-2xl p-8 ${
                  plan.popular ? 'ring-2 ring-blue-500 shadow-lg' : 'border border-gray-200'
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-blue-600 text-white text-sm font-medium rounded-full">
                    Most Popular
                    </div>
                )}
                <h3 className="text-xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                <p className="text-4xl font-bold text-gray-900 mb-6">
                  {plan.price}<span className="text-lg font-normal text-gray-500">/mo</span>
                </p>
                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, j) => (
                    <li key={j} className="flex items-center gap-3 text-gray-600">
                      <Check className="w-5 h-5 text-green-500" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <Link
                  href="/pricing"
                  className={`block w-full py-3 text-center font-semibold rounded-xl transition-all ${
                    plan.popular
                      ? 'bg-blue-600 text-white hover:bg-blue-700'
                      : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                  }`}
                >
                  Get Started
                  </Link>
              </motion.div>
                    ))}
                  </div>
            </div>
      </section>

      {/* FAQ */}
      <section className="section bg-gray-50">
        <div className="container max-w-3xl">
                    <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Frequently asked questions
            </h2>
                    </motion.div>

          <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-200">
            <FAQItem
              question="How does the AI video generation work?"
              answer="Our 10 specialized AI agents work together to create your video. The Content Agent analyzes your prompt, the Video Agent generates visuals, the Music Agent creates a custom soundtrack, and other agents handle voice, editing, and optimization."
            />
            <FAQItem
              question="Can I use the videos commercially?"
              answer="Yes! All videos created with Taj Chat are yours to use commercially. Our AI-generated music is royalty-free, and you have full rights to all content you create."
            />
            <FAQItem
              question="What platforms can I publish to?"
              answer="Taj Chat supports direct publishing to TikTok, Instagram Reels, YouTube Shorts, Twitter/X, Facebook, and Threads. You can also download videos in any format."
            />
            <FAQItem
              question="Do I need video editing experience?"
              answer="Not at all! Taj Chat is designed for everyone. Just describe what you want, and our AI handles everything. Advanced users can also fine-tune every detail in our Studio."
            />
                </div>
                  </div>
      </section>

      {/* Final CTA */}
      <section className="section bg-gray-900">
        <div className="container max-w-4xl">
                    <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative bg-white rounded-3xl p-12 text-center"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Ready to create your first video?
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Join millions of creators using Taj Chat to grow their audience.
              Start free, no credit card required.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/create"
                className="btn-primary inline-flex items-center justify-center gap-2"
              >
                Start Creating Free
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                href="/gallery"
                className="btn-secondary inline-flex items-center justify-center gap-2"
              >
                <Play className="w-5 h-5" />
                Watch Examples
              </Link>
            </div>
                    </motion.div>
                </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-gray-200 bg-white">
        <div className="container">
          <div className="grid md:grid-cols-5 gap-8 mb-12">
            <div className="md:col-span-2">
              <Link href="/" className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-white" />
              </div>
                <span className="text-lg font-bold text-gray-900">Taj Chat</span>
                  </Link>
              <p className="text-gray-600 mb-4">
                AI-powered video creation for everyone. Create stunning videos in minutes.
              </p>
                    </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-4">Product</h4>
              <ul className="space-y-2">
                <li><Link href="/studio" className="text-gray-600 hover:text-gray-900 transition-colors">Studio</Link></li>
                <li><Link href="/templates" className="text-gray-600 hover:text-gray-900 transition-colors">Templates</Link></li>
                <li><Link href="/pricing" className="text-gray-600 hover:text-gray-900 transition-colors">Pricing</Link></li>
                <li><Link href="/gallery" className="text-gray-600 hover:text-gray-900 transition-colors">Gallery</Link></li>
              </ul>
              </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-4">Features</h4>
              <ul className="space-y-2">
                <li><Link href="/create" className="text-gray-600 hover:text-gray-900 transition-colors">AI Video Generator</Link></li>
                <li><Link href="/create" className="text-gray-600 hover:text-gray-900 transition-colors">AI Music Creator</Link></li>
                <li><Link href="/create" className="text-gray-600 hover:text-gray-900 transition-colors">Virality Score</Link></li>
                <li><Link href="/create" className="text-gray-600 hover:text-gray-900 transition-colors">Brand Kit</Link></li>
              </ul>
        </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-4">Company</h4>
              <ul className="space-y-2">
                <li><a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">About</a></li>
                <li><a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">Blog</a></li>
                <li><a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">Careers</a></li>
                <li><a href="#" className="text-gray-600 hover:text-gray-900 transition-colors">Contact</a></li>
              </ul>
    </div>
          </div>
          <div className="pt-8 border-t border-gray-200 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-500 text-sm">© 2024 Taj Chat. All rights reserved.</p>
            <div className="flex gap-6">
              <a href="#" className="text-gray-500 hover:text-gray-700 text-sm transition-colors">Privacy Policy</a>
              <a href="#" className="text-gray-500 hover:text-gray-700 text-sm transition-colors">Terms of Service</a>
                </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
