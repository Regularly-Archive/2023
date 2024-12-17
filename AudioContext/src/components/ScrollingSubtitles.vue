<template>
  <div class="scrolling-subtitles">
    <div class="subtitles-container" ref="container">
      <div class="subtitles-content" :style="{ transform: `translateX(${-scrollPosition}px)` }">
        {{ visibleText }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScrollingSubtitles',
  props: {
    text: {
      type: String,
      default: ''
    },
    windowSize: {
      type: Number,
      default: 30
    },
    scrollSpeed: {
      type: Number,
      default: 50 // milliseconds per character
    }
  },
  data() {
    return {
      scrollPosition: 0,
      visibleText: '',
      intervalId: null
    }
  },
  watch: {
    text: {
      immediate: true,
      handler(newText) {
        this.resetScroll();
        this.startScrolling();
      }
    }
  },
  methods: {
    resetScroll() {
      this.scrollPosition = 0;
      this.visibleText = this.text.slice(0, this.windowSize);
    },
    startScrolling() {
      clearInterval(this.intervalId);
      this.intervalId = setInterval(this.scroll, this.scrollSpeed);
    },
    scroll() {
      if (this.scrollPosition < this.text.length - this.windowSize) {
        this.scrollPosition++;
        this.visibleText = this.text.slice(this.scrollPosition, this.scrollPosition + this.windowSize);
      } else {
        this.stopScrolling();
        this.$emit('scrolling-complete');
      }
    },
    stopScrolling() {
      clearInterval(this.intervalId);
    }
  },
  beforeUnmount() {
    this.stopScrolling();
  }
}
</script>

<style scoped>
.scrolling-subtitles {
  position: fixed;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
  width: 66.67%;
  height: 50px;
  overflow: hidden;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  font-size: 24px;
  display: flex;
  align-items: center;
}

.subtitles-container {
  width: 100%;
  overflow: hidden;
}

.subtitles-content {
  white-space: nowrap;
  transition: transform 0.1s linear;
}
</style>