'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
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
} from 'lucide-react';

// Platform options
const platforms = [
  { id: 'tiktok', name: 'TikTok', icon: '🎵', color: 'from-pink-500 to-red-500', ratio: '9:16' },
  { id: 'instagram', name: 'Instagram Reels', icon: '📸', color: 'from-purple-500 to-pink-500', ratio: '9:16' },
  { id: 'youtube', name: 'YouTube Shorts', icon: '📺', color: 'from-red-500 to-red-600', ratio: '9:16' },
  { id: 'twitter', name: 'Twitter/X', icon: '🐦', color: 'from-blue-400 to-blue-500', ratio: '16:9' },
  { id: 'facebook', name: 'Facebook', icon: '👥', color: 'from-blue-600 to-blue-700', ratio: '1:1' },
];

// Video styles
const videoStyles = [
  { id: 'cinematic', name: 'Cinematic', preview: '🎬' },
  { id: 'energetic', name: 'Energetic', preview: '⚡' },
  { id: 'minimal', name: 'Minimal', preview: '✨' },
  { id: 'documentary', name: 'Documentary', preview: '📹' },
  { id: 'vintage', name: 'Vintage', preview: '📼' },
  { id: 'neon', name: 'Neon', preview: '🌈' },
];

// Music moods
const musicMoods = [
  { id: 'upbeat', name: 'Upbeat', emoji: '🎉' },
  { id: 'calm', name: 'Calm', emoji: '🌊' },
  { id: 'dramatic', name: 'Dramatic', emoji: '🎭' },
  { id: 'happy', name: 'Happy', emoji: '😊' },
  { id: 'inspirational', name: 'Inspirational', emoji: '✨' },
  { id: 'mysterious', name: 'Mysterious', emoji: '🔮' },
];

// Voice options
const voiceOptions = [
  { id: 'none', name: 'No Voice', icon: VolumeX },
  { id: 'ai-female', name: 'AI Female', icon: Volume2 },
  { id: 'ai-male', name: 'AI Male', icon: Volume2 },
  { id: 'clone', name: 'Clone Voice', icon: Wand2 },
];

