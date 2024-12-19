<template>
    <div class="flex justify-center items-center mt-4">
      <button 
      @click="prevPage" 
      :disabled="currentPage === 1" 
      class="text-blue-500 px-3 py-2 rounded-md mr-2 hover:text-blue-600 hover:font-bold transition cursor-pointer"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>

    <div class="flex items-center">
      <span class="text-gray-700">第</span>
      <span class="font-bold mx-2">{{ currentPage }}</span>
      <span class="text-gray-700">页 / 共</span>
      <span class="font-bold mx-2">{{ totalPages }}</span>
      <span class="text-gray-700">页</span>
    </div>

    <button 
      @click="nextPage" 
      :disabled="currentPage === totalPages" 
      class="text-blue-500 px-3 py-2 rounded-md mr-2 hover:text-blue-600 hover:font-bold transition cursor-pointer"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      currentPage: {
        type: Number,
        required: true
      },
      pageSize: {
        type: Number,
        required: true
      },
      totalCount: {
        type: Number,
        required: true
      }
    },
    computed: {
      totalPages() {
        return Math.ceil(this.totalCount / this.pageSize)
      }
    },
    methods: {
      prevPage() {
        if (this.currentPage > 1) {
          this.$emit('change-page', this.currentPage - 1);
        }
      },
      nextPage() {
        if (this.currentPage < this.totalPages) {
          this.$emit('change-page', this.currentPage + 1);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* 添加样式 */
  </style>