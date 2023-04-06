<template>
    <TheHeader />
    <main>
        <div id="info" v-if="!isCookieSet">
            <h1>{{ $t('info.title') }}</h1>
            <p>{{ $t('info.description') }}</p>               
        </div>
        <div id="buttons" style="display: flex; flex-direction: column; justify-content: center; gap: 40px;">
            <h1 v-if="isCookieSet" style="display: flex; justify-content: center;">{{ $t('buttons.options') }}</h1>
            <router-link  v-if="isCookieSet" to="/listing"><button class="btn btn-primary w-100" type="button" style="padding: 0.75rem; font-size: 20px;">{{ $t('buttons.listingOffers') }}</button></router-link>
            <router-link  v-if="isCookieSet" to="/edit"><button class="btn btn-primary w-100" type="button" style="padding: 0.75rem; font-size: 20px;">{{ $t('buttons.editOffers') }}</button></router-link>
            <router-link  v-if="isCookieSet" to="/stats"><button class="btn btn-primary w-100" type="button" style="padding: 0.75rem; font-size: 20px;">{{ $t('buttons.statistics') }}</button></router-link>
            <router-link  v-if="!isCookieSet" to="/allegro-credentials"><button class="btn btn-primary w-100" type="button" style="padding: 0.5rem; font-size: 20px;">{{ $t('buttons.enterAllegroCredentials') }}</button></router-link>
        </div>
    </main>
</template>

<script>
    import TheHeader from "@/components/TheHeader.vue"
    export default {
        computed: {
            isCookieSet() {
                return this.$cookies.get("allegro-cred") === "true"
            },
        },
        components: {
            TheHeader,
        }
    }
</script>

<style lang="scss" scoped>
    main{
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        width: 100%;
        margin-top: 100px;
        #info{
            width: 40%;
            p{
                font-size: large;
            }
        }

        #buttons{
            width: 22.5%;
        }
    }
    @media only screen and (max-width: 1200px){
        main{
            #info{
                width: 55%;
            }

            #buttons{
                width: 40%;
            }
        }
    }
    @media only screen and (max-width: 700px){
        main{
            #info{
                width: 60%;
                p{
                    font-size: medium;
                }
            }
            #buttons{
                width: 50%;
            }
        }
    }
    @media only screen and (max-width: 500px){
        main{
            width: 500px;
        }
    }
</style>