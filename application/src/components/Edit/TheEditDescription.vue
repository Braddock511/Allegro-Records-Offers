<template>
    <span v-if="offerData">
        <div class="data" v-if="offerData.offer.name.length > 0 && !loading">
            <TheSlider :images="img.slice().reverse()"></TheSlider>
            <div style="width: 100%; text-align: center;">
                <button class="btn btn-primary" type="submit" style="width: 45%; padding: 0.5rem; font-size: 20px;" @click="next">{{ $t("table.next") }}</button>
            </div>
            <table>
                <tr style="background-color: rgb(34, 36, 35);">
                    <td><h2>{{ $t("table.label") }}</h2></td>
                    <td><h2>{{ $t("table.country") }}</h2></td>
                    <td><h2>{{ $t("table.year") }}</h2></td>
                    <td><h2>{{ $t("editSpecific.editOffer") }}</h2></td>
                </tr>
                <tr>
                    <td>{{ $t("table.enter_label") }} <input type="text" name="label" class="custom" placeholder="-"  v-model="label"></td>
                    <td>{{ $t("table.enter_country") }} <input type="text" name="country" class="custom" placeholder="-"  v-model="country"></td>
                    <td>{{ $t("table.enter_year") }} <input type="text" name="year" class="custom" placeholder="-" v-model="year"></td>
                    <td><button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="editOffer">{{ $t("editSpecific.edit") }}</button></td>
                </tr>
                <tr v-for="data in offerData.discogs" v-if="offerData && offerData.discogs">
                    <td>{{ data.label }}</td>
                    <td>{{ data.country }}</td>
                    <td>{{ data.year }}</td>
                    <td><button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="editOffer(data)">{{ $t("editSpecific.edit") }}</button></td>
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
    import TheSlider from '@/components/Global/TheSlider.vue'
    import TheAlert from '@/components/Global/TheAlert.vue'
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
                const response = (await axios.post("http://127.0.0.1:8000/allegro-edit-description", {offerId: this.allegroData.offers[this.offerIndex].id, images: this.offerData.offer.images, data: selectedData})).data
                if (response.error || response.errors){
                    this.alert = {variant: "danger", message: this.$t("alerts.descFailed")}
                    this.loading = false
                }
                else{
                    this.alert = {variant: "success", message: this.$t("alerts.descSuccess")}
                    // New offer
                    this.next()
                }
            },
            async next(){
                this.loading = true
                this.offerIndex += 1
                if (this.offerIndex >= this.allegroData.offers.length){
                    console.log(1)
                    window.location.reload()
                    return ""
                }
                else{
                    this.offerData = (await axios.post('http://127.0.0.1:8000/discogs-information', {index: this.offerIndex, allegroData: this.allegroData})).data
                    if (this.allegroData.error || this.allegroData.errors){
                        this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
                    }
                    else{
                        this.label = "",
                        this.country = "",
                        this.year = "",
                        this.img = this.offerData.offer.images
                    }
                }
                this.loading = false
            }
        },
        async beforeMount() {
            this.loading = true
            this.offerData = (await axios.post('http://127.0.0.1:8000/discogs-information', {index: 0, allegroData: this.allegroData})).data
            if (this.allegroData.error || this.allegroData.errors){
                this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
            }
            else{
                this.img = this.offerData.offer.images
            }
            this.loading = false
        },
        props: {
            allegroData: {
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
@media screen and (max-width: 1700px) {
    tr:nth-child(1){
        td:nth-child(1){
            display: flex;
            justify-content: center;
        }
    }
}
</style>