<!-- frontend/src/views/DriveApplication.vue -->

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useMessageStore } from '@/stores/message';
import Table from '@/components/Table.vue';
import Details from '@/components/Details.vue';

const route = useRoute();
const authStore = useAuthStore();
const msgStore = useMessageStore();

const students = ref([]);
const selectedStudent = ref(null);
const driveDetails = ref({});
const searchTerm = ref('');
const statusOptions = ['Applied','Shortlisted','Interview Scheduled', 'Selected', 'Rejected'];

const filteredStudents = computed(() => {
  const q = searchTerm.value.trim().toLowerCase();
  if (!q) return students.value;
  return students.value.filter(s => `${s.student_name} ${s.status} ${s.branch}`.toLowerCase().includes(q));
});

const apiFetch = async (url, method = 'GET', body = null) => {
  const res = await fetch(`http://localhost:5000/api${url}`, {
    method,
    headers: {
      'Authentication-Token': authStore.auth_token,
      'Content-Type': 'application/json'
    },
    body: body ? JSON.stringify(body) : null
  });
  return res.ok ? await res.json() : null;
};

onMounted(async () => {
  const id = route.params.id;
  students.value = await apiFetch(`/company/drives/${id}/applications`) || [];
  driveDetails.value = await apiFetch(`/company/drives/${id}`) || {};
});

function handleAction({ item, action }) {
  if (action === 'Review Application') {
    selectedStudent.value = item;
  }
}

async function updateStatus(newStatus) {
  if (!selectedStudent.value) return;

  const res = await apiFetch(`/company/applications/${selectedStudent.value.id}/status`, 'POST', {
    status: newStatus
  });

  if (res) {
    selectedStudent.value.status = newStatus;
    const idx = students.value.findIndex(s => s.id === selectedStudent.value.id);
    if (idx !== -1) students.value[idx].status = newStatus;
    msgStore.updateErrorMessage('Application status updated!');
  }
}
</script>

<template>
  <div class="container mt-4">
    <h3 class="mb-4">Update Applications for the Drive</h3>
    <div class="row">
      <div class="col-md-4">
        <div class="card shadow-sm p-4" style="max-width: 500px; width: 100%;">
          <h5 class="mb-3">Drive Information</h5>
          <p><strong>Job Title:</strong> {{ driveDetails.job_title }}</p>
          <p><strong>Description:</strong> {{ driveDetails.job_description }}</p>
          <p><strong>Company:</strong> {{ driveDetails.company_name }}</p>
          <p><strong>Total Applicants:</strong> {{ driveDetails.applicants_count }}</p>

          <Details :entity="selectedStudent || {}" type="student" />

          <div v-if="selectedStudent" class="mt-3">
            <label for="statusSelect"><strong>Application Status:</strong></label>
            <select
              id="statusSelect"
              class="form-select mt-2"
              v-model="selectedStudent.status"
              @change="updateStatus(selectedStudent.status)"
            >
              <option v-for="opt in statusOptions" :key="opt" :value="opt">
                {{ opt }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <div class="col-md-8">
        <div class="mb-3">
          <input
            v-model="searchTerm"
            class="form-control"
            placeholder="Search applicants by name, branch, or status"
          >
        </div>

        <Table
          title="Applications"
          :headers="['ID','Student Name','Branch','CGPA','Status']"
          :fields="['id','student_name','branch','cgpa','status']"
          :items="filteredStudents"
          :actions="[{ text: 'Review Application', class: 'btn-primary' }]"
          :serialNumber="false"
          @actionClicked="handleAction"
        />
      </div>
    </div>
  </div>
</template>
