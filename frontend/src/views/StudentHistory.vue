<!-- frontend/src/views/StudentHistory.vue -->

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import Table from '@/components/Table.vue';

const authStore = useAuthStore();
const history = ref([]);

async function loadHistory() {
  const res = await fetch('http://localhost:5000/api/student/applications', {
    headers: {
      'Authentication-Token': authStore.auth_token,
      'Content-Type': 'application/json'
    }
  });

  if (res.ok) {
    history.value = await res.json();
  }
}

onMounted(loadHistory);
</script>

<template>
  <div class="container mt-4">
    <h3 class="mb-3">Student Application History</h3>

    <Table
      title="Application History"
      :headers="['ID', 'Job Title', 'Company', 'Applied On', 'Status']"
      :fields="['id', 'job_title', 'company_name', 'application_date', 'status']"
      :items="history"
    />
  </div>
</template>
