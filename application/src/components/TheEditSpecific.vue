<template>
    <span>
        <section class="form-container" v-if="!offerData && !loading">
            <form>
                <div class="title">Enter offer id</div>
                <div class="input-container">
                    <input type="text" name="offer-id" v-model="offerId" required>
                </div>        
                <button type="submit" class="blue-button" @click="getOffer">Get offer</button>
            </form>
        </section>
    </span>
    <div class="data" v-if="offerData && !loading">
        <TheSlider :images="img.slice().reverse()"></TheSlider>
        <table>
            <tr>
                <td colspan="5"  style="border: none;">
                    <span style="display: flex; flex-direction: column; align-items: center; gap: 10px;">    
                        <a @click="editImage" style="width: 50%;">Clear image</a>
                        <a @click="offerData = ''" style="width: 50%;">Back</a>
                    </span>
                </td>
            </tr>
            <tr>
            </tr>
            <tr>
                <td><h2>Title</h2></td>
                <td><h2>Label</h2></td>
                <td><h2>Country</h2></td>
                <td><h2>Year</h2></td>
                <td><h2>Edit offer</h2></td>
            </tr>
            <tr>
                <td>{{ offerData.data.offer.name }}</td>
                <td>Enter label: <input type="text" name="label" class="custom" placeholder="-"  v-model="label"></td>
                <td>Enter country: <input type="text" name="country" class="custom" placeholder="-"  v-model="country"></td>
                <td>Enter year: <input type="text" name="year" class="custom" placeholder="-" v-model="year"></td>
                <td><a @click="editOffer">Edit</a></td>
            </tr>
            <tr v-for="data in offerData.data.discogs.data" v-if="offerData && offerData.data.discogs.data">
                <td>{{ offerData.data.offer.name  }}</td>
                <td>{{ data.label }}</td>
                <td>{{ data.country }}</td>
                <td>{{ data.year }}</td>
                <td><a @click="editOffer(data)">Edit</a></td>
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
                allegroData: "",
                offerData: "",
                offerId: "",
                img: "",
                label: "",
                country: "",
                year: "",
                loading: false,
            }
        },
        methods:{
            async getOffer() {
                this.loading = true
                try 
                {
                    this.allegroData = await axios.post('http://127.0.0.1:8000/allegro-offer', {offerId: this.offerId})
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
                catch (error) 
                {
                    alert('Upload failed.')
                }
                
                this.loading = false
            },
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
                    await axios.post("http://127.0.0.1:8000/allegro-edit-offer", {offerId: this.offerId, images: this.img, data: selectedData})
                }
                catch{
                    alert("Upload failed")
                }
                this.loading = false
            },
            async editImage(){
                try{
                    this.loading = true
                    this.clearImage = await axios.post('http://127.0.0.1:8000/clear-image', {image: this.img[0]})
                    let otherImages = this.img.slice(1, this.img.length)
                    let newImages = ([this.clearImage.data, otherImages]).flat()
                    await axios.post('http://127.0.0.1:8000/allegro-edit-image', {offerID: this.offerId, images: newImages})
                    this.loading = false
                }
                catch{
                    alert("Upload failed")
                }
            }
        },
        components:{
            TheSlider
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