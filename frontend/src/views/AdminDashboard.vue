<!-- frontend/src/views/AdminDashboard.vue -->

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

const router = useRouter()
const authStore = useAuthStore()
const msgStore = useMessageStore()

const pendingCompanies = ref([])
const activeCompanies = ref([])
const students = ref([])
const ongoingDrives = ref([])
const applications = ref([])
const searchTerm = ref('')

const normalizedSearch = computed(() => searchTerm.value.trim().toLowerCase())

function filterBySearch(list, fields) {
  if (!normalizedSearch.value) return list
  return list.filter(item =>
    fields.some(field => String(item[field] ?? '').toLowerCase().includes(normalizedSearch.value))
  )
}

const filteredPendingCompanies = computed(() => filterBySearch(pendingCompanies.value, ['name', 'email']))
const filteredActiveCompanies = computed(() => filterBySearch(activeCompanies.value, ['name', 'email']))
const filteredStudents = computed(() => filterBySearch(students.value, ['name', 'branch', 'email']))
const filteredOngoingDrives = computed(() => filterBySearch(ongoingDrives.value, ['job_title', 'company_name']))

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
  const compData = await apiFetch('/admin/companies')
  if (compData) {
    pendingCompanies.value = compData.applications
    activeCompanies.value = compData.registered
  }

  students.value = await apiFetch('/admin/students') || []
  ongoingDrives.value = await apiFetch('/admin/drives/ongoing') || []
  applications.value = await apiFetch('/admin/applications') || []
}

async function handleCompanyAction({ item, action }) {
  const payload = { active: action === 'Approve' }
  const res = await apiFetch(`/admin/companies/${item.id}`, 'PUT', payload)

  if (res?.message) {
    msgStore.updateErrorMessage(res.message)
    await loadDashboard()
  } else {
    msgStore.updateErrorMessage('Company action failed!')
  }
}

async function handleStudentAction({ item, action }) {
  if (action !== 'Blacklist') return

  const res = await apiFetch(`/admin/students/${item.id}`, 'PUT', { active: false })
  if (res?.message) {
    msgStore.updateErrorMessage(res.message)
    await loadDashboard()
  } else {
    msgStore.updateErrorMessage('Student action failed!')
  }
}

async function handleOngoingDriveAction({ item, action }) {
  if (action === 'View Details') {
    router.push(`/admin/drives/${item.id}/details`)
    return
  }

  if (action === 'Mark as Complete') {
    const res = await apiFetch(`/admin/drives/${item.id}/complete`, 'POST')
    if (res?.message) msgStore.updateErrorMessage(res.message)
    await loadDashboard()
  }
}

function handleApplicationAction({ item }) {
  if (item.student_id) router.push(`/student/${item.student_id}/details`)
}

onMounted(loadDashboard)
</script>

<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Admin Control Panel</h2>
      <SearchBar
        v-model="searchTerm"
        placeholder="Search students, companies, drives"
        maxWidth="320px"
      />
    </div>

    <Table title="Pending Company Approvals"
           :headers="['ID','Name','Email']"
           :fields="['id','name','email']"
           :items="filteredPendingCompanies"
           :actions="[{text:'Approve',class:'btn-success'}]"
           @actionClicked="handleCompanyAction" />

    <Table title="Registered Companies"
           :headers="['ID','Name','Email']"
           :fields="['id','name','email']"
           :items="filteredActiveCompanies"
           :actions="[{text:'Blacklist',class:'btn-outline-danger'}]"
           @actionClicked="handleCompanyAction" />

    <Table title="Student Records"
           :headers="['ID','Name','CGPA','Branch']"
           :fields="['id','name','cgpa','branch']"
           :items="filteredStudents"
           :actions="[{text:'Blacklist',class:'btn-outline-danger'}]"
           @actionClicked="handleStudentAction" />

    <Table title="Ongoing Drives"
           :headers="['ID','Job Title','Company','Deadline','Applicants']"
           :fields="['id','job_title','company_name','application_deadline','applicants_count']"
           :items="filteredOngoingDrives"
           :actions="[
             { text:'View Details', class:'btn-primary' },
             { text:'Mark as Complete', class:'btn-success' }
           ]"
           :serialNumber="false"
           @actionClicked="handleOngoingDriveAction" />

    <Table title="Student Applications"
           :headers="['ID','Student','Job Title','Company','Applied On']"
           :fields="['id','student_name','drive_title','company_name','application_date']"
           :items="applications"
           :actions="[{ text:'View', class:'btn-primary' }]"
           @actionClicked="handleApplicationAction" />
  </div>
</template>
