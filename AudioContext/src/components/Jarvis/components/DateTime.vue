<template>
    <p>{{ current }}</p>
</template>
<script>
export default {
    name: 'DateTime',
    data() {
        return {
            current: '',
            timerId: ''
        }
    },
    mounted() {
        this.updateDateTime()
        this.timerId = setInterval(this.updateDateTime, 1000)
    },
    beforeDestroy() {
        clearInterval(this.timerId)
        this.timerId = ''
    },
    methods: {
        updateDateTime() {
            const now = new Date();
            let hours = now.getHours();
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const amPm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12 || 12;
            const day = now.getDate();
            const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            const month = monthNames[now.getMonth()];
            const year = now.getFullYear();
            const weekdayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            const weekday = weekdayNames[now.getDay()];

            const formated = `${hours}:${minutes} ${amPm} ${day} ${month} ${year}, ${weekday}`;
            this.current = formated
        }
    }
}
</script>
<style scope>
p {
    color: #324042;
    text-align: center;
    margin-top: 10px;
}
</style>