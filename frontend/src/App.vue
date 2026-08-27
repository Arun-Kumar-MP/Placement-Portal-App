<!-- frontend/src/App.vue -->

<script setup>
import { computed } from 'vue';
import { RouterLink, RouterView, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useMessageStore } from '@/stores/message';

const authStore = useAuthStore();
const messageStore = useMessageStore();
const router = useRouter();
const role = computed(() =>
  authStore.role.charAt(0).toUpperCase() + authStore.role.slice(1)
);

// Access the global error message from the store
const errorMessage = computed(() => messageStore.errorMessage);

// Function to handle logout
function handleLogout() {
  authStore.clearAuth();
  messageStore.updateErrorMessage("Logout successful!"); // match backend wording
  router.push('/login');
}

// Compute dashboard route dynamically based on role
const dashboardRoute = computed(() => {
  if (authStore.role === 'admin') return '/admin-dashboard';
  if (authStore.role === 'company') return '/company-dashboard';
  if (authStore.role === 'student') return '/student-dashboard';
  return '/'; // fallback
});
</script>

<template>
  <div class="container">
    <!-- Global message -->
    <div
      v-if="errorMessage"
      class="alert alert-warning shadow-sm position-fixed bottom-0 start-0 m-3 w-45"
      style="z-index: 1080;"
      role="alert"
    >
      {{ errorMessage }}
    </div>

    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" to="/">Placement Portal</RouterLink>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">

            <!-- Before Login -->
            <li class="nav-item" v-if="!authStore.isAuthenticated">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
            <li class="nav-item" v-if="!authStore.isAuthenticated">
              <RouterLink class="nav-link" to="/register">Register</RouterLink>
            </li>

            <!-- After Login -->
            <li class="nav-item" v-if="authStore.isAuthenticated">
              <RouterLink class="nav-link" :to="dashboardRoute">Dashboard</RouterLink>
            </li>
            <li class="nav-item" v-if="authStore.isAuthenticated">
              <a class="nav-link" href="#" @click.prevent="handleLogout">
                Logout ({{ role}})
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <!-- Main content -->
    <RouterView/>
  </div>
</template>
