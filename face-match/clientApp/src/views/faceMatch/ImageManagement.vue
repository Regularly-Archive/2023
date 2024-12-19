<!-- src/views/faceMatch/ImageManagement.vue -->
<template>
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-2xl font-bold mb-6">图片管理</h1>
      <div class="mt-6 flex items-center mb-6">
        <input 
          type="text" 
          v-model="searchParams.label" 
          placeholder="输入标签进行搜索" 
          class="border rounded-md p-2 w-full mr-2"
          @keyup.enter="handleKeywordSearch"
        />
      </div>
      <div v-if="images.length === 0" class="text-center text-gray-500">
        <p>没有找到符合条件的图片</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" v-else>
        <div v-for="image in images" :key="image.id" class="relative group overflow-hidden rounded-lg shadow-lg">
          <img 
            :src="'http://localhost:8000' + image.faceUrl" 
            :alt="image.faceLabel" 
            class="w-full h-64 object-cover cursor-pointer transition-transform duration-300 hover:scale-105"
            @click="showPreview('http://localhost:8000' + image.faceUrl)"
          >
          <div class="flex justify-between items-center">
            <span class="px-2">{{ image.faceLabel }}</span>
            <div>
              <button @click="openEditModal(image)" class="text-black px-2 py-2 rounded-md hover:font-bold">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 4l4 4-8 8H8v-4l8-8z" />
                </svg> 编辑
              </button>
              <button @click="deleteImage(image.faceId)" class="text-black px-2 py-2 rounded-md hover:font-bold">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg> 删除
              </button>
            </div>
          </div>
        </div>
      </div>

      <MyPagination
        class="fixed bottom-0 left-0 right-0 shadow-lg z-10 bg-white bg-opacity-50"
        :currentPage="searchParams.page" 
        :pageSize="searchParams.pageSize" 
        :totalCount="totalCount"
        @change-page="handlePageChanged"
      />

      <!-- Image Preview Modal -->
      <ImagePreviewModal 
        :isVisible="isModalVisible" 
        :imageUrl="modalImageUrl" 
        @close="isModalVisible = false" 
      />

      <!-- Edit Label Modal -->
      <EditLabelModal 
        :isVisible="isEditModalVisible" 
        :currentLabel="currentLabel" 
        @close="isEditModalVisible = false" 
        @confirm="updateLabel(imageToEdit.faceId, $event)"
      />
    </div>
  </template>
  
  <script>
  const axios = require('axios').default;
  import EditLabelModal from '@/components/EditLabelModal.vue';
  import ImagePreviewModal from '@/components/ImagePreviewModal.vue';
  import MyPagination from '@/components/MyPagination.vue';
  
  export default {
    components: {
        ImagePreviewModal,
        EditLabelModal,
        MyPagination
    },
    data() {
      return {
        images: [],
        isModalVisible: false,
        modalImageUrl: '',
        isEditModalVisible: false,
        currentLabel: '',
        imageToEdit: null,
        searchParams: {
            label: '',
            page: 1, 
            pageSize: 12
        },
        totalCount: 0
      };
    },
    created() {
      this.fetchImages();
    },
    methods: {
      async fetchImages() {
        try {
          const response = await axios.get('http://localhost:8000/faces', {
            params: this.searchParams
          });
          const data = response.data.data;
          this.images = data.rows.map(x => {
            return {
                ...x,
                isEditing: false
            }
          });
          this.totalCount = data.total;
        } catch (error) {
          console.error('获取图片时出错:', error);
        }
      },
      async updateLabel(imageId, newLabel) {
        try {
          await axios.put(`http://localhost:8000/faces/${imageId}?label=${newLabel}`);
          this.fetchImages();
        } catch (error) {
          console.error('更新标签时出错:', error);
        }
      },
      async deleteImage(imageId) {
        if (confirm('确定要删除这张图片吗？')) {
          try {
            await axios.delete(`http://localhost:8000/faces/${imageId}`);
            this.fetchImages();
          } catch (error) {
            console.error('删除图片时出错:', error);
          }
        }
      },
      showPreview(imageUrl) {
        this.modalImageUrl = imageUrl;
        this.isModalVisible = true;
      },
      openEditModal(image) {
        this.currentLabel = image.faceLabel;
        this.imageToEdit = image;
        this.isEditModalVisible = true;
      },
      handlePageChanged(val) {
        this.searchParams.page = val;
        this.fetchImages();
      },
      handleKeywordSearch() {
        this.searchParams.page = 1;
        this.fetchImages();
      }
    }
  };
  </script>