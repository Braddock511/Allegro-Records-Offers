<template>
    <TheHeader/>
    <section class="form-container" v-if="formDisplay">
        <form @submit.prevent="allegroToken">
            <div class="title">{{ $t('formContainer.credentials') }}</div>
            <div class="input-container">
                <input v-model="user_id" id="client_id" class="input" type="text" :placeholder="$t('formContainer.clientId')" required style="width: 50%;"/>
            </div>
            <div class="input-container">
                <input v-model="user_secret" id="client_secret" class="input" type="text" :placeholder="$t('formContainer.clientSecret')" required style="width: 50%;"/>
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
                user_id: "",
                user_secret: "",
                response: "",
                formDisplay: true,
                loading: false,
                alert: {}
            }
        },
        methods:{
            async allegroToken() {
                this.response = (await axios.post("http://127.0.0.1:8000/allegro-auth", {client_id: this.user_id, client_secret: this.user_secret})).data.output
                this.formDisplay = false
                const tokenResponse = (await axios.post("http://127.0.0.1:8000/allegro-token", {client_id: this.user_id, client_secret: this.user_secret, device_code: this.response["device_code"],})).data
                if (tokenResponse.error){
                    this.formDisplay = true
                    this.alert = {variant: "danger", message: this.$t("alerts.tokenFailed")}
                }
                else{
                    this.$cookies.set('allegro-cred', true, '12h', '/', '', false, 'Lax')
                    this.loading = true
                    const response_offers = (await axios.get('http://127.0.0.1:8000/store-all-offers')).data
                    const response_payments = (await axios.get('http://127.0.0.1:8000/store-all-payments')).data
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