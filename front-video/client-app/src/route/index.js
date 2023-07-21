// export default router
import Vue from 'vue'
import VueRouter from 'vue-router'
import HelloWorld from '@/components/HelloWorld.vue'
import GeneralVideo from '@/components/GeneralVideo.vue'
import StreamingVideo from '@/components/StreamingVideo.vue'
import FlvVideo from '@/components/FlvVideo.vue'

Vue.use(VueRouter)

const route = new VueRouter({
    routes: [{
        path: '/',
        name: 'Home',
        component: HelloWorld,
    }, {
        path: '/home',
        name: 'Home',
        component: HelloWorld,
    },
    {
        path: '/generalVideo',
        name: 'GeneralVideo',
        component: GeneralVideo,
    },
    {
        path: '/streammingVideo',
        name: 'StreamingVideo',
        component: StreamingVideo,
    },
    {
        path: '/flvstreammingVideo',
        name: 'FlvVideo',
        component: FlvVideo,
    }]
})

export default route
