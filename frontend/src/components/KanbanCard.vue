<script setup lang="ts">
import type { Card } from '@/types'

defineProps<{
  card: Card
}>()

const emit = defineEmits<{
  edit: [cardId: string]
  delete: [cardId: string]
}>()

function formatDate(date: string | Date): string {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function getPriorityClass(priority?: string): string {
  switch (priority) {
    case 'high':
      return 'priority-high'
    case 'medium':
      return 'priority-medium'
    case 'low':
      return 'priority-low'
    default:
      return ''
  }
}
</script>

<template>
  <div :class="['kanban-card', getPriorityClass(card.priority)]">
    <div class="card-header">
      <h3 class="card-title">{{ card.title }}</h3>
      <div class="card-actions">
        <button class="action-btn edit-btn" @click="emit('edit', card.id)" title="Edit card">
          ✏️
        </button>
        <button class="action-btn delete-btn" @click="emit('delete', card.id)" title="Delete card">
          🗑️
        </button>
      </div>
    </div>

    <p v-if="card.description" class="card-description">{{ card.description }}</p>

    <div v-if="card.tags && card.tags.length > 0" class="card-tags">
      <span v-for="tag in card.tags" :key="tag" class="tag">{{ tag }}</span>
    </div>

    <div class="card-footer">
      <span class="card-date">{{ formatDate(card.updatedAt) }}</span>
      <span v-if="card.priority" class="card-priority">{{ card.priority }}</span>
    </div>
  </div>
</template>

<style scoped>
.kanban-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  cursor: move;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.kanban-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.kanban-card.priority-high {
  border-left: 4px solid #fa5252;
}

.kanban-card.priority-medium {
  border-left: 4px solid #fd7e14;
}

.kanban-card.priority-low {
  border-left: 4px solid #51cf66;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #212529;
  margin: 0;
  flex: 1;
  word-wrap: break-word;
}

.card-actions {
  display: flex;
  gap: 0.25rem;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  font-size: 1rem;
  opacity: 0.6;
  transition: opacity 0.2s ease;
}

.action-btn:hover {
  opacity: 1;
}

.card-description {
  font-size: 0.875rem;
  color: #6c757d;
  margin: 0 0 0.75rem 0;
  line-height: 1.5;
  word-wrap: break-word;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-bottom: 0.75rem;
}

.tag {
  background-color: #e7f5ff;
  color: #1971c2;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.5rem;
  border-top: 1px solid #f1f3f5;
}

.card-date {
  font-size: 0.75rem;
  color: #868e96;
}

.card-priority {
  font-size: 0.75rem;
  color: #495057;
  text-transform: capitalize;
  font-weight: 500;
}

@media (max-width: 768px) {
  .kanban-card {
    padding: 0.75rem;
  }

  .card-title {
    font-size: 0.9rem;
  }

  .card-description {
    font-size: 0.8rem;
  }
}
</style>
