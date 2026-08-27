<!-- frontend/src/views/Login.vue -->

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useMessageStore } from '@/stores/message';

const router = useRouter();
const authStore = useAuthStore();
const messageStore = useMessageStore();

const email = ref('');
const password = ref('');
const passwordError = ref('');

const validatePassword = () => {
    if (password.value.length < 5) {
        passwordError.value = 'Password must be at least 5 characters long!';
        return false;
    } else {
        passwordError.value = '';
        return true;
    }
};

async function login() {
    if (!validatePassword() || email.value === '' || password.value === '') {
        messageStore.updateErrorMessage('Please check your credentials and try again!');
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: email.value,
                password: password.value
            })
        });

        const data = await response.json();

        if (response.ok) {
            authStore.setUser(data.user.auth_token, data.user.roles[0], data.user.email);
            messageStore.updateErrorMessage(data.message || "Welcome back!");

            // Role-based routing
            if (authStore.role === 'admin') {
                router.push('/admin-dashboard');
            } else if (authStore.role === 'company') {
                router.push('/company-dashboard');
            } else {
                router.push('/student-dashboard');
            }
        } else {
            messageStore.updateErrorMessage(data.error || "Login failed!");
        }
    } catch (error) {
        messageStore.updateErrorMessage("Server is unreachable. Is Flask running?");
    }
}
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-4 card p-4 shadow-sm">
                <h2 class="text-center mb-4">PPA Login</h2>
                <form @submit.prevent="login">
                    <div class="mb-3">
                        <label class="form-label">Email address</label>
                        <input type="email" class="form-control" v-model="email" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="password" @input="validatePassword" required>
                        <div class="form-text text-danger">{{ passwordError }}</div>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
            </div>
        </div>
    </div>
</template>
