<template>
    <div class="data" v-if="dataFailed.length > 0 && !loading.flag">
        <h1 style="width: 100%; margin-top: 10px; text-align: center;">{{ $t("table.unlisted") }}</h1>
        <table>
            <tr>
                <td><h2>{{ $t("table.image") }}</h2></td>
                <td><h2>{{ $t("table.title") }}</h2></td>
                <td><h2>{{ $t("table.label") }}</h2></td>
                <td><h2>{{ $t("table.country") }}</h2></td>
                <td><h2>{{ $t("table.year") }}</h2></td>
                <td><h2>{{ $t("table.genre") }}</h2></td>
                <td v-if="typeRecord == 'CD'"><h2>{{ $t("table.barcode") }}</h2></td>
                <td><h2>{{ $t("table.condition") }}</h2></td>
                <td><h2>{{ $t("table.price") }}</h2></td>
                <td><h3>Allegro</h3></td>
            </tr>
            
            <tbody >
                <tr v-for="index in dataFailed.length" :key="index">
                    <td><img :src="dataFailed[index-1].images[0]" alt="preview image"  style="width: 150px; height: 150px;"></td>
                    <td>{{ dataFailed[index-1].title }}</td>
                    <td>{{ dataFailed[index-1].label }}</td>
                    <td>{{ dataFailed[index-1].country }}</td>
                    <td>{{ dataFailed[index-1].year }}</td>
                    <td>{{ dataFailed[index-1].genre }}</td>
                    <td v-if="typeRecord == 'CD'">{{ dataFailed[index-1].barcode }}</td>
                    <td>{{ dataFailed[index-1].condition }}</td>
                    <td>{{ dataFailed[index-1].price }}</td>
                    <td><button  class="btn btn-primary w-100 allegro" type="submit" style="padding: 0.5rem;" @click="listingOfferAllegro(dataFailed[index-1])">{{ $t("table.send") }}</button></td>
                </tr>
            </tbody>
        </table>

        <button class="btn btn-primary w-50" type="submit" style="padding: 0.5rem; font-size: 20px;"><a href="https://allegro.pl/offer/" style="color: white" target="_blank">{{ $t("table.allegroForm") }}</a></button>
        <button class="btn btn-primary w-50" type="submit" style="padding: 0.5rem; font-size: 20px;" @click="back">{{ $t("table.back") }}</button>
    </div>

    <div class="data" v-if="dataFailed.length == 0" style="justify-content: center;">
        <h1>{{ $t("listingView.allListed") }}</h1>
        <button class="btn btn-primary w-50" type="submit" style="padding: 0.5rem; font-size: 20px;" @click="back">{{ $t("table.back") }}</button>

    </div>

    <div id="loading" v-if="loading.flag">
        <img src="@/assets/spinner.gif" alt="loading">
        <h3>{{ loading.message }}</h3>
    </div>
    <TheAlert :alert="alert" />
</template>

<script>
    import axios from 'axios';
    import TheAlert from '@/components/Global/TheAlert.vue'

    export default {
        data(){
            return{
                loading: {"flag": false, "message": ""},
                alert: {},
            }
        },
        methods:{
            async back(){
                const userKey = this.$cookies.get('allegro-cred').userKey;
                await axios.post('http://127.0.0.1:8000/clear-image-data', {userKey: userKey}, {headers: {'Content-Type': 'application/json'}})
                window.location.reload()
            },
            async listingOfferAllegro(selectedData) {
                this.loading.flag = true
                const userKey = this.$cookies.get('allegro-cred').userKey;

                axios.post("http://127.0.0.1:8000/allegro-listing", {
                    userKey: userKey,
                    offer_data: selectedData,
                    carton: this.carton,
                    typeRecord: this.typeRecord,
                    typeOffer: this.typeOffer,
                    duration: this.duration,
                    clear: this.clear}, { 
                    headers: { 
                        "Content-Type": "application/json", 
                        "Access-Control-Allow-Origin": "*", 
                        } 
                    }).then((response) => {
                        response = response.data

                        if (response.error || response.output.errors) {
                            this.alert = { variant: "danger", message: `${this.$t("alerts.listingFailed")} - ${selectedData.title}` }
                        } else {
                            this.alert = { variant: "success", message: `${this.$t("alerts.listingSuccess")} - ${selectedData.title}` }
                        }
                    }).finally(()=>{
                        this.loading.flag = false
                    })
                
            },
            
        },
        props:{
            dataFailed:{
                type: Object,
                requried: true
            },
            typeRecord:{
                type: String,
                requried: true
            },
            carton:{
                type: String,
                requried: true
            },
            typeOffer:{
                type: String,
                requried: true
            }, 
            duration:{
                type: String,
                requried: true
            }, 
            clear:{
                type: Boolean,
                requried: true
            },
        },
        components:{
            TheAlert,
        }
    }
</script>

<style lang="scss" scoped>
    @media screen and (max-width: 1800px) {
    tr:nth-child(1){
        display: none;
    }

    tbody{
        tr{
            display: block !important;
        }
    }
}
</style>