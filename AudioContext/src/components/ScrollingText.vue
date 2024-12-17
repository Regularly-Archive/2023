<template>
  <div class="scrolling-text-container">
    <div class="scrolling-text">
      {{ visibleText }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScrollingText',
  props: {
    initialText: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      fullText: '',
      visibleText: '',
      windowSize: 100, // 可见字符数
      scrollPosition: 0,
      scrollInterval: null,
      isScrolling: false,
      lastInputTime: Date.now()
    }
  },
  mounted() {
    this.fullText = this.initialText;
    this.updateVisibleText();
    this.startScrolling()
  },
  beforeDestroy() {
    this.stopScrolling();
  },
  methods: {
    startScrolling() {
      if (!this.isScrolling) {
        this.isScrolling = true;
        this.scrollInterval = setInterval(() => {
          this.scrollPosition++;
          if (this.scrollPosition > this.fullText.length) {
            this.scrollPosition = 0;
          }
          this.updateVisibleText();
          
          // 检查是否应该停止滚动
          if (Date.now() - this.lastInputTime > 5000) { // 5秒无输入后停止
            this.stopScrolling();
            this.visibleText = ''
          }
        }, 100); // 调整滚动速度
      }
    },
    stopScrolling() {
      if (this.isScrolling) {
        this.isScrolling = false;
        clearInterval(this.scrollInterval);
      }
    },
    updateVisibleText() {
      let start = this.scrollPosition;
      let end = start + this.windowSize;
      if (end > this.fullText.length) {
        this.visibleText = this.fullText.slice(start) + this.fullText.slice(0, end - this.fullText.length);
      } else {
        this.visibleText = this.fullText.slice(start, end);
      }
    }
  }
}
</script>

<style scoped>
.scrolling-text-container {
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
  position: fixed;
  bottom: 120px; /* 调整位置，使其位于 AudioVisualizer 上方 */
  left: 0;
  z-index: 20; /* 确保在 AudioVisualizer 上方 */
}
.scrolling-text {
  font-size: 24px; /* 增大字体大小 */
  color: white; /* 设置字体颜色为白色 */
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5); /* 添加文字阴影以增加可读性 */
  padding: 10px;
}
</style>