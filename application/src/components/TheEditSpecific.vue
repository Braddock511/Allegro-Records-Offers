<template>
    <span>
        <section class="form-container" v-if="!offerData && !loading">
            <form>
                <div class="title">{{ $t("editSpecific.offerId") }}</div>
                <div class="input-container">
                    <input type="text" name="offer-id" v-model="offerId" required>
                </div>        
                <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem; font-size: 20px;" @click="getOffer">{{ $t("editSpecific.edit") }}</button>
            </form>
        </section>
    </span>
    <span v-if="offerData">
        <div class="data" v-if="offerData.data.offer && !loading">
            <TheSlider :images="img.slice().reverse()"></TheSlider>
            <table>
                <tr>
                    <td colspan="6"  style="border: none; background-color: #202833;">
                        <span style="display: flex; flex-direction: column; align-items: center; gap: 10px;">    
                            <button class="btn btn-primary w-50" type="type" style="padding: 0.5rem; font-size: 20px;" @click="editImage">{{ $t("editSpecific.clearImage") }}</button>
                            <button class="btn btn-primary w-50" type="type" style="padding: 0.5rem; font-size: 20px;" @click="offerData = ''; alert = {}">{{ $t("table.back") }}</button>
                        </span>
                    </td>
                </tr>
                <tr>
                </tr>
                <tr>
                    <td><h2>{{ $t("table.title") }}</h2></td>
                    <td><h2>{{ $t("table.label") }}</h2></td>
                    <td><h2>{{ $t("table.country") }}</h2></td>
                    <td><h2>{{ $t("table.year") }}</h2></td>
                    <td v-if="allegroData.data.sellingMode.format=='BUY_NOW'">
                        <h2>{{ $t("table.price") }}</h2>
                        <select v-model="condition" @change="this.price = ''">
                            <option value="Near Mint (NM or M-)">{{ $t("table.mintMinus") }}</option>
                            <option value="Mint (M)">{{ $t("table.mint") }}</option>
                            <option value="Very Good Plus (VG+)">{{ $t("table.veryGoodPlus") }}</option>
                            <option value="Very Good (VG)">{{ $t("table.veryGood") }}</option>
                            <option value="Good (G)">{{ $t("table.good") }}</option>
                        </select>
                    </td>
                    <td><h2>{{ $t("editSpecific.editOffer") }}</h2></td>
                </tr>
                <tr>
                    <td>{{ offerData.data.offer.name }}</td>
                    <td><input type="text" name="label" class="custom" placeholder="-"  v-model="label"></td>
                    <td><input type="text" name="country" class="custom" placeholder="-"  v-model="country"></td>
                    <td><input type="text" name="year" class="custom" placeholder="-" v-model="year"></td>
                    <td v-if="allegroData.data.sellingMode.format=='BUY_NOW'"><input type="text" name="price" class="custom" placeholder="-" v-model="price"></td>
                    <td><button class="btn btn-primary w-100" type="type" style="padding: 0.5rem;" @click="editOffer">{{ $t("editSpecific.edit") }}</button></td>
                </tr>
                <tr v-for="data in offerData.data.discogs.data" v-if="offerData && offerData.data.discogs.data">
                    <td>{{ offerData.data.offer.name  }}</td>
                    <td>{{ data.label }}</td>
                    <td>{{ data.country }}</td>
                    <td>{{ data.year }}</td>
                    <td v-if="data.price[condition] !== undefined && allegroData.data.sellingMode.format=='BUY_NOW'">
                        <input type="number" name="price" class="custom" min="1" :placeholder="roundedPrice(data.price[condition])" v-model="price" @click="price = roundedPrice(data.price[condition])">
                    </td>
                    <td v-if="data.price[condition] === undefined && allegroData.data.sellingMode.format=='BUY_NOW'">
                        <input type="number" name="price" class="custom" min="1" v-model="price">
                    </td>
                    <td><button class="btn btn-primary w-100" type="type" style="padding: 0.5rem;" @click="editOffer(data)">{{ $t("editSpecific.edit") }}</button></td>
                </tr>
            </table>
        </div>
    </span>
    <div id="loading" v-if="loading">
        <img src="../assets/spinner.gif" alt="loading">
    </div>
    <TheAlert :alert="alert" />
