<template>
    <TheHeader/>
    <span v-if="!imageData">
        <section class="form-container" v-if="!loading">
            <form @submit.prevent="getDataImage">
                <div class="title">Upload images</div>
                <div class="input-container">
                    <label for="files">Images:  </label>
                    <input @change="handleFiles" id="files" type="file" multiple required/>
                </div>
                <select v-model="type" style="display: flex; align-self: start; width: 200px;">
                        <option value="Vinyl">Vinyl</option>
                        <option value="CD">CD</option>
                </select>
                <span>
                    Clear first image background <input type="checkbox" v-model="clear">
                </span>
                <p>Offer have exactly 3 images, so upload 3 images on one offer</p>
                <p>The images must be in the following order: 1. Front cover 2. Back cover 3. Disc</p>
                <p>Payment, location and delivery settings are taken from the last offer </p>
                <p>Description is in polish language</p>
                <button type="submit" class="blue-button">Send images</button>
            </form>
        </section>
        <div id="loading" v-if="loading">
            <img src="../assets/spinner.gif" alt="loading">
        </div>
    </span>
    <TheListingData v-if="imageData" :imageData="imageData" :type="type" :clear="clear"/>
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
                files.sort((a, b) => a.name.localeCompare(b.name))
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
                try 
                {
                    await axios.post('http://127.0.0.1:8000/read-image', {images: this.images, typeRecord: this.type}, {headers: {'Content-Type': 'application/json'}})
                    this.imageData = await axios.post('http://127.0.0.1:8000/discogs-information-image', {typeRecord: this.type}, {headers: {'Content-Type': 'application/json'}})
                } 
                catch (error) 
                {
                    alert('Upload failed.')
                }
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
