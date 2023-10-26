<template>
    <span>
        <section class="form-container" v-if="!discogsData && !loading">
            <form>
                <div class="title">{{ $t("editSpecific.offerId") }}</div>
                <div class="input-container">
                    <input type="text" name="offer-id" v-model="offerId" required>
                </div>
                <span>
                    {{ $t("editSpecific.editPrice") }} &nbsp;<input type="checkbox" v-model="editPrice">
                </span>
                <span>
                    {{ $t("editSpecific.editDescription") }} &nbsp;<input type="checkbox" v-model="editDescription">
                </span>
                <span>
                    {{ $t("editSpecific.toBuy") }} &nbsp;<input type="checkbox" v-model="toBuy">
                </span>        
                <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem; font-size: 20px;" @click="getOffer">{{ $t("editSpecific.edit") }}</button>
            </form>
        </section>
    </span>
    <span v-if="!loading">
        <div class="data" v-if="discogsData">
            <TheSlider :images="img.slice()"></TheSlider>
            <div style="width: 100%;">
                <span style="display: flex; flex-direction: column; align-items: center; gap: 10px;">    
                    <button class="btn btn-primary w-50" type="type" style="padding: 0.5rem; font-size: 20px;" @click="editImage">{{ $t("editSpecific.clearImage") }}</button>
                    <button class="btn btn-primary w-50" type="type" style="padding: 0.5rem; font-size: 20px;" @click="discogsData = ''; alert = {}">{{ $t("table.back") }}</button>
                </span>
            </div>
            <table>
                <tr style="background-color: rgb(34, 36, 35); border-bottom: 0px;">
                    <td><h3>{{ $t("table.label") }}</h3></td>
                    <td><h3>{{ $t("table.country") }}</h3></td>
                    <td><h3>{{ $t("table.year") }}</h3></td>
                    <td v-if="editPrice">
                        <h3>{{ $t("table.price") }}</h3>
                        <select v-model="condition" @change="this.price = ''">
                            <option value="Near Mint (NM or M-)">{{ $t("table.mintMinus") }}</option>
                            <option value="Mint (M)">{{ $t("table.mint") }}</option>
                            <option value="Excellent (EX)">{{ $t("table.ex") }}</option>
                            <option value="Very Good Plus (VG+)">{{ $t("table.veryGoodPlus") }}</option>
                            <option value="Very Good (VG)">{{ $t("table.veryGood") }}</option>
                            <option value="Good (G)">{{ $t("table.good") }}</option>
                            <option value="Fair (F)">{{ $t("table.fair") }}</option>
                        </select>
                    </td>
                    <td><h3>{{ $t("editSpecific.editOffer") }}</h3></td>
                    <td><h3>{{ $t("editSpecific.listingSimilar") }}</h3></td>
                </tr>
                <tr>
                    <td><input type="text" name="label" class="custom" placeholder="Label" v-model="label"></td>
                    <td><input type="text" name="country" class="custom" placeholder="Country" v-model="country"></td>
                    <td><input type="text" name="year" class="custom" placeholder="Year" v-model="year"></td>
                    <td v-if="editPrice"><input type="text" name="price" class="custom" placeholder="Price" v-model="price"></td>
                    <td><button class="btn btn-primary w-100" type="type" @click="editOffer">{{ $t("editSpecific.edit") }}</button></td>
                    <td><button class="btn btn-primary w-100" type="type" @click="listing_similar=true; editOffer({})">{{ $t("table.send") }}</button></td>
                </tr>
                <tr v-for="data in discogsData.output[0].information" v-if="discogsData && discogsData.output">
                    <td>
                        <span v-if="data.label !== '-'">{{ data.label }}</span>
                        <input v-else type="text" name="label" class="custom" placeholder="Label" v-model="label">
                    </td>
                    <td>
                        <span v-if="data.country !== '-'">{{ data.country }}</span>
                        <input v-else type="text" name="country" class="custom" placeholder="Country" v-model="country">
                    </td>
                    <td>
                        <span v-if="data.year !== '-'">{{ data.year }}</span>
                        <input v-else type="text" name="year" class="custom" placeholder="Year" v-model="year">
                    </td>
                    <td v-if="editPrice && data.price[condition == 'Excellent (EX)' ? 'Very Good Plus (VG+)' : condition] !== undefined">
                        Want: {{ data.community.want }} | Have: {{ data.community.have }}<br><br>
                        <input type="number" name="price" class="custom" min="1" :placeholder="roundedPrice(data.price[condition == 'Excellent (EX)' ? 'Very Good Plus (VG+)' : condition])" v-model="price" @click="price = roundedPrice(data.price[condition == 'Excellent (EX)' ? 'Very Good Plus (VG+)' : condition])">
                    </td>
                    <td v-if="editPrice && data.price[condition == 'Excellent (EX)' ? 'Very Good Plus (VG+)' : condition] === undefined">
                        Want: ? | Have: ?<br><br>
                        <input type="number" name="price" class="custom" min="1" v-model="price">
                    </td>
                    <td><button class="btn btn-primary w-100" type="type" @click="editOffer(data)">{{ $t("editSpecific.edit") }}</button></td>
                    <td><button class="btn btn-primary w-100" type="type" @click="listing_similar=true; editOffer(data)">{{ $t("table.send") }}</button></td>
                </tr>
                <tr>
                    <td colspan="3"><h4>{{ $t("table.notFound") }}</h4></td>
                    <td><input type="text" class="custom" v-model="newSearch" placeholder="-" ></td>
                    <td colspan="2"><button class="btn btn-primary w-100 allegro" type="submit" style="padding: 0.5rem;" @click="search">{{ $t("table.search") }}</button></td>
                </tr>
            </table>
        </div>
    </span>
    <div id="loading" v-if="loading">
        <img src="@/assets/spinner.gif" alt="loading">
    </div>
    <TheAlert :alert="alert" />
