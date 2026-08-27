<!-- frontend/src/views/CompanyDashboard.vue -->

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
const msgStore = useMessageStore()
const router = useRouter()

const searchTerm = ref('')
const ongoingDrives = ref([])
const closedDrives = ref([])

const normalizedSearch = computed(() => searchTerm.value.trim().toLowerCase())

function filterList(list) {
  if (!normalizedSearch.value) return list
  return list.filter(d => `${d.job_title} ${d.status}`.toLowerCase().includes(normalizedSearch.value))
}

const filteredOngoing = computed(() => filterList(ongoingDrives.value))
const filteredClosed = computed(() => filterList(closedDrives.value))

async function apiFetch(url, method = 'GET', body = null) {
  const res = await fetch(`http://localhost:5000/api${url}`, {
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
  const drives = await apiFetch('/company/drives') || []
  ongoingDrives.value = drives.filter(d => d.status === 'Ongoing')
  closedDrives.value = drives.filter(d => d.status === 'Completed')
}

async function handleOngoingAction({ item, action }) {
  if (action === 'View Applications') {
    router.push(`/company/drives/${item.id}/applications`)
    return
  }

  if (action === 'Update') {
    router.push(`/company/drives/${item.id}/edit`)
    return
  }

  if (action === 'Mark as Completed') {
    const res = await apiFetch(`/company/drives/${item.id}/complete`, 'POST')
    if (res?.message) msgStore.updateErrorMessage(res.message)
    await loadDashboard()
  }
}

function handleClosedAction({ item, action }) {
  if (action === 'Review') {
    router.push(`/company/drives/${item.id}/review`)
  }
}

onMounted(loadDashboard)
</script>

<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Company Dashboard</h2>
      <router-link to="/drive/create" class="btn btn-success">Create Drive</router-link>
    </div>

    <div class="mb-3">
      <SearchBar v-model="searchTerm" placeholder="Search drives" maxWidth="320px" />
    </div>

    <Table
      title="Ongoing Drives"
      :headers="['ID','Job Title','Applicants','Status']"
      :fields="['id','job_title','applicants_count','status']"
      :items="filteredOngoing"
      :actions="[
        { text: 'View Applications', class: 'btn-primary' },
        { text: 'Update', class: 'btn-info' },
        { text: 'Mark as Completed', class: 'btn-success' }
      ]"
      :serialNumber="false"
      @actionClicked="handleOngoingAction"
    />

    <Table
      title="Closed Drives"
      :headers="['ID','Job Title','Applicants','Status']"
      :fields="['id','job_title','applicants_count','status']"
      :items="filteredClosed"
      :actions="[{ text: 'Review', class: 'btn-secondary' }]"
      :serialNumber="false"
      @actionClicked="handleClosedAction"
    />
  </div>
</template>
