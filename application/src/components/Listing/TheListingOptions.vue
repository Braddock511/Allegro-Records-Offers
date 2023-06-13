<template>
    <span v-if="!read">
        <section class="form-container" v-if="!loading">
            <form @submit.prevent="getImageData">
                <div class="title">{{ $t("listingView.upload") }}</div>
                <div class="input-container">
                    <label for="files">{{ $t("listingView.images") }} &nbsp;</label>
                    <input @change="handleImagesFiles" id="files" type="file" multiple required style="font-size: 14px;"/>
                </div>
                <select v-model="typeRecord" style="display: flex; align-self: start; width: 200px; font-size: 14px;">
                        <option value="Vinyl">{{ $t("vinyl") }}</option>
                        <option value="CD">CD</option>
                </select>
                <span>
                    <select v-model="typeOffer" style="display: flex; align-self: start; width: 200px; font-size: 14px;">
                            <option value="BUY_NOW">{{ $t("listingView.buyNow") }}</option>
                            <option value="AUCTION">{{ $t("listingView.auction") }}</option>
                    </select>
                    <select v-if="typeOffer == 'AUCTION'" v-model="duration" style="display: flex; align-self: start; width: 200px; font-size: 14px;">
                            <option value="P1D">1 {{ $t("listingView.day") }}</option>
                            <option value="P3D">3 {{ $t("listingView.day") }}</option>
                            <option value="P5D">5 {{ $t("listingView.day") }}</option>
                            <option value="P7D">7 {{ $t("listingView.day") }}</option>
                            <option value="P10D">10 {{ $t("listingView.day") }}</option>
                    </select>
                </span>
                <span>
                    {{ $t("listingView.clearFirstImage") }} &nbsp;<input type="checkbox" v-model="clear">
                </span>
                <div class="input-container">
                    <label for="number-images">{{ $t("listingView.numberImages") }}</label>
                    <input v-model="numberImages" id="number-images" type="number" min="2" required style="font-size: 14px; margin-left: 10px;"/>
                </div>
                <div class="input-container">
                    <label for="number-images">{{ $t("conditionFile") }}&nbsp;</label>
                    <input type="file" @change="handleConditionFile" accept=".txt" style="font-size: 14px;"/>
                </div>
                <p>{{ $t("listingView.imageOrder") }}</p>
                <p>{{ $t("listingView.paymentLocationDelivery") }}</p>
                <p>{{ $t("listingView.description") }}</p>
                <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem; font-size: 20px;">{{ $t("listingView.sendImages") }}</button>
            </form>
        </section>
        <div id="loading" v-if="loading">
            <img src="@/assets/spinner.gif" alt="loading">
            <h3>{{ $t('loading.readImage') }}</h3>
        </div>
    </span>
    <TheListingData v-if="read" :typeRecord="typeRecord" :typeOffer="typeOffer" :duration="duration" :clear="clear" :numberImages="numberImages" :numberFiles="files.length" :conditions="conditions"/>
</template>

<script>
    import TheListingData from '@/components/Listing/TheListingData.vue'
    import VueCookies from 'vue-cookies'
    import axios from 'axios'
    export default {        
        data(){
            return{
                images: [],
                numberImages: 3,
                read: "",
                files: "",
                typeRecord: "Vinyl",
                typeOffer: "BUY_NOW",
                duration: "P1D",
                conditionFile: null,
                conditions: [],
                clear: false,
                loading: false,
                alert: {}
            }
        },
        methods:{
            handleImagesFiles(event) {
                // Get an array of the selected files and sort them by name
                const files = Array.from(event.target.files)
                this.files = files
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
            handleConditionFile(event) {
                const file = event.target.files[0]
                this.conditionFile = file
                const reader = new FileReader()
                reader.onload = () => {
                    const content = reader.result
                    this.validateAndSave(content)
                }
                reader.readAsText(this.conditionFile)
                },
                validateAndSave(content) {
                    const lines = content.includes('\n') ? content.split('\n') : content.split(' ')
                    const processedLines = lines.map((line) => line.trim())
                    this.conditions = this.conditions.concat(processedLines).reverse()
            },
            splitImages(images, numberImages) {
                const chunks = [];

                for (let i = 0; i < images.length; i += numberImages) {
                    const chunk = images.slice(i, i + numberImages)
                    chunks.push(chunk)
                }

                return chunks
            },
            async getImageData() {
                this.loading = true
                const splitImages = this.splitImages(this.images, this.numberImages)
                
                if (this.typeRecord == "Vinyl"){
                    this.read = await axios.post('http://127.0.0.1:8000/read-vinyl-image', {images: splitImages}, {headers: {'Content-Type': 'application/json'}})
                }
                else if (this.typeRecord == "CD"){
                    this.read = await axios.post('http://127.0.0.1:8000/read-cd-image', {images: splitImages}, {headers: {'Content-Type': 'application/json'}})
                }
                console.log(this.read)
                this.loading = false
            },
        },
        components:{
            TheListingData,
            VueCookies
        }
    }
</script>
