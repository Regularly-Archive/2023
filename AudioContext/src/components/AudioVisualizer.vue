<template>
    <div class="audio-visualizer-container">
        <canvas ref="visualizer" :width="canvasWidth" :height="canvasHeight"></canvas>
    </div>
</template>

<script>
export default {
    name: 'AudioVisualizer',
    props: {
        audioData: {
            type: Uint8Array,
            required: true
        },
        isAwake: {
            type: Boolean,
            required: true
        }
    },
    data() {
        return {
            canvasWidth: 0,
            canvasHeight: 0,
            ctx: null,
            animationId: null,
            dataHistory: [],
            maxDataPoints: 1000, // 存储的最大数据点数
            displayPoints: 64, // 显示的数据点数，与频率区间数量相匹配
            barWidth: 4,
            barGap: 1,
            maxBarHeight: 50,
            smoothedData: [],
        }
    },
    mounted() {
        this.setupCanvas();
        window.addEventListener('resize', this.setupCanvas);
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.setupCanvas);
        cancelAnimationFrame(this.animationId);
    },
    methods: {
        setupCanvas() {
            const canvas = this.$refs.visualizer;
            // 修改这一行,将宽度设置为屏幕宽度的 1/3
            this.canvasWidth = Math.floor(window.innerWidth / 3);
            this.canvasHeight = 100; // 固定高度
            canvas.width = this.canvasWidth;
            canvas.height = this.canvasHeight;
            this.ctx = canvas.getContext('2d');
            this.dataHistory = new Array(this.maxDataPoints).fill(new Array(this.displayPoints).fill(0));
            this.smoothedData = new Array(this.displayPoints).fill(0);
            this.render();
        },
        updateDataHistory() {
            if (this.audioData && this.audioData.length > 0) {
                const newData = Array.from(this.audioData.slice(0, this.displayPoints));
                this.dataHistory.push(newData);
                if (this.dataHistory.length > this.maxDataPoints) {
                    this.dataHistory.shift();
                }
            } else {
                console.warn('Invalid audioData:', this.audioData);
            }
        },
        render() {

            const ctx = this.ctx;
            const width = this.canvasWidth;
            const height = this.canvasHeight;

            // 清除画布
            ctx.clearRect(0, 0, width, height);

            if (!this.isAwake) return;
            this.updateDataHistory();

            // 计算当前显示的数据（使用最新的数据）
            const currentData = this.dataHistory[this.dataHistory.length - 1];
            if (!currentData || currentData.length === 0) {
                console.warn('No current data available');
                this.animationId = requestAnimationFrame(this.render);
                return;
            }

            const totalBarWidth = this.displayPoints * (this.barWidth + this.barGap) - this.barGap;
            const startX = (width - totalBarWidth) / 2;

            // 更新和绘制柱形图
            for (let i = 0; i < this.displayPoints; i++) {
                const dataValue = currentData[i];
                if (typeof dataValue !== 'number' || isNaN(dataValue)) {
                    console.warn(`Invalid data value at index ${i}:`, dataValue);
                    continue;
                }

                const targetHeight = (dataValue / 255) * this.maxBarHeight;
                
                // 平滑过渡
                this.smoothedData[i] += (targetHeight - this.smoothedData[i]) * 0.2;

                const barHeight = Math.max(0, Math.min(this.smoothedData[i], this.maxBarHeight));
                const x = startX + i * (this.barWidth + this.barGap);
                const y = Math.max(0, height - barHeight);

                // 设置渐变
                if (isFinite(y) && isFinite(height)) {
                    const gradient = ctx.createLinearGradient(0, y, 0, height);
                    gradient.addColorStop(0, 'rgba(0, 255, 255, 0.8)');
                    gradient.addColorStop(1, 'rgba(0, 255, 255, 0.2)');
                    ctx.fillStyle = gradient;
                } else {
                    ctx.fillStyle = 'rgba(0, 255, 255, 0.5)'; // 使用固定颜色作为后备
                }

                ctx.fillRect(x, y, this.barWidth, barHeight);
            }

            this.animationId = requestAnimationFrame(this.render);
        }
    },
    watch: {
        audioData: {
            handler(newData) {
                if (!(newData instanceof Uint8Array) || newData.length === 0) {
                    console.warn('Invalid audioData received:', newData);
                }
            },
            immediate: true
        }
    }
}
</script>

<style scoped>
.audio-visualizer-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000; /* 确保在最前面 */
    pointer-events: none; /* 允许点击穿透 */
}

canvas {
    width: 100%;
    height: 100%;
}
</style>