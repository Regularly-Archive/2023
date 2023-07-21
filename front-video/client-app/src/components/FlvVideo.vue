<template>
    <div class="hello">
        <video ref="videoPlayer" class="video-js vjs-big-play-centered vjs-fluid" controls preload="auto" width="100%"
            height="100%">
        </video>
    </div>
</template>
  
<script>

import videojs from 'video.js'
import 'video.js/dist/video-js.css'
import "videojs-flvjs-es6";

export default {
    data() {
        return {
            videoPlayer: undefined,
            options: {
                autoplay: true,
                controls: true,
                sources: [
                    {
                        src:
                            "https://sample-videos.com/video123/flv/720/big_buck_bunny_720p_2mb.flv",
                        type: "video/x-flv"
                    }
                ]
            }
        }
    },
    created() {
        this.videoPlayer = videojs(this.$refs.videoPlayer, this.options, function () {
            console.log(this.videoPlayer)
        })

    },
    beforeDestroy() {
        if (this.videoPlayer) {
            this.videoPlayer.dispose()
        }
    }
};
</script>
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
  

