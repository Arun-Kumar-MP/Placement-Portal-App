// frontend/src/stores/message.js

import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useMessageStore = defineStore('messageStore', () => {
    const errorMessage = ref('')

    function updateErrorMessage(message) {
        errorMessage.value = message
        // Automatically hide the message after 3 seconds
        setTimeout(() => {
            errorMessage.value = ''
        }, 3000)
    }

    return { errorMessage, updateErrorMessage }
})