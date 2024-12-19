<template>
    <div v-if="isVisible" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-75 z-50">
      <div class="bg-white rounded-lg p-4 w-1/3">
        <h2 class="text-lg font-bold mb-4">编辑标签</h2>
        <input type="text" v-model="label" class="border rounded-md p-2 w-full" />
        <div class="flex justify-end mt-4">
          <button @click="close" class="bg-gray-500 text-white px-4 py-2 rounded-md mr-2">取消</button>
          <button @click="confirmEdit" class="bg-green-500 text-white px-4 py-2 rounded-md">确认</button>
        </div>
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
      currentLabel: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        label: ''
      };
    },
    mounted() {
        this.label = this.currentLabel;
    },
    methods: {
      close() {
        this.$emit('close');
      },
      confirmEdit() {
        this.$emit('confirm', this.label);
        this.close();
      }
    }
  };
  </script>
  
  <style scoped>
  </style>