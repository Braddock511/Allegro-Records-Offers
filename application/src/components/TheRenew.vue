<template>
    <section class="form-container" v-if="!offerData && !loading">
        <form>
            <div class="title">{{ $t("editView.renew") }}</div>
            <p>
                {{ $t("renew.info") }}
            </p>
            <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem; font-size: 20px;" @click="getOffer">{{ $t("renew.renew") }}</button>
        </form>
    </section>
    <div id="loading" v-if="loading">
        <img src="../assets/spinner.gif" alt="loading">
    </div>
    <TheAlert :alert="alert" />
</template>

<script>
    import TheAlert from '../components/TheAlert.vue'
    import axios from 'axios'

    export default {
        data(){
            return{
                loading: false,
                alert: {}
            }
        },
        methods:{
            async renewOffers(){
                this.loading = true
                
            }
        }        
    }

</script>
