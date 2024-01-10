<template>
  <TheHeader />
  <section v-if="formDisplay" class="w-full flex justify-center items-center">
    <form @submit.prevent="allegroToken" class="w-[40rem] h-[28rem] bg-lighter-black p-4 py-5 mt-12 rounded-xl flex flex-col gap-10">
      <div class="text-2xl text-white font-semibold">{{ $t("formContainer.credentials") }}</div>
      <div class="px-4 h-full flex flex-col gap-5">
        <div class="relative">
          <label for="user-key" class="absolute flex justify-center items-center text-gray-300 left-2 h-[1.5px] bg-lighter-black px-1 text-sm font-semibold" >{{ $t("formContainer.userKey") }}</label>
          <input v-model="userKey" id="user-key" type="text" required class="bg-lighter-black font-semibold h-10 w-full p-1 rounded-md placeholder:text-center px-1 outline-none border-css" />
        </div>
        <div class="relative">
          <label for="discogs-token" class="absolute flex justify-center items-center text-gray-300 left-2 h-[1.5px] bg-lighter-black px-1 text-sm font-semibold">Discogs token</label>
          <input v-model="discogsToken" id="discogs-token" type="text" required class="bg-lighter-black font-semibold h-10 w-full p-1 rounded-md placeholder:text-center px-1 outline-none border-css"/>
        </div>
        <div class="relative">
          <label for="client-id" class="absolute flex justify-center items-center text-gray-300 left-2 h-[1.5px] bg-lighter-black px-1 text-sm font-semibold" >{{ $t("formContainer.clientId") }}</label>
          <input v-model="allegroId" id="client-id" type="text" required class="bg-lighter-black font-semibold h-10 w-full p-1 rounded-md placeholder:text-center px-1 outline-none border-css" />
        </div>
        <div class="relative">
          <label for="client-secret" class="absolute flex justify-center items-center text-gray-300 left-2 h-[1.5px] bg-lighter-black px-1 text-sm font-semibold" >{{ $t("formContainer.clientSecret") }}</label>
          <input v-model="allegroSecret" id="client-secret" type="text" required class="bg-lighter-black font-semibold h-10 w-full p-1 rounded-md placeholder:text-center px-1 outline-none border-css"/>
        </div>
      </div>
      <button class="btn btn-primary w-full" type="submit" style="padding: 0.5rem; margin-top: 30px; font-size: 20px">{{ $t("formContainer.button") }}</button>
    </form>
  </section>
  <div class="flex justify-center items-center mt-20" v-if="!formDisplay && !loading">
    <a :href="response.verification_uri_complete" target="_blank">
      <button class="btn btn-primary w-full" type="button" style="padding: 0.5rem; font-size: 20px" >{{ $t("formContainer.confirm") }}</button>
    </a>
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
import axios from "axios";
export default {
  data() {
    return {
      userKey: "",
      discogsToken: "",
      allegroId: "",
      allegroSecret: "",
      login: "",
      response: "",
      formDisplay: true,
      loading: false,
      alert: {},
    };
  },
  created() {
    this.loadSavedData();
  },
  methods: {
    loadSavedData() {
      const savedCred = this.$cookies.get("allegro-cred");
      if (savedCred.flag) {
        this.userKey = savedCred.userKey || "";
        this.discogsToken = savedCred.discogsToken || "";
        this.allegroId = savedCred.allegroId || "";
        this.allegroSecret = savedCred.allegroSecret || "";
        this.login = savedCred.login || "";
      }
    },
    async allegroToken() {
      this.response = (
        await axios.post(`${baseUrl}/allegro-auth`, {
          client_id: this.allegroId,
          client_secret: this.allegroSecret,
        })
      ).data.output;
      this.formDisplay = false;
      const tokenResponse = (
        await axios.post(`${baseUrl}/allegro-token`, {
          userKey: this.userKey,
          discogs_token: this.discogsToken,
          client_id: this.allegroId,
          client_secret: this.allegroSecret,
          device_code: this.response["device_code"],
        })).data;
      if (tokenResponse.error || tokenResponse.status == 401) {
        this.formDisplay = true;
        this.alert = {
          variant: "danger",
          message: this.$t("alerts.tokenFailed"),
        };
      } else {
        const user = (await axios.post(`${baseUrl}/allegro-user`, {userKey: this.userKey})).data.output
        const credData = {
          flag: true,
          userKey: this.userKey,
          discogsToken: this.discogsToken,
          allegroId: this.allegroId,
          allegroSecret: this.allegroSecret,
          login: user.login, 
        };
        this.$cookies.set("allegro-cred", credData, "12h", "/", "", false, "Lax");
        this.loading = true;
        const response_offers = (
          await axios.post(`${baseUrl}/store-all-offers`, { userKey: this.userKey })
        ).data;
        const response_payments = (
          await axios.post(`${baseUrl}/store-all-payments`, {
            userKey: this.userKey,
          })
        ).data;
        if (response_offers.error) {
          this.alert = {
            variant: "danger",
            message: this.$t("alerts.offersFailed"),
          };
          this.formDisplay = true;
        } else if (response_payments.error) {
          this.alert = {
            variant: "danger",
            message: this.$t("alerts.paymentsFailed"),
          };
          this.formDisplay = true;
        } else {
          this.$router.push("/");
        }
        this.loading = false;
      }
    },
  },
  components: {
    TheAlert,
    TheHeader,
  },
};
</script>
