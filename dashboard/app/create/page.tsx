'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import {
  Sparkles,
  Video,
  Music,
  Image as ImageIcon,
  Type,
  Wand2,
  ArrowRight,
  ArrowLeft,
  Check,
  Globe,
  Clock,
  Zap,
  Upload,
  Link as LinkIcon,
  FileText,
  Play,
  Pause,
  Volume2,
  VolumeX,
  Settings,
  ChevronDown,
  Bot,
  Loader2,
  X,
  Copy,
  Mic,
  Languages,
  Subtitles,
  Instagram,
  Youtube,
  Twitter,
  Facebook,
  Linkedin,
  Smartphone,
  Monitor,
  Square,
  Share2,
  Download,
  Eye,
  TrendingUp,
  Star,
} from 'lucide-react';

// Platform options with modern design
const platforms = [
  { id: 'tiktok', name: 'TikTok', icon: Smartphone, color: 'from-pink-500 to-red-500', ratio: '9:16', description: 'Vertical short-form' },
  { id: 'instagram', name: 'Instagram Reels', icon: Instagram, color: 'from-purple-500 to-pink-500', ratio: '9:16', description: 'Stories & Reels' },
  { id: 'youtube', name: 'YouTube Shorts', icon: Youtube, color: 'from-red-500 to-red-600', ratio: '9:16', description: 'Vertical YouTube' },
  { id: 'youtube-long', name: 'YouTube', icon: Youtube, color: 'from-red-600 to-red-700', ratio: '16:9', description: 'Full-length videos' },
  { id: 'twitter', name: 'Twitter/X', icon: Twitter, color: 'from-gray-600 to-gray-800', ratio: '16:9', description: 'Viral content' },
  { id: 'facebook', name: 'Facebook', icon: Facebook, color: 'from-blue-500 to-blue-600', ratio: '1:1', description: 'Social sharing' },
];

// Video styles with previews
const videoStyles = [
  { id: 'cinematic', name: 'Cinematic', preview: '🎬', desc: 'Hollywood-style quality' },
  { id: 'energetic', name: 'Energetic', preview: '⚡', desc: 'Fast cuts, high energy' },
  { id: 'minimal', name: 'Minimal', preview: '✨', desc: 'Clean and modern' },
  { id: 'documentary', name: 'Documentary', preview: '📹', desc: 'Authentic storytelling' },
  { id: 'vintage', name: 'Vintage', preview: '📼', desc: 'Retro aesthetic' },
  { id: 'neon', name: 'Neon', preview: '🌈', desc: 'Cyberpunk vibes' },
];

// Music moods with better descriptions
const musicMoods = [
  { id: 'upbeat', name: 'Upbeat', emoji: '🎉', color: 'from-orange-500 to-yellow-500' },
  { id: 'calm', name: 'Calm', emoji: '🌊', color: 'from-blue-400 to-cyan-400' },
  { id: 'dramatic', name: 'Dramatic', emoji: '🎭', color: 'from-red-600 to-purple-600' },
  { id: 'happy', name: 'Happy', emoji: '😊', color: 'from-yellow-400 to-orange-400' },
  { id: 'inspirational', name: 'Inspirational', emoji: '✨', color: 'from-violet-500 to-pink-500' },
  { id: 'mysterious', name: 'Mysterious', emoji: '🔮', color: 'from-purple-600 to-indigo-600' },
  { id: 'corporate', name: 'Corporate', emoji: '💼', color: 'from-blue-500 to-blue-600' },
  { id: 'trending', name: 'Trending', emoji: '🔥', color: 'from-pink-500 to-red-500' },
];

// Voice options with language support
const voiceOptions = [
  { id: 'none', name: 'No Voiceover', icon: VolumeX, desc: 'Music only' },
  { id: 'ai-female', name: 'AI Female', icon: Volume2, desc: '50+ languages' },
  { id: 'ai-male', name: 'AI Male', icon: Volume2, desc: '50+ languages' },
  { id: 'clone', name: 'Clone Voice', icon: Wand2, desc: 'Your voice, AI-powered' },
];

// Prompt examples for inspiration
const promptExamples = [
  { text: 'Create a 30-second product showcase for a smartwatch with futuristic transitions', category: 'Product' },
  { text: 'Make a motivational morning routine video with energetic music', category: 'Lifestyle' },
  { text: 'Generate a travel vlog intro for Bali with cinematic drone shots', category: 'Travel' },
  { text: 'Create an educational explainer about AI technology for beginners', category: 'Education' },
];

