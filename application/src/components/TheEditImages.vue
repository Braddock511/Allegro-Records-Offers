<template>
    <div id="data" v-if="!loading">
        <h1 v-if="!clearImage">Clears only the first image</h1>
        <TheSlider :images="allegroImages" v-if="!clearImage"></TheSlider>
        
        <img :src="clearImage.data" alt="clear-image" v-if="clearImage">
        <h2 v-if="clearImage">Cleared image</h2>

        <span id="buttons">
            <button class="blue-button" @click="editImages" v-if="clearImage">Edit image</button>
            <button class="blue-button" @click="clearImages" v-if="!clearImage">Clear</button>
            <button class="blue-button" @click="next">Next</button>
        </span>
    </div>

    <div id="loading" v-if="loading">
        <img src="../assets/spinner.gif" alt="loading">
    </div>

</template>

<script>
    import TheSlider from '@/components/TheSlider.vue'
    import axios from 'axios'
    
    export default {
        data(){
            return{
                clearImage: "",
                allegroImages: "",
                offerIndex: 0,
                loading: false,
            }
        },

        methods:{
            async clearImages(){
                try{
                    this.loading = true
                    this.clearImage = await axios.post('http://127.0.0.1:8000/clear-image', {images: this.allegroImages})
                    setTimeout(() => { this.loading = false }, 2500)
                }
                catch{
                    alert("Upload failed")
                }
            },

            async editImages(){
                // OFFERID
                this.loading = true
                let otherImages = this.allegroImages.slice(1, this.allegroImages.length)
                let newImages = ([this.clearImage.data, otherImages]).flat()
                await axios.post('http://127.0.0.1:8000/edit-image', {offerID: this.allegroData.data.offers[this.offerIndex].id, images: newImages})

                // Next images
                this.next()
            },  

            async next(){
                this.loading = true
                this.offerIndex += 1

                if (this.offerIndex == this.allegroData.data.offers.length){
                    this.$router.push("/")
                    return ""
                }
                
                this.offerData = await axios.post('http://127.0.0.1:8000/discogs-information', {id: this.offerIndex, allegroData: this.allegroData.data, typeRecord: this.typeRecord})
                
                this.clearImage = ""
                this.allegroImages = this.offerData.data.offer.images
                setTimeout(() => { this.loading = false }, 2500)
            }
        },

        async beforeMount() {
            this.loading = true
            this.offerData = await axios.post('http://127.0.0.1:8000/discogs-information', {id: 0, allegroData: this.allegroData.data, typeRecord: this.typeRecord})
            this.allegroImages = this.offerData.data.offer.images
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
            TheSlider
        }
    }
</script>

<style lang="scss" scoped>
    #data{
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        padding: 10px;
        gap: 10px;
        
        #buttons{
            display: flex; 
            flex-direction: column; 
            justify-content: center;
            align-items: center;
            width: 50%;
        }

        img{
            width: 750px;
            height: 750px;
            border: 3px solid black;
        }
    }
</style>