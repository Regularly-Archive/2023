<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Upload Section -->
    <div class="mb-8">
      <div class="flex flex-col items-center">
        <label for="file-upload" 
               class="flex flex-col items-center px-6 py-8 bg-white text-blue-600 rounded-xl shadow-lg cursor-pointer border-2 border-dashed border-blue-400 hover:border-blue-600 hover:bg-blue-50 transition-all duration-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span class="text-lg font-semibold">点击上传图片</span>
          <span class="text-sm text-gray-500 mt-1">支持 JPG, PNG 格式</span>
        </label>
        <input id="file-upload" type="file" accept="image/*" class="hidden" @change="handleFileChange">
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6" role="alert">
      <span class="block sm:inline">{{ error }}</span>
      <button @click="error = null" class="absolute top-0 bottom-0 right-0 px-4 py-3">
        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Results Grid -->
    <div v-if="!isLoading && (previewUrl || similarImages.length > 0)" class="space-y-6">
      <!-- Preview Section -->
      <div v-if="previewUrl" class="mb-8">
        <h2 class="text-xl font-semibold mb-4">上传的图片</h2>
        <div class="relative group overflow-hidden rounded-lg shadow-lg">
          <img :src="'http://localhost:8000' + previewUrl" 
               alt="Uploaded Image" 
               class="w-full h-64 object-cover">
          <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4">
            <p class="text-white font-medium">参考图片</p>
          </div>
        </div>
      </div>

      <!-- Similar Images Section -->
      <div v-if="similarImages.length > 0">
        <h2 class="text-xl font-semibold mb-4">相似图片</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div v-for="image in similarImages" 
               :key="image.faceId" 
               class="relative group overflow-hidden rounded-lg shadow-lg transition-transform duration-300 hover:scale-105">
            <img :src="'http://localhost:8000' + image.faceUrl" 
                 :alt="image.faceLabel" 
                 class="w-full h-64 object-cover">
            <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4">
              <p class="text-white font-medium">{{ image.faceLabel }}</p>
              <p class="text-white/90 text-sm">
                相似度: <span class="font-semibold">{{ ((1 - image.distance) * 100).toFixed(2) }}%</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require('axios').default;

export default {
  data() {
    return {
      similarImages: [],
      previewUrl: undefined,
      isLoading: false,
      error: null
    };
  },
  methods: {
    async handleFileChange(event) {
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

      this.error = null;
      this.isLoading = true;
      const formData = new FormData();
      formData.append('image', file);

      try {
        const response = await axios.post('http://localhost:8000/search?top=5&threshold=0.25', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        const data = response.data.data;
        this.similarImages = data.output;
        this.previewUrl = data.input.faceUrl;
      } catch (error) {
        this.error = error.response?.data?.message || '图片上传失败，请重试';
        console.error('Error:', error);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 1400px;
}
</style>
