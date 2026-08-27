<!-- frontend/src/components/DriveForm.vue -->

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({})
  },
  submitLabel: {
    type: String,
    default: 'Save'
  },
  showCancel: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

function emptyForm() {
  return {
    job_title: '',
    job_description: '',
    salary: '',
    skills_required: '',
    min_cgpa: '',
    eligibility_branch: '',
    eligibility_year: '',
    application_deadline: ''
  }
}

const form = reactive(emptyForm())

watch(
  () => props.initialData,
  (value) => {
    const next = { ...emptyForm(), ...(value || {}) }
    Object.assign(form, next)
  },
  { immediate: true, deep: true }
)

function submitForm() {
  emit('submit', { ...form })
}
</script>

<template>
  <form @submit.prevent="submitForm">
    <div class="mb-3">
      <label class="form-label"><strong>Job Title</strong></label>
      <input v-model="form.job_title" class="form-control" placeholder="Software Engineer" required>
    </div>

    <div class="mb-3">
      <label class="form-label"><strong>Job Description</strong></label>
      <textarea
        v-model="form.job_description"
        class="form-control"
        placeholder="Responsible for developing and maintaining web applications..."
        required
      />
    </div>

    <div class="row">
      <div class="col-md-6 mb-3">
        <label class="form-label"><strong>Salary (CTC)</strong></label>
        <input v-model="form.salary" type="number" step="1" class="form-control" placeholder="650000" required>
        <small class="text-muted">Enter CTC in INR (e.g., 650000)</small>
      </div>

      <div class="col-md-6 mb-3">
        <label class="form-label"><strong>Minimum CGPA</strong></label>
        <input v-model="form.min_cgpa" type="number" step="0.01" class="form-control" placeholder="7.5" required>
      </div>
    </div>

    <div class="mb-3">
      <label class="form-label"><strong>Skills Required</strong></label>
      <input v-model="form.skills_required" class="form-control" placeholder="Java, SQL, Problem Solving" required>
    </div>

    <div class="mb-3">
      <label class="form-label"><strong>Eligibility Branch</strong></label>
      <input v-model="form.eligibility_branch" class="form-control" placeholder="CSE, IT, ECE" required>
    </div>

    <div class="mb-3">
      <label class="form-label"><strong>Eligibility Year</strong></label>
      <input v-model="form.eligibility_year" type="number" class="form-control" placeholder="2026" required>
    </div>

    <div class="mb-3">
      <label class="form-label"><strong>Application Deadline</strong></label>
      <input v-model="form.application_deadline" type="date" class="form-control" required>
    </div>

    <div class="d-flex gap-2">
      <button type="submit" class="btn btn-success">{{ submitLabel }}</button>
      <button v-if="showCancel" type="button" class="btn btn-outline-secondary" @click="emit('cancel')">Cancel</button>
    </div>
  </form>
</template>

