import { create } from 'zustand'

interface Agent {
  type: string
  name: string
  status: 'idle' | 'running' | 'completed' | 'error'
  progress: number
  lastResult?: any
}

interface Workflow {
  id: string
  prompt: string
  mode: 'sequential' | 'parallel' | 'hybrid'
  platforms: string[]
  status: 'pending' | 'running' | 'completed' | 'error'
  progress: number
  currentAgent?: string
  results: Record<string, any>
  outputFiles: string[]
  errors: string[]
  startedAt?: Date
  completedAt?: Date
}

interface AppState {
  // Agents
  agents: Record<string, Agent>
  setAgents: (agents: Record<string, Agent>) => void
  updateAgent: (type: string, updates: Partial<Agent>) => void

  // Workflows
  workflows: Workflow[]
  activeWorkflow: Workflow | null
  addWorkflow: (workflow: Workflow) => void
  updateWorkflow: (id: string, updates: Partial<Workflow>) => void
  setActiveWorkflow: (workflow: Workflow | null) => void

  // UI State
  sidebarCollapsed: boolean
  toggleSidebar: () => void

  // Create form
  createForm: {
    prompt: string
    mode: 'sequential' | 'parallel' | 'hybrid'
    platforms: string[]
  }
  updateCreateForm: (updates: Partial<AppState['createForm']>) => void
  resetCreateForm: () => void
}

const defaultAgents: Record<string, Agent> = {
  content_analysis: { type: 'content_analysis', name: 'Content Analysis', status: 'idle', progress: 0 },
  video_generation: { type: 'video_generation', name: 'Video Generation', status: 'idle', progress: 0 },
  music_generation: { type: 'music_generation', name: 'Music Generation', status: 'idle', progress: 0 },
  image_generation: { type: 'image_generation', name: 'Image Generation', status: 'idle', progress: 0 },
  voice_speech: { type: 'voice_speech', name: 'Voice & Speech', status: 'idle', progress: 0 },
  editing: { type: 'editing', name: 'Editing', status: 'idle', progress: 0 },
  optimization: { type: 'optimization', name: 'Optimization', status: 'idle', progress: 0 },
  analytics: { type: 'analytics', name: 'Analytics', status: 'idle', progress: 0 },
  safety: { type: 'safety', name: 'Safety', status: 'idle', progress: 0 },
  social_media: { type: 'social_media', name: 'Social Media', status: 'idle', progress: 0 },
}

export const useStore = create<AppState>((set) => ({
  // Agents
  agents: defaultAgents,
  setAgents: (agents) => set({ agents }),
  updateAgent: (type, updates) =>
    set((state) => ({
      agents: {
        ...state.agents,
        [type]: { ...state.agents[type], ...updates },
      },
    })),

  // Workflows
  workflows: [],
  activeWorkflow: null,
  addWorkflow: (workflow) =>
    set((state) => ({
      workflows: [workflow, ...state.workflows],
      activeWorkflow: workflow,
    })),
  updateWorkflow: (id, updates) =>
    set((state) => ({
      workflows: state.workflows.map((w) =>
        w.id === id ? { ...w, ...updates } : w
      ),
      activeWorkflow:
        state.activeWorkflow?.id === id
          ? { ...state.activeWorkflow, ...updates }
          : state.activeWorkflow,
    })),
  setActiveWorkflow: (workflow) => set({ activeWorkflow: workflow }),

  // UI State
  sidebarCollapsed: false,
  toggleSidebar: () =>
    set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

  // Create form
  createForm: {
    prompt: '',
    mode: 'hybrid',
    platforms: ['tiktok'],
  },
  updateCreateForm: (updates) =>
    set((state) => ({
      createForm: { ...state.createForm, ...updates },
    })),
  resetCreateForm: () =>
    set({
      createForm: {
        prompt: '',
        mode: 'hybrid',
        platforms: ['tiktok'],
      },
    }),
}))
