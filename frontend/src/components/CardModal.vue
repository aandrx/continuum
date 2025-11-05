<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useKanbanStore } from '@/stores/kanban'
import type { CategoryId, ColumnId } from '@/types'

const props = defineProps<{
  cardId: string | null
  categoryId: CategoryId
}>()

const emit = defineEmits<{
  close: []
}>()

const kanbanStore = useKanbanStore()

const title = ref('')
const description = ref('')
const columnId = ref<ColumnId>('todo')
const priority = ref<'low' | 'medium' | 'high'>('medium')
const tags = ref<string>('')

const isEditing = computed(() => props.cardId !== null)
const modalTitle = computed(() => (isEditing.value ? 'Edit Card' : 'New Card'))

onMounted(() => {
  if (props.cardId) {
    const card = kanbanStore.cards.find((c) => c.id === props.cardId)
    if (card) {
      title.value = card.title
      description.value = card.description
      columnId.value = card.columnId
      priority.value = card.priority || 'medium'
      tags.value = card.tags?.join(', ') || ''
    }
  }
})

function handleSubmit() {
  if (!title.value.trim()) {
    alert('Please enter a card title')
    return
  }

  const tagsArray = tags.value
    .split(',')
    .map((t) => t.trim())
    .filter((t) => t.length > 0)

  if (isEditing.value && props.cardId) {
    kanbanStore.updateCard(props.cardId, {
      title: title.value.trim(),
      description: description.value.trim(),
      columnId: columnId.value,
      priority: priority.value,
      tags: tagsArray
    })
  } else {
    kanbanStore.createCard(
      title.value.trim(),
      description.value.trim(),
      props.categoryId,
      columnId.value
    )
    // Update tags and priority after creation
    const newCard = kanbanStore.cards[kanbanStore.cards.length - 1]
    if (newCard) {
      kanbanStore.updateCard(newCard.id, {
        priority: priority.value,
        tags: tagsArray
      })
    }
  }

  emit('close')
}

function handleCancel() {
  emit('close')
}

function handleBackdropClick(event: MouseEvent) {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}
</script>

<template>
  <div class="modal-backdrop" @click="handleBackdropClick">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ modalTitle }}</h2>
        <button class="close-btn" @click="handleCancel" title="Close">×</button>
      </div>

      <form class="modal-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="card-title">Title *</label>
          <input
            id="card-title"
            v-model="title"
            type="text"
            placeholder="Enter card title..."
            required
            autofocus
          />
        </div>

        <div class="form-group">
          <label for="card-description">Description</label>
          <textarea
            id="card-description"
            v-model="description"
            rows="4"
            placeholder="Enter card description..."
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="card-column">Column</label>
            <select id="card-column" v-model="columnId">
              <option value="todo">To Do</option>
              <option value="in-progress">In Progress</option>
              <option value="done">Done</option>
            </select>
          </div>

          <div class="form-group">
            <label for="card-priority">Priority</label>
            <select id="card-priority" v-model="priority">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label for="card-tags">Tags</label>
          <input
            id="card-tags"
            v-model="tags"
            type="text"
            placeholder="Enter tags separated by commas..."
          />
          <small>Separate tags with commas (e.g., frontend, urgent, bug)</small>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn btn-cancel" @click="handleCancel">Cancel</button>
          <button type="submit" class="btn btn-submit">
            {{ isEditing ? 'Update' : 'Create' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #212529;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  line-height: 1;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: #f8f9fa;
  color: #212529;
}

.modal-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #495057;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #4c6ef5;
  box-shadow: 0 0 0 3px rgba(76, 110, 245, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-group small {
  display: block;
  margin-top: 0.25rem;
  color: #6c757d;
  font-size: 0.8rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-cancel {
  background-color: #e9ecef;
  color: #495057;
}

.btn-cancel:hover {
  background-color: #dee2e6;
}

.btn-submit {
  background-color: #364fc7;
  color: #ffffff;
}

.btn-submit:hover {
  background-color: #2b3e9e;
  box-shadow: 0 4px 8px rgba(54, 79, 199, 0.3);
}

@media (max-width: 768px) {
  .modal-content {
    max-height: 95vh;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-form {
    padding: 1rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .btn {
    padding: 0.625rem 1.25rem;
    font-size: 0.9rem;
  }
}
</style>