export default function CreatePage() {
  const searchParams = useSearchParams();
  const [step, setStep] = useState(1);
  const [prompt, setPrompt] = useState(searchParams?.get('prompt') || '');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['tiktok']);
  const [selectedStyle, setSelectedStyle] = useState('cinematic');
  const [selectedMood, setSelectedMood] = useState('upbeat');
  const [selectedVoice, setSelectedVoice] = useState('ai-female');
  const [duration, setDuration] = useState(30);
  const [isGenerating, setIsGenerating] = useState(false);
  const [inputType, setInputType] = useState<'prompt' | 'url' | 'upload'>('prompt');
  const [generatingProgress, setGeneratingProgress] = useState(0);
  const [currentAgent, setCurrentAgent] = useState('');

  const togglePlatform = (id: string) => {
    setSelectedPlatforms(prev =>
      prev.includes(id)
        ? prev.filter(p => p !== id)
        : [...prev, id]
    );
  };

  const copyPrompt = (text: string) => {
    setPrompt(text);
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    setGeneratingProgress(0);

    // Simulate agent processing
    const agents = [
      'Content Analysis',
      'Storyboard Generation',
      'Video Generation',
      'Music Generation',
      'Voice Synthesis',
      'Editing & Effects',
      'Optimization',
      'Safety Check',
      'Final Render'
    ];

    for (let i = 0; i < agents.length; i++) {
      setCurrentAgent(agents[i]);
      setGeneratingProgress((i + 1) / agents.length * 100);
      await new Promise(resolve => setTimeout(resolve, 400));
    }

    setIsGenerating(false);
    setStep(4);
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-black/95 backdrop-blur-xl border-b border-white/10">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-violet-500 to-fuchsia-500 rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold">Taj Chat</span>
            </Link>

            {/* Progress indicator */}
            <div className="hidden md:flex items-center gap-4">
              {[
                { num: 1, label: 'Content' },
                { num: 2, label: 'Style' },
                { num: 3, label: 'Generate' }
              ].map((s, i) => (
                <div key={s.num} className="flex items-center gap-3">
                  <div className={`flex items-center gap-2 ${step >= s.num ? 'text-white' : 'text-white/40'}`}>
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold text-sm transition-all ${
                      step > s.num
                        ? 'bg-green-500 text-white'
                        : step === s.num
                        ? 'bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white'
                        : 'bg-white/10 text-white/40'
                    }`}>
                      {step > s.num ? <Check className="w-4 h-4" /> : s.num}
                    </div>
                    <span className="text-sm font-medium">{s.label}</span>
                  </div>
                  {i < 2 && (
                    <div className={`w-12 h-0.5 ${step > s.num ? 'bg-green-500' : 'bg-white/10'}`} />
                  )}
                </div>
              ))}
            </div>

            <Link href="/" className="text-white/60 hover:text-white transition-colors">
              <X className="w-6 h-6" />
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-24 pb-32 px-6">
        <div className="max-w-4xl mx-auto">
          <AnimatePresence mode="wait">
            {/* Step 1: Content Input */}
            {step === 1 && (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                <div className="text-center">
                  <h1 className="text-4xl md:text-5xl font-bold mb-4">
                    What will you create?
                  </h1>
                  <p className="text-xl text-white/60">
                    Describe your idea, paste a URL, or upload content
                  </p>
                </div>

                {/* Input type selector */}
                <div className="flex justify-center gap-3">
                  {[
                    { id: 'prompt', label: 'Text Prompt', icon: Type },
                    { id: 'url', label: 'URL to Video', icon: LinkIcon },
                    { id: 'upload', label: 'Upload', icon: Upload },
                  ].map((type) => (
                    <button
                      key={type.id}
                      onClick={() => setInputType(type.id as any)}
                      className={`flex items-center gap-2 px-5 py-2.5 rounded-full font-medium transition-all ${
                        inputType === type.id
                          ? 'bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white'
                          : 'bg-white/5 text-white/70 hover:bg-white/10 hover:text-white'
                      }`}
                    >
                      <type.icon className="w-4 h-4" />
                      {type.label}
                    </button>
                  ))}
                </div>

                {/* Input area */}
                <div className="relative bg-white/5 rounded-2xl border border-white/10 overflow-hidden">
                  {inputType === 'prompt' && (
                    <>
                      <div className="absolute top-4 left-6 flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                        <span className="text-xs text-white/40">10 AI Agents Ready</span>
                      </div>
                      <textarea
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        placeholder="Describe your video idea in detail..."
                        className="w-full h-40 pt-12 px-6 pb-4 bg-transparent text-white placeholder:text-white/30 resize-none focus:outline-none text-lg"
                      />
                    </>
                  )}

                  {inputType === 'url' && (
                    <div className="p-6 space-y-4">
                      <input
                        type="url"
                        placeholder="Paste a blog post, article, or product page URL..."
                        className="w-full p-4 text-lg bg-white/5 border border-white/10 rounded-xl focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 outline-none text-white placeholder:text-white/30"
                      />
                      <p className="text-sm text-white/40">
                        We'll extract the content and create a video from it automatically.
                      </p>
                    </div>
                  )}

                  {inputType === 'upload' && (
                    <div className="p-8 text-center">
                      <div className="border-2 border-dashed border-white/20 rounded-2xl p-12 hover:border-violet-500/50 transition-colors cursor-pointer">
                        <Upload className="w-12 h-12 text-white/40 mx-auto mb-4" />
                        <p className="text-lg font-medium mb-2">
                          Drop your files here
                        </p>
                        <p className="text-white/50 mb-4">
                          Support for images, videos, audio, and documents
                        </p>
                        <button className="px-6 py-2.5 bg-white/10 text-white font-medium rounded-full hover:bg-white/20 transition-colors">
                          Browse Files
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                {/* Prompt Examples */}
                {inputType === 'prompt' && (
                  <div>
                    <p className="text-sm text-white/40 mb-3">Try these examples:</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {promptExamples.map((example, i) => (
                        <button
                          key={i}
                          onClick={() => copyPrompt(example.text)}
                          className="flex items-start gap-3 p-4 rounded-xl bg-white/5 border border-white/10 hover:border-violet-500/50 text-left transition-all group"
                        >
                          <Copy className="w-4 h-4 text-white/40 group-hover:text-violet-400 mt-0.5 flex-shrink-0" />
                          <div>
                            <span className="text-xs text-violet-400 font-medium">{example.category}</span>
                            <p className="text-sm text-white/70 group-hover:text-white/90 line-clamp-2">{example.text}</p>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Platform selection */}
                <div>
                  <h3 className="text-lg font-semibold mb-4">Select platforms</h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {platforms.map((platform) => (
                      <button
                        key={platform.id}
                        onClick={() => togglePlatform(platform.id)}
                        className={`flex items-center gap-3 p-4 rounded-xl transition-all ${
                          selectedPlatforms.includes(platform.id)
                            ? `bg-gradient-to-r ${platform.color} text-white shadow-lg`
                            : 'bg-white/5 text-white/70 border border-white/10 hover:border-white/20'
                        }`}
                      >
                        <platform.icon className="w-5 h-5" />
                        <div className="text-left">
                          <p className="font-medium text-sm">{platform.name}</p>
                          <p className="text-xs opacity-70">{platform.description}</p>
                        </div>
                        {selectedPlatforms.includes(platform.id) && (
                          <Check className="w-4 h-4 ml-auto" />
                        )}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Duration slider */}
                <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Clock className="w-5 h-5 text-violet-400" />
                      <h3 className="font-semibold">Video Duration</h3>
                    </div>
                    <span className="text-2xl font-bold text-violet-400">{duration}s</span>
                  </div>
                  <input
                    type="range"
                    min="15"
                    max="120"
                    step="5"
                    value={duration}
                    onChange={(e) => setDuration(parseInt(e.target.value))}
                    className="w-full h-2 bg-white/10 rounded-full appearance-none cursor-pointer accent-violet-500"
                  />
                  <div className="flex justify-between text-sm text-white/40 mt-2">
                    <span>15s</span>
                    <span>30s</span>
                    <span>60s</span>
                    <span>120s</span>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Step 2: Style Selection */}
            {step === 2 && (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                <div className="text-center">
                  <h1 className="text-4xl md:text-5xl font-bold mb-4">
                    Define your style
                  </h1>
                  <p className="text-xl text-white/60">
                    Choose visuals, music, and voice for your video
                  </p>
                </div>

                {/* Video Style */}
                <div>
                  <h3 className="text-lg font-semibold mb-4">Visual Style</h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {videoStyles.map((style) => (
                      <button
                        key={style.id}
                        onClick={() => setSelectedStyle(style.id)}
                        className={`p-6 rounded-2xl text-center transition-all ${
                          selectedStyle === style.id
                            ? 'bg-gradient-to-br from-violet-600 to-fuchsia-600 text-white shadow-lg shadow-violet-500/25'
                            : 'bg-white/5 text-white/70 border border-white/10 hover:border-white/20'
                        }`}
                      >
                        <span className="text-4xl mb-3 block">{style.preview}</span>
                        <span className="font-medium block">{style.name}</span>
                        <span className="text-xs opacity-60 mt-1 block">{style.desc}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Music Mood */}
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <Music className="w-5 h-5 text-violet-400" />
                    <h3 className="text-lg font-semibold">Music Mood</h3>
                  </div>
                  <div className="flex flex-wrap gap-3">
                    {musicMoods.map((mood) => (
                      <button
                        key={mood.id}
                        onClick={() => setSelectedMood(mood.id)}
                        className={`flex items-center gap-2 px-5 py-3 rounded-xl font-medium transition-all ${
                          selectedMood === mood.id
                            ? `bg-gradient-to-r ${mood.color} text-white shadow-lg`
                            : 'bg-white/5 text-white/70 border border-white/10 hover:border-white/20'
                        }`}
                      >
                        <span>{mood.emoji}</span>
                        {mood.name}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Voice Selection */}
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <Mic className="w-5 h-5 text-violet-400" />
                    <h3 className="text-lg font-semibold">Voice Over</h3>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {voiceOptions.map((voice) => (
                      <button
                        key={voice.id}
                        onClick={() => setSelectedVoice(voice.id)}
                        className={`p-4 rounded-2xl text-center transition-all ${
                          selectedVoice === voice.id
                            ? 'bg-gradient-to-br from-violet-600 to-fuchsia-600 text-white shadow-lg'
                            : 'bg-white/5 text-white/70 border border-white/10 hover:border-white/20'
                        }`}
                      >
                        <voice.icon className="w-6 h-6 mx-auto mb-2" />
                        <span className="font-medium text-sm block">{voice.name}</span>
                        <span className="text-xs opacity-60 mt-1 block">{voice.desc}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Additional Features */}
                <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
                  <h3 className="font-semibold mb-4">AI Features</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                      { icon: Subtitles, name: 'Auto Captions', active: true },
                      { icon: Languages, name: 'Translate', active: false },
                      { icon: TrendingUp, name: 'Virality Score', active: true },
                      { icon: Wand2, name: 'AI B-Roll', active: true },
                    ].map((feature, i) => (
                      <div
                        key={i}
                        className={`flex items-center gap-3 p-3 rounded-xl ${
                          feature.active ? 'bg-violet-500/20 text-violet-400' : 'bg-white/5 text-white/40'
                        }`}
                      >
                        <feature.icon className="w-5 h-5" />
                        <span className="text-sm font-medium">{feature.name}</span>
                        {feature.active && <Check className="w-4 h-4 ml-auto" />}
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {/* Step 3: Generate */}
            {step === 3 && !isGenerating && (
              <motion.div
                key="step3"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="space-y-8"
              >
                <div className="text-center">
                  <h1 className="text-4xl md:text-5xl font-bold mb-4">
                    Ready to create
                  </h1>
                  <p className="text-xl text-white/60">
                    Review your settings and let our AI agents work their magic
                  </p>
                </div>

                {/* Summary */}
                <div className="bg-white/5 rounded-2xl p-8 border border-white/10">
                  <h3 className="font-semibold mb-6">Summary</h3>
                  <div className="space-y-4">
                    {[
                      { label: 'Content', value: prompt || 'Text prompt' },
                      { label: 'Platforms', value: selectedPlatforms.map(p => platforms.find(pl => pl.id === p)?.name).join(', ') },
                      { label: 'Duration', value: `${duration} seconds` },
                      { label: 'Style', value: videoStyles.find(s => s.id === selectedStyle)?.name },
                      { label: 'Music', value: musicMoods.find(m => m.id === selectedMood)?.name },
                      { label: 'Voice', value: voiceOptions.find(v => v.id === selectedVoice)?.name },
                    ].map((item, i) => (
                      <div key={i} className="flex justify-between py-3 border-b border-white/5 last:border-0">
                        <span className="text-white/50">{item.label}</span>
                        <span className="text-white font-medium text-right max-w-xs truncate">{item.value}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* AI Agents Card */}
                <div className="bg-gradient-to-br from-violet-600/20 to-fuchsia-600/20 rounded-2xl p-8 border border-violet-500/30">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="w-12 h-12 bg-gradient-to-br from-violet-500 to-fuchsia-500 rounded-xl flex items-center justify-center">
                      <Bot className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="font-bold text-lg">10 AI Agents Ready</h3>
                      <p className="text-white/60 text-sm">Working together to create your video</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                    {['Content', 'Video', 'Music', 'Voice', 'Editing', 'Image', 'Analytics', 'Safety', 'Social', 'Optimization'].map((agent, i) => (
                      <div key={i} className="flex items-center gap-2 text-sm bg-black/20 px-3 py-2 rounded-lg">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                        <span className="text-white/70">{agent}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Generate button */}
                <button
                  onClick={handleGenerate}
                  className="w-full py-5 bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white text-xl font-bold rounded-2xl hover:shadow-xl hover:shadow-violet-500/25 transition-all flex items-center justify-center gap-3"
                >
                  <Wand2 className="w-6 h-6" />
                  Generate Video
                </button>
              </motion.div>
            )}

            {/* Generating Animation */}
            {step === 3 && isGenerating && (
              <motion.div
                key="generating"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center py-20"
              >
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
                  className="w-24 h-24 mx-auto mb-8 relative"
                >
                  <div className="absolute inset-0 rounded-full bg-gradient-to-r from-violet-500 via-fuchsia-500 to-violet-500 animate-pulse" />
                  <div className="absolute inset-2 rounded-full bg-black flex items-center justify-center">
                    <Sparkles className="w-8 h-8 text-white" />
                  </div>
                </motion.div>
                <h2 className="text-3xl font-bold mb-4">Creating your video...</h2>
                <p className="text-white/60 mb-8">{currentAgent}</p>
                <div className="max-w-md mx-auto">
                  <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-violet-500 to-fuchsia-500 rounded-full"
                      animate={{ width: `${generatingProgress}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                  <p className="text-sm text-white/40 mt-2">{Math.round(generatingProgress)}% complete</p>
                </div>
              </motion.div>
            )}

            {/* Step 4: Result */}
            {step === 4 && (
              <motion.div
                key="step4"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center space-y-8"
              >
                <div>
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6"
                  >
                    <Check className="w-10 h-10 text-white" />
                  </motion.div>
                  <h1 className="text-4xl md:text-5xl font-bold mb-4">
                    Your video is ready!
                  </h1>
                  <p className="text-xl text-white/60">
                    Preview, edit, or publish directly to your platforms
                  </p>
                </div>

                {/* Video preview */}
                <div className="bg-gray-900 rounded-3xl overflow-hidden aspect-[9/16] max-w-xs mx-auto relative group">
                  <img
                    src="https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=400&h=711&fit=crop"
                    alt="Preview"
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <button className="w-20 h-20 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center hover:bg-white/30 transition-colors border border-white/30">
                      <Play className="w-8 h-8 text-white ml-1" fill="white" />
                    </button>
                  </div>
                  <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between text-white/80 text-sm">
                    <div className="flex items-center gap-2">
                      <Eye className="w-4 h-4" />
                      <span>Preview</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Star className="w-4 h-4 text-amber-400" />
                      <span>87/100 Virality Score</span>
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
                  <Link
                    href="/studio"
                    className="flex-1 py-4 px-6 bg-white/10 text-white font-semibold rounded-xl border border-white/20 hover:bg-white/20 transition-colors text-center"
                  >
                    Edit in Studio
                  </Link>
                  <button className="flex-1 py-4 px-6 bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-violet-500/25 transition-all flex items-center justify-center gap-2">
                    <Share2 className="w-5 h-5" />
                    Publish
                  </button>
                </div>

                <div className="flex items-center justify-center gap-4">
                  <button className="flex items-center gap-2 text-white/60 hover:text-white transition-colors">
                    <Download className="w-5 h-5" />
                    Download
                  </button>
                  <button
                    onClick={() => { setStep(1); setPrompt(''); }}
                    className="flex items-center gap-2 text-white/60 hover:text-white transition-colors"
                  >
                    <Wand2 className="w-5 h-5" />
                    Create Another
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>

      {/* Footer Navigation */}
      {step < 4 && !isGenerating && (
        <footer className="fixed bottom-0 left-0 right-0 bg-black/95 backdrop-blur-xl border-t border-white/10 py-4 px-6">
          <div className="max-w-4xl mx-auto flex justify-between items-center">
            <button
              onClick={() => setStep(Math.max(1, step - 1))}
              disabled={step === 1}
              className="flex items-center gap-2 px-6 py-3 text-white/60 font-medium hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              Back
            </button>

            <div className="flex items-center gap-2">
              {[1, 2, 3].map((s) => (
                <div
                  key={s}
                  className={`w-2 h-2 rounded-full transition-colors ${
                    step >= s ? 'bg-gradient-to-r from-violet-500 to-fuchsia-500' : 'bg-white/20'
                  }`}
                />
              ))}
            </div>

            <button
              onClick={() => setStep(Math.min(3, step + 1))}
              disabled={step === 3 || (step === 1 && !prompt.trim())}
              className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-violet-600 to-fuchsia-600 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-violet-500/25 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              Next
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </footer>
      )}
    </div>
  );
}
