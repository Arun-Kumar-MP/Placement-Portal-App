<!-- frontend/src/views/CompanyDriveReview.vue -->

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Table from '@/components/Table.vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const selectedApplications = ref([])
const driveName = ref('Drive')

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

onMounted(async () => {
  const driveId = route.params.id
  const drive = await apiFetch(`/company/drives/${driveId}`)
  const apps = await apiFetch(`/company/drives/${driveId}/applications`) || []

  driveName.value = drive?.job_title || 'Drive'
  selectedApplications.value = apps.filter(a => (a.status || '').startsWith('Selected'))
})
</script>

<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>Review - {{ driveName }}</h3>
      <button class="btn btn-outline-secondary" @click="router.push('/company-dashboard')">Back</button>
    </div>

    <div class="alert alert-success">
      Selected Applications: <strong>{{ selectedApplications.length }}</strong>
    </div>

    <Table
      title="Selected Candidates"
      :headers="['Application ID','Student Name','Branch','CGPA','Status']"
      :fields="['id','student_name','branch','cgpa','status']"
      :items="selectedApplications"
      :serialNumber="false"
    />
  </div>
</template>
