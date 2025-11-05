<script setup lang="ts">
import { useKanbanStore } from '@/stores/kanban'
import type { CategoryId } from '@/types'

const kanbanStore = useKanbanStore()

function switchCategory(categoryId: CategoryId) {
  kanbanStore.setActiveCategory(categoryId)
}
</script>

<template>
  <div class="category-switcher">
    <button
      v-for="category in kanbanStore.categories"
      :key="category.id"
      :class="['category-tab', { active: kanbanStore.activeCategory === category.id }]"
      @click="switchCategory(category.id)"
    >
      <span class="category-icon">{{ category.icon }}</span>
      <span class="category-name">{{ category.name }}</span>
    </button>
  </div>
</template>

<style scoped>
.category-switcher {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-bottom: 2px solid #e9ecef;
  overflow-x: auto;
  flex-shrink: 0;
  max-height: 80px;
}

/* Custom scrollbar for category switcher */
.category-switcher::-webkit-scrollbar {
  height: 4px;
}

.category-switcher::-webkit-scrollbar-track {
  background: transparent;
}

.category-switcher::-webkit-scrollbar-thumb {
  background: #dee2e6;
  border-radius: 2px;
}

.category-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: white;
  border: 2px solid #dee2e6;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  font-weight: 500;
  color: #495057;
  white-space: nowrap;
  flex-shrink: 0;
}

.category-tab:hover {
  background-color: #f1f3f5;
  border-color: #adb5bd;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.category-tab.active {
  background-color: #364fc7;
  border-color: #364fc7;
  color: #ffffff;
  font-weight: 600;
}

.category-icon {
  font-size: 1.1rem;
}

.category-name {
  user-select: none;
}

@media (max-width: 768px) {
  .category-switcher {
    padding: 0.75rem;
    gap: 0.25rem;
  }

  .category-tab {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }

  .category-name {
    display: none;
  }
}
</style>
