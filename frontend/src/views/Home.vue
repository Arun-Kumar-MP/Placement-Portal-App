<!-- frontend/src/views/Home.vue -->

<template>
  <div class="container py-5 min-vh-100 d-flex flex-column">
    <div class="text-center mb-5">
      <h1 class="fw-bold">Placement Portal Application (PPA)</h1>
      <p class="lead text-muted mb-0">
        A role-based platform for Admin, Companies, and Students to manage campus placements smoothly.
      </p>
    </div>

    <div class="row g-4 mb-4">
      <div class="col-md-4">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Admin</h5>
            <p class="card-text mb-0">
              Approve companies, manage students, monitor applications, and track placement drives.
            </p>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Company</h5>
            <p class="card-text mb-0">
              Create drives, review applications, shortlist candidates, and update recruitment status.
            </p>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Student</h5>
            <p class="card-text mb-0">
              Build profile, browse drives, apply for opportunities, and track application progress.
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm mb-5">
      <div class="card-body">
        <h5 class="card-title">Key Features</h5>
        <ul class="mb-0">
          <li>Role-based authentication and dashboards</li>
          <li>Company approval and student management</li>
          <li>Placement drive creation and application tracking</li>
          <li>Application status updates from Applied to Selected</li>
        </ul>
      </div>
    </div>

    <footer class="mt-auto border-top pt-3 text-center text-muted small">
      <p class="mb-0">
        <strong>Developer:</strong> Arun Kumar M P |
        <strong>Contact:</strong> arunkpugal16@gmail.com |
        <strong><a href="https://github.com/arun-kumar-mp" target="_blank" rel="noopener noreferrer">GitHub</a></strong>
        | &copy; 2026
      </p>
    </footer>
  </div>
</template>
