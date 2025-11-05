<script setup lang="ts">
import CategorySwitcher from './components/CategorySwitcher.vue'
import KanbanBoard from './components/KanbanBoard.vue'
import AppFooter from './components/AppFooter.vue'
</script>

<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <h1 class="app-title">Continuum</h1>
        <p class="app-subtitle">Personal Productivity Dashboard</p>
      </div>
    </header>

    <CategorySwitcher />

    <main class="app-main">
      <KanbanBoard />
    </main>

    <AppFooter />
  </div>
</template>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100vw;
  background-color: #f8f9fa;
}

.app-header {
  background: linear-gradient(135deg, #364fc7 0%, #2b3e9e 100%);
  color: #ffffff;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.header-content {
  max-width: 100%;
  margin: 0 auto;
}

.app-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
}

.app-subtitle {
  margin: 0;
  font-size: 1rem;
  opacity: 0.9;
  font-weight: 400;
}

.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

@media (max-width: 768px) {
  .app-header {
    padding: 1rem;
  }

  .app-title {
    font-size: 1.5rem;
  }

  .app-subtitle {
    font-size: 0.875rem;
  }
}
</style>
