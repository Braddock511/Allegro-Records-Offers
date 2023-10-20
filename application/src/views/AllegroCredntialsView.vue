<template>
  <TheHeader/>
  <section class="form-container" v-if="formDisplay">
    <form @submit.prevent="allegroToken">
      <div class="title">{{ $t('formContainer.credentials') }}</div>
      <div class="input-container">
        <input v-model="userKey" id="user-key" class="input" type="text" :placeholder="$t('formContainer.userKey')" required style="width: 50%;"/>
      </div>    
      <div class="input-container">
        <input v-model="discogsToken" id="discogs-token" class="input" type="text" placeholder="Discogs token" required style="width: 50%;"/>&nbsp;
      </div>         
      <div class="input-container">
        <input v-model="allegroId" id="client-id" class="input" type="text" :placeholder="$t('formContainer.clientId')" required style="width: 50%;"/>
      </div>
      <div class="input-container">
        <input v-model="allegroSecret" id="client-secret" class="input" type="text" :placeholder="$t('formContainer.clientSecret')" required style="width: 50%;"/>
      </div>
      <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem; margin-top: 30px; font-size: 20px;">{{ $t('formContainer.button') }}</button>
    </form>
  </section>
  <div id="confirm" v-if="!formDisplay && !loading">
    <a :href="response.verification_uri_complete" target="_blank"><button class="btn btn-primary w-100" type="button" style="padding: 0.5rem; font-size: 20px;">{{ $t('formContainer.confirm') }}</button></a>
  </div>
  <div id="loading" v-if="loading">
    <img src="@/assets/spinner.gif" alt="loading">
    <h3>{{ $t('loading.loadData') }}</h3>
  </div>
  <TheAlert :alert="alert" />
</template>

<script>
    import TheHeader from '@/components/Global/TheHeader.vue'
    import TheAlert from "@/components/Global/TheAlert.vue"
    import axios from 'axios'
    export default {
        data(){
            return{
                userKey: "",
                discogsToken: "",
                allegroId: "",
                allegroSecret: "",
                response: "",
                formDisplay: true,
                loading: false,
                alert: {}
            }
        },
        created() {
            this.loadSavedData();
        },
        methods:{
            loadSavedData() {
                const savedCred = this.$cookies.get('allegro-cred');
                if (savedCred.flag) {
                    this.userKey = savedCred.userKey || "";
                    this.discogsToken = savedCred.discogsToken || "";
                    this.allegroId = savedCred.allegroId || "";
                    this.allegroSecret = savedCred.allegroSecret || "";
                }
            },
            async allegroToken() {
                this.response = (await axios.post("http://127.0.0.1:8000/allegro-auth", {client_id: this.allegroId, client_secret: this.allegroSecret})).data.output
                this.formDisplay = false
                const tokenResponse = (await axios.post("http://127.0.0.1:8000/allegro-token", {user_key: this.userKey, discogs_token: this.discogsToken, client_id: this.allegroId, client_secret: this.allegroSecret, device_code: this.response["device_code"],})).data
                if (tokenResponse.error || tokenResponse.status == 401){
                    this.formDisplay = true
                    this.alert = {variant: "danger", message: this.$t("alerts.tokenFailed")}
                }
                else{
                    const credData = {
                        flag: true,
                        userKey: this.userKey,
                        discogsToken: this.discogsToken,
                        allegroId: this.allegroId,
                        allegroSecret: this.allegroSecret
                    };
                    this.$cookies.set('allegro-cred', credData, '12h', '/', '', false, 'Lax');
                    this.loading = true
                    const response_offers = (await axios.post('http://127.0.0.1:8000/store-all-offers', {userKey: this.userKey})).data
                    const response_payments = (await axios.post('http://127.0.0.1:8000/store-all-payments', {userKey: this.userKey})).data
                    if (response_offers.error){
                        this.alert = {variant: "danger", message: this.$t("alerts.offersFailed")}
                        this.formDisplay = true
                    }
                    else if (response_payments.error){
                        this.alert = {variant: "danger", message: this.$t("alerts.paymentsFailed")}
                        this.formDisplay = true
                    }
                    else{
                        this.$router.push("/")
                    }
                    this.loading = false
                }
            },
        },
        components:{
            TheAlert,
            TheHeader
        }
    }
</script>

<style lang="scss" scoped>
    #confirm{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 200px;
        a{
            width: 30%;
        }
    }
</style>