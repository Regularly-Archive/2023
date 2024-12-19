<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">人脸上传</h1>
    <div class="max-w-2xl mx-auto">
      <!-- Upload Section -->
      <div class="mb-8">
        <div class="flex flex-col items-center">
          <label for="file-upload" 
                 class="flex flex-col items-center px-6 py-8 bg-white text-blue-600 rounded-xl shadow-lg cursor-pointer border-2 border-dashed border-blue-400 hover:border-blue-600 hover:bg-blue-50 transition-all duration-300 w-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span class="text-lg font-semibold">点击上传图片</span>
            <span class="text-sm text-gray-500 mt-1">支持 JPG, PNG 格式</span>
          </label>
          <input id="file-upload" type="file" accept="image/*" class="hidden" @change="handleFileChange">
        </div>
      </div>

      <!-- Preview and Form -->
      <div v-if="previewUrl" class="space-y-6">
        <div class="relative overflow-hidden rounded-lg shadow-lg">
          <img 
              :src="previewUrl" 
              alt="Preview" 
              class="w-full h-64 object-cover cursor-pointer"
              @click="showPreview(previewUrl)"
          >
        </div>

        <!-- Label Input -->
        <div class="space-y-2">
          <label for="image-label" class="block text-sm font-medium text-gray-700">图片标签</label>
          <input type="text" 
                 id="image-label" 
                 v-model="imageLabel"
                 class="mt-1 block w-full rounded-md border border-blue-400 shadow-sm focus:border-blue-600 hover:border-blue-600 sm:text-sm h-12 px-2"
                 placeholder="请输入图片标签">
        </div>

        <!-- Submit Button -->
        <button @click="handleSubmit"
                :disabled="isLoading || !imageLabel"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">
          {{ isLoading ? '上传中...' : '确认上传' }}
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="mt-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <span class="block sm:inline">{{ error }}</span>
        <button @click="error = null" class="absolute top-0 bottom-0 right-0 px-4 py-3">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="mt-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
        <span class="block sm:inline">{{ successMessage }}</span>
        <button @click="successMessage = null" class="absolute top-0 bottom-0 right-0 px-4 py-3">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Image Preview Modal -->
    <ImagePreviewModal 
      :isVisible="isModalVisible" 
      :imageUrl="modalImageUrl" 
      @close="isModalVisible = false" 
    />
  </div>
  
</template>

<script>
import ImagePreviewModal from '@/components/ImagePreviewModal.vue';
const axios = require('axios').default;

export default {
  components: {
    ImagePreviewModal
  },
  data() {
    return {
      previewUrl: null,
      imageLabel: '',
      selectedFile: null,
      isLoading: false,
      error: null,
      successMessage: null,
      isModalVisible: false,
      modalImageUrl: ''
    };
  },
  methods: {
    handleFileChange(event) {
      const file = event.target.files[0];
      
      // Validate file type
      if (!file.type.match('image.*')) {
        this.error = '请上传图片文件（JPG, PNG）';
        return;
      }

      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        this.error = '图片大小不能超过5MB';
        return;
      }

      this.selectedFile = file;
      this.previewUrl = URL.createObjectURL(file);
      this.error = null;
    },

    async handleSubmit() {
      if (!this.selectedFile || !this.imageLabel) {
        this.error = '请选择图片并输入标签';
        return;
      }

      this.isLoading = true;
      this.error = null;
      this.successMessage = null;

      const formData = new FormData();
      formData.append('image', this.selectedFile);

      try {
        await axios.post(`http://localhost:8000/faces/upload?label=${this.imageLabel}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        this.successMessage = '图片上传成功！';
        this.resetForm();
      } catch (error) {
        this.error = error.response?.data?.message || '上传失败，请重试';
        console.error('Error:', error);
      } finally {
        this.isLoading = false;
      }
    },

    resetForm() {
      this.selectedFile = null;
      this.previewUrl = null;
      this.imageLabel = '';
    },
    showPreview(imageUrl) {
      this.modalImageUrl = imageUrl;
      this.isModalVisible = true;
    }
  }
};
</script>
