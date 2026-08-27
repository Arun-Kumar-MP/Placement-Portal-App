<!-- frontend/src/views/StudentDashboard.vue -->

<script setup>
// Vue3
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// Stores
import { useAuthStore } from '@/stores/auth'
import { useMessageStore } from '@/stores/message'

// Components
import Table from '@/components/Table.vue'
import SearchBar from '@/components/SearchBar.vue'

const authStore = useAuthStore()
const messageStore = useMessageStore()
const router = useRouter()

const studentName = ref('Student')
const organizations = ref([])
const appliedDrives = ref([])
const searchDrive = ref('')
const appliedStatusFilter = ref('All')

const filteredOrganizations = computed(() => {
  const q = searchDrive.value.trim().toLowerCase()
  if (!q) return organizations.value
  return organizations.value.filter(d => `${d.company_name} ${d.job_title}`.toLowerCase().includes(q))
})

const filteredAppliedDrives = computed(() => {
  let list = [...appliedDrives.value]
  if (appliedStatusFilter.value !== 'All') {
    list = list.filter(a => (a.status || '') === appliedStatusFilter.value)
  }
  return list
})

async function apiFetch(url, method = 'GET', body = null) {
  const res = await fetch(`http://127.0.0.1:5000/api${url}`, {
    method,
    headers: {
      'Authentication-Token': authStore.auth_token,
      'Content-Type': 'application/json'
    },
    body: body ? JSON.stringify(body) : null
  })

  if (!res.ok) return null
  return res.json()
}

async function loadDashboard() {
  const profile = await apiFetch('/student/profile')
  if (profile?.name) studentName.value = profile.name

  organizations.value = await apiFetch('/student/drives') || []
  appliedDrives.value = await apiFetch('/student/applications') || []
}

async function exportApplicationsCsv() {
  const res = await apiFetch('/student/applications/export', 'POST')
  if (res?.message) {
    messageStore.updateErrorMessage(res.message)
  } else {
    messageStore.updateErrorMessage('Failed to start CSV export.')
  }
}

function handleOrgAction({ item, action }) {
  if (action === 'View Details') router.push(`/student/drives/${item.id}`)
}

function handleApplicationAction({ item, action }) {
  if (action === 'View Details') router.push(`/student/drives/${item.drive_id}`)
}

onMounted(loadDashboard)
</script>

<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold">Welcome, {{ studentName }}</h2>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-success" @click="exportApplicationsCsv">Export CSV</button>
        <router-link to="/student/profile" class="btn btn-outline-primary">Edit Profile</router-link>
        <router-link to="/student/history" class="btn btn-outline-secondary">View History</router-link>
      </div>
    </div>

    <div class="row g-2 mb-3">
      <div class="col-md-8">
        <SearchBar
          v-model="searchDrive"
          placeholder="Search approved drives by company or role"
          maxWidth="100%"
        />
      </div>
      <div class="col-md-4">
        <select v-model="appliedStatusFilter" class="form-select">
          <option>All</option>
          <option>Applied</option>
          <option>Shortlisted</option>
          <option>Interview Scheduled</option>
          <option>Selected</option>
          <option>Rejected</option>
        </select>
      </div>
    </div>

    <Table
      title="Organizations"
      :headers="['Company','Job Title','Deadline']"
      :fields="['company_name','job_title','application_deadline']"
      :items="filteredOrganizations"
      :actions="[{ text:'View Details', class:'btn-primary' }]"
      @actionClicked="handleOrgAction"
    />

    <Table
      title="Applied Drives"
      :headers="['ID','Drive Name','Company','Applied On','Status']"
      :fields="['id','job_title','company_name','application_date','status']"
      :items="filteredAppliedDrives"
      :actions="[{ text:'View Details', class:'btn-info' }]"
      @actionClicked="handleApplicationAction"
    />
  </div>
</template>
