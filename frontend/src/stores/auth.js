// frontend/src/stores/auth.js

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('authStore', () => {
    const auth_token = ref(localStorage.getItem('auth_token') || null)
    const role = ref(localStorage.getItem('role') || null)
    const email = ref(localStorage.getItem('email') || null)

    const isAuthenticated = computed(() => !!auth_token.value)

    function setUser(token, userRole, userEmail = null) {
        localStorage.setItem('auth_token', token)
        localStorage.setItem('role', userRole)
        auth_token.value = token
        role.value = userRole

        if (userEmail) {
            localStorage.setItem('email', userEmail)
            email.value = userEmail
        }
    }

    function clearAuth() {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('role')
        localStorage.removeItem('email')
        auth_token.value = null
        role.value = null
        email.value = null
    }

    return { auth_token, role, email, isAuthenticated, setUser, clearAuth }
})
