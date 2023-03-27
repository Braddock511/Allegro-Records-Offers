<template>
    <span v-if="!allegroData" >
        <section class="form-container" v-if="!loading">
            <form>
                <div class="title">Offer Types</div>
                <div class="input-container">
                    Limit (1-1000) <br> <input type="number" name="limit" v-model="limit">
                </div>
                <div class="input-container">
                    Offset <br> <input type="number" name="offset" v-model="offset">
                </div>
                <div class="input-container">
                    Type of offer
                    <select v-model="typeOffer">
                        <option value="all">All</option>
                        <option value="BUY_NOW">Buy now</option>
                        <option value="AUCTION">Auction</option>
                    </select>
                </div>
                <div class="input-container">
                    Type of record
                    <select v-model="typeRecord">
                        <option value="Vinyl">Vinyl</option>
                        <option value="CD">Cd</option>
                    </select>
                </div>
                <div class="input-container">
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
                    <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="getData('desc')">Edit description</button>
                    <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem;" @click="getData('images')">Edit images</button>
                </span>
            </form>
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
                typeRecord: "Vinyl",
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
            TheEditDescription,
            TheEditImages,
        }
    }
</script>

<style lang="scss" scoped>
@media screen and (max-width: 1000px) {
    tr {
      &:nth-child(1){
        display: none;
      }
    }
}
</style>