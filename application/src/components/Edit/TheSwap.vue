<template>
    <section class="form-container" v-if="!loading  && !displaySpecific" style="height: 500px;">
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
            <span style="display:flex; justify-content: center; gap: 10px; margin-top: 50px;">
                    <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="swap">{{ $t("swap.swapAll") }}</button>
                    <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="displaySpecific = true">{{ $t("swap.swapSpecific") }}</button>
            </span>
        </form>
    </section>

    <section class="form-container" v-if="!loading && displaySpecific" style="height: 500px;">
        <form>
            <div class="title">{{ $t("swap.title") }}</div>
            <h5>{{ $t('swap.info') }}</h5>
            <div class="input-container">
                {{ $t('editSpecific.offerId') }}<br>
                <input type="text" name="offer-id" v-model="offerId">
            </div>
            
            <div class="input-container" style="margin-top: 10px; margin-bottom: 10px;">
                {{ $t('swap.orFile') }}<br>
                <input type="file" @change="handleIdsFile" accept=".txt" style="font-size: 14px;"/>
            </div>

            <span style="display: flex; justify-content: center; gap: 10px; margin-top: 50px;">
                <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="swapSpecific">{{ $t("swap.swapOffer") }}</button>
                <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="displaySpecific = false">{{ $t("table.back") }}</button>
            </span>
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
                offerId: "",
                offersId: [],
                displaySpecific: false,
                alert: {},
                loading: false,
                userKey: this.$cookies.get('allegro-cred').userKey,
            }
        },
        methods:{
            async swap() {
                this.loading = true
                const response = (await axios.post('http://127.0.0.1:8000/swap-all', {userKey: this.userKey, swapCarton: this.swapCarton, withCarton: this.withCarton})).data
                if (response.error || response.errors){
                    this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
                }
                else{
                    this.alert = {variant: "success", message: this.$t("alerts.success")}
                }
                this.loading = false
            },
            async swapSpecific() {
                this.loading = true
                if(this.offersId.length == 0)
                {
                    const response = (await axios.post('http://127.0.0.1:8000/swap-specific', {userKey: this.userKey, swapCarton: this.swapCarton, withCarton: this.withCarton, offerId: this.offerId})).data
                    if (response.error || response.errors){
                        this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
                    }
                    else{
                        this.alert = {variant: "success", message: this.$t("alerts.success")}
                    }
                }
                else
                {
                    for (let i = 0; i < this.offersId.length; i++) {
                        const id = this.offersId[i]
                        const response = (await axios.post('http://127.0.0.1:8000/swap-specific', {userKey: userKey, swapCarton: this.swapCarton, withCarton: this.withCarton, offerId: id })).data

                        if (response.error || response.errors) {
                            this.alert = { variant: "danger", message: this.$t("alerts.someWrong") }
                        } else {
                            this.alert = { variant: "success", message: this.$t("alerts.success") }
                        }
                    }
                }

                this.offerId = ""
                this.offersId = []
                this.loading = false
            },
            handleIdsFile(event) {
                const file = event.target.files[0]
                this.idsFile = file
                const reader = new FileReader()
                reader.onload = () => {
                    const content = reader.result
                    this.validateAndSave(content)
                }
                reader.readAsText(this.idsFile)
                },
                validateAndSave(content) {
                    const lines = content.includes('\n') ? content.split('\n') : content.split(' ')
                    const processedLines = lines.map((line) => line.trim())
                    this.offersId = this.offersId.concat(processedLines).reverse()
            },
        },
        components:{
            TheAlert,
        }
    }
</script>