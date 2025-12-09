'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Sparkles,
  Zap,
  Layers,
  ArrowRight,
  Play,
  Pause,
  RotateCcw,
  Check,
  ChevronDown,
} from 'lucide-react'
import Button from '@/components/ui/Button'
import Card from '@/components/ui/Card'
import { useStore } from '@/lib/store'
import { api } from '@/lib/api'

const platforms = [
  { id: 'tiktok', name: 'TikTok', icon: '📱', color: 'from-[#00F2EA] to-[#FF0050]' },
  { id: 'instagram_reels', name: 'Instagram Reels', icon: '📸', color: 'from-[#F58529] via-[#DD2A7B] to-[#8134AF]' },
  { id: 'youtube_shorts', name: 'YouTube Shorts', icon: '▶️', color: 'from-[#FF0000] to-[#CC0000]' },
  { id: 'twitter', name: 'Twitter/X', icon: '🐦', color: 'from-[#1DA1F2] to-[#0D8BD9]' },
]

const workflowModes = [
  {
    id: 'hybrid',
    name: 'Hybrid',
    description: 'Balanced speed & quality',
    icon: Layers,
    recommended: true,
  },
  {
    id: 'sequential',
    name: 'Sequential',
    description: 'Best quality, step-by-step',
    icon: ArrowRight,
  },
  {
    id: 'parallel',
    name: 'Parallel',
    description: 'Fastest, concurrent processing',
    icon: Zap,
  },
]

const examplePrompts = [
  "Create an energetic motivational video about achieving goals with epic music",
  "Make a calming nature video with ambient sounds and peaceful imagery",
  "Generate a fun cooking tutorial for a quick breakfast smoothie",
  "Create an educational explainer about how AI works",
]

