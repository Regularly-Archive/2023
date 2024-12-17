<template>
  <div class="iron-man-container">
    <img :src="currentImage" alt="Iron Man" class="iron-man-image">
    <div class="clickable-areas" style="display: none;">
      <div class="clickable-area reactor" @click="toggleReactor" :class="{ 'area-off': !reactorOn }"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IronManMask',
  data() {
    return {
      reactorOn: true,
      imageOff: '/assets/background.jpg',
      imageOn: '/assets/background.jpg'
    }
  },
  computed: {
    currentImage() {
      return this.reactorOn ? this.imageOn : this.imageOff;
    }
  },
  methods: {
    toggleReactor() {
      this.reactorOn = !this.reactorOn;
      console.log('Reactor toggled:', this.reactorOn);
      this.$emit('reactor-click');
    }
  }
}
</script>

<style scoped>
.iron-man-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.iron-man-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.clickable-areas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.clickable-area {
  position: absolute;
  transition: background-color 0.3s ease;
  pointer-events: auto;
}

.clickable-area:hover {
  cursor: pointer;
}

.reactor {
  bottom: calc(120 / 1080 * 100vh); /* 120px in 1080p becomes ~11.11vh */
  left: 50%;
  transform: translateX(-50%);
  width: calc(200 / 1920 * 100vw); /* 200px diameter in 1920p becomes ~10.42vw */
  height: calc(200 / 1920 * 100vw);
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.3);
}

.area-off {
  background-color: transparent;
}
</style>