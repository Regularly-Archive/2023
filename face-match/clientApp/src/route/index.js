// export default router
import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

const route = new VueRouter({
    routes: [{
        path: '/home',
        name: 'Home',
        component: () => import('@/views/faceMatch/SearchImage.vue'),
    }]
})

export default route
