<!-- frontend/src/components/Status.vue -->

<script setup>
const props = defineProps({
  drive: { type: Object, default: () => ({}) },
  students: { type: Array, default: () => [] },
  mode: { type: String, default: 'view' } // 'view' for drive details, 'applications' for student list
});
const emit = defineEmits(['reviewStudent']);
</script>

<template>
  <div class="card p-4 shadow-sm mb-4">
    <h4 class="mb-3">
      {{ mode === 'view' ? 'Drive Details' : 'Applications Received' }}
    </h4>

    <!-- Drive Details -->
    <div v-if="mode === 'view'">
      <p><strong>Job Title:</strong> {{ drive.job_title }}</p>
      <p><strong>Description:</strong> {{ drive.job_description }}</p>
      <p><strong>Salary:</strong> {{ drive.salary }}</p>
      <p><strong>Skills Required:</strong> {{ drive.skills_required }}</p>
      <p><strong>Minimum CGPA:</strong> {{ drive.min_cgpa }}</p>
      <p><strong>Eligibility Branch:</strong> {{ drive.eligibility_branch }}</p>
      <p><strong>Eligibility Year:</strong> {{ drive.eligibility_year }}</p>
      <p><strong>Application Deadline:</strong> {{ drive.application_deadline }}</p>
    </div>

    <!-- Student Applications -->
    <div v-else>
      <table class="table table-hover">
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Branch</th><th>CGPA</th><th>Status</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in students" :key="s.id">
            <td>{{ s.id }}</td>
            <td>{{ s.student_name }}</td>
            <td>{{ s.branch }}</td>
            <td>{{ s.cgpa }}</td>
            <td>{{ s.status }}</td>
            <td>
              <button class="btn btn-sm btn-primary"
                      @click="emit('reviewStudent', s)">
                Review Application
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>