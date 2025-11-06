/**
 * Continuum - Kanban Store
 * Manages the state for cards, categories, and columns with API integration
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Card, Category, CategoryId, ColumnId } from '@/types'
import { v4 as uuidv4 } from 'uuid'
import api from '@/services/api'

const STORAGE_KEY = 'continuum-kanban-data'

export const useKanbanStore = defineStore('kanban', () => {
  // State
  const categories = ref<Category[]>([])
  const cards = ref<Card[]>([])
  const activeCategory = ref<CategoryId>('coding')
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const activeCategoryCards = computed(() => {
    return cards.value.filter((card) => card.categoryId === activeCategory.value)
  })

  const todoCards = computed(() => {
    return activeCategoryCards.value.filter((card) => card.columnId === 'todo')
  })

  const inProgressCards = computed(() => {
    return activeCategoryCards.value.filter((card) => card.columnId === 'inProgress')
  })

  const doneCards = computed(() => {
    return activeCategoryCards.value.filter((card) => card.columnId === 'done')
  })

  // Actions
  function setActiveCategory(categoryId: CategoryId) {
    activeCategory.value = categoryId
    // Don't refetch cards - they're already filtered by activeCategoryCards computed property
    // Just save the preference to localStorage
    saveToLocalStorage()
  }

  async function fetchCategories() {
    loading.value = true
    error.value = null
    try {
      const fetchedCategories = await api.getCategories()
      categories.value = fetchedCategories
    } catch (err) {
      error.value = 'Failed to load categories'
      console.error('Error fetching categories:', err)
      // Fallback to default categories if API fails
      console.warn('Using default categories as fallback')
      categories.value = [
        { id: 'business', name: 'Business', icon: '💼', description: 'Business & Finance' },
        { id: 'coding', name: 'Coding', icon: '💻', description: 'Programming Projects' },
        { id: 'health', name: 'Health', icon: '🏥', description: 'Health & Wellness' },
        { id: 'communications', name: 'Communications', icon: '💬', description: 'Messages & Emails' }
      ]
      // Also try to load cards from localStorage
      loadFromLocalStorage()
    } finally {
      loading.value = false
    }
  }

  async function fetchCards(categoryId?: CategoryId) {
    loading.value = true
    error.value = null
    try {
      const fetchedCards = await api.getCards(categoryId)
      // Convert date strings to Date objects
      cards.value = fetchedCards.map(card => ({
        ...card,
        createdAt: new Date(card.createdAt),
        updatedAt: new Date(card.updatedAt)
      }))
      // Also save to localStorage as backup
      saveToLocalStorage()
    } catch (err) {
      error.value = 'Failed to load cards'
      console.error('Error fetching cards:', err)
      // Fallback to localStorage
      loadFromLocalStorage()
    } finally {
      loading.value = false
    }
  }

  async function createCard(
    title: string,
    description: string,
    categoryId: CategoryId,
    columnId: ColumnId = 'todo',
    priority?: 'low' | 'medium' | 'high',
    tags?: string[]
  ): Promise<Card | null> {
    loading.value = true
    error.value = null
    
    const newCard = {
      id: uuidv4(),
      title,
      description,
      categoryId,
      columnId,
      priority,
      tags: tags || [],
      createdAt: new Date(),
      updatedAt: new Date()
    }

    try {
      const createdCard = await api.createCard(newCard)
      // Convert date strings to Date objects
      const cardWithDates = {
        ...createdCard,
        createdAt: new Date(createdCard.createdAt),
        updatedAt: new Date(createdCard.updatedAt)
      }
      cards.value.push(cardWithDates)
      saveToLocalStorage()
      return cardWithDates
    } catch (err) {
      error.value = 'Failed to create card'
      console.error('Error creating card:', err)
      // Fallback: add to localStorage only
      cards.value.push(newCard)
      saveToLocalStorage()
      return newCard
    } finally {
      loading.value = false
    }
  }

  async function updateCard(cardId: string, updates: Partial<Omit<Card, 'id' | 'createdAt'>>) {
    loading.value = true
    error.value = null
    
    try {
      const updatedCard = await api.updateCard(cardId, updates)
      // Update local state
      const index = cards.value.findIndex((c) => c.id === cardId)
      if (index !== -1) {
        cards.value[index] = {
          ...updatedCard,
          createdAt: new Date(updatedCard.createdAt),
          updatedAt: new Date(updatedCard.updatedAt)
        }
        saveToLocalStorage()
      }
    } catch (err) {
      error.value = 'Failed to update card'
      console.error('Error updating card:', err)
      // Fallback: update localStorage only
      const card = cards.value.find((c) => c.id === cardId)
      if (card) {
        Object.assign(card, updates, { updatedAt: new Date() })
        saveToLocalStorage()
      }
    } finally {
      loading.value = false
    }
  }

  async function deleteCard(cardId: string) {
    loading.value = true
    error.value = null
    
    try {
      await api.deleteCard(cardId)
      // Remove from local state
      const index = cards.value.findIndex((card) => card.id === cardId)
      if (index !== -1) {
        cards.value.splice(index, 1)
        saveToLocalStorage()
      }
    } catch (err) {
      error.value = 'Failed to delete card'
      console.error('Error deleting card:', err)
    } finally {
      loading.value = false
    }
  }

  async function moveCard(cardId: string, newColumnId: ColumnId) {
    loading.value = true
    error.value = null
    
    try {
      const movedCard = await api.moveCard(cardId, newColumnId)
      // Update local state
      const index = cards.value.findIndex((c) => c.id === cardId)
      if (index !== -1) {
        cards.value[index] = {
          ...movedCard,
          createdAt: new Date(movedCard.createdAt),
          updatedAt: new Date(movedCard.updatedAt)
        }
        saveToLocalStorage()
      }
    } catch (err) {
      error.value = 'Failed to move card'
      console.error('Error moving card:', err)
      // Fallback: update localStorage only
      const card = cards.value.find((c) => c.id === cardId)
      if (card) {
        Object.assign(card, { columnId: newColumnId, updatedAt: new Date() })
        saveToLocalStorage()
      }
    } finally {
      loading.value = false
    }
  }

  function saveToLocalStorage() {
    const data = {
      cards: cards.value,
      activeCategory: activeCategory.value
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  }

  function loadFromLocalStorage() {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      try {
        const data = JSON.parse(stored)
        cards.value = data.cards.map((card: any) => ({
          ...card,
          createdAt: new Date(card.createdAt),
          updatedAt: new Date(card.updatedAt)
        }))
        activeCategory.value = data.activeCategory
      } catch (error) {
        console.error('Failed to load from localStorage:', error)
      }
    }
  }

  function clearAllData() {
    cards.value = []
    localStorage.removeItem(STORAGE_KEY)
  }

  // Initialize
  fetchCategories()
  fetchCards()

  return {
    // State
    categories,
    cards,
    activeCategory,
    loading,
    error,
    // Computed
    activeCategoryCards,
    todoCards,
    inProgressCards,
    doneCards,
    // Actions
    setActiveCategory,
    fetchCategories,
    fetchCards,
    createCard,
    updateCard,
    deleteCard,
    moveCard,
    saveToLocalStorage,
    loadFromLocalStorage,
    clearAllData
  }
})
