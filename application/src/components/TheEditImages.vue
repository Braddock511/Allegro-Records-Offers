<template>
    <div class="data" v-if="!loading">
        <h1 v-if="!clearImage">Clears only the first image</h1>
        <TheSlider :images="allegroImages" v-if="!clearImage"></TheSlider>
        <img :src="clearImage.data" alt="clear-image" v-if="clearImage">
        <h2 v-if="clearImage">Cleared image</h2>
        <span id="buttons" style="width: 50%; display: flex; flex-direction: column; gap: 10px;">
            <button class="btn btn-primary w-100" type="button" style="padding: 0.5rem; font-size: 20px;" @click="editImages" v-if="clearImage">Edit image</button>
            <button class="btn btn-primary w-100" type="button" style="padding: 0.5rem; font-size: 20px;" @click="clearImages" v-if="!clearImage">Clear</button>
            <button class="btn btn-primary w-100" type="button" style="padding: 0.5rem; font-size: 20px;" @click="next">Next</button>
        </span>
    </div>
    <div id="loading" v-if="loading">
        <img src="../assets/spinner.gif" alt="loading">
    </div>
    <TheAlert :alert="alert" />
</template>

<script>
    import TheSlider from '@/components/TheSlider.vue'
    import TheAlert from '../components/TheAlert.vue'
    import axios from 'axios'
    export default {
        data(){
            return{
                clearImage: "",
                allegroImages: "",
                offerIndex: 0,
                loading: false,
                alert: {}
            }
        },
        methods:{
            async clearImages(){
                this.loading = true
                this.clearImage = await axios.post('http://127.0.0.1:8000/clear-image', {image: this.allegroImages[0]})
                if (this.clearImage.data.error || this.clearImage.data.errors){
                    this.alert = {variant: "danger", message: "Clear image failed"}
                }

                setTimeout(() => { this.loading = false }, 2500)
            },
            async editImages(){
                this.loading = true
                let otherImages = this.allegroImages.slice(1, this.allegroImages.length)
                let newImages = ([this.clearImage.data, otherImages]).flat()
                const response = await axios.post('http://127.0.0.1:8000/allegro-edit-image', {offerID: this.allegroData.data.offers[this.offerIndex].id, images: newImages})
                if (response.data.error || response.data.errors){
                    this.alert = {variant: "danger", message: "Edit image failed"}
                }
                else{
                    this.alert = {variant: "success", message: "Edit image success"}
                    // Next images
                    this.next()
                }
                this.loading = false
            },  
            async next(){
                this.loading = true
                this.offerIndex += 1
                if (this.offerIndex >= this.allegroData.data.offers.length){
                    this.$router.push("/")
                    return ""
                }
                this.offerData = await axios.post('http://127.0.0.1:8000/discogs-information', {id: this.offerIndex, allegroData: this.allegroData.data, typeRecord: this.typeRecord})
                if (this.allegroData.data.error || this.allegroData.data.errors){
                    this.alert = {variant: "danger", message: "Something went wrong with getting offer"}
                }
                else{    
                    this.clearImage = ""
                    this.allegroImages = this.offerData.data.offer.images
                    setTimeout(() => { this.loading = false }, 2500)
                }
            }
        },
        async beforeMount() {
            this.loading = true
            this.offerData = await axios.post('http://127.0.0.1:8000/discogs-information', {id: 0, allegroData: this.allegroData.data, typeRecord: this.typeRecord})
            if (this.allegroData.data.error || this.allegroData.data.errors){
                this.alert = {variant: "danger", message: "Something went wrong with getting discogs information"}
            }
            else{
                this.allegroImages = this.offerData.data.offer.images
            }
            this.loading = false
        },
        props: {
            allegroData: {
                required: true
            },
            typeRecord: {
                required: true
            },
        },
        components:{
            TheSlider,
            TheAlert
        }
    }
</script>

<style lang="scss" scoped>
    .data{
        img{
            min-width: 750px;
            min-height: 750px;
            border: 3px solid black;
        }
    }
</style>