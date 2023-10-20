<template>
    <div class="data" v-if="!loading">
        <h1 v-if="!clearImage">{{ $t("editImages.firstImage") }}</h1>
        <TheSlider :images="allegroImages" v-if="!clearImage"></TheSlider>
        <img id="clear-image" :src="clearImage" alt="clear-image" v-if="clearImage" style="width: 750px; height: 564px; border: 3px solid black;">
        <h2 v-if="clearImage">{{ $t("editImages.cleared") }}</h2>
        <span id="buttons" style="width: 50%; display: flex; flex-direction: column; gap: 10px;">
            <button class="btn btn-primary w-100" type="button" style="padding: 0.5rem; font-size: 20px;" @click="editImages" v-if="clearImage">{{ $t("editImages.editImage") }}</button>
            <button class="btn btn-primary w-100" type="button" style="padding: 0.5rem; font-size: 20px;" @click="clearImages" v-if="!clearImage">{{ $t("editImages.clear") }}</button>
            <button class="btn btn-primary w-100" type="button" style="padding: 0.5rem; font-size: 20px;" @click="next">{{ $t("table.next") }}</button>
        </span>
    </div>
    <div id="loading" v-if="loading">
        <img src="@/assets/spinner.gif" alt="loading">
    </div>
    <TheAlert :alert="alert" />
</template>

<script>
    import TheSlider from '@/components/Global/TheSlider.vue'
    import TheAlert from '@/components/Global/TheAlert.vue'
    import axios from 'axios'
    export default {
        data(){
            return{
                clearImage: "",
                allegroImages: "",
                offerIndex: 0,
                loading: false,
                alert: {},
                userKey: this.$cookies.get('allegro-cred').userKey,
            }
        },
        methods:{
            async clearImages(){
                this.loading = true
                this.clearImage = (await axios.post('http://127.0.0.1:8000/clear-image', {userKey: this.userKey, image: this.allegroImages[0]})).data
                if (this.clearImage.error || this.clearImage.errors){
                    this.alert = {variant: "danger", message: this.$t("alerts.clearFailed")}
                }
                else{
                    this.clearImage = this.clearImage.output
                }
                this.loading = false
            },
            async editImages(){
                this.loading = true
                let otherImages = this.allegroImages.slice(1, this.allegroImages.length)
                let newImages = ([this.clearImage, otherImages]).flat()
                const response = (await axios.post('http://127.0.0.1:8000/allegro-edit-image', {userKey: this.userKey, offerID: this.allegroData.offers[this.offerIndex].id, images: newImages})).data
                if (response.error || response.errors){
                    this.alert = {variant: "danger", message: this.$t("alerts.imageFailed")}
                    this.loading = false
                }
                else{
                    this.alert = {variant: "success", message: this.$t("alerts.imageSuccess")}
                    // Next images
                    this.next()
                }
            },  
            async next(){
                this.loading = true
                this.offerIndex += 1
                if (this.offerIndex >= this.allegroData.offers.length){
                    window.location.reload()
                    return ""
                }
                else{
                    this.offerData = (await axios.post('http://127.0.0.1:8000/allegro-offer', {userKey: this.userKey, offerId: this.allegroData.offers[this.offerIndex].id})).data
                    if (this.offerData.error || this.offerData.errors){
                        this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
                    }
                    else{    
                        this.clearImage = ""
                        this.allegroImages = this.offerData.output.images
                    }
                }
                this.loading = false
            }
        },
        async beforeMount() {
            this.loading = true
            this.offerData = (await axios.post('http://127.0.0.1:8000/allegro-offer', {userKey: this.userKey, offerId: this.allegroData.offers[0].id})).data
            if (this.offerData.error || this.offerData.errors){
                this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
            }
            else{
                this.allegroImages = this.offerData.output.images
            }
            this.loading = false
        },
        props: {
            allegroData: {
                required: true
            }
        },
        components:{
            TheSlider,
            TheAlert
        }
    }
</script>

<style lang="scss" scoped>
    @media screen and (max-width: 1000px) {
        #clear-image{
            max-width: 300px !important;
            max-height: 300px !important;
        }
    }
    
</style>