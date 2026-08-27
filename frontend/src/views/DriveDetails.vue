<!-- frontend/src/views/DriveDetails.vue -->

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useMessageStore } from '@/stores/message';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const msgStore = useMessageStore();

const drive = ref({});
const isAlreadyApplied = ref(false);
const isApplying = ref(false);

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
  const id = route.params.id;
  const detailsEndpoint = authStore.role === 'admin'
    ? `/admin/drives/${id}`
    : `/student/drives/${id}`;

  drive.value = await apiFetch(detailsEndpoint) || {};

  if (authStore.role === 'student' && drive.value?.id) {
    const applied = await apiFetch('/student/applications');
    if (Array.isArray(applied)) {
      isAlreadyApplied.value = applied.some(app => app.drive_id === drive.value.id);
    }
  }
});

async function applyToDrive() {
  if (isAlreadyApplied.value || isApplying.value) return;
  isApplying.value = true;

  const res = await apiFetch('/student/applications', 'POST', { drive_id: drive.value.id });
  if (res && res.message) {
    msgStore.updateErrorMessage(res.message);
    isAlreadyApplied.value = true;
  }

  isApplying.value = false;
}

function goBack() {
  if (authStore.role === 'admin') {
    router.push('/admin-dashboard');
  } else {
    router.push('/student-dashboard');
  }
}
</script>

<template>
  <div class="d-flex justify-content-center mt-4">
    <div class="card shadow-sm p-4" style="max-width: 500px; width: 100%;">
      <h5 class="mb-3">Drive Details</h5>

      <p><strong>Job Title:</strong> {{ drive.job_title }}</p>
      <p><strong>Description:</strong> {{ drive.job_description }}</p>
      <p><strong>Salary:</strong> {{ drive.salary }}</p>
      <p><strong>Skills Required:</strong> {{ drive.skills_required }}</p>
      <p><strong>Minimum CGPA:</strong> {{ drive.min_cgpa }}</p>
      <p><strong>Eligibility Branch:</strong> {{ drive.eligibility_branch }}</p>
      <p><strong>Eligibility Year:</strong> {{ drive.eligibility_year }}</p>
      <p><strong>Status:</strong> {{ drive.status }}</p>
      <p><strong>Company:</strong> {{ drive.company_name }}</p>
      <p><strong>Website:</strong> {{ drive.company_website }}</p>
      <p><strong>Application Deadline:</strong> {{ drive.application_deadline }}</p>

      <div class="d-flex gap-2 mt-3">
        <button
          v-if="authStore.role === 'student'"
          class="btn w-100"
          :class="isAlreadyApplied ? 'btn-secondary' : 'btn-success'"
          :disabled="isAlreadyApplied || isApplying"
          @click="applyToDrive"
        >
          {{ isAlreadyApplied ? 'Already Applied' : (isApplying ? 'Applying...' : 'Apply') }}
        </button>
        <button class="btn btn-outline-secondary w-100" @click="goBack">
          Go Back
        </button>
      </div>
    </div>
  </div>
</template>
