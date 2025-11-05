<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="app-footer">
    <div class="footer-content">
      <div class="footer-section">
        <h4 class="footer-title">Continuum</h4>
        <p class="footer-description">Personal Productivity Dashboard</p>
      </div>

      <div class="footer-section">
        <h5 class="footer-heading">Project</h5>
        <ul class="footer-links">
          <li><a href="https://github.com/aandrx/continuum" target="_blank" rel="noopener">GitHub</a></li>
          <li><a href="#" @click.prevent>Documentation</a></li>
          <li><a href="#" @click.prevent>API</a></li>
        </ul>
      </div>

      <div class="footer-section">
        <h5 class="footer-heading">Features</h5>
        <ul class="footer-links">
          <li>4 Category Boards</li>
          <li>Drag & Drop</li>
          <li>Local Storage</li>
          <li>Responsive Design</li>
        </ul>
      </div>

      <div class="footer-section">
        <h5 class="footer-heading">Tech Stack</h5>
        <ul class="footer-links">
          <li>Vue.js 3</li>
          <li>TypeScript</li>
          <li>Python Flask</li>
          <li>Pinia</li>
        </ul>
      </div>

      <div class="footer-section footer-info">
        <p class="footer-version">Version 0.2.0</p>
        <p class="footer-phase">Phase 1 Complete</p>
        <p class="footer-copyright">&copy; {{ currentYear }} aandrx. MIT License.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background-color: #212529;
  color: #e9ecef;
  padding: 2rem 2rem 1rem;
  border-top: 3px solid #364fc7;
  flex-shrink: 0;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr;
  gap: 2rem;
}

.footer-section {
  display: flex;
  flex-direction: column;
}

.footer-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 0.5rem 0;
}

.footer-description {
  color: #adb5bd;
  margin: 0;
  font-size: 0.9rem;
}

.footer-heading {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 0.75rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-links li {
  font-size: 0.875rem;
  color: #adb5bd;
}

.footer-links a {
  color: #adb5bd;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: #ffffff;
}

.footer-info {
  text-align: right;
}

.footer-version,
.footer-phase,
.footer-copyright {
  font-size: 0.875rem;
  color: #adb5bd;
  margin: 0.25rem 0;
}

.footer-version {
  font-weight: 600;
  color: #6c757d;
}

.footer-phase {
  color: #51cf66;
  font-weight: 500;
}

@media (max-width: 1024px) {
  .footer-content {
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }

  .footer-info {
    text-align: left;
    grid-column: 1 / -1;
  }
}

@media (max-width: 768px) {
  .app-footer {
    padding: 1.5rem 1rem 1rem;
  }

  .footer-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .footer-section {
    text-align: center;
  }

  .footer-info {
    text-align: center;
  }

  .footer-links {
    align-items: center;
  }
}
</style>
