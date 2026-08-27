<!-- frontend/src/views/StudentDetails.vue -->

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import Details from '@/components/Details.vue';

const route = useRoute();
const authStore = useAuthStore();
const student = ref({});

async function apiFetch(url) {
  const res = await fetch(`http://localhost:5000/api${url}`, {
    headers: { 'Authentication-Token': authStore.auth_token }
  });
  return res.ok ? await res.json() : null;
}

onMounted(async () => {
  const id = route.params.id;
  student.value = await apiFetch(`/admin/students/${id}`) || {};
});
</script>

<template>
  <div class="container mt-4">
    <Details :entity="student" type="student" />
  </div>
</template>