</template>

<script>
    import TheAlert from '@/components/Global/TheAlert.vue'
    import TheSlider from '@/components/Global/TheSlider.vue'
    import axios from 'axios'
    export default {
        data(){
            return{
                allegroData: "",
                discogsData: "",
                offerId: "",
                img: "",
                label: "",
                country: "",
                year: "",
                price: "",
                condition: "Near Mint (NM or M-)",
                newSearch: "",
                loading: false,
                listing_similar: false,
                alert: {},
                userKey: this.$cookies.get('allegro-cred').userKey,
                editPrice: false,
                editDescription: false,
                toBuy: false,
            }
        },
        methods:{
            async getOffer() {
                this.loading = true
                this.allegroData = (await axios.post(`${url}/allegro-offer`, {userKey: this.userKey, offerId: this.offerId})).data
                if (this.allegroData.error || this.allegroData.errors){
                    this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
                }
                else{
                    this.allegroData = this.allegroData.output
                        await axios.post(`${url}/discogs-information`, {userKey: this.userKey, index: 0, allegroData: this.allegroData})
                        .then((response) => {
                            this.discogsData = response.data

                            if (this.discogsData.status == 500) {
                                this.alert = {variant: "danger", message: `${this.$t("alerts.failed")} - ${this.discogsData.error}`}
                                this.discogsData = ""
                            }  
                            else {
                                this.img = this.discogsData.offer.images
                            }
                        })
                        .catch((error) => {
                            console.error('Error:', error)
                        })
                }
                this.loading = false
            },
            async editOffer(data){
                let selectedData = {}
                selectedData = {
                    id: data.id,
                    label: data.label != "-" ? data.label : this.label,
                    country: data.country != "-" ? data.country : this.country,
                    year: data.year != "-" ? data.year : this.year,
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
                // Edit offer
                this.loading = true
                axios.post(`${url}/allegro-edit`, {
                    userKey: this.userKey,
                    offerId: this.offerId,
                    images: this.img,
                    newEditData: selectedData,
                    listingSimilar: this.listing_similar,
                    editPrice: this.editPrice,
                    editDescription: this.editDescription,
                    toBuy: this.toBuy
                })
                .then(response => {
                    const responseData = response.data
                    if (responseData.status == 500) {
                        this.alert = {variant: "danger", message: `${this.$t("alerts.failed")} - ${responseData.error.errors[0].userMessage}`}
                    }   
                    else{
                        this.alert = {variant: "success", message: this.$t("alerts.success")}
                        this.discogsData = ""
                        this.offerId = ""
                        this.label = ""
                        this.country = ""
                        this.year = ""
                        this.price = ""
                    }
                    this.loading = false
                })
                .catch(error => {
                    this.alert = {variant: "danger", message: `${this.$t("alerts.failed")} - ${error}`}
                    this.loading = false
                })
                this.listing_similar = false
            },
            async editImage(){
                this.loading = true

                axios.post(`${url}/clear-image`, {userKey: this.userKey, image: this.img[0]})
                .then((response) => {
                    this.clearImage = response.data.output
                })
                .catch((error) => {
                    console.error('Error:', error)
                })
                
                let otherImages = this.img.slice(1, this.img.length)
                let newImages = ([this.clearImage, otherImages]).flat()
                axios.post(`${url}/allegro-edit-image`, {userKey: this.userKey, offerId: this.offerId, images: newImages})
                .then((response) => {
                    const responseData = response.data
                    if (responseData.status == 500) {
                        this.alert = {variant: "danger", message: `${this.$t("alerts.failed")} - ${responseData.error.errors[0].userMessage}`}
                    }  
                    else {
                        this.alert = { variant: "success", message: this.$t("alerts.imageSuccess") }
                    }
                })
                .catch((error) => {
                    console.error('Error:', error)
                })
                .finally(() => {
                    this.loading = false
                })
            },
            roundedPrice(price) {
                let finalValue
                if (price){
                    const roundedValue = Math.round((price.value * 3) / 10) * 10 - 0.01
                    finalValue = (roundedValue < 19.99) ? 19.99 : roundedValue 
                }
                else{
                    finalValue = 0
                }
                return finalValue
            },
            async search(){
                this.loading = true
                axios.post(`${url}/discogs-information-new-search`, {userKey: this.userKey, newSearch: this.newSearch, typeRecord: "", allegroData: this.allegroData}, { headers: { "Content-Type": "application/json" } })
                .then((response) =>{
                    this.discogsData = response.data
                    
                    this.newSearch = ""
                    this.loading = false
                })
            },
        },
        components:{
            TheSlider,
            TheAlert
        }
    }
</script>
