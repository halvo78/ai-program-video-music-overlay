const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// API Error types
export class ApiError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    message: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export class NetworkError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'NetworkError'
  }
}

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
    options: RequestInit = {},
    retries: number = 3
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`

    for (let attempt = 0; attempt < retries; attempt++) {
      try {
        const response = await fetch(url, {
          ...options,
          headers: {
            'Content-Type': 'application/json',
            ...options.headers,
          },
        })

        if (!response.ok) {
          const errorText = await response.text().catch(() => 'Unknown error')
          throw new ApiError(response.status, response.statusText, errorText)
        }

        return response.json()
      } catch (error) {
        if (error instanceof ApiError) {
          throw error
        }

        // Network error - retry with exponential backoff
        if (attempt < retries - 1) {
          await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000))
          continue
        }

        throw new NetworkError(`Failed to connect to API after ${retries} attempts: ${error}`)
      }
    }

    throw new NetworkError('Request failed after all retries')
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

  // Template methods
  async getTemplates(): Promise<any[]> {
    return this.request('/templates')
  }

  async getTemplate(id: string): Promise<any> {
    return this.request(`/templates/${id}`)
  }

  // Gallery methods
  async getGallery(page: number = 1, limit: number = 20): Promise<any> {
    return this.request(`/gallery?page=${page}&limit=${limit}`)
  }

  // Analytics methods
  async getAnalytics(period: string = '7d'): Promise<any> {
    return this.request(`/analytics?period=${period}`)
  }

  // Social media publishing
  async publishToSocial(videoId: string, platforms: string[]): Promise<any> {
    return this.request('/publish', {
      method: 'POST',
      body: JSON.stringify({ video_id: videoId, platforms }),
    })
  }

  // Settings
  async getSettings(): Promise<any> {
    return this.request('/settings')
  }

  async updateSettings(settings: Record<string, any>): Promise<any> {
    return this.request('/settings', {
      method: 'PUT',
      body: JSON.stringify(settings),
    })
  }
}

export const api = new ApiClient()
