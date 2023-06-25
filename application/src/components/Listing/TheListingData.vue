<template>
    <span v-if="!cartonFlag && !loading.flag" id="carton">
        <h1>{{ $t("carton.enter_carton") }}</h1> 
        <input type="text" name="carton" v-model="carton" style="padding: 5px;"> 
        <button class="btn btn-primary" type="button" @click="confirmCarton" style="width: 300px; padding: 0.5rem; font-size: 20px;">{{ $t("carton.confirm") }}</button>
    </span>
    <div class="data" v-if="cartonFlag && !failedFlag && !loading.flag">
        <TheSlider :images="offerImages"></TheSlider>
        <h3>{{ $t("table.condition") }} {{ conditions[currentIndex/numberImages] }}</h3>
        <div style="width: 100%; text-align: center;">
            <button class="btn btn-primary" type="submit" style="padding: 0.5rem; width: 50%; font-size: 20px;" 
                @click="activeRequests+=1; failed.push({id: '', title: '-', label: '-', country: '-', year: '-', genre: '-', price: '-', barcode: '-', condition: this.condition, images: this.offerImages}); next()">
                {{ $t("table.next") }}
            </button>
        </div>
        <table>
            <tr style="background-color: rgb(34, 36, 35); border-bottom: 0px;">
                <td><h3>{{ $t("table.title") }}</h3></td>
                <td><h3>{{ $t("table.label") }}</h3></td>
                <td><h3>{{ $t("table.country") }}</h3></td>
                <td><h3>{{ $t("table.year") }}</h3></td>
                <td><h3>{{ $t("table.genre") }}</h3></td>
                <td v-if="typeRecord == 'CD'"><h3>{{ $t("table.barcode") }}</h3></td>
                <td>
                    <h3>{{ $t("table.condition") }}</h3>
                    <select v-model="condition">
                        <option value="Near Mint (NM or M-)">{{ $t("table.mintMinus") }}</option>
                        <option value="Mint (M)">{{ $t("table.mint") }}</option>
                        <option value="Excellent (EX)">{{ $t("table.ex") }}</option>
                        <option value="Very Good Plus (VG+)">{{ $t("table.veryGoodPlus") }}</option>
                        <option value="Very Good (VG)">{{ $t("table.veryGood") }}</option>
                        <option value="Good (G)">{{ $t("table.good") }}</option>
                        <option value="Fair (F)">{{ $t("table.fair") }}</option>
                    </select>
                </td>
                <td><h3>Allegro</h3></td>
                <td><h3>Discogs</h3></td>
            </tr>
            <tr>
                <td><span class="enter">{{ $t("table.enter_title") }}</span> <input type="text" name="title" class="custom" v-model="title"></td>
                <td><span class="enter">{{ $t("table.enter_label") }}</span> <input type="text" name="label" class="custom" placeholder="-"  v-model="label"></td>
                <td><span class="enter">{{ $t("table.enter_country") }}</span> <input type="text" name="country" class="custom" placeholder="-"  v-model="country"></td>
                <td><span class="enter">{{ $t("table.enter_year") }}</span> <input type="text" name="year" class="custom" placeholder="-" v-model="year"></td>
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
                        <option value="hip hop">{{ $t("genre_options.rap") }}</option>
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
                <td v-if="typeRecord == 'CD'">{{ $t("table.enter_barcode") }} <input type="text" name="barcode" class="custom" placeholder="-"  v-model="barcode"></td>
                <td>{{ $t("table.enter_price") }} <input type="number" name="price" class="custom" min="1" v-model="price"></td>
                <td class="media-condition" style="display: none">
                    {{ $t("table.condition") }}
                    <select v-model="condition">
                        <option value="Near Mint (NM or M-)">{{ $t("table.mintMinus") }}</option>
                        <option value="Mint (M)">{{ $t("table.mint") }}</option>
                        <option value="Excellent (EX)">{{ $t("table.ex") }}</option>
                        <option value="Very Good Plus (VG+)">{{ $t("table.veryGoodPlus") }}</option>
                        <option value="Very Good (VG)">{{ $t("table.veryGood") }}</option>
                        <option value="Good (G)">{{ $t("table.good") }}</option>
                        <option value="Fair (F)">{{ $t("table.fair") }}</option>
                    </select>
                </td>
                <td><button class="btn btn-primary w-100 allegro" type="submit" style="padding: 0.5rem;" @click="listingOfferAllegro">{{ $t("table.send") }}</button></td>
                <td>
                    {{ $t("table.sleeveCondition") }}
                    <select v-model="sleeveCondition" style="width: 100%;">
                        <option value="Near Mint (NM or M-)">{{ $t("table.mintMinus") }}</option>
                        <option value="Mint (M)">{{ $t("table.mint") }}</option>
                        <option value="Excellent (EX)">{{ $t("table.ex") }}</option>
                        <option value="Very Good Plus (VG+)">{{ $t("table.veryGoodPlus") }}</option>
                        <option value="Very Good (VG)">{{ $t("table.veryGood") }}</option>
                        <option value="Good (G)">{{ $t("table.good") }}</option>
                        <option value="Fair (F)">{{ $t("table.fair") }}</option>
                    </select>
                </td>
            </tr>
            <tbody>
            <tr v-for="data in discogsData[recordIndex].information">
                <td><a :href="data.uri" style="background-color: #203640; " target="_blank">{{ data.title }}</a></td>
                <td>{{ data.label }}</td>
                <td>{{ data.country }}</td>
                <td>{{ data.year }}</td>
                <td>{{ data.genre }}</td>
                <td v-if="typeRecord == 'CD'">{{ data.barcode }}</td>
                <td class="media-condition" style="display: none">
                    {{ $t("table.condition") }}
                    <select v-model="condition">
                        <option value="Near Mint (NM or M-)">{{ $t("table.mintMinus") }}</option>
                        <option value="Mint (M)">{{ $t("table.mint") }}</option>
                        <option value="Excellent (EX)">{{ $t("table.ex") }}</option>
                        <option value="Very Good Plus (VG+)">{{ $t("table.veryGoodPlus") }}</option>
                        <option value="Very Good (VG)">{{ $t("table.veryGood") }}</option>
                        <option value="Good (G)">{{ $t("table.good") }}</option>
                        <option value="Fair (F)">{{ $t("table.fair") }}</option>
                    </select>
                </td>
                <td v-if="data.price[condition == 'Excellent (EX)' ? 'Very Good Plus (VG+)' : condition] !== undefined">
                    Want: {{ data.community.want }} | Have: {{ data.community.have }}<br>
                    <input type="number" name="price" class="custom" min="1" :placeholder="roundedPriceToPLN(data.price[condition == 'Excellent (EX)' ? 'Very Good Plus (VG+)' : condition])" v-model="price" @click="price = roundedPriceToPLN(data.price[condition == 'Excellent (EX)' ? 'Very Good Plus (VG+)' : condition])">
                </td>
                <td v-else>
                    Want: ? | Have: ?<br><br>
                    <input type="number" name="price" class="custom" min="1" v-model="price">
                </td>
                <td><button  class="btn btn-primary w-100 allegro" type="submit" style="padding: 0.5rem;" @click="listingOfferAllegro(data)">{{ $t("table.send") }}</button></td>
                <td><button  class="btn btn-primary w-100 discogs" type="submit" style="padding: 0.5rem;" @click="listingOfferDiscogs(data)">{{ $t("table.send") }}</button></td>
            </tr>
            </tbody>
        </table>
    </div>
    <div id="loading" v-if="loading.flag">
        <img src="@/assets/spinner.gif" alt="loading">
        <h3>{{ loading.message }}</h3>
    </div>
    <TheAlert :alert="alert" />

    <TheFailed :dataFailed="failed" :typeRecord="typeRecord" :carton="carton" :typeOffer=" this.typeOffer" :duration=" this.duration" :clear=" this.clear" v-if="failedFlag"/>
