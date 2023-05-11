<template>
    <section class="form-container" v-if="!loading" style="height: 500px;">
        <form>
            <div class="title">{{ $t("swap.title") }}</div>
            <h5>{{ $t('swap.info') }}</h5>
            <div class="input-container">
                {{ $t('swap.swap') }}<br>
                <input type="text" name="swap" v-model="swapCarton">
            </div>
            <div class="input-container" style="margin-top: 10px; margin-bottom: 10px;">
                {{ $t('swap.with') }}<br>
                <input type="text" name="with" v-model="withCarton">
            </div>
            <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem; font-size: 20px;" @click="swap">{{ $t("swap.buttonSwap") }}</button>
        </form>
    </section>
    <div id="loading" v-if="loading">
        <img src="@/assets/spinner.gif" alt="loading">
    </div>
    <TheAlert :alert="alert" />
</template>

<script>
    import TheAlert from "@/components/Global/TheAlert.vue"
    import axios from 'axios'
    export default {
        data(){
            return{
                swapCarton: "",
                withCarton: "",
                alert: {},
                loading: false,
            }
        },
        methods:{
            async swap() {
                this.loading = true
                const response = (await axios.post('http://127.0.0.1:8000/swap-cartons', {swapCarton: this.swapCarton, withCarton: this.withCarton})).data
                console.log(response)
                if (response.error || response.errors){
                    this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
                }
                else{
                    this.alert = {variant: "success", message: this.$t("alerts.success")}
                }
                this.loading = false
            },
        },
        components:{
            TheAlert,
        }
    }
</script>