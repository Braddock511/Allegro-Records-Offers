<template>
    <span v-if="!cartonFlag" id="carton"><h2>{{ $t("carton.enter_carton") }}</h2> <input type="text" name="carton" v-model="carton" style="width: 17%; padding: 7.5px;"> <button class="btn btn-primary w-30" type="button" @click="confirmCarton" style="width: 17%; padding: 0.5rem;  font-size: 20px;">{{ $t("carton.confirm") }}</button></span>
    <div class="data" v-if="img && cartonFlag && !waitFlag && !failedFlag">
        <TheSlider :images="img" ></TheSlider>
        <table v-if="imgFlag">
            <tr style="border: none;">
                <td colspan="8" style="border: none; text-align: center; background-color: #202833;">
                    <button class="btn btn-primary" type="submit" style="padding: 0.5rem; width: 50%; font-size: 20px;" @click="failed.data.push({id: '', title: '-', label: '-', country: '-', year: '-', genre: '-', price: '-', barcode: '-'}); failed.condition.push(this.condition); failed.img.push(this.img[0]); next()">{{ $t("table.next") }}</button>
                </td>
            </tr>
            <tr>
                <td><h2>{{ $t("table.title") }}</h2></td>
                <td><h2>{{ $t("table.label") }}</h2></td>
                <td><h2>{{ $t("table.country") }}</h2></td>
                <td><h2>{{ $t("table.year") }}</h2></td>
                <td><h2>{{ $t("table.genre") }}</h2></td>
                <td v-if="type == 'CD'"><h2>{{ $t("table.barcode") }}</h2></td>
                <td>
                    <h2>{{ $t("table.condition") }}</h2>
                    <select v-model="condition">
                        <option value="Near Mint (NM or M-)">{{ $t("table.mintMinus") }}</option>
                        <option value="Mint (M)">{{ $t("table.mint") }}</option>
                        <option value="Very Good Plus (VG+)">{{ $t("table.veryGoodPlus") }}</option>
                        <option value="Very Good (VG)">{{ $t("table.veryGood") }}</option>
                        <option value="Good (G)">{{ $t("table.good") }}</option>
                    </select>
                </td>
                <td><h2>{{ $t("table.listing_offer") }}</h2></td>
            </tr>
            <tr>
                <td>{{ $t("table.enter_title") }} <input type="text" name="title" class="custom" v-model="title"></td>
                <td>{{ $t("table.enter_label") }} <input type="text" name="label" class="custom" placeholder="-"  v-model="label"></td>
                <td>{{ $t("table.enter_country") }} <input type="text" name="country" class="custom" placeholder="-"  v-model="country"></td>
                <td>{{ $t("table.enter_year") }} <input type="text" name="year" class="custom" placeholder="-" v-model="year"></td>
                <td>                    
                    <select v-model="genre" style="width: 85%;">
                        <option value="ballad">{{ $t("genre_options.ballad") }}</option>
                        <option value="blues">{{ $t("genre_options.blues") }}</option>
                        <option value="country">{{ $t("genre_options.country") }}</option>
                        <option value="dance">{{ $t("genre_options.dance") }}</option>
                        <option value="disco">{{ $t("genre_options.disco") }}</option>
                        <option value="children's">{{ $t("genre_options.children") }}</option>
                        <option value="ethno">{{ $t("genre_options.ethno") }}</option>
                        <option value="jazz">{{ $t("genre_options.jazz") }}</option>
                        <option value="carols">{{ $t("genre_options.carols") }}</option>
                        <option value="metal">{{ $t("genre_options.metal") }}</option>
                        <option value="alternative">{{ $t("genre_options.alternative") }}</option>
                        <option value="electronic">{{ $t("genre_options.electronic") }}</option>
                        <option value="film">{{ $t("genre_options.film") }}</option>
                        <option value="classical">{{ $t("genre_options.classical") }}</option>
                        <option value="religious">{{ $t("genre_options.religious") }}</option>
                        <option value="new">{{ $t("genre_options.new") }}</option>
                        <option value="opera">{{ $t("genre_options.opera") }}</option>
                        <option value="pop">{{ $t("genre_options.pop") }}</option>
                        <option value="rap">{{ $t("genre_options.rap") }}</option>
                        <option value="reggae">{{ $t("genre_options.reggae") }}</option>
                        <option value="rock">{{ $t("genre_options.rock") }}</option>
                        <option value="rock'n'roll">{{ $t("genre_options.rock_and_roll") }}</option>
                        <option value="single">{{ $t("genre_options.single") }}</option>
                        <option value="compilations">{{ $t("genre_options.compilations") }}</option>
                        <option value="soul">{{ $t("genre_options.soul") }}</option>
                        <option value="synth-pop">{{ $t("genre_options.synth_pop") }}</option>
                        <option value="other">{{ $t("genre_options.other") }}</option>
                        <option value="sets">{{ $t("genre_options.sets") }}</option>
                    </select>
                </td>
                <td v-if="type == 'CD'">{{ $t("table.enter_barcode") }} <input type="text" name="barcode" class="custom" placeholder="-"  v-model="barcode"></td>
                <td>{{ $t("table.enter_price") }} <input type="number" name="price" class="custom" min="1" v-model="price"></td>
                <td><button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="listingOffer">{{ $t("table.send") }}</button></td>
            </tr>
            <tbody>
            <tr v-for="data in imageData.data[currentIndex].information.data">
                <td>{{ data.title }}</td>
                <td>{{ data.label }}</td>
                <td>{{ data.country }}</td>
                <td>{{ data.year }}</td>
                <td>{{ data.genre }}</td>
                <td v-if="type == 'CD'">{{ data.barcode }}</td>
                <td v-if="data.price[condition] !== undefined">
                    {{ roundedPrice(data.price[condition])}}
                </td>
                <td v-else>
                    <input type="number" name="price" class="custom" min="1" v-model="price">
                </td>
                <td><button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="listingOffer(data)">{{ $t("table.send") }}</button></td>
            </tr>
            </tbody>
        </table>
    </div>
    <div id="loading" v-if="loading">
        <img src="../assets/spinner.gif" alt="loading">
    </div>
    <TheAlert :alert="alert" />

    <TheFailed :dataFailed="failed" :type="type" v-if="failedFlag"/>
