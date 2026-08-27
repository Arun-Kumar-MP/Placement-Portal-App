<!-- frontend/src/views/StudentProfile.vue -->

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useMessageStore } from '@/stores/message';

const authStore = useAuthStore();
const msgStore = useMessageStore();

const form = ref({
  name: '',
  email: '',
  branch: '',
  cgpa: '',
  year: '',
  resume: ''
});

async function apiFetch(url, method = 'GET', body = null) {
  const res = await fetch(`http://localhost:5000/api${url}`, {
    method,
    headers: {
      'Authentication-Token': authStore.auth_token,
      'Content-Type': 'application/json'
    },
    body: body ? JSON.stringify(body) : null
  });
  return res.ok ? await res.json() : null;
}

onMounted(async () => {
  const data = await apiFetch('/student/profile');
  if (data) {
    form.value = {
      name: data.name ?? '',
      email: data.email ?? '',
      branch: data.branch ?? '',
      cgpa: data.cgpa ?? '',
      year: data.year ?? '',
      resume: data.resume ?? ''
    };
  }
});

async function saveProfile() {
  const payload = {
    name: form.value.name,
    branch: form.value.branch,
    cgpa: form.value.cgpa,
    year: form.value.year,
    resume: form.value.resume
  };

  const res = await apiFetch('/student/profile', 'PUT', payload);
  if (res?.message) {
    msgStore.updateErrorMessage(res.message);
  } else {
    msgStore.updateErrorMessage('Failed to update profile!');
  }
}
</script>

<template>
  <div class="container mt-4">
    <div class="card shadow-sm p-4" style="max-width: 700px;">
      <h3 class="mb-4">Edit Student Profile</h3>

      <form @submit.prevent="saveProfile">
        <div class="mb-3">
          <label class="form-label">Name</label>
          <input v-model="form.name" class="form-control" required>
        </div>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input v-model="form.email" class="form-control" disabled>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label">Branch</label>
            <input v-model="form.branch" class="form-control" placeholder="CSE">
          </div>
          <div class="col-md-3 mb-3">
            <label class="form-label">CGPA</label>
            <input v-model="form.cgpa" type="number" step="0.01" class="form-control" placeholder="8.2">
          </div>
          <div class="col-md-3 mb-3">
            <label class="form-label">Year</label>
            <input v-model="form.year" type="number" class="form-control" placeholder="2026">
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Resume URL</label>
          <input v-model="form.resume" class="form-control" placeholder="https://...">
          <small class="text-muted">Paste a public resume link (Google Drive, GitHub, etc.)</small>
        </div>

        <button type="submit" class="btn btn-success">Save Profile</button>
      </form>
    </div>
  </div>
</template>
