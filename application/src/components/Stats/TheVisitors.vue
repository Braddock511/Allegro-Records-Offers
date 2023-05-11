<template>
    <span v-if="!loading">
        <div class="data">
            <table v-if="visitors_viewers">
                <tr style="background-color: rgb(34, 36, 35);">
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
    <div id="loading" v-if="loading">
        <img src="@/assets/spinner.gif" alt="loading">
    </div>
    <TheAlert :alert="alert" />
</template>

<script>
    import TheAlert from '@/components/Global/TheAlert.vue'
    import axios from 'axios'

    export default {
        data(){
            return{
                visitors_viewers: "",
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
            TheAlert
        }
    }
</script>

<style lang="scss" scoped>
.data{
    width: 80vw;

    table{
        tr{
            td{
                a{
                    background-color: #203640;
                }

                .arrow:hover{
                    color: green;
                }
            }
        }
    }
}

@media screen and (max-width: 1650px) {
    table {
        tr {
        &:nth-child(1){
            display: block;
        }

        td {
            display: block;
            font-size: 18px;
            text-align: left;

            &:nth-child(1)::before{
                content: "";
            }
            &:nth-child(2)::before{
                content: "";
            }
            &:nth-child(3)::before{
                content: "";
            }
            &:nth-child(4)::before{
                content: "";
            }
            }
        }
    }
}
</style>