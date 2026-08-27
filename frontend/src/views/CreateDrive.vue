<!-- frontend/src/views/CreateDrive.vue -->

<script setup>
import { ref } from 'vue'
import DriveForm from '@/components/DriveForm.vue'
import { useAuthStore } from '@/stores/auth'
import { useMessageStore } from '@/stores/message'

const authStore = useAuthStore()
const msgStore = useMessageStore()
const formKey = ref(0)

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

async function createDrive(formData) {
  const res = await apiFetch('/company/drives', 'POST', formData)

  if (res?.message) {
    msgStore.updateErrorMessage(res.message)
    formKey.value += 1
  } else {
    msgStore.updateErrorMessage('Failed to create drive!')
  }
}
</script>

<template>
  <div class="container mt-4">
    <h3 class="mb-4">Create a Drive</h3>
    <div class="card p-4 shadow-sm">
      <DriveForm :key="formKey" :initialData="{}" submitLabel="Save" @submit="createDrive" />
    </div>
  </div>
</template>
