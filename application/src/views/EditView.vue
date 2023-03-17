<template>
    <TheHeader />
    <span v-if="!allegroData">
        <section id="form-container" v-if="!loading">
            <div id="form">
                <div class="title">Offer Types</div>

                <div class="input-container">
                    Limit (1-1000) <input type="number" name="limit" v-model="limit">
                    Offset <input type="number" name="offset" v-model="offset">

                    Type of offer
                    <select v-model="typeOffer">
                        <option value="all">All</option>
                        <option value="BUY_NOW">Buy now</option>
                        <option value="AUCTION">Auction</option>
                    </select>

                    Type of record
                    <select v-model="typeRecord">
                        <option value="vinyl">Vinyl</option>
                        <option value="cd">Cd</option>
                    </select>

                    Genre
                    <select v-model="genre">
                        <option value="all">All</option>
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

                </div>
                
                <span style="display:flex; justify-content: center; gap: 10px;">
                    <button type="submit" class="blue-button" @click="getData('desc')">Edit description</button>
                    <button type="submit" class="blue-button" @click="getData('images')">Edit images</button>
                </span>
            </div>
        </section>

        <div id="loading" v-if="loading">
            <img src="../assets/spinner.gif" alt="loading">
        </div>
    </span>

    <TheEditDescription v-if="allegroData && typeEdit=='desc'" :allegroData="allegroData" :typeRecord="typeRecord"/>
    <TheEditImages v-if="allegroData && typeEdit=='images'" :allegroData="allegroData" :typeRecord="typeRecord"/>
    
</template>

<script>
    import TheEditDescription from '@/components/TheEditDescription.vue'
    import TheEditImages from '@/components/TheEditImages.vue'
    import TheHeader from '@/components/TheHeader.vue'
    import axios from 'axios'

    export default {
        data(){
            return{
                allegroData: "",
                discogsData: "",
                typeEdit: "",
                limit: 1,
                offset: 0,
                typeOffer: "all",
                typeRecord: "vinyl",
                genre: "all",
                loading: false,
            }
        },

        methods:{
            async getData(edit) {
                this.loading = true
                try 
                {
                    this.allegroData = await axios.post('http://127.0.0.1:8000/allegro-offers', {limit: this.limit, offset: this.offset, typeOffer: this.typeOffer, typeRecord: this.typeRecord, genre: this.genre})
                } 
                catch (error) 
                {
                    alert('Upload failed.')
                }
                
                this.typeEdit = edit
                this.loading = false
            },
        },


        components:{
            TheHeader,
            TheEditDescription,
            TheEditImages,
        }
    }
</script>

<style lang="scss" scoped>
    #form-container {
        display: flex;
        justify-content: center;

        #form {
            display: flex;
            flex-direction: column;
            margin-top: 50px;
            border-radius: 25px;
            padding: 20px;
            background-color: rgb(34, 36, 36);
            width: 50%;
            gap: 20px;

            .title {
                font-size: 36px;
                font-weight: 600;
                margin-top: 15px;
            }

            .input-container {
                display: flex;
                flex-direction: column;
                gap: 20px;

                select{
                    align-self: normal;
                }

                input{
                    padding: 5px;
                }
            }
        }

        p{
            a{
                opacity: 0.8;
            }

            a:hover{
                opacity: 1;
            }
        }
    }

    #loading{
        width: 100%;
        height: 500px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    @media only screen and (max-width: 1300px) {
        #form-container{
            #form{
                width: 80%;
            }
        }
    }

    @media only screen and (max-width: 500px) {
        #form-container{
            width: 500px;
        }
    }

    
</style>