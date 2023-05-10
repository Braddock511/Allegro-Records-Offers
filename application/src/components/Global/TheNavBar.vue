<template>
  <div id="container">
    <nav>
      <h2>Allegro offers</h2>
      <hr>
      <ul>
        <li>
          <span @click="option='listing'">{{ $t("buttons.listingOffers") }}</span>
        </li>
        <hr>
        <li>
          <span @click="option='many'">{{ $t("editView.many") }}</span>
          <span @click="option='specific'">{{ $t("editView.specific") }}</span>
          <span @click="option='swap'">{{ $t("editView.swap") }}</span>
        </li>
        <hr>
        <li>
          <span>{{ $t('statistics.visitorsViewers') }}</span>
          <span>{{ $t('statistics.sales') }}</span>
          <span>{{ $t('statistics.genres') }}</span>
        </li>
        <hr>
        <li>
          <span>{{ $t('buttons.refresh') }}</span>
        </li>
        <hr>
        <li style="display: flex; gap: 10px; padding: 10px;">
          <img src="@/assets/poland.png" alt="poland" @click="changeLanguage('pl')">
          <img src="@/assets/uk.png" alt="uk" @click="changeLanguage('en')">
        </li> 
      </ul>
    </nav>

    
    <main v-if="!loading">
      <ListingView v-if="option='listing'"/>
      <TheEditMany v-if="option=='many'"/>
      <TheEditSpecific v-if="option=='specific'"/>
      <TheSwap v-if="option=='swap'"/>
    </main>

    <div id="loading" v-if="loading">
        <img src="@/assets/spinner.gif" alt="loading">
    </div>
    <TheAlert :alert="alert" />
  </div>
</template>

<script>
    import axios from 'axios'
    import ListingView from '@/views/ListingView.vue'
    import TheEditMany from '@/components/Edit/TheEditMany.vue'
    import TheEditSpecific from '@/components/Edit/TheEditSpecific.vue'
    import TheAlert from "@/components/Global/TheAlert.vue"
    import TheSwap from '@/components/Edit/TheSwap.vue'

    export default {
        data(){
            return{
                option: "listing",
                loading: false,
                alert: {}
            }
        },
        methods:{
            async refreshDatabase(){
                this.loading = true
                await axios.get("http://127.0.0.1:8000/refresh-database")
                const response_offers = (await axios.get('http://127.0.0.1:8000/store-all-offers')).data
                const response_payments = (await axios.get('http://127.0.0.1:8000/store-all-payments')).data
                if (response_offers.error){
                    this.alert = {variant: "danger", message: this.$t("alerts.offersFailed")}
                    this.formDisplay = true
                }
                else if (response_payments.error){
                    this.alert = {variant: "danger", message: this.$t("alerts.paymentsFailed")}
                    this.formDisplay = true
                }
                else{
                    this.$router.push("/")
                }
                this.loading = false
            },
            changeLanguage(locale) {
                this.$i18n.locale = locale
            }
        },
        components: {
          ListingView,
          TheEditMany,
          TheEditSpecific,
          TheSwap,
          TheAlert,
        }
    }
</script>

<style lang="scss" scoped>
  #container{
    display: flex;

    nav {
      width: 250px;
      background-color: #202020;
      transition: all .3s ease;
      cursor: pointer;
      box-shadow:4px 7px 10px rgba(0,0,0,.4);
      
      h2{
        margin-top: 5px;
        text-align: center;
      }
      
        ul {
          color:white;
          list-style-type:none;
          padding:0px;
          margin:0px;  

          li {
            padding-bottom: 5px;
            span {
              display: block;
              padding: 15px;
              transition: all .3s ease;
              font-size: 20px;

              &:hover{
                background-color: #303030;
              }
            }
            
            img{
              width: 50px;

              &:hover{
                opacity: .8;
              }
            }

          }
        }
      }

      main{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: 1000px;
      }
    }


@media only screen and (max-width: 750px) {
  #container{
    flex-direction: column;
    
    nav {
      display: flex;
      width: 100%;
      h2{
        display: none;
      }
      ul{
        display: flex;

        li{
          img{
            height: 50px;
          }
        }
      }
    }
  }
}
</style>