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
  }

  function createCard(
    title: string,
    description: string,
    categoryId: CategoryId,
    columnId: ColumnId = 'todo'
  ): Card {
    const newCard: Card = {
      id: uuidv4(),
      title,
      description,
      categoryId,
      columnId,
      createdAt: new Date(),
      updatedAt: new Date(),
      tags: [],
      priority: 'medium'
    }

    cards.value.push(newCard)
    saveToLocalStorage()
    return newCard
  }

  function updateCard(cardId: string, updates: Partial<Omit<Card, 'id' | 'createdAt'>>) {
    const card = cards.value.find((c) => c.id === cardId)
    if (card) {
      Object.assign(card, updates, { updatedAt: new Date() })
      saveToLocalStorage()
    }
  }

  function deleteCard(cardId: string) {
    const index = cards.value.findIndex((card) => card.id === cardId)
    if (index !== -1) {
      cards.value.splice(index, 1)
      saveToLocalStorage()
    }
  }

  function moveCard(cardId: string, newColumnId: ColumnId) {
    updateCard(cardId, { columnId: newColumnId })
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
  loadFromLocalStorage()

  return {
    // State
    categories,
    cards,
    activeCategory,
    // Computed
    activeCategoryCards,
    todoCards,
    inProgressCards,
    doneCards,
    // Actions
    setActiveCategory,
    createCard,
    updateCard,
    deleteCard,
    moveCard,
    saveToLocalStorage,
    loadFromLocalStorage,
    clearAllData
  }
})
