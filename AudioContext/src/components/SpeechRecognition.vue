<template>
    <div class="speech-recognition">
      <canvas ref="canvas"></canvas>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SpeechRecognition',
    props: {
      isRecognizing: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        recognition: null,
        audioContext: null,
        analyser: null,
        source: null,
        isAnimating: false,
        animationId: null,
        canvas: null,
        ctx: null,
        ripples: [],
        minRadius: 75,
        maxRadius: 200,
        animationSpeed: 0.15,
        marginBottom: 253
      };
    },
    watch: {
      isRecognizing(newValue) {
        if (newValue) {
          this.startRecognition();
        } else {
          this.stopRecognition();
        }
      }
    },
    mounted() {
      this.initializeCanvas();
      this.setupSpeechRecognition();
    },
    methods: {
      initializeCanvas() {
        this.canvas = this.$refs.canvas;
        if (!this.canvas) {
          console.error('Canvas element not found');
          return;
        }
        this.ctx = this.canvas.getContext('2d');
        this.resizeCanvas();
        window.addEventListener('resize', this.resizeCanvas);
      },
      resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
      },
      setupSpeechRecognition() {
        if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
          this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
          this.recognition.lang = 'zh-CN';
          this.recognition.continuous = true;
          this.recognition.interimResults = true;
  
          this.recognition.onresult = (event) => {
            const result = event.results[event.results.length - 1];
            const transcript = result[0].transcript;
            this.$emit('recognition-result', transcript);
          };
  
          this.recognition.onend = () => {
            if (this.isRecognizing) {
              this.recognition.start();
            }
          };
        } else {
          console.error('浏览器不支持语音识别');
        }
      },
      async startRecognition() {
        console.log('Starting recognition...');
        if (this.isAnimating) return;
  
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
          this.analyser = this.audioContext.createAnalyser();
          this.source = this.audioContext.createMediaStreamSource(stream);
          this.source.connect(this.analyser);
          this.analyser.fftSize = 256;
  
          if (!this.isRecognizing) {
            this.recognition.start();
          }
          
          this.isAnimating = true;
          this.createRipples();
          this.drawRipples();
          this.updateAnimationSpeed();
  
          this.$emit('recognition-start');
        } catch (error) {
          console.error('Error accessing microphone:', error);
        }
      },
      stopRecognition() {
        console.log('Stopping recognition...');
        if (!this.isAnimating) return;
  
        this.recognition.stop();
        this.stopRecording();
        this.isAnimating = false;
  
        this.$emit('recognition-stop');
      },
      stopRecording() {
        if (this.source) {
          this.source.disconnect();
        }
        if (this.audioContext) {
          this.audioContext.close();
        }
      },
      createRipples() {
        this.ripples = [];
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2 + this.marginBottom * (this.canvas.height / 1080) ;
        for (let i = 0; i < 3; i++) {
          this.ripples.push(new Ripple(centerX, centerY, this.minRadius, this.maxRadius));
          this.ripples[i].radius = this.minRadius + i * (this.maxRadius - this.minRadius) / 3;
        }
      },
      drawRipples() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ripples.forEach((ripple, index) => {
          ripple.draw(this.ctx);
          ripple.update(this.animationSpeed);
        });
        if (this.isAnimating) {
          this.animationId = requestAnimationFrame(this.drawRipples);
        } else {
          this.animationSpeed *= 0.95;
          if (this.animationSpeed > 0.01) {
            this.animationId = requestAnimationFrame(this.drawRipples);
          } else {
            cancelAnimationFrame(this.animationId);
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
          }
        }
      },
      updateAnimationSpeed() {
        if (!this.analyser) return;
  
        const dataArray = new Uint8Array(this.analyser.frequencyBinCount);
        this.analyser.getByteFrequencyData(dataArray);
        const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
        this.animationSpeed = 0.5 + average / 25;
  
        if (this.isAnimating) {
          requestAnimationFrame(this.updateAnimationSpeed);
        }
      },
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.resizeCanvas);
      cancelAnimationFrame(this.animationId);
      this.stopRecording();
    },
  };
  
  class Ripple {
    constructor(x, y, minRadius, maxRadius) {
      this.x = x;
      this.y = y;
      this.radius = minRadius;
      this.minRadius = minRadius;
      this.maxRadius = maxRadius;
      this.opacity = 1;
    }
  
    draw(ctx) {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(66, 176, 203, ${this.opacity})`;
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  
    update(speed) {
      this.radius += speed;
      this.opacity = 1 - (this.radius - this.minRadius) / (this.maxRadius - this.minRadius);
      if (this.radius >= this.maxRadius) {
        this.radius = this.minRadius;
        this.opacity = 1;
      }
    }
  }
  </script>
  
  <style>
  .speech-recognition {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1000;
  }

  canvas {
    width: 100%;
    height: 100%;
  }
  </style>