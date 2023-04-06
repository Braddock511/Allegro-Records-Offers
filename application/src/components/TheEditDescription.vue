<template>
    <span v-if="offerData">
        <div class="data" v-if="offerData.data.offer.name.length > 0 && !loading">
            <TheSlider :images="img.slice().reverse()"></TheSlider>
            <table>
                <tr>
                    <td colspan="7" style="border: none; background-color: #202833;"><button class="btn btn-primary" type="submit" style="width: 45%; padding: 0.5rem; font-size: 20px;" @click="next">{{ $t("table.next") }}</button></td>
                </tr>
                <tr>
                    <td><h2>{{ $t("table.title") }}</h2></td>
                    <td><h2>{{ $t("table.label") }}</h2></td>
                    <td><h2>{{ $t("table.country") }}</h2></td>
                    <td><h2>{{ $t("table.year") }}</h2></td>
                    <td><h2>{{ $t("editSpecific.editOffer") }}</h2></td>
                </tr>
                <tr>
                    <td>{{ offerData.data.offer.name }}</td>
                    <td>{{ $t("table.enter_label") }} <input type="text" name="label" class="custom" placeholder="-"  v-model="label"></td>
                    <td>{{ $t("table.enter_country") }} <input type="text" name="country" class="custom" placeholder="-"  v-model="country"></td>
                    <td>{{ $t("table.enter_year") }} <input type="text" name="year" class="custom" placeholder="-" v-model="year"></td>
                    <td><button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="editOffer">{{ $t("editSpecific.edit") }}</button></td>
                </tr>
                <tr v-for="data in offerData.data.discogs.data" v-if="offerData && offerData.data.discogs.data">
                    <td>{{ offerData.data.offer.name  }}</td>
                    <td>{{ data.label }}</td>
                    <td>{{ data.country }}</td>
                    <td>{{ data.year }}</td>
                    <td><button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="editOffer(data)">{{ $t("editSpecific.edit") }}</button></td>
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
    import TheSlider from '@/components/TheSlider.vue'
    import TheAlert from '../components/TheAlert.vue'
    import axios from 'axios'
    export default {
        data(){
            return{
                offerIndex: 0,
                offerData: "",
                img: "",
                label: "",
                country: "",
                year: "",
                loading: false,
                alert: {}
            }
        },
        methods:{
            async editOffer(data){
                let selectedData = {}
                // Edit offer
                selectedData = {
                    id: data.id,
                    label: data.label,
                    country: data.country,
                    year: data.year,
                }
                if (selectedData.id == undefined)
                    selectedData = {
                        id: "",
                        label: this.label ? this.label : "-",
                        country: this.country ? this.country : "-",
                        year: this.year ? this.year : "-",
                    }
                this.loading = true
                const response = await axios.post("http://127.0.0.1:8000/allegro-edit-offer", {offerId: this.allegroData.data.offers[this.offerIndex].id, images: this.offerData.data.offer.images, data: selectedData})
                if (response.data.error || response.data.errors){
                    this.alert = {variant: "danger", message: this.$t("alerts.descFailed")}
                }
                else{
                    this.alert = {variant: "success", message: this.$t("alerts.descSuccess")}
                    // New offer
                    this.next()
                }
                this.loading = false
            },
            async next(){
                this.loading = true
                this.offerIndex += 1
                if (this.offerIndex >= this.allegroData.data.offers.length){
                    this.$router.push("/")
                }
                this.offerData = await axios.post('http://127.0.0.1:8000/discogs-information', {id: this.offerIndex, allegroData: this.allegroData.data, typeRecord: this.typeRecord})
                if (this.allegroData.data.error || this.allegroData.data.errors){
                    this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
                }
                else{
                    this.label = "",
                    this.country = "",
                    this.year = "",
                    this.img = this.offerData.data.offer.images
                    setTimeout(() => { this.loading = false }, 3500)
                }
            }
        },
        async beforeMount() {
            this.loading = true
            this.offerData = await axios.post('http://127.0.0.1:8000/discogs-information', {id: 0, allegroData: this.allegroData.data, typeRecord: this.typeRecord})
            if (this.allegroData.data.error || this.allegroData.data.errors){
                this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
            }
            else{
                this.img = this.offerData.data.offer.images
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
