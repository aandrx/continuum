<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useKanbanStore } from '@/stores/kanban'
import KanbanColumn from './KanbanColumn.vue'
import CardModal from './CardModal.vue'
import type { ColumnId } from '@/types'

const kanbanStore = useKanbanStore()
const showModal = ref(false)
const editingCardId = ref<string | null>(null)

// Initialize data when component mounts
onMounted(async () => {
  await kanbanStore.fetchCategories()
  await kanbanStore.fetchCards()
})

function handleNewCard() {
  editingCardId.value = null
  showModal.value = true
}

function handleEditCard(cardId: string) {
  editingCardId.value = cardId
  showModal.value = true
}

function handleDeleteCard(cardId: string) {
  if (confirm('Are you sure you want to delete this card?')) {
    kanbanStore.deleteCard(cardId)
  }
}

function handleMoveCard(cardId: string, newColumnId: ColumnId) {
  kanbanStore.moveCard(cardId, newColumnId)
}

function handleCloseModal() {
  showModal.value = false
  editingCardId.value = null
}
</script>

<template>
  <div class="kanban-board">
    <div class="board-header">
      <h1 class="board-title">
        {{ kanbanStore.categories.find((c) => c.id === kanbanStore.activeCategory)?.name || 'Loading...' }}
      </h1>
      <button class="new-card-btn" @click="handleNewCard" :disabled="kanbanStore.loading">
        + New Card
      </button>
    </div>

    <div v-if="kanbanStore.loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading cards...</p>
    </div>

    <div v-else class="board-columns">
      <KanbanColumn
        column-id="todo"
        title="To Do"
        :cards="kanbanStore.todoCards"
        @move-card="handleMoveCard"
        @edit-card="handleEditCard"
        @delete-card="handleDeleteCard"
      />

      <KanbanColumn
        column-id="inProgress"
        title="In Progress"
        :cards="kanbanStore.inProgressCards"
        @move-card="handleMoveCard"
        @edit-card="handleEditCard"
        @delete-card="handleDeleteCard"
      />

      <KanbanColumn
        column-id="done"
        title="Done"
        :cards="kanbanStore.doneCards"
        @move-card="handleMoveCard"
        @edit-card="handleEditCard"
        @delete-card="handleDeleteCard"
      />
    </div>

    <CardModal
      v-if="showModal"
      :card-id="editingCardId"
      :category-id="kanbanStore.activeCategory"
      @close="handleCloseModal"
    />
  </div>
</template>

<style scoped>
.kanban-board {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  background-color: #ffffff;
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
  flex-shrink: 0;
}

.board-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #212529;
  margin: 0;
}

.new-card-btn {
  background-color: #364fc7;
  color: #ffffff;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(54, 79, 199, 0.2);
  flex-shrink: 0;
}

.new-card-btn:hover {
  background-color: #2b3e9e;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(54, 79, 199, 0.3);
}

.new-card-btn:active {
  transform: translateY(0);
}

.new-card-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #6c757d;
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #364fc7;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.board-columns {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding-bottom: 1rem;
  align-items: flex-start;
}

@media (max-width: 768px) {
  .kanban-board {
    padding: 1rem;
  }

  .board-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .board-title {
    font-size: 1.5rem;
    text-align: center;
  }

  .new-card-btn {
    width: 100%;
  }

  .board-columns {
    gap: 1rem;
  }
}
</style>
