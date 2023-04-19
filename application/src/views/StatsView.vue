<template>
    <TheHeader />
    <nav v-if="!loading">
        <ul>
            <li @click="activeOption = 'visitors'">
                <h3>{{ $t('statistics.visitorsViewers') }}</h3>
            </li>
            <li @click="activeOption = 'sales'; getSaleBarplot()">
                <h3>{{ $t('statistics.sales') }}</h3>
            </li>
            <li @click="activeOption = 'genres'; getGenreBarplot()">
                <h3>{{ $t('statistics.genres') }}</h3>
            </li>
        </ul>
    </nav>
    <span v-if="!loading && activeOption == 'visitors'">
        <div class="data">
            <table v-if="visitors_viewers">
                <tr>
                    <td>{{ $t("statistics.name") }}</td>
                    <td @click="sortVisitors" style="cursor: pointer;"><span class="arrow">{{ $t("statistics.visitors") }}&#8595</span></td>
                    <td @click="sortWatchers" style="cursor: pointer;"><span class="arrow">{{ $t("statistics.watchers") }}&#8595</span></td>
                </tr>
                <tr v-for="index in 60" :key="index" v-if="visitors_viewers[0]">
                    <td><a :href="getUrl(visitors_viewers[index-1]?.id, visitors_viewers[index-1]?.name)" target="_blank" style="background-color: none;">{{ visitors_viewers[index-1]?.name}}</a></td>
                    <td>{{ visitors_viewers[index-1]?.stats.visitsCount }}</td>
                    <td>{{ visitors_viewers[index-1]?.stats.watchersCount }}</td>
                </tr>
            </table>
        </div>
    </span>
    <span v-if="!loading && activeOption == 'sales'" style="flex-direction: column; width: 100%;">
        <div class="data" style="width: 100%; flex-direction: row; justify-content: center; flex-wrap: wrap;">
            <img :src="saleBarplot" alt="bar plot">
        </div>
    </span>
    <span v-if="!loading && activeOption == 'genres'" style="flex-direction: column; width: 100%;">
        <div class="data" style="width: 100%; flex-direction: row; justify-content: center; flex-wrap: wrap;">
            <img :src="genreBarplot" alt="bar plot">
        </div>
    </span>
    <div id="loading" v-if="loading">
        <img src="../assets/spinner.gif" alt="loading">
        <h3>{{ $t('loading.loadData') }}</h3>
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
                visitors_viewers: "",
                saleBarplot: "",
                genreBarplot: "",
                activeOption: 'visitors',
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
                this.visitors_viewers = this.visitors_viewers.sort((a, b) => b.stats.visitsCount - a.stats.visitsCount)
            },
            sortWatchers(){
                this.visitors_viewers = this.visitors_viewers.sort((a, b) => b.stats.watchersCount - a.stats.watchersCount)
            },

            async getSaleBarplot(){
                if (this.saleBarplot == ""){
                    this.loading = true
                    const response = (await axios.get('http://127.0.0.1:8000/sale-barplot')).data
                    console.log(response)
                    if (response.error || response.errors)
                    {
                        this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
                    }
                    else{
                        this.saleBarplot = response.output
                        this.alert = {variant: "success", message: this.$t("alerts.statistics")}
                    }
                    this.loading = false
                }
            },

            async getGenreBarplot(){
                if (this.genreBarplot == ""){
                    this.loading = true
                    const response = (await axios.get('http://127.0.0.1:8000/genre-barplot')).data
                    console.log(response)
                    if (response.error || response.errors)
                    {
                        this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
                    }
                    else{
                        this.genreBarplot = response.output
                        this.alert = {variant: "success", message: this.$t("alerts.statistics")}
                    }
                    this.loading = false
                }
            }
        },
        async beforeMount(){
            this.loading = true
            const response = (await axios.get('http://127.0.0.1:8000/allegro-visitors-viewers')).data
            if (response.error || response.errors){
                this.alert = {variant: "danger", message: this.$t("alerts.someWrong")}
            }
            else{
                this.visitors_viewers = response.output
                this.alert = {variant: "success", message: this.$t("alerts.statistics")}
            }
            
            this.loading = false
        },
        components:{
            TheHeader,
            TheAlert
        }
    }
</script>

<style lang="scss" scoped>
    nav{
        display: flex;
        justify-content: center;
        background-color: rgba(33, 69, 78, 0.4588235294);
        margin-bottom: 10px;

        ul {
            list-style: none;
            margin: 0;
            padding: 0;
            display: flex;
            li {
                padding: 1rem;
                cursor: pointer;
                &:hover, &:active{
                    background-color: rgba(33, 69, 78);
                }
            }
        }
    }

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

        img{
            max-width: 100%;
            height: 750px;
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