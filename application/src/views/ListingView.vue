<template>
    <TheHeader/>
    <span v-if="!imageData">
        <section class="form-container" v-if="!loading">
            <form @submit.prevent="getDataImage">
                <div class="title">{{ $t("listingView.upload") }}</div>
                <div class="input-container">
                    <label for="files">{{ $t("listingView.images") }} &nbsp;</label>
                    <input @change="handleFiles" id="files" type="file" multiple required style="font-size: 14px;"/>
                </div>
                <select v-model="type" style="display: flex; align-self: start; width: 200px; font-size: 14px;">
                        <option value="Vinyl">{{ $t("vinyl") }}</option>
                        <option value="CD">CD</option>
                </select>
                <span>
                    {{ $t("listingView.clearFirstImage") }} &nbsp;<input type="checkbox" v-model="clear">
                </span>
                <div class="input-container">
                    <label for="number-images">{{ $t("listingView.numberImages") }}</label>
                    <input v-model="numberImages" id="number-images" type="number" min="2" required style="font-size: 14px; margin-left: 10px;"/>
                </div>
                <p>{{ $t("listingView.imageOrder") }}</p>
                <p>{{ $t("listingView.paymentLocationDelivery") }}</p>
                <p>{{ $t("listingView.description") }}</p>
                <button class="btn btn-primary w-100" type="button" style="padding: 0.5rem; font-size: 20px;" @click="getDataImage">{{ $t("listingView.sendImages") }}</button>
            </form>
        </section>
        <div id="loading" v-if="loading">
            <img src="../assets/spinner.gif" alt="loading">
        </div>
    </span>
    <TheListingData v-if="imageData" :imageData="imageData" :type="type" :clear="clear" :numberImages="numberImages"/>
</template>

<script>
    import TheHeader from '@/components/TheHeader.vue'
    import TheListingData from '@/components/TheListingData.vue'
    import VueCookies from 'vue-cookies'
    import axios from 'axios'
    export default {        
        data(){
            return{
                images: [],
                numberImages: 3,
                imageData: "",
                type: "Vinyl",
                clear: false,
                loading: false,
            }
        },
        methods:{
            handleFiles(event) {
                // Get an array of the selected files and sort them by name
                const files = Array.from(event.target.files)
                let loadedCount = 0

                // Loop through the files and read each one as a data URL
                for (let i = 0; i < files.length; i++) {
                    const reader = new FileReader()
                    reader.readAsDataURL(files[i])
                    reader.onload = () => {
                        this.images[i] = reader.result
                        loadedCount++
                        if (loadedCount === files.length) {
                            // All files have been loaded, sort the data array
                            this.images.sort((a, b) => files.findIndex(file => file.name === a.split(',')[0].split(';')[1]) - files.findIndex(file => file.name === b.split(',')[0].split(';')[1]))
                        }
                    }
                }
            },
            async getDataImage() {
                this.loading = true
                await axios.post('http://127.0.0.1:8000/read-image', {images: this.images, typeRecord: this.type, numberImages: this.numberImages}, {headers: {'Content-Type': 'application/json'}})
                this.imageData = await axios.post('http://127.0.0.1:8000/discogs-information-image', {typeRecord: this.type}, {headers: {'Content-Type': 'application/json'}})
                this.loading = false
            },
        },
        components:{
            TheHeader,
            TheListingData,
            VueCookies 
        }
    }
</script>
