<template>
    <TheHeader />
    <span>
        <div class="data">
            <table v-if="!loading && allegroStats">
                <tr>
                    <td>Name (Click to go to the offer)</td>
                    <td @click="sortVisitors" style="cursor: pointer;"><span class="arrow">Visitors &#8595</span></td>
                    <td @click="sortWatchers" style="cursor: pointer;"><span class="arrow">Watchers &#8595</span></td>
                </tr>
                <tr v-for="index in 60" :key="index" v-if="allegroStats[0]">
                    <td><a :href="getUrl(allegroStats[index-1]?.id, allegroStats[index-1]?.name)" target="_blank" style="background-color: none;">{{ allegroStats[index-1]?.name}}</a></td>
                    <td>{{ allegroStats[index-1]?.stats.visitsCount }}</td>
                    <td>{{ allegroStats[index-1]?.stats.watchersCount }}</td>
                </tr>
            </table>
        </div>
    </span>
    <div id="loading" v-if="loading">
        <img src="../assets/spinner.gif" alt="loading">
    </div>
    <TheAlert :alert="alert" />
</template>

<script>
    import TheHeader from '@/components/TheHeader.vue'
    import TheAlert from '../components/TheAlert.vue'
    import axios from 'axios'

    export default {
        data(){
            return{
                allegroStats: "",
                loading: false,
                alert: {}
            }
        },
        methods:{
            getUrl(id, name){
                let formattedName = name.replace(/[^a-zA-Z0-9\s.]/g, "")
                formattedName = formattedName.replace(/\s+/g, "-").toLowerCase()
                formattedName = `${formattedName}-${id}`
                return "https://allegro.pl/oferta/" + formattedName
            },
            sortVisitors(){
                this.allegroStats = this.allegroStats.sort((a, b) => b.stats.visitsCount - a.stats.visitsCount)
            },
            sortWatchers(){
                this.allegroStats = this.allegroStats.sort((a, b) => b.stats.watchersCount - a.stats.watchersCount)
            }
        },
        async beforeMount(){
            this.loading = true
            this.allegroStats = await axios.get('http://127.0.0.1:8000/allegro-stats')
            this.allegroStats = this.allegroStats.data
            if (this.allegroStats.error){
                this.alert = {variant: "danger", message: "Something went wrong"}
            }
            else{
                this.alert = {variant: "success", message: "Uploading statistics - success"}
            }
            
            setTimeout(()=>{this.alert = {}}, 2500)
            this.loading = false
        },
        components:{
            TheHeader,
            TheAlert
        }
    }
</script>

<style lang="scss" scoped>
    span{
        display: flex;
        justify-content: center;
        .data{
            width: 75%;
            a{
                background-color: inherit !important;
                color: white;
                &:hover{
                    opacity: 0.7;
                }
            }   
            .arrow:hover{
                color: #4CAF50;
            }
        }
    }
@media screen and (max-width: 500px) {
    span{
        display: block;
        .data{
            width: 500px;
        }
    }
}
</style>