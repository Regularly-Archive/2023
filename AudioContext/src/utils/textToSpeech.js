let synth = window.speechSynthesis;
let audioContext = null;
let analyser = null;

export function speakText(text, onAudioData) {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
  }

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'zh-CN';

  utterance.onstart = () => {
    navigator.mediaDevices
      .getUserMedia({ audio: true, video: true })
      .then(stream => {
        const source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);
      })

    const dataArray = new Uint8Array(analyser.frequencyBinCount);

    function updateAudioData() {
      analyser.getByteFrequencyData(dataArray);
      onAudioData(dataArray);
      if (synth.speaking) {
        requestAnimationFrame(updateAudioData);
      }
    }

    updateAudioData();
  };

  synth.speak(utterance);
}