export default function CreatePage() {
  const [step, setStep] = useState(1);
  const [prompt, setPrompt] = useState('');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['tiktok']);
  const [selectedStyle, setSelectedStyle] = useState('cinematic');
  const [selectedMood, setSelectedMood] = useState('upbeat');
  const [selectedVoice, setSelectedVoice] = useState('ai-female');
  const [duration, setDuration] = useState(30);
  const [isGenerating, setIsGenerating] = useState(false);
  const [inputType, setInputType] = useState<'prompt' | 'url' | 'upload'>('prompt');

  const togglePlatform = (id: string) => {
    setSelectedPlatforms(prev =>
      prev.includes(id)
        ? prev.filter(p => p !== id)
        : [...prev, id]
    );
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    // Simulate generation
    await new Promise(resolve => setTimeout(resolve, 3000));
    setIsGenerating(false);
    setStep(4);
  };

  const totalSteps = 3;
  const progress = (step / totalSteps) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-xl border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3">
              <div className="w-10 h-10 bg-black rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Taj Chat</span>
            </Link>

            {/* Progress indicator */}
            <div className="hidden md:flex items-center gap-4">
              {[1, 2, 3].map((s) => (
                <div key={s} className="flex items-center gap-2">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold text-sm ${
                    step >= s
                      ? 'bg-gradient-to-r from-pink-500 to-violet-500 text-white'
                      : 'bg-gray-100 text-gray-400'
                  }`}>
                    {step > s ? <Check className="w-4 h-4" /> : s}
                  </div>
                  <span className={`text-sm ${step >= s ? 'text-gray-900' : 'text-gray-400'}`}>
                    {s === 1 ? 'Content' : s === 2 ? 'Style' : 'Generate'}
                  </span>
                  {s < 3 && <div className={`w-12 h-0.5 ${step > s ? 'bg-pink-500' : 'bg-gray-200'}`} />}
                </div>
              ))}
            </div>

            <Link href="/" className="text-gray-600 hover:text-gray-900">
              Cancel
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
              >
                <div className="text-center mb-12">
                  <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                    What video do you want to create?
                  </h1>
                  <p className="text-xl text-gray-600">
                    Describe your idea, paste a URL, or upload content
                  </p>
                </div>

                {/* Input type selector */}
                <div className="flex justify-center gap-3 mb-8">
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
                          ? 'bg-gray-900 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      <type.icon className="w-4 h-4" />
                      {type.label}
                    </button>
                  ))}
                </div>

                {/* Input area */}
                <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200 mb-8">
                  {inputType === 'prompt' && (
                    <textarea
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      placeholder="Describe your video idea in detail...

Example: Create a 30-second product launch video for a new eco-friendly water bottle. Show the bottle in nature settings, highlight its features like being made from recycled materials, and end with a call to action."
                      className="w-full h-48 p-4 text-lg border-0 resize-none focus:outline-none focus:ring-0"
                    />
                  )}

                  {inputType === 'url' && (
                    <div className="space-y-4">
                      <input
                        type="url"
                        placeholder="Paste a blog post, article, or product page URL..."
                        className="w-full p-4 text-lg border-2 border-gray-200 rounded-xl focus:border-pink-500 focus:ring-4 focus:ring-pink-500/10 outline-none"
                      />
                      <p className="text-sm text-gray-500">
                        We'll extract the content and create a video from it automatically.
                      </p>
                    </div>
                  )}

                  {inputType === 'upload' && (
                    <div className="border-2 border-dashed border-gray-300 rounded-2xl p-12 text-center hover:border-pink-500 transition-colors cursor-pointer">
                      <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-lg font-medium text-gray-900 mb-2">
                        Drop your files here
                      </p>
                      <p className="text-gray-500 mb-4">
                        Support for images, videos, audio, and documents
                      </p>
                      <button className="px-6 py-2.5 bg-gray-100 text-gray-700 font-medium rounded-full hover:bg-gray-200 transition-colors">
                        Browse Files
                      </button>
                    </div>
                  )}
                </div>

                {/* Platform selection */}
                <div className="mb-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Select platforms
                  </h3>
                  <div className="flex flex-wrap gap-3">
                    {platforms.map((platform) => (
                      <button
                        key={platform.id}
                        onClick={() => togglePlatform(platform.id)}
                        className={`flex items-center gap-2 px-5 py-3 rounded-xl font-medium transition-all ${
                          selectedPlatforms.includes(platform.id)
                            ? 'bg-gradient-to-r ' + platform.color + ' text-white shadow-lg'
                            : 'bg-white text-gray-700 border border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        <span className="text-xl">{platform.icon}</span>
                        {platform.name}
                        {selectedPlatforms.includes(platform.id) && (
                          <Check className="w-4 h-4" />
                        )}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Duration slider */}
                <div className="bg-white rounded-2xl p-6 border border-gray-200">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Video Duration
                    </h3>
                    <span className="text-2xl font-bold text-gray-900">
                      {duration}s
                    </span>
                  </div>
                  <input
                    type="range"
                    min="15"
                    max="60"
                    value={duration}
                    onChange={(e) => setDuration(parseInt(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-full appearance-none cursor-pointer accent-pink-500"
                  />
                  <div className="flex justify-between text-sm text-gray-500 mt-2">
                    <span>15s</span>
                    <span>30s</span>
                    <span>45s</span>
                    <span>60s</span>
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
              >
                <div className="text-center mb-12">
                  <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                    Choose your style
                  </h1>
                  <p className="text-xl text-gray-600">
                    Select the visual style, music mood, and voice for your video
                  </p>
                </div>

                {/* Video Style */}
                <div className="mb-10">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Visual Style
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {videoStyles.map((style) => (
                      <button
                        key={style.id}
                        onClick={() => setSelectedStyle(style.id)}
                        className={`p-6 rounded-2xl text-center transition-all ${
                          selectedStyle === style.id
                            ? 'bg-gradient-to-br from-pink-500 to-violet-500 text-white shadow-lg shadow-pink-500/25'
                            : 'bg-white text-gray-700 border border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        <span className="text-4xl mb-3 block">{style.preview}</span>
                        <span className="font-medium">{style.name}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Music Mood */}
                <div className="mb-10">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Music Mood
                  </h3>
                  <div className="flex flex-wrap gap-3">
                    {musicMoods.map((mood) => (
                      <button
                        key={mood.id}
                        onClick={() => setSelectedMood(mood.id)}
                        className={`flex items-center gap-2 px-5 py-3 rounded-xl font-medium transition-all ${
                          selectedMood === mood.id
                            ? 'bg-gray-900 text-white'
                            : 'bg-white text-gray-700 border border-gray-200 hover:border-gray-300'
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
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Voice Over
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {voiceOptions.map((voice) => (
                      <button
                        key={voice.id}
                        onClick={() => setSelectedVoice(voice.id)}
                        className={`p-4 rounded-2xl text-center transition-all ${
                          selectedVoice === voice.id
                            ? 'bg-gray-900 text-white'
                            : 'bg-white text-gray-700 border border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        <voice.icon className="w-6 h-6 mx-auto mb-2" />
                        <span className="font-medium text-sm">{voice.name}</span>
                      </button>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {/* Step 3: Generate */}
            {step === 3 && (
              <motion.div
                key="step3"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <div className="text-center mb-12">
                  <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                    Ready to create your video
                  </h1>
                  <p className="text-xl text-gray-600">
                    Review your settings and let our AI agents work their magic
                  </p>
                </div>

                {/* Summary */}
                <div className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200 mb-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">Summary</h3>
                  
                  <div className="space-y-4">
                    <div className="flex justify-between py-3 border-b border-gray-100">
                      <span className="text-gray-600">Content</span>
                      <span className="text-gray-900 font-medium text-right max-w-md truncate">
                        {prompt || 'Text prompt'}
                      </span>
                    </div>
                    <div className="flex justify-between py-3 border-b border-gray-100">
                      <span className="text-gray-600">Platforms</span>
                      <span className="text-gray-900 font-medium">
                        {selectedPlatforms.map(p => platforms.find(pl => pl.id === p)?.name).join(', ')}
                      </span>
                    </div>
                    <div className="flex justify-between py-3 border-b border-gray-100">
                      <span className="text-gray-600">Duration</span>
                      <span className="text-gray-900 font-medium">{duration} seconds</span>
                    </div>
                    <div className="flex justify-between py-3 border-b border-gray-100">
                      <span className="text-gray-600">Style</span>
                      <span className="text-gray-900 font-medium">
                        {videoStyles.find(s => s.id === selectedStyle)?.name}
                      </span>
                    </div>
                    <div className="flex justify-between py-3 border-b border-gray-100">
                      <span className="text-gray-600">Music</span>
                      <span className="text-gray-900 font-medium">
                        {musicMoods.find(m => m.id === selectedMood)?.name}
                      </span>
                    </div>
                    <div className="flex justify-between py-3">
                      <span className="text-gray-600">Voice</span>
                      <span className="text-gray-900 font-medium">
                        {voiceOptions.find(v => v.id === selectedVoice)?.name}
                      </span>
                    </div>
                  </div>
                </div>

                {/* AI Agents */}
                <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl p-8 text-white mb-8">
                  <div className="flex items-center gap-3 mb-6">
                    <Bot className="w-6 h-6" />
                    <h3 className="text-lg font-semibold">10 AI Agents Ready</h3>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    {['Content', 'Video', 'Music', 'Voice', 'Editing', 'Image', 'Analytics', 'Safety', 'Social', 'Optimization'].map((agent, i) => (
                      <div key={i} className="flex items-center gap-2 text-sm">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                        <span className="text-gray-300">{agent}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Generate button */}
                <button
                  onClick={handleGenerate}
                  disabled={isGenerating}
                  className="w-full py-5 bg-gradient-to-r from-pink-500 to-violet-500 text-white text-xl font-semibold rounded-2xl hover:shadow-xl hover:shadow-pink-500/25 transition-all disabled:opacity-50 flex items-center justify-center gap-3"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="w-6 h-6 animate-spin" />
                      Creating your video...
                    </>
                  ) : (
                    <>
                      <Wand2 className="w-6 h-6" />
                      Generate Video
                    </>
                  )}
                </button>
              </motion.div>
            )}

            {/* Step 4: Result */}
            {step === 4 && (
              <motion.div
                key="step4"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
              >
                <div className="text-center mb-12">
                  <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <Check className="w-10 h-10 text-green-600" />
                  </div>
                  <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                    Your video is ready!
                  </h1>
                  <p className="text-xl text-gray-600">
                    Preview, edit, or publish directly to your platforms
                  </p>
                </div>

                {/* Video preview */}
                <div className="bg-gray-900 rounded-3xl overflow-hidden mb-8 aspect-[9/16] max-w-sm mx-auto">
                  <div className="w-full h-full flex items-center justify-center">
                    <button className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center hover:bg-white/30 transition-colors">
                      <Play className="w-8 h-8 text-white ml-1" />
                    </button>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
                  <Link
                    href="/studio"
                    className="flex-1 py-4 px-6 bg-white text-gray-900 font-semibold rounded-xl border border-gray-200 hover:bg-gray-50 transition-colors text-center"
                  >
                    Edit in Studio
                  </Link>
                  <button className="flex-1 py-4 px-6 bg-gradient-to-r from-pink-500 to-violet-500 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-pink-500/25 transition-all flex items-center justify-center gap-2">
                    <Share2 className="w-5 h-5" />
                    Publish
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>

      {/* Footer Navigation */}
      {step < 4 && (
        <footer className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-4 px-6">
          <div className="max-w-4xl mx-auto flex justify-between items-center">
            <button
              onClick={() => setStep(Math.max(1, step - 1))}
              disabled={step === 1}
              className="flex items-center gap-2 px-6 py-3 text-gray-600 font-medium hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ArrowLeft className="w-5 h-5" />
              Back
            </button>

            <div className="flex items-center gap-2">
              {[1, 2, 3].map((s) => (
                <div
                  key={s}
                  className={`w-2 h-2 rounded-full transition-colors ${
                    step >= s ? 'bg-pink-500' : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>

            <button
              onClick={() => setStep(Math.min(3, step + 1))}
              disabled={step === 3}
              className="flex items-center gap-2 px-6 py-3 bg-gray-900 text-white font-medium rounded-xl hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
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
