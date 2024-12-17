<template>
  <div id="app">
    <!-- <div class="background-container">
      <IronManMask class="iron-man-mask" @reactor-click="wakeUp" />
    </div> -->
    
    <!-- <SpeechRecognition
      ref="speechRecognition"
      :isRecognizing="isRecognizing"
      @recognition-start="onRecognitionStart"
      @recognition-stop="onRecognitionStop"
      @recognition-result="onRecognitionResult"
    /> -->

    <!-- <ScrollingSubtitles
      :text="recognizedText"
      @scrolling-complete="onScrollingComplete"
    />

    <button class="start-recognition-btn" @click="startRecognition">
      Start Recognition
    </button> -->
    <Jarvis/>
  </div>
</template>

<script>
import AudioVisualizer from './components/AudioVisualizer.vue';
import ScrollingSubtitles from './components/ScrollingSubtitles.vue';
import IronManMask from './components/IronManMask.vue';
import SpeechRecognition from './components/SpeechRecognition.vue'
import Jarvis from './components/Jarvis/index.vue'

export default {
  name: 'App',
  components: {
    AudioVisualizer,
    ScrollingSubtitles,
    IronManMask,
    SpeechRecognition,
    Jarvis
  },
  data() {
    return {
      audioData: new Uint8Array(0),
      recognizedText: '',
      isRecognizing: false,
      isAwake: false
    }
  },
  methods: {
    wakeUp() {
      console.log('Waking up...');
      this.isAwake = true;
    },
    startRecognition() {
      console.log('Starting recognition...');
      this.isRecognizing = true;
      this.$refs.speechRecognition.startRecognition();
    },
    onRecognitionStart() {
      console.log('Recognition started');
    },
    onRecognitionStop() {
      console.log('Recognition stopped');
      this.isRecognizing = false;
    },
    onRecognitionResult(result) {
      console.log('Recognition result:', result);
      this.recognizedText = result;
    },
    onScrollingComplete() {
      console.log('Scrolling complete');
      this.recognizedText = '';
      this.isRecognizing = false;
      this.$refs.speechRecognition.stopRecognition();
    }
  },
  mounted() {
    console.log('App mounted');
  },
  watch: {
    isAwake(newValue) {
      console.log('isAwake changed:', newValue);
    }
  }
}
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
}

.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.iron-man-mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 3;
}

.start-recognition-btn {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  z-index: 1000;
}

.start-recognition-btn:hover {
  background-color: #45a049;
}
</style>