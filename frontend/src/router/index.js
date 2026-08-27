// frontend/src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Home', component: () => import('../views/Home.vue') },
    { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
    { path: '/register', name: 'Register', component: () => import('../views/Register.vue') },

    {
      path: '/admin-dashboard',
      name: 'AdminDashboard',
      component: () => import('../views/AdminDashboard.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/drives/:id/details',
      name: 'AdminDriveDetails',
      component: () => import('../views/DriveDetails.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/student/:id/details',
      name: 'StudentDetails',
      component: () => import('@/views/StudentDetails.vue'),
      props: true,
      meta: { requiresAuth: true, role: 'admin' }
    },

    {
      path: '/company-dashboard',
      name: 'CompanyDashboard',
      component: () => import('../views/CompanyDashboard.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },
    {
      path: '/drive/create',
      name: 'CreateDrive',
      component: () => import('../views/CreateDrive.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },
    {
      path: '/company/drives/:id/applications',
      name: 'DriveApplication',
      component: () => import('../views/DriveApplication.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },
    {
      path: '/company/drives/:id/edit',
      name: 'CompanyUpdateDrive',
      component: () => import('../views/CompanyUpdateDrive.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },
    {
      path: '/company/drives/:id/review',
      name: 'CompanyDriveReview',
      component: () => import('../views/CompanyDriveReview.vue'),
      meta: { requiresAuth: true, role: 'company' }
    },

    {
      path: '/student-dashboard',
      name: 'StudentDashboard',
      component: () => import('../views/StudentDashboard.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/student/profile',
      name: 'StudentProfile',
      component: () => import('../views/StudentProfile.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/student/history',
      name: 'StudentHistory',
      component: () => import('../views/StudentHistory.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/student/drives/:id',
      name: 'StudentDriveDetails',
      component: () => import('../views/DriveDetails.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.role && authStore.role !== to.meta.role) {
    next('/')
  } else {
    next()
  }
})

export default router
