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
                <tr v-for="index in 60" :key="index" v-if="allegroStats">
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
</template>

<script>
    import TheHeader from '@/components/TheHeader.vue'
    import axios from 'axios'

    export default {
        data(){
            return{
                allegroStats: "",
                loading: false,
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
            this.loading = false
        },
        components:{
            TheHeader
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