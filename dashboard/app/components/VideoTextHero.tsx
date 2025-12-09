'use client';

import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';

interface VideoTextHeroProps {
  text: string;
  videoSrc?: string;
  fallbackImage?: string;
}

// Videos that will play inside the text
const showcaseVideos = [
  'https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-traffic-at-night-11-large.mp4',
  'https://assets.mixkit.co/videos/preview/mixkit-woman-running-above-the-camera-on-a-running-track-32807-large.mp4',
  'https://assets.mixkit.co/videos/preview/mixkit-going-down-a-curved-highway-through-a-mountain-range-41576-large.mp4',
];

export function VideoTextHero({ text, videoSrc, fallbackImage }: VideoTextHeroProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0);

  useEffect(() => {
    // Rotate videos every 5 seconds
    const interval = setInterval(() => {
      setCurrentVideoIndex((prev) => (prev + 1) % showcaseVideos.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.play().catch(() => {
        // Autoplay might be blocked
      });
    }
  }, [currentVideoIndex]);

  return (
    <div className="relative w-full overflow-hidden">
      {/* Video Background that shows through text */}
      <div className="absolute inset-0 z-0">
        <video
          ref={videoRef}
          key={currentVideoIndex}
          autoPlay
          muted
          loop
          playsInline
          className="w-full h-full object-cover"
          onLoadedData={() => setIsLoaded(true)}
        >
          <source src={videoSrc || showcaseVideos[currentVideoIndex]} type="video/mp4" />
        </video>
        {/* Fallback gradient if video doesn't load */}
        {!isLoaded && (
          <div className="absolute inset-0 bg-gradient-to-br from-pink-500 via-purple-500 to-violet-600 animate-gradient" />
        )}
      </div>

      {/* Text mask - video shows through the text */}
      <div className="relative z-10">
        <h1
          className="text-[12vw] md:text-[10vw] lg:text-[8vw] font-black tracking-tighter leading-none text-center uppercase"
          style={{
            background: 'white',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            mixBlendMode: 'difference',
          }}
        >
          {text}
        </h1>
      </div>

      {/* Overlay gradient for better readability */}
      <div className="absolute inset-0 bg-gradient-to-b from-white/20 via-transparent to-white/20 pointer-events-none z-20" />
    </div>
  );
}

// Alternative: CSS-based video text effect (more compatible)
export function VideoTextMask({ line1, line2 }: { line1: string; line2: string }) {
  const [currentVideo, setCurrentVideo] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentVideo((prev) => (prev + 1) % showcaseVideos.length);
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative py-8 md:py-12">
      {/* First line with video background */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative overflow-hidden"
      >
        <div className="relative">
          {/* Video container */}
          <div className="absolute inset-0 overflow-hidden rounded-lg">
            <video
              key={currentVideo}
              autoPlay
              muted
              loop
              playsInline
              className="w-full h-full object-cover scale-150"
            >
              <source src={showcaseVideos[currentVideo]} type="video/mp4" />
            </video>
          </div>

          {/* Text with video clip mask */}
          <h1
            className="relative text-[15vw] md:text-[12vw] lg:text-[10vw] font-black tracking-tighter leading-[0.85] text-center uppercase"
            style={{
              WebkitTextStroke: '2px rgba(0,0,0,0.1)',
              color: 'transparent',
              backgroundImage: `url(${showcaseVideos[currentVideo].replace('.mp4', '.jpg')})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              WebkitBackgroundClip: 'text',
              backgroundClip: 'text',
            }}
          >
            {line1}
          </h1>
        </div>
      </motion.div>

      {/* Second line - solid color */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <h1 className="text-[15vw] md:text-[12vw] lg:text-[10vw] font-black tracking-tighter leading-[0.85] text-center uppercase text-gray-200">
          {line2}
        </h1>
      </motion.div>
    </div>
  );
}

// Video Wall Component - Grid of video showcases
export function VideoWall() {
  const videos = [
    {
      thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=400&h=600&fit=crop',
      title: 'Product Launch',
      category: 'Marketing',
      views: '2.4M',
    },
    {
      thumbnail: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&h=600&fit=crop',
      title: 'AI Art Tutorial',
      category: 'Education',
      views: '1.8M',
    },
    {
      thumbnail: 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=400&h=600&fit=crop',
      title: 'Tech Review',
      category: 'Technology',
      views: '3.2M',
    },
    {
      thumbnail: 'https://images.unsplash.com/photo-1614850523459-c2f4c699c52e?w=400&h=600&fit=crop',
      title: 'Fitness Journey',
      category: 'Health',
      views: '4.1M',
    },
    {
      thumbnail: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=600&fit=crop',
      title: 'Travel Vlog',
      category: 'Lifestyle',
      views: '1.2M',
    },
    {
      thumbnail: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=600&fit=crop',
      title: 'Music Video',
      category: 'Entertainment',
      views: '5.6M',
    },
    {
      thumbnail: 'https://images.unsplash.com/photo-1504805572947-34fad45aed93?w=400&h=600&fit=crop',
      title: 'Motivation',
      category: 'Inspiration',
      views: '2.9M',
    },
    {
      thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=600&fit=crop',
      title: 'Business Tips',
      category: 'Business',
      views: '1.5M',
    },
  ];

  return (
    <div className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            See what creators are making
          </h2>
          <p className="text-xl text-gray-600">
            Join millions creating viral content with Taj Chat
          </p>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {videos.map((video, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.05, zIndex: 10 }}
              className="relative group cursor-pointer"
            >
              <div className="relative aspect-[9/16] rounded-2xl overflow-hidden shadow-lg">
                <img
                  src={video.thumbnail}
                  alt={video.title}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />

                {/* Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

                {/* Play button */}
                <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                  <div className="w-14 h-14 bg-white/90 rounded-full flex items-center justify-center shadow-xl transform scale-75 group-hover:scale-100 transition-transform">
                    <svg className="w-6 h-6 text-gray-900 ml-1" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                    </svg>
                  </div>
                </div>

                {/* Info */}
                <div className="absolute bottom-0 left-0 right-0 p-4 transform translate-y-full group-hover:translate-y-0 transition-transform">
                  <span className="inline-block px-2 py-1 bg-pink-500 text-white text-xs font-medium rounded-full mb-2">
                    {video.category}
                  </span>
                  <p className="text-white font-semibold text-sm">{video.title}</p>
                  <p className="text-white/70 text-xs">{video.views} views</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Animated Feature Cards with Video Preview
export function FeatureShowcase() {
  const features = [
    {
      title: 'AI Video Generation',
      description: 'Generate stunning videos from text prompts',
      video: 'https://assets.mixkit.co/videos/preview/mixkit-hands-typing-on-a-laptop-in-an-office-4492-large.mp4',
      gradient: 'from-pink-500 to-rose-600',
    },
    {
      title: 'AI Music Creation',
      description: 'Create custom royalty-free soundtracks',
      video: 'https://assets.mixkit.co/videos/preview/mixkit-dj-mixing-at-a-nightclub-4477-large.mp4',
      gradient: 'from-violet-500 to-purple-600',
    },
    {
      title: 'Voice Cloning',
      description: 'Clone your voice for AI narration',
      video: 'https://assets.mixkit.co/videos/preview/mixkit-woman-talking-on-a-podcast-4800-large.mp4',
      gradient: 'from-blue-500 to-cyan-600',
    },
    {
      title: 'AI Avatars',
      description: 'Create digital spokespersons',
      video: 'https://assets.mixkit.co/videos/preview/mixkit-woman-dancing-happily-at-a-party-4800-large.mp4',
      gradient: 'from-amber-500 to-orange-600',
    },
  ];

  return (
    <div className="py-20">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="group relative bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-shadow"
            >
              {/* Video Background */}
              <div className="relative h-64 overflow-hidden">
                <video
                  autoPlay
                  muted
                  loop
                  playsInline
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                >
                  <source src={feature.video} type="video/mp4" />
                </video>
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />

                {/* Play indicator */}
                <div className="absolute top-4 right-4 px-3 py-1 bg-black/50 backdrop-blur-sm rounded-full text-white text-xs flex items-center gap-1">
                  <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
                  Live Preview
                </div>
              </div>

              {/* Content */}
              <div className="p-8">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-4 shadow-lg`}>
                  <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default VideoTextHero;