</template>
  
<script>
    import TheSlider from '@/components/TheSlider.vue'
    import TheAlert from '../components/TheAlert.vue'
    import TheFailed from './TheFailed.vue'
    import axios from 'axios'
    export default {
        data(){
            return{
                condition: "Near Mint (NM or M-)",
                carton: "",
                title: "",
                label: "",
                country: "",
                year: "",
                genre: "rock",
                barcode: "",
                price: "",
                currentIndex: 0,
                img: [],
                failed: {"data": [], "condition": [], "img": []},
                alert: {},
                cartonFlag: false,
                visible: false,
                imgFlag: false,
                waitFlag: false,
                failedFlag: false,
                loading: false
            }
        },
        methods:{
            async listingOffer(data) {
                let selectedData = {}
                // Get data
                if (data.title !== undefined){
                    selectedData = {
                        id: data.id,
                        title: data.title,
                        label: data.label,
                        country: data.country,
                        year: data.year,
                        genre: data.genre,
                        price: data.price[this.condition] !== undefined ? this.roundedPrice(data.price[this.condition]) : data.price,
                        barcode: data.barcode
                    }
                }
                else{
                    if (this.title !== "" && this.price !== ""){
                        if (this.title.length+3 < 50){
                            selectedData = {
                                id: "",
                                title: this.title,
                                label: this.label ? this.label : "-",
                                country: this.country ? this.country : "-",
                                year: this.year ? this.year : "-",
                                genre: this.genre,
                                price: this.price,
                                barcode: this.barcode ? this.barcode : "-"
                            }
                        }
                        else{
                            this.alert = {variant: "warning", message: this.$t("alerts.toLong")}
                        }
                    }
                    else{
                        this.alert = {variant: "warning", message: this.$t("alerts.complete")}
                    }
                }
                // Send data
                this.loading = true
                this.waitFlag = true
                const response = await axios.post('http://127.0.0.1:8000/allegro-listing', {data: selectedData, condition: this.condition, carton: this.carton, images: this.img, type: this.type, clear: this.clear}, { headers: { 'Content-Type': 'application/json' } })
                if (response.data.error || response.data.errors){
                    this.failed.data.push(selectedData)
                    this.failed.condition.push(this.condition)
                    this.failed.img.push(this.img[0])
                    this.alert = {variant: "danger", message: this.$t("alerts.listingFailed")}
                    // Next offer   
                    this.next()
                }
                else{
                    this.alert = {variant: "success", message: this.$t("alerts.listingSuccess")}
                    this.title = "",
                    this.label = "",
                    this.country = "",
                    this.year = "",
                    this.price = ""
                    // Next offer
                    this.next()
                }
            },
            next(){
                this.loading = true
                this.waitFlag = true
                this.currentIndex += this.numberImages
                if (this.currentIndex >= this.imageData.data.length) {
                    if(this.failed.img.length != 0){
                        this.failedFlag = true
                    }
                    else{
                        this.$router.push('/')
                    }
                    
                    this.imgFlag = false
                    this.loading = false
                }
                else{
                    this.img = []
                    let data
                    if (this.type == "CD"){
                        data = this.imageData.data.slice(this.currentIndex-1, this.currentIndex+this.numberImages-1)
                    }
                    else{
                        data = this.imageData.data.slice(this.currentIndex, this.currentIndex+this.numberImages)
                    }
                    for (let i = 0; i < data.length; i++) {
                        this.img.push(data[i].url)
                    }
                    this.img.reverse()
                    setTimeout(() => { this.imgFlag = true; this.loading = false; this.waitFlag = false }, 500)
                }
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
            },
            confirmCarton(){
                this.loading = true
                this.cartonFlag = true
                setTimeout(() => { this.imgFlag = true; this.loading = false }, 2500)
            },
            showImage() {
                this.show()
            },
            show() {
                this.visible = true
            },
            handleHide() {
                this.visible = false
            }
        },
        beforeMount() {
            this.loading =  true
            try{
                let data = this.imageData.data.slice(0, this.numberImages)
                for (let i = 0; i < data.length; i++) {
                    this.img.push(data[i].url)
                }
                if (this.type == "CD"){
                    this.currentIndex = 1
                }
                this.img.reverse()
            }
            catch{
                this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
            }
            this.loading =  false
        },
        props: {
            imageData: {
                required: true
            },
            type:{
                required: true
            },
            clear:{
                required: true
            },
            numberImages:{
                required: true
            }
        },
        components:{
            TheSlider,
            TheAlert,
            TheFailed
        }
    }
</script>
  
<style lang="scss" scoped>
    #carton{
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        gap: 10px;
        margin-top: 10px;
    }
</style>