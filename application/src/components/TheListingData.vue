<template>
    <span v-if="!cartonFlag" id="carton"><h2>Enter carton:</h2> <input type="text" name="carton" v-model="carton" style="width: 15%; padding: 7.5px;"> <button class="btn btn-primary w-30" type="button" @click="confirmCarton" style="width: 15%; padding: 0.5rem;">Confirm</button></span>
    <div class="data" v-if="img && cartonFlag && !waitFlag">
        <TheSlider :images="img" ></TheSlider>
        <table v-if="imgFlag">
            <tr style="border: none;">
                <td colspan="7" style="border: none; text-align: center;"><button class="btn btn-primary" type="submit" style="padding: 0.5rem; width: 50%;" @click="next">Next</button></td>
            </tr>
            <tr>
                <td><h2>Title</h2></td>
                <td><h2>Label</h2></td>
                <td><h2>Country</h2></td>
                <td><h2>Year</h2></td>
                <td><h2>Genre</h2></td>
                <td>
                    <h2>Condition:</h2>
                    <select v-model="condition">
                        <option value="Near Mint (NM or M-)">M- (Almost Perfect)</option>
                        <option value="Mint (M)">M (New)</option>
                        <option value="Very Good Plus (VG+)">VG+ (Excellent)</option>
                        <option value="Very Good (VG)">VG (Very Good)</option>
                        <option value="Good (G)">G (Good)</option>
                    </select>
                </td>
                <td><h2>Listing offer</h2></td>
            </tr>
            <tr>
                <td>Enter title: <input type="text" name="title" class="custom" v-model="title"></td>
                <td>Enter label: <input type="text" name="label" class="custom" placeholder="-"  v-model="label"></td>
                <td>Enter country: <input type="text" name="country" class="custom" placeholder="-"  v-model="country"></td>
                <td>Enter year: <input type="text" name="year" class="custom" placeholder="-" v-model="year"></td>
                <td>                    
                    <select v-model="genre" style="width: 85%;">
                        <option value="ballad">Ballada, Poezja śpiewana</option>
                        <option value="blues">Blues, Rhythm'n'Blues</option>
                        <option value="country">Country</option>
                        <option value="dance">Dance</option>
                        <option value="disco">Disco polo, biesiadna, karaoke</option>
                        <option value="kids">Dla dzieci</option>
                        <option value="ethno">Ethno, Folk, World music</option>
                        <option value="jazz">Jazz, Swing</option>
                        <option value="carols">Kolędy</option>
                        <option value="metal">Metal</option>
                        <option value="alternative">Muzyka alternatywna</option>
                        <option value="electronic">Muzyka elektroniczna</option>
                        <option value="film">Muzyka filmowa</option>
                        <option value="classical">Muzyka klasyczna</option>
                        <option value="religious">Muzyka religijna, oazowa</option>
                        <option value="new">Nowe brzmienia</option>
                        <option value="opera">Opera, Operetka</option>
                        <option value="pop">Pop</option>
                        <option value="rap">Rap, Hip-Hop</option>
                        <option value="reggae">Reggae, Ska</option>
                        <option value="rock">Rock</option>
                        <option value="rock'n'roll">Rock'n'roll</option>
                        <option value="single">Single</option>
                        <option value="compilations">Składanki</option>
                        <option value="soul">Soul, Funk</option>
                        <option value="synth-po">Synth-pop</option>
                        <option value="other">Pozostałe</option>
                        <option value="sets">Zestawy, pakiety</option>
                    </select>
                </td>
                <td>Enter price: <input type="number" name="price" class="custom" v-model="price"></td>
                <td><button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="listingOffer">Send</button></td>
            </tr>
            <tbody>
            <tr v-for="data in imageData.data[currentIndex].information.data">
                <td>{{ data.title }}</td>
                <td>{{ data.label }}</td>
                <td>{{ data.country }}</td>
                <td>{{ data.year }}</td>
                <td>{{ data.genre }}</td>
                <td v-if="Object.keys(data.price).length != 0 && data.price != ''">{{ roundedPrice(data.price[condition].value) }}</td>
                <td v-if="Object.keys(data.price).length == 0">Enter price: <input type="number" name="price" class="custom" v-model="price"></td>
                <td><button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="listingOffer(data)">Send</button></td>
            </tr>
            </tbody>
        </table>
    </div>
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
                condition: "Near Mint (NM or M-)",
                carton: "",
                title: "",
                label: "",
                country: "",
                year: "",
                genre: "rock",
                price: "",
                priceEnter: 'Enter price: <input type="number" name="price" class="custom" v-model="price">',
                currentIndex: 0,
                img: [],
                cartonFlag: false,
                visible: false,
                imgFlag: false,
                waitFlag: false,
                loading: false,
                alert: {}
            }
        },
        methods:{
            async listingOffer(data) {
                let selectedData = []
                let barcode = ""
                let input_data = this.imageData.data.slice(this.currentIndex-1, this.currentIndex+2)
                if (input_data.length > 0){
                    for (let i = 0; i<3; i++){
                        barcode += input_data[i].input_data
                    }
                }
                // Listing offer
                try{
                    selectedData = [{
                        id: data.id,
                        title: data.title,
                        label: data.label,
                        country: data.country,
                        year: data.year,
                        genre: data.genre,
                        price: Object.keys(data.price).length != 0 && data.price.hasOwnProperty(this.condition) ? this.roundedPrice(data.price[this.condition].value) : this.price,
                        barcode: barcode
                    }]
                }
                catch{
                    selectedData = [{
                        id: "",
                        title: this.title,
                        label: this.label ? this.label : "-",
                        country: this.country ? this.country : "-",
                        year: this.year ? this.year : "-",
                        genre: this.genre,
                        price: this.price,
                        barcode: barcode
                    }]
                }
                if (selectedData[0].title != "" && selectedData[0].price != ""){
                    this.loading = true
                    this.waitFlag = true
                    const response = await axios.post('http://127.0.0.1:8000/allegro-listing', {data: selectedData, condition: this.condition, carton: this.carton, images: [this.img[2], this.img[1], this.img[0]], type: this.type, clear: this.clear}, { headers: { 'Content-Type': 'application/json' } })
                    if (response.data.error || response.data.errors){
                        this.alert = {variant: "danger", message: "Listing offer failed"}
                    }
                    else{
                        this.alert = {variant: "success", message: "Listing offer success"}
                        this.title = "",
                        this.label = "",
                        this.country = "",
                        this.year = "",
                        this.price = ""
                        // New offer
                        this.next()
                    }
                }
                else{
                    this.alert = {variant: "warning", message: "Complete title and price"}
                }
            },

            next(){
                this.loading = true
                this.currentIndex += 3
                if (this.currentIndex >= this.imageData.data.length) {
                    this.$router.push('/')
                    this.cartonFlag = false
                    this.imgFlag = false
                    this.loading = false
                    return ""
                }
                else{
                    this.img = []
                    let data = this.imageData.data.slice(this.currentIndex, this.currentIndex+3)
                    for (let i = 0; i < data.length; i++) {
                        this.img.push(data[i].url)
                    }
                    setTimeout(() => { this.imgFlag = true; this.loading = false; this.waitFlag = false }, 2500)
                }
            },
            roundedPrice(price) {
                const roundedValue = Math.round((price * 3) / 10) * 10 - 0.01
                const finalValue = (roundedValue < 9.99) ? 9.99 : roundedValue 
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
                let data = this.imageData.data.slice(0, 3)
                for (let i = 0; i < data.length; i++) {
                    this.img.push(data[i].url)
                }
                if (this.type == "CD"){
                    this.currentIndex = 1
                }
            }
            catch{
                this.alert = {variant: "danger", message: "Something went wrong with getting data"}
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
            }
        },
        components:{
            TheSlider,
            TheAlert
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