/**
 * API Client for Taj Chat Backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
  /**
   * Get status of all agents
   */
  async getAgents() {
    try {
      const response = await fetch(`${API_BASE_URL}/agents`);
      if (!response.ok) {
        throw new Error('Failed to fetch agents');
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      return {};
    }
  },

  /**
   * Get system status
   */
  async getStatus() {
    try {
      const response = await fetch(`${API_BASE_URL}/status`);
      if (!response.ok) {
        throw new Error('Failed to fetch status');
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      return null;
    }
  },

  /**
   * Create a video
   */
  async createVideo(params: { prompt: string; mode?: string; platforms?: string[] }) {
    try {
      const response = await fetch(`${API_BASE_URL}/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: params.prompt,
          mode: params.mode || 'hybrid',
          platforms: params.platforms || ['tiktok'],
        }),
      });
      if (!response.ok) {
        throw new Error('Failed to create video');
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  /**
   * Get workflow status
   */
  async getWorkflow(workflowId: string) {
    try {
      const response = await fetch(`${API_BASE_URL}/workflow/${workflowId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch workflow');
      }
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      return null;
    }
  },
};
