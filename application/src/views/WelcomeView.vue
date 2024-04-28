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
import axios from "axios";
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
  created() {
    const tokenExp = this.$cookies.get("refreshExp");

    if (!tokenExp){
      const expirationTime = Date.now() + 1000 * 3600 * 11 // 11 hours 
      this.$cookies.set("refreshExp", expirationTime);
    }
    setInterval(this.refreshToken, 60000);
  },
  methods: {
    async refreshToken() {
        const expirationTime = this.$cookies.get("refreshExp");
        const currentTime = Date.now();
        if (currentTime < expirationTime) {
          return;
        }
        const userKey = this.$cookies.get("allegro-cred").userKey
        const response = (await axios.post(`${baseUrl}/refresh-token`, { userKey })).data.status

        if (response == 400){
          this.alert = {
            variant: "danger",
            message: this.$t("alerts.refresh"),
          };
        }
        else{
          this.$cookies.remove("refreshExp")
        }
    },
  },
  components: {
    TheHeader,
    TheAlert,
    TheNavBar,
  },
};
</script>
