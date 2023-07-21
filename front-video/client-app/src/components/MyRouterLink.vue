<template>
  <a v-if="isExternal" :href="formatedUrl" :target="target">
    <slot></slot>
  </a>
  <router-link v-else v-bind="originProps">
    <slot></slot>
  </router-link>
</template>
<script>
export default {
  name: "MyRouterLink",
  props: {
    to: {
      type: [Object, String],
      default: () => { 
        path: '/'
      },
      required: true,
    },
    target: {
      type: String,
      default: () => '',
    },
  },
  computed: {
    originProps() {
      return { ...this.$props, ...this.$attrs };
    },
    isExternal() {
      if (typeof(this.to) === 'object') {
        return this.to.path && this.to.path[0] !== '/'
      }
      if (typeof(this.to) === 'string') {
        return this.to && this.to[0] !== '/'
      }
      
      return false
    },
    formatedUrl() {
      let url = "";
      if (typeof(this.to) === 'object') {
        url = this.to.path
      } else if (typeof(this.to) === 'string') {
        url = this.to
      }

      let queryArray = [];
      if (this.to.query) {
        for (let key in this.to.query) {
          const value = encodeURIComponent(this.to.query[key]);
          queryArray.push(`${key}=${value}`);
        }
      }

      if (queryArray.length == 0) {
        return url;
      }

      if (url.indexOf("?") != -1) {
        url = `${url}${queryArray.join("&")}`;
      } else {
        url = `${url}?${queryArray.join("&")}`;
      }

      return url;
    },
  },
};
</script>