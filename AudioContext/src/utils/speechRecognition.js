let recognition = null;
let audioContext = null;
let analyser = null;
let isRecognizing = false; // 添加状态标志

export async function startSpeechRecognition(onResult, onAudioData) {
  if (isRecognizing) return; // 如果已经在识别中，直接返回
  isRecognizing = true; // 设置状态为正在识别

  if (!recognition) {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'zh-CN';
    recognition.continuous = true;
    recognition.interimResults = true;
  }

  recognition.onresult = (event) => {
    const result = event.results[event.results.length - 1][0].transcript;
    onResult(result);
  };

  recognition.onaudiostart = (event) => {
    console.log("onaudiostart", event)
  }

  recognition.onaudioend = (event) => {
    console.log("onaudioend", event)
  }
  
  recognition.onsoundstart = (event) => {
    console.log("onsoundstart", event)
  }

  recognition.onsoundend = (event) => {
    console.log("onsoundend", event)
  }  

  recognition.onspeechstart = (event) => {
    console.log("onspeechstart", event)
  }

  recognition.onspeechend = (event) => {
    console.log("onspeechend", event)
  } 

  try {
    recognition.start();
  } catch (error) {
    console.error("Speech recognition start error:", error); // 添加错误日志
  }

  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const source = audioContext.createMediaStreamSource(stream);
    source.connect(analyser);

    const dataArray = new Uint8Array(analyser.frequencyBinCount);

    function updateAudioData() {
      analyser.getByteFrequencyData(dataArray);
      onAudioData(dataArray);
      requestAnimationFrame(updateAudioData);
    }

    updateAudioData();
  } catch (error) {
    console.error("Error accessing audio stream:", error); // 处理用户拒绝权限的情况
  }
}

export function stopSpeechRecognition() {
  if (recognition) {
    recognition.stop();
    recognition = null; // 清理识别器
  }
  if (audioContext) {
    audioContext.close(); // 关闭音频上下文
    audioContext = null; // 清理音频上下文
    analyser = null; // 清理分析器
  }
  isRecognizing = false; // 重置状态
}