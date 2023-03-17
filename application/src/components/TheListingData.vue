<template>
    <span v-if="!cartoonFlag" id="cartoon"><h1>Enter cartoon:</h1> <input type="text" name="cartoon" v-model="cartoon" style="width: 15%; padding: 7.5px;"> <button class="blue-button" @click="confirmCartoon" style="width: 15%;">Confirm</button></span>
    <div id="data" v-if="img && !loading && cartoonFlag">
        <TheSlider :images="img"></TheSlider>

        <table>
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

            <tbody  v-if="imageData.data[currentIndex].information.data.length > 0">
            <tr v-for="data in imageData.data[currentIndex].information.data">
                <td>{{ data.title }}</td>
                <td>{{ data.label }}</td>
                <td>{{ data.country }}</td>
                <td>{{ data.year }}</td>
                <td>{{ data.genre }}</td>
                <td v-if="Object.keys(data.price).length != 0">{{ roundedPrice(data.price[condition].value)}}</td>
                <td v-if="Object.keys(data.price).length == 0">Enter price: <input type="number" name="price" class="custom" v-model="price"></td>
                <td><a @click="listingOffer(data)">Send</a></td>
            </tr>
            </tbody>

            <tr>
                <td>Enter title: <br><input type="text" name="title" class="custom" v-model="title"></td>
                <td>Enter label: <input type="text" name="label" class="custom" placeholder="-"  v-model="label"></td>
                <td>Enter country: <input type="text" name="country" class="custom" placeholder="-"  v-model="country"></td>
                <td>Enter year: <input type="text" name="year" class="custom" placeholder="-" v-model="year"></td>
                <td>-</td>
                <td>Enter price: <input type="number" name="price" class="custom" v-model="price"></td>
                <td><a @click="listingOffer">Send</a></td>
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
                condition: "Near Mint (NM or M-)",
                cartoon: "",
                cartoonFlag: false,
                currentIndex: 0,
                visible: false,
                loading: false,
                img: [],
                title: "",
                label: "",
                country: "",
                year: "",
                price: "",
                priceEnter: 'Enter price: <input type="number" name="price" class="custom" v-model="price">'
            }
        },

        methods:{
            async listingOffer(data) {
                let selectedData = []
                // Listing offer
                try{
                    selectedData = [{
                        id: data.id,
                        title: data.title,
                        label: data.label,
                        country: data.country,
                        year: data.year,
                        genre: data.genre,
                        price: Object.keys(data.price).length != 0 && data.price.hasOwnProperty(this.condition) ? this.roundedPrice(data.price[this.condition].value) : this.price
                    }]
                }
                catch{
                    selectedData = [{
                        id: "",
                        title: this.title,
                        label: this.label ? this.label : "-",
                        country: this.country ? this.country : "-",
                        year: this.year ? this.year : "-",
                        genre: "",
                        price: this.price
                    }]
                }
                

                if (selectedData[0].title != "" && selectedData[0].price != ""){
                    this.loading = true

                    await axios.post('http://127.0.0.1:8000/allegro-listing', {data: selectedData, condition: this.condition, cartoon: this.cartoon, images: [this.img[2], this.img[1], this.img[0]]}, { headers: { 'Content-Type': 'application/json' } })

                    this.title = "",
                    this.label = "",
                    this.country = "",
                    this.year = "",
                    this.price = ""

                    // Change images

                    this.currentIndex += 3

                    if (this.currentIndex == this.imageData.data.length) {
                        this.loading = true
                        setTimeout(() => {this.$router.push('/')}, 1000)
                        this.loading = false
                        return ""
                    }

                    else{
                        this.img = []
                        let data = this.imageData.data.slice(this.currentIndex, this.currentIndex+3)
                        for (let i = 0; i < data.length; i++) {
                            this.img.push(data[i].url)
                        }
                        setTimeout(() => { this.loading = false }, 3500)
                        this.loading = false
                    }
                }
                else{
                    alert("Complete title and price")
                }
            },

            roundedPrice(price) {
                const roundedValue = Math.round((price * 3) / 10) * 10 - 0.01
                const finalValue = (roundedValue < 9.99) ? 9.99 : roundedValue 
                return finalValue
            },

            confirmCartoon(){
                this.loading = true
                this.cartoonFlag = true
                setTimeout(() => { this.loading = false }, 1500)
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
            let data = this.imageData.data.slice(0, 3)
            for (let i = 0; i < data.length; i++) {
                this.img.push(data[i].url)
            }
            this.loading =  false
        },

        props: [
            'imageData'
        ],

        components:{
            TheSlider
        }
    }
</script>
  
<style lang="scss" scoped>
    #cartoon{
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        gap: 10px;
        margin-top: 10px;
    }

    #data{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 10px;
        gap: 10px;

        #imgs{
            display: flex;
            gap: 10px;

            img{
                width: 33%;
                height: 33%;
            }
            
            #vinyl-image{
                cursor: pointer;

                &:hover{
                    opacity: 0.9;
                }
            }
            
        }
            
        table {
            border-collapse: collapse;
            color: white;
            font-family: Arial, sans-serif;
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
                text-decoration: none;
                cursor: pointer;
                background-color: #4CAF50;
                transition: background-color 0.3s ease;

                &:hover{
                    background-color: #3e8e41;
                }
            }
        }

    }

    @media only screen and (max-width: 1100px){
        .image-data {
            table{
                margin: 0px 10px 0px 10px;
            }
        }
    }

    @media only screen and (max-width: 800px){
        .image-data {
            table{
                td{
                    font-size: 14px;
                }

                h2{
                    font-size: 16px;
                }
            }
        }
    }

    @media only screen and (max-width: 600px){
        .image-data {
            margin-top: 20px;
        }
    }

    @media only screen and (max-width: 600px){
        .image-data {
            table{
                td{
                    font-size: 10px;
                }

                h2{
                    font-size: 12px;
                }
            }
        }
    }
 
</style>
  