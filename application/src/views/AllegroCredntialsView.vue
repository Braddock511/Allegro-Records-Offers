<template>
    <TheHeader/>
    <section id="form-container" v-if="formDisplay">
        <form id="credentials-form" @submit.prevent="allegroToken">
            <div class="title">Credentials</div>

            <div class="input-container ic1">
                <input v-model="user_id" id="client_id" class="input" type="text" placeholder=" " required/>
                <label for="client_id" class="placeholder">Client id</label>
            </div>

            <div class="input-container ic2">
                <input v-model="user_secret" id="client_secret" class="input" type="text" placeholder=" " required/>
                <label for="client_secret" class="placeholder">Client secret</label>
            </div>

            <button type="submit" class="blue-button">Send credentials</button>
        </form>
    </section>

    <div id="confirm">
        <a :href="response.data.verification_uri_complete" v-if="!formDisplay" class="blue-button" target="_blank">Confirm</a>
    </div>
</template>

<script>
    import TheHeader from '@/components/TheHeader.vue'
    import VueCookies from 'vue-cookies'
    import axios from 'axios'

    export default {
        
        data(){
            return{
                user_id: "",
                user_secret: "",
                response: "",
                formDisplay: true
            }
        },

        methods:{
            async allegroToken() {
                try 
                {
                    this.response = await axios.post('http://127.0.0.1:8000/allegro-auth', {client_id: this.user_id, client_secret: this.user_secret})
                    this.formDisplay = false 
                    await axios.post('http://127.0.0.1:8000/allegro-token', {client_id: this.user_id, client_secret: this.user_secret, device_code: this.response.data['device_code']})
                    VueCookies.set('allegro-cred', true)
                    this.$router.push('/')
                } 
                catch (error) 
                {
                    alert("Upload failed")
                }
            },
        },

        components:{
            VueCookies, 
            TheHeader
        }
    }
</script>

<style lang="scss" scoped>
    #form-container {
        display: flex;
        justify-content: center;
        width: 100%;

        #credentials-form {
            display: flex;
            flex-direction: column;
            margin-top: 50px;
            border-radius: 25px;
            padding: 20px;
            background-color: rgb(34, 36, 36);
            width: 50%;
            gap: 20px;

            .title {
                font-size: 36px;
                font-weight: 600;
                margin-top: 15px;
            }

            .input-container {
                height: 50px;
                position: relative;
                width: 100%;

                .ic1 {
                    margin-top: 40px;
                }

                .ic2 {
                    margin-top: 30px;
                }

                .input {
                    background-color: #303245;
                    border-radius: 12px;
                    border: 0;
                    color: #eee;
                    font-size: 18px;
                    height: 100%;
                    outline: 0;
                    padding: 4px 20px 0;
                    width: 100%;

                    &:focus ~ .placeholder,
                    &:not(:placeholder-shown) ~ .placeholder {
                        transform: translateY(-35px) translateX(-18px) scale(0.75);
                    }

                    &:not(:placeholder-shown) ~ .placeholder {
                        color: #808097;
                    }

                    &:focus ~ .placeholder {
                        color: #08d;
                    }
                }

                .placeholder {
                    color: #65657b;
                    font-family: sans-serif;
                    left: 20px;
                    line-height: 14px;
                    pointer-events: none;
                    position: absolute;
                    transform-origin: 0 50%;
                    transition: transform 200ms, color 200ms;
                    top: 20px;
                }
            }

        }
    }

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