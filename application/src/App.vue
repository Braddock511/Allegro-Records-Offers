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
        if (!VueCookies.get('allegro-cred')) {
          VueCookies.set('allegro-cred', false, "12h")
        }
      }
      
  }
</script>