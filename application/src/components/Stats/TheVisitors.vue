<template>
    <span v-if="!loading">
        <div className="overflow-x-auto w-full custom-scrollbar">
            <table v-if="visitors_viewers" class="table table-sm">
                <thead class="thead-css h-14 text-base">
                    <tr>
                        <th>{{ $t("statistics.name") }}</th>
                        <th @click="sortVisitors" style="cursor: pointer;"><span class="arrow">{{ $t("statistics.visitors") }}&#8595</span></th>
                        <th @click="sortWatchers" style="cursor: pointer;"><span class="arrow">{{ $t("statistics.watchers") }}&#8595</span></th>
                    </tr>
                </thead>
                <tbody>
                <tr v-for="index in 60" :key="index" v-if="visitors_viewers[0]"   class="mapping odd:bg-dark-gray even:bg-lighter-gray h-10">
                    <td class="text-slate-200 text-base hover:underline cursor-pointer"><a :href="getUrl(visitors_viewers[index-1]?.id, visitors_viewers[index-1]?.name)" target="_blank" >{{ visitors_viewers[index-1]?.name}}</a></td>
                    <td class="text-slate-200 text-base">{{ visitors_viewers[index-1]?.stats.visitsCount }}</td>
                    <td class="text-slate-200 text-base">{{ visitors_viewers[index-1]?.stats.watchersCount }}</td>
                </tr>
            </tbody>
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
            const userKey = this.$cookies.get('allegro-cred').userKey;
            const response = (await axios.post(`${url}/allegro-visitors-viewers`, {userKey: userKey})).data
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
