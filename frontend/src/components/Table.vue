<!-- frontend/src/components/Table.vue -->

<script setup>
const props = defineProps({
    title: String,
    headers: Array,
    fields: Array,
    items: { type: Array, default: () => [] },
    actions: Array,
    serialNumber: { type: Boolean, default: true } // toggle S.No vs actual ID
});
const emit = defineEmits(['actionClicked']);
</script>

<template>
    <div class="card shadow-sm mb-4">
        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
            <span>{{ title }}</span>
            <span class="badge bg-primary">{{ items.length }} Total</span>
        </div>
        <table class="table table-hover mb-0">
            <thead class="table-light">
                <tr>
                    <th v-for="h in headers" :key="h" class="text-center">{{ h }}</th>
                    <th v-if="actions" class="text-center">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-if="items.length === 0">
                    <td :colspan="headers.length + (actions ? 1 : 0)" class="text-center text-muted">
                        No records found
                    </td>
                </tr>
                <tr v-for="(item, index) in items" :key="item.id">
                    <td v-for="field in fields" :key="field" class="text-center">
                        <span v-if="field === 'active'" :class="['badge', item[field] ? 'bg-success' : 'bg-secondary']">
                            {{ item[field] ? 'Active' : 'Pending' }}
                        </span>
                        <span v-else-if="field === 'id'">
                            {{ serialNumber ? index + 1 : item.id }}
                        </span>
                        <span v-else>{{ item[field] }}</span>
                    </td>
                    <td v-if="actions" class="text-center">
                        <button v-for="act in actions" :key="act.text"
                                @click="emit('actionClicked', {item, action: act.text})"
                                :class="['btn btn-sm ms-1', act.class]">
                            {{ act.text }}
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>