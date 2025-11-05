<script setup lang="ts">
import { computed } from 'vue'
import draggable from 'vuedraggable'
import KanbanCard from './KanbanCard.vue'
import type { Card, ColumnId } from '@/types'

const props = defineProps<{
  columnId: ColumnId
  title: string
  cards: Card[]
}>()

const emit = defineEmits<{
  moveCard: [cardId: string, newColumnId: ColumnId]
  editCard: [cardId: string]
  deleteCard: [cardId: string]
}>()

const localCards = computed({
  get: () => props.cards,
  set: (value) => {
    // Draggable will update this when cards are moved
  }
})

function onCardMoved(event: any) {
  if (event.added) {
    const card = event.added.element
    emit('moveCard', card.id, props.columnId)
  }
}
</script>

<template>
  <div class="kanban-column">
    <div class="column-header">
      <h2 class="column-title">{{ title }}</h2>
      <span class="card-count">{{ cards.length }}</span>
    </div>

    <draggable
      v-model="localCards"
      :group="{ name: 'cards', pull: true, put: true }"
      item-key="id"
      class="column-content"
      :animation="200"
      ghost-class="ghost-card"
      @change="onCardMoved"
    >
      <template #item="{ element: card }">
        <KanbanCard
          :card="card"
          @edit="(id) => emit('editCard', id)"
          @delete="(id) => emit('deleteCard', id)"
        />
      </template>
    </draggable>

    <div v-if="cards.length === 0" class="empty-state">
      <p>No cards yet</p>
    </div>
  </div>
</template>

<style scoped>
.kanban-column {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  min-width: 300px;
  max-width: 400px;
  min-height: 600px;
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #dee2e6;
  flex-shrink: 0;
}

.column-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #212529;
  margin: 0;
}

.card-count {
  background-color: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.column-content {
  padding-right: 0.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 150px;
  color: #adb5bd;
  font-style: italic;
  padding: 2rem;
  text-align: center;
}

.ghost-card {
  opacity: 0.5;
  background-color: #e7f5ff;
  border: 2px dashed #4c6ef5;
}

@media (max-width: 768px) {
  .kanban-column {
    min-width: 250px;
    padding: 0.75rem;
  }

  .column-title {
    font-size: 1rem;
  }
}
</style>
