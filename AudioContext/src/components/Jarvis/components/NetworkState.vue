<template>
    <p class="online" v-if="online">◉ Online, {{ networkType }}</p>
    <p class="offline" v-else>◉ Offline, {{ networkType }}</p>
</template>
<script>
export default {
    name: 'NetworkState',
    props: {
        refreshInterval: {
            type: Number,
            default: 5000
        }
    },
    data() {
        return {
            online: navigator.onLine,
            networkType: navigator.connection.effectiveType.toUpperCase(),
            timerId: ''
        }
    },
    mounted() {
        this.updateState()
    },
    beforeDestroy() {
        clearInterval(this.timerId)
        this.timerId = ''
    },
    methods: {
        updateState() {
            this.timerId = setInterval(() => {
                this.online = navigator.onLine,
                this.networkType = navigator.connection.effectiveType.toUpperCase()
            }, this.refreshInterval)
        }
    }
}
</script>
<style scoped>
 .online {
    color: #00f6f8; 
    margin-top: 10px;
 }

 .offline {
    color: red;
    margin-top: 10px;
 }
</style>