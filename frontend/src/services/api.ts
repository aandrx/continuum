/**
 * API Client for Continuum Backend
 * Handles all HTTP requests to the backend API
 */

import type { Card, CategoryId, ColumnId } from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

interface ApiError {
  error: string
  message?: string
  details?: unknown
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const error: ApiError = await response.json()
        throw new Error(error.message || error.error || 'API request failed')
      }

      return await response.json()
    } catch (error) {
      console.error('API request error:', error)
      throw error
    }
  }

  // Categories

  async getCategories() {
    return this.request<Array<{
      id: CategoryId
      name: string
      description: string
      icon: string
    }>>('/categories')
  }

  // Cards

  async getCards(categoryId?: CategoryId): Promise<Card[]> {
    const query = categoryId ? `?categoryId=${categoryId}` : ''
    return this.request<Card[]>(`/cards${query}`)
  }

  async getCard(id: string): Promise<Card> {
    return this.request<Card>(`/cards/${id}`)
  }

  async createCard(card: Omit<Card, 'createdAt' | 'updatedAt'>): Promise<Card> {
    return this.request<Card>('/cards', {
      method: 'POST',
      body: JSON.stringify(card),
    })
  }

  async updateCard(id: string, updates: Partial<Card>): Promise<Card> {
    return this.request<Card>(`/cards/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    })
  }

  async moveCard(id: string, columnId: ColumnId): Promise<Card> {
    return this.request<Card>(`/cards/${id}/move`, {
      method: 'PATCH',
      body: JSON.stringify({ columnId }),
    })
  }

  async deleteCard(id: string): Promise<void> {
    await this.request<{ message: string }>(`/cards/${id}`, {
      method: 'DELETE',
    })
  }

  // Health check

  async healthCheck() {
    return this.request<{ status: string; message: string }>('/health')
  }
}

// Export singleton instance
export const api = new ApiClient()
export default api
