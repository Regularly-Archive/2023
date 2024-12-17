<template>
  <div id="app">
    <div class="background-container">
      <IronManMask class="iron-man-mask" @reactor-click="wakeUp" />
    </div>
    
    
    <SpeechRecognition
      :isRecognizing="isAwake"
      @recognition-start="onRecognitionStart"
      @recognition-stop="onRecognitionStop"
      @recognition-result="onRecognitionResult"
    />
    <!-- 添加调试信息 -->
    <div class="debug-info">
      <p>isAwake: {{ isAwake }}</p>
      <p>isListening: {{ isListening }}</p>
      <p>audioData length: {{ audioData.length }}</p>
    </div>
  </div>
</template>

<script>
import AudioVisualizer from './components/AudioVisualizer.vue';
import ScrollingText from './components/ScrollingText.vue';
import IronManMask from './components/IronManMask.vue';
import SpeechRecognition from './components/SpeechRecognition.vue'
import { startSpeechRecognition, stopSpeechRecognition } from './utils/speechRecognition';
import { getAIResponse } from './utils/aiService';
import { speakText } from './utils/textToSpeech';

export default {
  name: 'App',
  components: {
    AudioVisualizer,
    ScrollingText,
    IronManMask,
    SpeechRecognition
  },
  data() {
    return {
      audioData: new Uint8Array(0),
      recognizedText: '',
      isListening: false,
      isAwake: false
    }
  },
  methods: {
    wakeUp() {
      console.log('Waking up...');
      this.isAwake = true;
      this.startListening();
    },
    async startListening() {
      console.log('Starting to listen...');
      if (!this.isListening) {
        this.isListening = true;
        await startSpeechRecognition(
          (result) => {
            console.log('Speech recognized:', result);
            this.recognizedText += result;
            this.getAIResponseAndSpeak(result);
          },
          (audioData) => {
            console.log('Received audio data, length:', audioData.length);
            this.audioData = audioData;
          }
        );
      }
    },
    stopListening() {
      if (this.isListening) {
        this.isListening = false;
        stopSpeechRecognition();
      }
      this.isAwake = false;
    },
    async getAIResponseAndSpeak(text) {
      const aiResponse = await getAIResponse(text);
        this.recognizedText = aiResponse;
        await speakText(aiResponse, (audioData) => {
          this.audioData = audioData;
        });
        // 在 AI 回答完毕后，继续监听
        this.startListening()
      try {
        
      } catch (error) {
        
      }
    },
    onRecognitionStart() {

    },
    onRecognitionStop() {

    },
    onRecognitionResult(e) {
      console.log(e)
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

.audio-visualizer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  z-index: 10;
}

.debug-info {
  position: fixed;
  bottom: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px;
  border-radius: 5px;
  font-size: 12px;
}
</style>