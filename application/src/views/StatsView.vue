<template>
    <TheHeader />
    <h1 @click="flagToogle" style="width: 100%; text-align: center; cursor: pointer; ;opacity: 0.8 hover;">{{ $t('statistics.header') }}</h1>
    <span v-if="!loading && flag">
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
    <span v-if="!loading && !flag" style="flex-direction: column; width: 100%;">
        <div class="data" style="width: 100%; flex-direction: row; justify-content: center; flex-wrap: wrap;">
            <img :src="barPlot" alt="bar plot">
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
                visitors_viewers: "",
                barPlot: "",
                flag: true,
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
            flagToogle(){
                this.flag = !this.flag
            }
        },
        async beforeMount(){
            this.loading = true
            this.visitors_viewers = await axios.get('http://127.0.0.1:8000/allegro-visitors-viewers')
            this.visitors_viewers = this.visitors_viewers.data
            
            const plots = await axios.get('http://127.0.0.1:8000/plots')
            if (this.visitors_viewers.error || plots.data.error)
            {
                this.alert = {variant: "danger", message: this.$t("alerts.complete")}
            }
            else{
                this.barPlot = plots.data.bar_plot
                this.alert = {variant: "success", message: this.$t("alerts.statistics")}
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
    h1:hover{
        opacity: 0.7;
    };
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