</template>

<script>
    import TheAlert from '../components/TheAlert.vue'
    import TheSlider from '@/components/TheSlider.vue'
    import axios from 'axios'
    export default {
        data(){
            return{
                allegroData: "",
                offerData: "",
                offerId: "",
                img: "",
                label: "",
                country: "",
                year: "",
                price: "",
                condition: "Near Mint (NM or M-)",
                loading: false,
                alert: {}
            }
        },
        methods:{
            async getOffer() {
                this.loading = true
                this.allegroData = await axios.post('http://127.0.0.1:8000/allegro-offer', {offerId: this.offerId})
                if (this.allegroData.data.error || this.allegroData.data.errors){
                    this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
                }
                else{
                    let parameters = this.allegroData.data.productSet[0].product.parameters
                    let typeRecord
                    for (let i = 0; i<parameters.length; i++){
                        if (parameters[i].name == "Nośnik"){
                            typeRecord = parameters[i].values[0]
                            if (typeRecord == "Winyl"){
                                typeRecord = "Vinyl"
                            }  
                            break
                        }
                    }
                    this.offerData = await axios.post('http://127.0.0.1:8000/discogs-information', {id: 0, allegroData: this.allegroData.data, typeRecord: typeRecord})
                    this.img = this.offerData.data.offer.images
                }
                this.loading = false
            },
            async editOffer(data){
                let selectedData = {}
                selectedData = {
                    id: data.id,
                    label: data.label,
                    country: data.country,
                    year: data.year,
                    price: this.price
                }

                if (selectedData.id === undefined){
                    selectedData = {
                        id: "-",
                        label: this.label ? this.label : "-",
                        country: this.country ? this.country : "-",
                        year: this.year ? this.year : "-",
                        price: this.price
                    }
                }
                if (this.allegroData.data.sellingMode.format=='BUY_NOW'){
                    if (this.price !== ""){
                        // Edit offer
                        this.loading = true
                        const response = await axios.post("http://127.0.0.1:8000/allegro-edit-offer", {offerId: this.offerId, images: this.img, data: selectedData})
                        if (response.data.error || response.data.errors){
                            this.alert = {variant: "danger", message: this.$t("alerts.descFailed")}
                        }
                        else{
                            this.alert = {variant: "success", message: this.$t("alerts.descSuccess")}
                        }
                        this.label = ""
                        this.country = ""
                        this.year = ""
                        this.price = ""
                        this.loading = false
                    }
                    else{
                        this.alert = {variant: "warning", message: this.$t("alerts.completePrice")}
                    }
                }
                else{
                    // Edit offer
                    this.loading = true
                    const response = await axios.post("http://127.0.0.1:8000/allegro-edit-offer", {offerId: this.offerId, images: this.img, data: selectedData})
                    if (response.data.error || response.data.errors){
                        this.alert = {variant: "danger", message: this.$t("alerts.descFailed")}
                    }
                    else{
                        this.alert = {variant: "success", message: this.$t("alerts.descSuccess")}
                    }
                    this.label = ""
                    this.country = ""
                    this.year = ""
                    this.price = ""
                    this.loading = false
                }
            },
            async editImage(){
                this.loading = true
                this.clearImage = await axios.post('http://127.0.0.1:8000/clear-image', {image: this.img[0]})
                let otherImages = this.img.slice(1, this.img.length)
                let newImages = ([this.clearImage.data, otherImages]).flat()
                const response = await axios.post('http://127.0.0.1:8000/allegro-edit-image', {offerID: this.offerId, images: newImages})
                if (response.data.error || response.data.errors){
                    this.alert = {variant: "danger", message: this.$t("alerts.imageFailed")}
                }
                else{
                    this.alert = {variant: "success", message: this.$t("alerts.imageSuccess")}
                }
                this.loading = false
            },
            roundedPrice(price) {
                let finalValue
                if (price){
                    const roundedValue = Math.round((price.value * 3) / 10) * 10 - 0.01
                    finalValue = (roundedValue < 9.99) ? 9.99 : roundedValue 
                }
                else{
                    finalValue = 0
                }
                return finalValue
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
    tr {
      &:nth-child(2){
        display: none;
      }
    }
}
</style>