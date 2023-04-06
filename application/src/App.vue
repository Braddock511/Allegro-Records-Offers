<template>
  <div id="app">
    <router-view/>
  </div>
</template>


<script>

  export default {
      created() {
        if (!this.$cookies.get('allegro-cred')) {
          this.$cookies.set('allegro-cred', false, '0', '/', '', false, 'Lax');
        }
        this.$i18n.locale = "en"
      }
  }
</script>