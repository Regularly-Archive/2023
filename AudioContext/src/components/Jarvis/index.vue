<template>
    <section class="main">
        <div class="image-container">
            <div class="image" style="position: relative;">
                <button class="talk" @click="startRecognition">
                    <h1>
                        <i class="fas fa-microphone-alt" ref="microphone" style="animation-play-state: paused;"></i>
                    </h1>
                </button>
                <svg width="210" height="210" id="jarvis-like">
                    <defs>
                        <filter id="light-circle">
                            <feGaussianBlur result="blurred" in="SourceGraphic" stdDeviation="1" />
                        </filter>
                        <!-- <filter id="light-triangle">
						<feGaussianBlur stdDeviation="2" in="SourceGraphic" result="blur2" />
						<feComposite in="SourceAlpha" in2="offOut" operator="arithmetic" k1="1" k2="1" k3="1" k4="0" />
					</filter> -->
                    </defs>
                    <!-- circle outer -->
                    <circle cx="105" cy="105" r="100"
                        style="fill: transparent;stroke: #B4F6FB;stroke-width: 2; stroke-dasharray: 50, 5"></circle>
                    <circle cx="105" cy="105" r="95" style="fill: transparent;stroke: #64E6EF;stroke-width: 1.5;">
                    </circle>
                    <!-- circle dash cool :D -->
                    <circle cx="105" cy="105" r="80"
                        style="fill: transparent; stroke: #B4F6FB; stroke-width: 10; stroke-dasharray: 2,2.29">
                        <animateTransform attributeName="transform" attributType="XML" type="rotate" from="0 105 105"
                            to="360 105 105" dur="10s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="105" cy="105" r="61" transform="rotate(0 105 105)"
                        style="fill: transparent; stroke: #B4F6FB; stroke-width: 2; stroke-dasharray: 50, 25">
                        <animateTransform attributeName="transform" attributType="XML" type="rotate" from="0 105 105"
                            to="-360 105 105" dur="10s" repeatCount="indefinite" />
                    </circle>
                    <!-- circle inner -->
                    <circle cx="105" cy="105" r="50"
                        style="fill: transparent; stroke: #64E6EF; stroke-width: 15;filter: url(#light-circle);">
                    </circle>
                    <circle cx="105" cy="105" r="40" style="fill: transparent; stroke: #64E6EF; stroke-width: 2">
                    </circle>
                    <!-- triangle primary -->
                </svg>
            </div>
            <h1>J A R V I S</h1>
            <Subtitles ref="subtitles" />
        </div>
        <div class="input">
            <h1 class="content">Click on the mic to speak</h1>
        </div>

        <NetworkState refresh-interval="5000" />
        <BatteryState />
        <DateTime />
    </section>
</template>
<script>
import BatteryState from './components/BatteryState.vue'
import NetworkState from './components/NetworkState.vue'
import Subtitles from './components/Subtitles.vue'
import DateTime from './components/DateTime.vue'
export default {
    components: {
        BatteryState,
        NetworkState,
        Subtitles,
        DateTime
    },
    data() {
        return {
            welcome: "I'm JARVIS, a Virtual Assistant. How may I help you?",
            subtitles: '',
            recognition: null,
            isRecognizing: false
        }
    },
    mounted() {
        this.subtitles = this.welcome
        this.$refs.subtitles.go(this.welcome)
        this.setupSpeechRecognition()
    },
    methods: {
        setupSpeechRecognition() {
            if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
                this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                this.recognition.lang = 'zh-CN';
                this.recognition.continuous = true;
                this.recognition.interimResults = true;
                this.recognition.onresult = (event) => {
                    const result = event.results[event.results.length - 1];
                    const transcript = result[0].transcript;
                    //this.subtitles = transcript
                    this.$refs.subtitles.go(transcript)
                };

                this.recognition.onend = () => {
                    this.isRecognizing = true
                };
            } else {
                console.error('浏览器不支持语音识别');
            }
        },
        startRecognition() {
            if (this.isRecognizing) return;

            this.recognition.start()
            this.isRecognizing = true
            this.$refs.microphone.style['animationPlayState'] = 'running'
        }
    },
}
</script>
<style>
@import url("https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@100;200;300;400;500;600;700&display=swap");

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Roboto Mono", monospace;
}

.main {
    min-height: 100vh;
    position: relative;
    width: 100%;
    background: #000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.main .image-container {
    padding: 10px;
}

.main .image-container .image {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.main .image-container .image img {
    width: 170px;
    align-items: center;
}

.main .image-container h1 {
    color: #00bcd4;
    text-align: center;
    margin-bottom: 10px;
    font-size: 40px;
}

#battery-status {
    color: #324042;
}

.main .image-container p {
    color: #324042;
    text-align: center;
}

.main .input {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100vw;
    height: 50px;
    border-radius: 20px;
}

.talk {
    color: #ffffff00;
    background-color: #ffffff00;
    border: none;
}

.talk h1 {
    position: absolute;
    top: 75px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 2;
    filter: drop-shadow(1px 4px 20px #000000);
}

.talk h1 i {
    animation: blink 1.5s infinite;
}

@keyframes blink {
    to {
        color: transparent;
    }
}

.talk i:hover {
    cursor: pointer;
    color: #fff;
}

.main .input .talk {
    background: transparent;
    outline: none;
    border: none;
    width: 250px;
    height: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 15px;
    cursor: pointer;
}

.main .input .talk i {
    font-size: 20px;
    color: #aed0d0;
}

.main .input .content {
    color: #aed0d0;
    font-size: 15px;
}
</style>