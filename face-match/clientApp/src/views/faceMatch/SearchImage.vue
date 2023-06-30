<template>
  <div>
      <div class="flex justify-center items-center">
      <label for="file-upload" class="flex flex-col items-center px-4 py-6 bg-white text-blue-500 rounded-lg shadow-lg tracking-wide uppercase cursor-pointer border border-blue-500 hover:bg-blue-500 hover:text-white">
        <span class="mt-2 leading-normal">上传图片</span>
        <input id="file-upload" type="file" class="hidden" @change="handleFileChange">
      </label>
    </div>
    <div class="grid grid-cols-4 gap-4">
      <div v-if="previewUrl" class="p-2 relative flex items-center justify-center">
        <img :src="'http://localhost:8000' + previewUrl" alt="Similar Image" class="w-full h-auto">
        <div class="absolute bottom-0 left-0 bg-black bg-opacity-50 p-4">
          <p class="text-white text-center">当前上传</p>
        </div>
      </div>
      <div v-for="image in similarImages" :key="image.faceId" class="relative flex items-center justify-center">
        <img :src="'http://localhost:8000' + image.faceUrl" alt="Similar Image" class="w-full h-auto">
        <div class="absolute bottom-0 left-0 bg-black bg-opacity-50 p-4">
          <p class="text-white text-center">{{ image.faceLabel }}, 相似度为: {{ ((1 - image.distance) * 100).toFixed(4) }}%</p>
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
      previewUrl: undefined
    };
  },
  methods: {
    handleFileChange(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('image', file);
      axios.post('http://localhost:8000/search?top=5&threshold-0.25', formData)
        .then(res => {
          const data = res.data.data
          this.similarImages = data.output;
          this.previewUrl = data.input.faceUrl;
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};
</script>

<style>
/* 可以在这里添加 Tailwind CSS 的自定义样式 */
</style>
