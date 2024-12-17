<template>
    <p id="subtitles"></p>
</template>
<script>
import TypeIt from 'typeit'
export default {
    name: 'Subtitles',
    props: {
        speed: {
            type: Number,
            default: 0
        }
    },
    data() {
        return {
        }
    },
    mounted() {
        
    },
    methods: {
        go(text) {
            new TypeIt("#subtitles", {
                strings: text,
                speed: this.speed
            }).go();
        }
    }
}
</script>
<style scoped>
p {
    font-size: 1rem !important;
    color: #fff !important;
}

p {
    --ti-cursor-color: white;
    --ti-cursor-font-weight: 500;
    --ti-cursor-transform: translateX(.125em);
    --ti-cursor-font-style: bold;
}
</style>