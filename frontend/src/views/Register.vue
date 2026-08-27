<!-- frontend/src/views/Register.vue -->

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useMessageStore } from '@/stores/message';

const router = useRouter();
const messageStore = useMessageStore();

const name = ref('');
const email = ref('');
const password = ref('');
const role = ref('student'); // Default role
const passwordMessage = ref('');
const checkEmailMessage = ref('');

const validatePassword = () => {
    if (password.value.length < 5) {
        passwordMessage.value = 'Password must be at least 5 characters long!';
        return false;
    } else {
        passwordMessage.value = '';
        return true;
    }
};

async function checkEmail() {
    if (email.value === '') {
        checkEmailMessage.value = '';
        return;
    }
    const response = await fetch("http://localhost:5000/api/auth/check-email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.value })
    });
    const data = await response.json();
    checkEmailMessage.value = data.available ? 'Email is Available!' : 'Email is Not Available!';
}

async function register() {
    if (email.value === '' || password.value === '' || name.value === '') {
        messageStore.updateErrorMessage('Please fill in all fields!');
        return;
    }

    if (!validatePassword()) return;

    if (checkEmailMessage.value === 'Email is Not Available!') {
        messageStore.updateErrorMessage('Email is already taken!');
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/api/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: name.value,   // ✅ backend expects username
                email: email.value,
                password: password.value,
                role_name: role.value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            messageStore.updateErrorMessage(data.error || 'Registration failed!');
        } else {
            messageStore.updateErrorMessage(data.message || "Registration Successful! Please Login :)");
            router.push('/login');
        }
    } catch (error) {
        messageStore.updateErrorMessage("Connection error. Is the backend running?");
    }
}
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-5 card p-4 shadow-sm">
                <h2 class="text-center mb-4">Create PPA Account</h2>
                <form @submit.prevent="register">
                    <div class="mb-3">
                        <label class="form-label">{{ role === 'company' ? 'Company Name' : 'Full Name' }}</label>
                        <input type="text" class="form-control" v-model="name" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Register As</label>
                        <select class="form-select" v-model="role">
                            <option value="student">Student</option>
                            <option value="company">Company</option>
                        </select>
                        <div class="form-text" v-if="role === 'company'">
                            Note: Company accounts require Admin approval.
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email address</label>
                        <input type="email" class="form-control" v-model="email" @input="checkEmail" required>
                        <div :class="['form-text', checkEmailMessage.includes('Not') ? 'text-danger' : 'text-success']">
                            {{ checkEmailMessage }}
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="password" @input="validatePassword" required>
                        <div class="form-text text-danger">{{ passwordMessage }}</div>
                    </div>
                    <button type="submit" class="btn btn-success w-100">Register</button>
                </form>
            </div>
        </div>
    </div>
</template>