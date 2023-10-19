<template>
    <div>
        <button type="button" @click="createConnection">连接MQTT</button>
        <button type="button" @click="doPublish">发送消息</button>
        <hr />
        <div id="messgesList">
            {{ receiveNews  }}
        </div>
    </div>
</template>
  
<script>
import * as mqtt from "mqtt/dist/mqtt.min";

export default {
    name: 'Mqtt',
    data() {
        return {
            connection: {
                protocol: "ws",
                host: "192.168.14.191",
                // ws: 8083; wss: 8084
                port: 8083,
                endpoint: "/mqtt",
                // for more options, please refer to https://github.com/mqttjs/MQTT.js#mqttclientstreambuilder-options
                clean: true,
                connectTimeout: 30 * 1000, // ms
                reconnectPeriod: 4000, // ms
                clientId: "emqx_vue_" + Math.random().toString(16).substring(2, 8),
                // auth
                username: "emqx_test",
                password: "emqx_test",
            },
            subscription: {
                topic: "testtopic/#",
                qos: 0,
            },
            publish: {
                topic: "topic/browser",
                qos: 0,
                payload: '{ "msg": "Hello, I am browser." }',
            },
            receiveNews: "",
            qosList: [0, 1, 2],
            client: {
                connected: false,
            },
            subscribeSuccess: false,
            connecting: false,
            retryTimes: 0,
        };
    },
    methods: {
        initData() {
            this.client = {
                connected: false,
            };
            this.retryTimes = 0;
            this.connecting = false;
            this.subscribeSuccess = false;
        },
        handleOnReConnect() {
            this.retryTimes += 1;
            if (this.retryTimes > 5) {
                try {
                    this.client.end();
                    this.initData();
                    this.$message.error("Connection maxReconnectTimes limit, stop retry");
                } catch (error) {
                    this.$message.error(error.toString());
                }
            }
        },
        createConnection() {
            try {
                this.connecting = true;
                const { protocol, host, port, endpoint, ...options } = this.connection;
                const connectUrl = `${protocol}://${host}:${port}${endpoint}`;
                console.log(connectUrl)
                this.client = mqtt.connect(connectUrl, options);
                if (this.client.on) {
                    this.client.on("connect", () => {
                        this.connecting = false;
                        const message = "Connection succeeded!"
                        console.log(message);
                        this.receiveNews = this.receiveNews.concat(message);
                        this.doSubscribe();
                    });
                    this.client.on("reconnect", this.handleOnReConnect);
                    this.client.on("error", (error) => {
                        console.log("Connection failed", error);
                    });
                    this.client.on("message", (topic, message) => {
                        this.receiveNews = this.receiveNews.concat("\n" + message);
                        console.log(`Received message ${message} from topic ${topic}`);
                    });
                }
            } catch (error) {
                this.connecting = false;
                console.log("mqtt.connect error", error);
            }
        },
        doSubscribe() {
            const { topic, qos } = this.subscription
            this.client.subscribe(topic, { qos }, (error, res) => {
                if (error) {
                    console.log('Subscribe to topics error', error)
                    return
                }
                this.subscribeSuccess = true
                console.log('Subscribe to topics res', res)
            })
        },
        doUnSubscribe() {
            const { topic } = this.subscription
            this.client.unsubscribe(topic, error => {
                if (error) {
                    console.log('Unsubscribe error', error)
                }
            })
        },
        doPublish() {
            const { topic, qos, payload } = this.publish
            this.client.publish(topic, payload, { qos }, error => {
                if (error) {
                    console.log('Publish error', error)
                }
            })
        },
        destroyConnection() {
            if (this.client.connected) {
                try {
                    this.client.end(false, () => {
                        this.initData()
                        console.log('Successfully disconnected!')
                    })
                } catch (error) {
                    console.log('Disconnect failed', error.toString())
                }
            }
        }
    },
    mounted() {
        this.initData();
    },
    destroyed() {
        this.doUnSubscribe();
        this.destroyConnection();
    }
}
</script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
    margin: 40px 0 0;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    display: inline-block;
    margin: 0 10px;
}

a {
    color: #42b983;
}
</style>
  