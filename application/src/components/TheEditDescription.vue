<template>
    <div id="data" v-if="offerData.data.offer.name.length > 0 && !loading">
        <TheSlider :images="img.slice().reverse()"></TheSlider>

        <table>
            <tr>
                <td><h2>Title</h2></td>
                <td><h2>Label</h2></td>
                <td><h2>Country</h2></td>
                <td><h2>Year</h2></td>
                <td><h2>Edit offer</h2></td>
            </tr>

            <tr v-for="data in offerData.data.discogs.data" v-if="offerData && offerData.data.discogs.data">
                <td>{{ offerData.data.offer.name  }}</td>
                <td>{{ data.label }}</td>
                <td>{{ data.country }}</td>
                <td>{{ data.year }}</td>
                <td><a @click="editOffer(data)">Edit</a></td>
            </tr>

            <tr>
                <td>{{ offerData.data.offer.name }}</td>
                <td>Enter label: <input type="text" name="label" class="custom" placeholder="-"  v-model="label"></td>
                <td>Enter country: <input type="text" name="country" class="custom" placeholder="-"  v-model="country"></td>
                <td>Enter year: <input type="text" name="year" class="custom" placeholder="-" v-model="year"></td>
                <td><a @click="editOffer">Edit</a></td>
            </tr>

            <tr>
                <td colspan="7"><a @click="next" style="width: 25%;">Next</a></td>
            </tr>
        </table>
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
                offerIndex: 0,
                offerData: "",
                img: "",
                label: "",
                country: "",
                year: "",
                loading: false,
            }
        },

        methods:{
            async editOffer(data){
                let selectedData = []
                // Edit offer
                selectedData = [{
                    id: data.id,
                    label: data.label,
                    country: data.country,
                    year: data.year,
                }]

                if (selectedData[0].id == undefined)
                    selectedData = [{
                        id: "",
                        label: this.label ? this.label : "-",
                        country: this.country ? this.country : "-",
                        year: this.year ? this.year : "-",
                }]

                this.loading = true
                try{
                    await axios.post("http://127.0.0.1:8000/edit-offer", {offerId: this.allegroData.data.offers[this.offerIndex].id, images: this.offerData.data.offer.images, data: selectedData})
                }

                catch{
                    alert("Upload failed")
                }

                // New offer
                this.next()
            },

            async next(){
                this.loading = true
                this.offerIndex += 1

                if (this.offerIndex == this.allegroData.data.offers.length){
                    this.$router.push("/")
                }
                
                try{
                    this.offerData = await axios.post('http://127.0.0.1:8000/discogs-information', {id: this.offerIndex, allegroData: this.allegroData.data, typeRecord: this.typeRecord})
                }
                catch{
                    alert("Upload failed")
                }
                
                this.label = "",
                this.country = "",
                this.year = "",
                this.img = this.offerData.data.offer.images
                setTimeout(() => { this.loading = false }, 3500)
            }
        },

        async beforeMount() {
            this.loading = true
            this.offerData = await axios.post('http://127.0.0.1:8000/discogs-information', {id: 0, allegroData: this.allegroData.data, typeRecord: this.typeRecord})
            this.img = this.offerData.data.offer.images
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
        padding: 10px;
        gap: 10px;

        table {
            border-collapse: collapse;
            color: white;
            text-align: center;
            margin-bottom: 50px;
            width: 100%;
            
            td {
                border: 1px solid #ddd;
                padding: 15px;
                font-size: 18px;

                .custom{
                    text-align: center;
                }
            }

            a {
                display: inline-block;
                width: 100%;
                padding: 5px 10px;
                border-radius: 4px;
                cursor: pointer;
                background-color: #4CAF50;
                transition: background-color 0.3s ease;

                &:hover{
                    background-color: #3e8e41;
                }
            }
        }

    }
</style>
