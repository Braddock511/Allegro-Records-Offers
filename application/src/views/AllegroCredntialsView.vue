<template>
    <TheHeader/>
    <section class="form-container" v-if="formDisplay">
        <form @submit.prevent="allegroToken">
            <div class="title">Credentials</div>
            <div class="input-container">
                <input v-model="user_id" id="client_id" class="input" type="text" placeholder="Client id" required style="width: 50%;"/>
            </div>
            <div class="input-container">
                <input v-model="user_secret" id="client_secret" class="input" type="text" placeholder="Client secret" required style="width: 50%;"/>
            </div>
            <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem; margin-top: 30px;">Send credentials</button>
        </form>
    </section>
    <div id="confirm" v-if="!formDisplay">
        <a :href="response.data.verification_uri_complete" target="_blank"><button class="btn btn-primary w-100" type="button" style="padding: 0.5rem;">Confirm</button></a>
    </div>

    <TheAlert :alert="alert" />
</template>

<script>
    import TheHeader from '@/components/TheHeader.vue'
    import VueCookies from 'vue-cookies'
    import TheAlert from "@/components/TheAlert.vue"
    import axios from 'axios'
    export default {
        data(){
            return{
                user_id: "",
                user_secret: "",
                response: "",
                tokenResponse: "",
                formDisplay: true,
                alert: {}
            }
        },
        methods:{
            async allegroToken() {
                try {
                    this.response = await axios.post("http://127.0.0.1:8000/allegro-auth", {client_id: this.user_id, client_secret: this.user_secret});
                    this.formDisplay = false;
                    this.tokenResponse = await axios.post("http://127.0.0.1:8000/allegro-token", {client_id: this.user_id, client_secret: this.user_secret, device_code: this.response.data["device_code"],});
                    console.log(this.tokenResponse.data.error)
                    if (this.tokenResponse.data.error){
                        this.formDisplay = true
                        this.alert = {variant: "danger", message: "Failed to obtain Allegro token"};
                    }
                    else{
                        VueCookies.set("allegro-cred", true);
                        this.$router.push("/");
                    }
                } catch (error) {
                    this.alert = {variant: "danger", message: "Failed to obtain Allegro token"};
                }
                },
        },
        components:{
            VueCookies,
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