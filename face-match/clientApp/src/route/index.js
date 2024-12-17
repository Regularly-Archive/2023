// export default router
import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

const route = new VueRouter({
    routes: [
        {
            path: '/',
            component: () => import('@/layout/MainLayout.vue'),
            children: [
                {
                    path: '',
                    redirect: '/search'
                },
                {
                    path: '/search',
                    name: 'Search',
                    component: () => import('@/views/faceMatch/SearchImage.vue'),
                },
                {
                    path: '/upload',
                    name: 'Upload',
                    component: () => import('@/views/faceMatch/UploadImage.vue'),
                }
            ]
        }
    ]
})

export default route