</template>
  
<script>
    import TheSlider from '@/components/Global/TheSlider.vue'
    import TheAlert from '@/components/Global/TheAlert.vue'
    import TheFailed from '@/components/Listing/TheFailed.vue'
    import axios from 'axios'
    export default {
        data(){
            return{
                condition: "Near Mint (NM or M-)", 
                sleeveCondition: "Near Mint (NM or M-)",
                carton: "", 
                title: "",
                label: "",
                country: "",
                year: "",
                genre: "rock",
                barcode: "",
                price: "",
                currentIndex: 0,
                recordIndex: this.typeRecord == "Vinyl" ? 0 : 1, 
                offerImages: [],
                failed: [],
                alert: {},
                cartonFlag: false,
                visible: false,
                failedFlag: false,
                loading: {"flag": false, "message": ""},
                activeRequests: 0
            }
        },
        methods:{
            resetVariables() {
                this.title = ""
                this.label = ""
                this.country = ""
                this.year = ""
                this.price = ""
                this.barcode = ""
                this.condition = "Near Mint (NM or M-)"
            },
            async listingOfferDiscogs(data) {
                if (this.price === "") {
                    this.alert = { variant: "warning", message: this.$t("alerts.complete") }
                    return
                }

                let selectedData = {
                    id: data.id,
                    condition: this.condition,
                    price: this.price,
                }

                // Send data
                this.loading.flag = true
                this.loading.message = this.$t("loading.listingOffer")

                await axios.post("http://127.0.0.1:8000/discogs-listing",{
                        listing_id: data.id,
                        mediaCondition: this.condition,
                        carton: this.carton,
                        sleeveCondition: this.sleeveCondition,
                        price: this.roundedPriceToEUR(this.price),
                    }, { headers: { "Content-Type": "application/json" } }).then((response) => {
                        response = response.data

                        if (response.error || response.output.errors) {
                            this.failed.push(selectedData)
                            this.alert = { variant: "danger", message: this.$t("alerts.listingFailed") }
                        } else {
                            this.alert = { variant: "success", message: this.$t("alerts.listingSuccess") }
                        }
                    }).finally(() => {
                        this.activeRequests += 1
                        
                    })

                this.resetVariables(); 
                await this.next();
            },
            async listingOfferAllegro(data) {
                let selectedData = {}

                if (this.price === "") {
                    this.alert = { variant: "warning", message: this.$t("alerts.complete") }
                    return
                }

                if (data.title !== undefined) {
                    selectedData = {
                        id: data.id,
                        title: data.title,
                        label: data.label,
                        country: data.country,
                        year: data.year,
                        genre: data.genre,
                        price: this.price,
                        barcode: data.barcode,
                        quantity: data.quantity,
                        images: this.offerImages,
                        condition: this.condition 
                    }
                } else {
                    if (this.title === "" || this.price === "") {
                        this.alert = { variant: "warning", message: this.$t("alerts.complete") }
                        return
                    }

                    if (this.title.length + 3 >= 50) {
                        this.alert = { variant: "warning", message: this.$t("alerts.toLong") }
                        return
                    }

                    selectedData = {
                        id: "",
                        title: this.title,
                        label: this.label ? this.label : "-",
                        country: this.country ? this.country : "-",
                        year: this.year ? this.year : "-",
                        genre: this.genre,
                        price: this.price,
                        barcode: this.barcode ? this.barcode : "-",
                        quantity: "",
                        images: this.offerImages,
                        condition: this.condition
                    }
                }

                // Send data 
                this.loading.flag = true
                this.next()
                
                axios.post("http://127.0.0.1:8000/allegro-listing", {
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
                        console.log(response)

                        if (response.error || response.output.errors) {
                            this.failed.push(selectedData)
                            this.alert = { variant: "danger", message: `${this.$t("alerts.listingFailed")} - ${selectedData.title}` }
                        } else {
                            this.alert = { variant: "success", message: `${this.$t("alerts.listingSuccess")} - ${selectedData.title}` }
                        }
                    }).finally(()=>{
                        this.activeRequests += 1
                        
                        // Last offer
                        if (this.activeRequests == (this.numberFiles / this.numberImages))
                        {
                            this.next()
                        }
                    })
                
                this.resetVariables()
            },
            async next(){
                this.loading.flag = true
                this.loading.message = this.$t("loading.loadData")
                this.currentIndex += this.numberImages

                if (this.currentIndex >= this.numberFiles) {
                    this.loading.message = ""
                    if (this.activeRequests == (this.numberFiles / this.numberImages))
                    {
                        this.loading.flag = false
                        this.failedFlag = true
                    }
                }
                else{
                    this.offerImages = []
                    axios.post("http://127.0.0.1:8000/discogs-information-image", {typeRecord: this.typeRecord, index: this.currentIndex, numberImages: this.numberImages,}, { headers: { "Content-Type": "application/json" } }).then((response) =>{
                        this.discogsData = response.data.output
                        
                        for (let i = 0; i < this.numberImages; i++) {
                            this.offerImages.push(this.discogsData[i].url)
                        }
                        
                        this.offerImages.reverse()
                        this.loading.message = "" 
                        this.loading.flag = false
                    })
                }
            },
            roundedPriceToPLN(price) {
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
            roundedPriceToEUR(price) {
                let finalValue
                if (price){
                    const roundedValue = Math.round((price * 0.3) / 10) * 10 - 0.01
                    finalValue = (roundedValue < 3.99) ? 3.99 : roundedValue 
                }
                else{
                    finalValue = 0
                }
                return finalValue
            },
            confirmCarton(){
                this.cartonFlag = true
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
        async beforeMount() {
            this.loading.flag =  true
            this.loading.message = this.$t("loading.loadData") 
            this.discogsData = (await axios.post('http://127.0.0.1:8000/discogs-information-image', {typeRecord: this.typeRecord, index: 0, numberImages: this.numberImages}, {headers: {'Content-Type': 'application/json'}})).data.output

            try{
                for (let i = 0; i < this.numberImages; i++) {
                    this.offerImages.push(this.discogsData[i].url)
                }
                this.offerImages.reverse()
            }
            catch{
                this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
            }
            this.loading.message = ""
            this.loading.flag =  false
        },
        props: {
            typeRecord:{
                type: String,
                required: true
            },
            typeOffer:{
                type: String,
                required: true
            },
            duration:{
                type: String,
                required: true
            },
            clear:{
                type: Boolean,
                required: true
            },
            numberImages:{
                type: Number,
                required: true,
                integer: true
            },
            numberFiles:{
                type: Number,
                required: true,
                integer: true
            },
            conditions:{
                type: Array,
                required: false
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
        align-items: center;
        flex-direction: column;
        justify-content: center;
        gap: 10px;
        font-size: 24px;
        margin-top: 50px;
    }
    .enter{
        display: none;
    }
    @media screen and (max-width: 1750px) {
        .media-condition{
            display: block !important;
          }

        .enter{
            display: contents;
        }
    }
</style>
