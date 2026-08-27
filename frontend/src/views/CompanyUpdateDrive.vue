<!-- frontend/src/views/CompanyUpdateDrive.vue -->

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DriveForm from '@/components/DriveForm.vue'
import { useAuthStore } from '@/stores/auth'
import { useMessageStore } from '@/stores/message'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const msgStore = useMessageStore()

const driveId = route.params.id
const initialData = ref({})

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
  const data = await apiFetch(`/company/drives/${driveId}`)
  if (!data) return

  initialData.value = {
    job_title: data.job_title ?? '',
    job_description: data.job_description ?? '',
    salary: data.salary ?? '',
    skills_required: data.skills_required ?? '',
    min_cgpa: data.min_cgpa ?? '',
    eligibility_branch: data.eligibility_branch ?? '',
    eligibility_year: data.eligibility_year ?? '',
    application_deadline: data.application_deadline ?? ''
  }
})

async function updateDrive(formData) {
  const res = await apiFetch(`/company/drives/${driveId}/update`, 'POST', formData)

  if (res?.message) {
    msgStore.updateErrorMessage(res.message)
    router.push('/company-dashboard')
  } else {
    msgStore.updateErrorMessage('Failed to update drive!')
  }
}

function cancelEdit() {
  router.push('/company-dashboard')
}
</script>

<template>
  <div class="container mt-4">
    <h3 class="mb-4">Update Drive</h3>
    <div class="card p-4 shadow-sm">
      <DriveForm
        :initialData="initialData"
        submitLabel="Save Updates"
        :showCancel="true"
        @submit="updateDrive"
        @cancel="cancelEdit"
      />
    </div>
  </div>
</template>