export default function VideoCreator() {
  const { createForm, updateCreateForm, addWorkflow } = useStore()
  const [isGenerating, setIsGenerating] = useState(false)
  const [showAdvanced, setShowAdvanced] = useState(false)

  const handleGenerate = async () => {
    if (!createForm.prompt.trim()) return

    setIsGenerating(true)

    try {
      const result = await api.createVideo({
        prompt: createForm.prompt,
        mode: createForm.mode,
        platforms: createForm.platforms,
      })

      addWorkflow({
        id: result.workflow_id,
        prompt: createForm.prompt,
        mode: createForm.mode,
        platforms: createForm.platforms,
        status: 'running',
        progress: 0,
        results: {},
        outputFiles: [],
        errors: [],
        startedAt: new Date(),
      })
    } catch (error) {
      console.error('Generation failed:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const togglePlatform = (platformId: string) => {
    const current = createForm.platforms
    if (current.includes(platformId)) {
      if (current.length > 1) {
        updateCreateForm({ platforms: current.filter(p => p !== platformId) })
      }
    } else {
      updateCreateForm({ platforms: [...current, platformId] })
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Main Input Card */}
      <Card variant="glass" className="p-8">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-display font-bold">Create Your Video</h2>
            <p className="text-sm text-muted-foreground">Describe what you want to create</p>
          </div>
        </div>

        {/* Prompt Input */}
        <div className="relative mb-6">
          <textarea
            value={createForm.prompt}
            onChange={(e) => updateCreateForm({ prompt: e.target.value })}
            placeholder="Describe your video... Be specific about the mood, style, content, and any text overlays you want."
            className="textarea-field min-h-[140px] text-base"
          />
          <div className="absolute bottom-3 right-3 text-xs text-muted-foreground">
            {createForm.prompt.length} / 2000
          </div>
        </div>

        {/* Example Prompts */}
        <div className="mb-6">
          <p className="text-xs text-muted-foreground mb-2">Try an example:</p>
          <div className="flex flex-wrap gap-2">
            {examplePrompts.map((prompt, i) => (
              <motion.button
                key={i}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => updateCreateForm({ prompt })}
                className="px-3 py-1.5 bg-white/5 hover:bg-white/10 border border-white/10
                  rounded-lg text-xs text-muted-foreground hover:text-white transition-all"
              >
                {prompt.slice(0, 40)}...
              </motion.button>
            ))}
          </div>
        </div>

        {/* Platforms */}
        <div className="mb-6">
          <p className="text-sm font-medium mb-3">Target Platforms</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {platforms.map((platform) => {
              const isSelected = createForm.platforms.includes(platform.id)
              return (
                <motion.button
                  key={platform.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => togglePlatform(platform.id)}
                  className={`
                    relative p-4 rounded-xl border transition-all duration-200
                    ${isSelected
                      ? 'border-primary/50 bg-primary/10'
                      : 'border-white/10 bg-white/5 hover:bg-white/10'
                    }
                  `}
                >
                  {isSelected && (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="absolute top-2 right-2 w-5 h-5 rounded-full bg-primary
                        flex items-center justify-center"
                    >
                      <Check className="w-3 h-3 text-white" />
                    </motion.div>
                  )}
                  <span className="text-2xl mb-2 block">{platform.icon}</span>
                  <span className="text-sm font-medium">{platform.name}</span>
                </motion.button>
              )
            })}
          </div>
        </div>

        {/* Workflow Mode */}
        <div className="mb-6">
          <p className="text-sm font-medium mb-3">Workflow Mode</p>
          <div className="grid grid-cols-3 gap-3">
            {workflowModes.map((mode) => {
              const isSelected = createForm.mode === mode.id
              const Icon = mode.icon
              return (
                <motion.button
                  key={mode.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => updateCreateForm({ mode: mode.id as any })}
                  className={`
                    relative p-4 rounded-xl border text-left transition-all duration-200
                    ${isSelected
                      ? 'border-primary/50 bg-primary/10'
                      : 'border-white/10 bg-white/5 hover:bg-white/10'
                    }
                  `}
                >
                  {mode.recommended && (
                    <span className="absolute -top-2 -right-2 px-2 py-0.5 bg-secondary
                      text-white text-xs font-medium rounded-full">
                      Recommended
                    </span>
                  )}
                  <Icon className={`w-5 h-5 mb-2 ${isSelected ? 'text-primary' : 'text-muted-foreground'}`} />
                  <p className="font-medium text-sm">{mode.name}</p>
                  <p className="text-xs text-muted-foreground">{mode.description}</p>
                </motion.button>
              )
            })}
          </div>
        </div>

        {/* Advanced Options Toggle */}
        <button
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex items-center gap-2 text-sm text-muted-foreground hover:text-white mb-4"
        >
          <ChevronDown className={`w-4 h-4 transition-transform ${showAdvanced ? 'rotate-180' : ''}`} />
          Advanced Options
        </button>

        <AnimatePresence>
          {showAdvanced && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="overflow-hidden mb-6"
            >
              <div className="grid grid-cols-2 gap-4 p-4 bg-white/5 rounded-xl">
                <div>
                  <label className="text-xs text-muted-foreground mb-1 block">Duration (seconds)</label>
                  <input type="number" defaultValue={30} className="input-field" />
                </div>
                <div>
                  <label className="text-xs text-muted-foreground mb-1 block">Aspect Ratio</label>
                  <select className="input-field">
                    <option value="9:16">9:16 (Vertical)</option>
                    <option value="16:9">16:9 (Horizontal)</option>
                    <option value="1:1">1:1 (Square)</option>
                  </select>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Generate Button */}
        <Button
          variant="gradient"
          size="lg"
          className="w-full"
          onClick={handleGenerate}
          isLoading={isGenerating}
          disabled={!createForm.prompt.trim()}
          leftIcon={<Sparkles className="w-5 h-5" />}
        >
          {isGenerating ? 'Generating...' : 'Generate Video'}
        </Button>
      </Card>

      {/* Info Cards */}
      <div className="grid grid-cols-3 gap-4">
        <Card variant="default" className="p-4 text-center">
          <div className="text-2xl font-bold gradient-text">10</div>
          <div className="text-xs text-muted-foreground">AI Agents</div>
        </Card>
        <Card variant="default" className="p-4 text-center">
          <div className="text-2xl font-bold gradient-text">~30s</div>
          <div className="text-xs text-muted-foreground">Avg. Generation</div>
        </Card>
        <Card variant="default" className="p-4 text-center">
          <div className="text-2xl font-bold gradient-text">4</div>
          <div className="text-xs text-muted-foreground">Platforms</div>
        </Card>
      </div>
    </div>
  )
}
