/**
 * Continuum - Type Definitions
 * Core data structures for the kanban board
 */

export type CategoryId = 'business-finance' | 'coding-projects' | 'health-life' | 'communications'

export type ColumnId = 'todo' | 'in-progress' | 'done'

export interface Category {
  id: CategoryId
  name: string
  icon: string
  description: string
}

export interface Card {
  id: string
  title: string
  description: string
  categoryId: CategoryId
  columnId: ColumnId
  createdAt: Date
  updatedAt: Date
  tags?: string[]
  priority?: 'low' | 'medium' | 'high'
}

export interface Column {
  id: ColumnId
  name: string
  cards: Card[]
}

export interface KanbanState {
  categories: Category[]
  cards: Card[]
  activeCategory: CategoryId
}
