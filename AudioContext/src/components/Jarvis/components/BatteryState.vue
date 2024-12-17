<template>
    <p class="battery-status">
        <i :class="['fas', iconClass]"></i> Battery: {{percentage}}, {{charging ? 'Charging' : 'Not Charging'}}
    </p>
</template>
<script>
export default {
    name: 'BatteryState',
    props: {
        refreshInterval: {
            type: Number,
            default: 5000
        }
    },
    data() {
        return {
            charging: false,
            percentage: '0%',
            timerId: '',
            batteryInfo: null
        }
    },
    computed:{
        iconClass() {
            return this.charging ? "fa-bolt" : "fa-battery-empty";
        }
    },
    async mounted() {
        await this.updateBatteryInfo()
        this.timerId = setInterval(this.updateBatteryInfo, this.refreshInterval)
    },
    beforeDestroy() {
        clearInterval(this.timerId)
        this.timerId = ''
    },
    methods: {
        async updateBatteryInfo() {
            const batteryInfo = await navigator.getBattery();
            batteryInfo.addEventListener('chargingchange', this.updateBatteryInfo)
        batteryInfo.addEventListener('levelchange', this.updateBatteryInfo);
            this.charging = batteryInfo.charging
            this.percentage = Math.round(batteryInfo.level * 100) + "%"
        }
    }
}
</script>
<style scoped>
.battery-status {
    margin-top: 10px;
    color: #00f6f8;
}
</style>