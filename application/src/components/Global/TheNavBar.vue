<template>
  <div id="container" v-if="!loading">
    <nav>
      <h2>Allegro offers</h2>
      <hr>
      <ul>
        <li>
          <span @click="option='listing'">{{ $t("buttons.listingOffers") }}</span>
        </li>
        <hr>
        <li>
          <span @click="option='specific'">{{ $t("editView.specific") }}</span>
          <span @click="option='swap'">{{ $t("editView.swap") }}</span>
        </li>
        <hr>
        <li>
          <span @click="option='visitors'">{{ $t('statistics.visitorsViewers') }}</span>
          <span @click="option='sales'">{{ $t('statistics.sales') }}</span>
          <span @click="option='genres'">{{ $t('statistics.genres') }}</span>
        </li>
        <hr>
        <li>
          <span @click="refreshDatabase">{{ $t('buttons.refresh') }}</span>
        </li>
        <hr>
        <li style="display: flex; gap: 10px; padding: 13.5px;">
          <img src="@/assets/poland.png" alt="poland" @click="changeLanguage('pl')">
          <img src="@/assets/uk.png" alt="uk" @click="changeLanguage('en')">
        </li> 
      </ul>
    </nav>

    
    <main v-if="!loading">
      <TheListingOptions v-if="option=='listing'"/>
      <TheEditSpecific v-if="option=='specific'"/>
      <TheSwap v-if="option=='swap'"/>
      <TheVisitors v-if="option=='visitors'"/>
      <TheSales v-if="option=='sales'"/>
      <TheGenres v-if="option=='genres'"/>
    </main>

    <TheAlert :alert="alert" />
  </div>
  <div id="loading" v-if="loading">
      <img src="@/assets/spinner.gif" alt="loading">
  </div>
</template>

<script>
    import axios from 'axios'
    import TheAlert from "@/components/Global/TheAlert.vue"
    import TheListingOptions from '@/components/Listing/TheListingOptions.vue'
    import TheEditSpecific from '@/components/Edit/TheEditSpecific.vue'
    import TheSwap from '@/components/Edit/TheSwap.vue'
    import TheVisitors from '@/components/Stats/TheVisitors.vue'
    import TheGenres from '@/components/Stats/TheGenres.vue'
    import TheSales from '@/components/Stats/TheSales.vue'

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
                const userKey = this.$cookies.get('allegro-cred').userKey;

                await axios.post(`${url}/refresh-database`, {userKey: userKey})
                await axios.post(`${url}/store-all-offers`, {userKey: userKey})
                await axios.post(`${url}/store-all-payments`, {userKey: userKey})

                this.loading = false
            },
            changeLanguage(locale) {
                this.$i18n.locale = locale
            }
        },
        components: {
          TheAlert,
          TheListingOptions,
          TheEditSpecific,
          TheSwap,
          TheVisitors,
          TheGenres,
          TheSales,
        }
    }
</script>

<style lang="scss" scoped>
  #container{
    display: flex;

    nav {
      width: 250px;
      min-height: 100vh;
      background-color: #202020;
      transition: all .3s ease;
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
        margin-left: 5px;
        margin-right: 5px;

        li {
          cursor: pointer;
          span {
            display: block;
            padding: 15px;
            transition: all .3s ease;
            font-size: 18.5px;

            &:hover{
              background-color: #303030;
              border-radius: 3%;
            }
          }
          
          img{
            width: 40px;
            height: 40px;

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
        margin-bottom: 250px;
      }
    }


@media only screen and (max-width: 750px) {
  #container{
    flex-direction: column;
    
    nav {
      width: 100%;
      font-size: 1px;
      ul{
        li{
          img{
            height: 40px;
          }
        }
      }
    }
  }
}
</style>