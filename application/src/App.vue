<template>
  <div id="app">
    <router-view/>
  </div>
</template>


<script>
  import VueCookies from 'vue-cookies'

  export default {
      components:{VueCookies},
      
      created() {
        VueCookies.set('allegro-cred', false, { expires: 0, path: '/' })
      }
      
  }
</script>