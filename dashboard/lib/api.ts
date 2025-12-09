const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface VideoRequest {
  prompt: string
  mode: 'sequential' | 'parallel' | 'hybrid'
  platforms: string[]
  parameters?: Record<string, any>
}

export interface VideoResponse {
  workflow_id: string
  status: string
  mode: string
  platforms: string[]
  execution_time_ms: number
  output_files: string[]
  errors: string[]
}

export interface AgentStatus {
  agent_type: string
  name: string
  priority: string
  parallel_capable: boolean
  is_running: boolean
  current_task: string | null
  models: string[]
  capabilities: string[]
}

export interface SystemStatus {
  app_name: string
  version: string
  agents_registered: string[]
  ai_providers: Record<string, boolean>
  social_media: Record<string, boolean>
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    if (!response.ok) {
      const error = await response.text()
      throw new Error(`API Error: ${response.status} - ${error}`)
    }

    return response.json()
  }

  async getStatus(): Promise<SystemStatus> {
    return this.request<SystemStatus>('/status')
  }

  async getAgents(): Promise<Record<string, AgentStatus>> {
    return this.request<Record<string, AgentStatus>>('/agents')
  }

  async createVideo(request: VideoRequest): Promise<VideoResponse> {
    return this.request<VideoResponse>('/create', {
      method: 'POST',
      body: JSON.stringify(request),
    })
  }

  async getWorkflow(workflowId: string): Promise<any> {
    return this.request(`/workflow/${workflowId}`)
  }

  async healthCheck(): Promise<{ status: string; engine: boolean }> {
    return this.request('/health')
  }
}

export const api = new ApiClient()
