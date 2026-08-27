<!-- frontend/src/components/Details.vue -->

<script setup>
import { defineProps } from 'vue';

defineProps({
  entity: { type: Object, default: () => ({}) },
  type: { type: String, default: 'student' } // 'student' or 'drive'
});
</script>

<template>
  <div class="d-flex justify-content-center mt-4">
    <div class="card shadow-sm p-4" style="max-width: 500px; width: 100%;">
      <h5 class="mb-3">
        {{ type === 'student' ? 'Student Details' : 'Drive Details' }}
      </h5>

      <template v-if="type === 'student'">
        <p><strong>Name:</strong> {{ entity.student_name || entity.name || 'Unknown' }}</p>
        <p><strong>Branch:</strong> {{ entity.branch || 'Unknown' }}</p>
        <p><strong>CGPA:</strong> {{ entity.cgpa || 'N/A' }}</p>
        <p><strong>Year:</strong> {{ entity.year || 'N/A' }}</p>

        <div>
          <a
            v-if="entity.resume"
            :href="entity.resume"
            target="_blank"
            rel="noopener noreferrer"
            class="btn btn-primary btn-sm"
          >
            View Resume
          </a>
          <span v-else class="text-muted small">Resume not uploaded</span>
        </div>
      </template>

      <template v-else>
        <p><strong>Job Title:</strong> {{ entity.job_title || 'Unknown' }}</p>
        <p><strong>Description:</strong> {{ entity.job_description || 'N/A' }}</p>
        <p><strong>Salary:</strong> {{ entity.salary || 'N/A' }}</p>
        <p><strong>Skills Required:</strong> {{ entity.skills_required || 'N/A' }}</p>
        <p><strong>Minimum CGPA:</strong> {{ entity.min_cgpa || 'N/A' }}</p>
        <p><strong>Eligibility Branch:</strong> {{ entity.eligibility_branch || 'N/A' }}</p>
        <p><strong>Eligibility Year:</strong> {{ entity.eligibility_year || 'N/A' }}</p>
        <p><strong>Status:</strong> {{ entity.status || 'N/A' }}</p>
        <p><strong>Company:</strong> {{ entity.company_name || 'Unknown' }}</p>
        <p><strong>Website:</strong> {{ entity.company_website || 'N/A' }}</p>
        <p><strong>Application Deadline:</strong> {{ entity.application_deadline || 'N/A' }}</p>
      </template>
    </div>
  </div>
</template>
