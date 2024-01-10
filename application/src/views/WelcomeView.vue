<template>
  <TheNavBar v-if="isCookieSet" />
  <div v-if="!loading && !isCookieSet">
    <TheHeader/>
    <main>
      <div id="info" class="mt-10 flex flex-col gap-10 text-center px-10 mx-auto w-1/2">
        <div class="text-3xl text-white">{{ $t("info.title") }}</div>
        <p class="text-lg text-slate-400e">{{ $t("info.description") }}</p>
        <router-link to="/allegro-credentials">
          <button class="btn btn-primary w-75" type="button" style="padding: 0.5rem; font-size: 20px" >{{ $t("buttons.enterAllegroCredentials") }}</button>
        </router-link>
      </div>
    </main>
  </div>
  <div id="loading" v-if="loading">
    <img src="@/assets/spinner.gif" alt="loading" />
    <h3>{{ $t("loading.loadData") }}</h3>
  </div>
  <TheAlert :alert="alert" />
</template>

<script>
import TheHeader from "@/components/Global/TheHeader.vue";
import TheAlert from "@/components/Global/TheAlert.vue";
import TheNavBar from "@/components/Global/TheNavBar.vue";
export default {
  data() {
    return {
      loading: false,
      alert: {},
    };
  },
  computed: {
    isCookieSet() {
      return this.$cookies.get("allegro-cred").flag === true;
    },
  },
  components: {
    TheHeader,
    TheAlert,
    TheNavBar,
  },
};
</script>
