<template>
    <span v-if="!allegroData" >
        <section class="form-container" v-if="!loading">
            <form>
                <div class="title">{{ $t("editMany.offerType") }}</div>
                <div class="input-container">
                    {{ $t("editMany.limit") }} (1-1000) <br> <input type="number" name="limit" min="1" v-model="limit">
                </div>
                <div class="input-container">
                    {{ $t("editMany.offset") }} <br> <input type="number" name="offset" min="0" v-model="offset">
                </div>
                <div class="input-container">
                    {{ $t("editMany.typeOffer") }}
                    <select v-model="typeOffer">
                        <option value="all">{{ $t("genre_options.all") }}</option>
                        <option value="BUY_NOW">{{ $t("editMany.buy") }}</option>
                        <option value="AUCTION">{{ $t("editMany.auction") }}</option>
                    </select>
                </div>
                <div class="input-container">
                    {{ $t("editMany.typeRecord") }}
                    <select v-model="typeRecord">
                        <option value="Vinyl">{{ $t("vinyl") }}</option>
                        <option value="CD">CD</option>
                    </select>
                </div>
                <div class="input-container">
                    {{ $t("table.genre") }}
                    <select v-model="genre">
                        <option value="all">{{ $t("genre_options.all") }}</option>
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
                </div>
                <span style="display:flex; justify-content: center; gap: 10px;">
                    <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem; font-size: 20px;" @click="getData('desc')">{{ $t("editMany.editDescription") }}</button>
                    <button class="btn btn-primary w-100" type="submit" style="padding: 0.5rem; font-size: 20px;" @click="getData('images')">{{ $t("editMany.editImages") }}</button>
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
                this.allegroData = await axios.post('http://127.0.0.1:8000/allegro-offers', {limit: this.limit, offset: this.offset, typeOffer: this.typeOffer, typeRecord: this.typeRecord, genre: this.genre})
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