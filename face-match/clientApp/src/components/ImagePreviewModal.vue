<!-- src/components/ImagePreviewModal.vue -->
<template>
    <div v-if="isVisible" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-75 z-50">
      <div class="relative bg-white rounded-lg p-4">
        <button @click="close" class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 bg-gray-200 rounded-full p-2">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <img :src="imageUrl" alt="Preview" class="max-w-full max-h-screen" />
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      isVisible: {
        type: Boolean,
        required: true
      },
      imageUrl: {
        type: String,
        required: true
      }
    },
    methods: {
      close() {
        this.$emit('close');
      }
    }
  };
  </script>
  
  <style scoped>
  </style>