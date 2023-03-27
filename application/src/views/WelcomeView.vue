<template>
    <TheHeader />
    <main>
        <div id="info" v-if="!isCookieSet">
            <p>The "Allegro Records Offers" application is a tool designed to help users effectively manage their records offers on Allegro, one of the largest online marketplaces in Poland. Thanks to this application, users can easily list their products on Allegro and edit existing offers.</p>
            <p>The application features a user-friendly interface that allows you to quickly and easily upload your products to the Allegro platform. Users can add product photos, descriptions, prices, and other important details to create engaging and informative listings that will appeal to potential buyers. </p>
            <p>In addition, the user can clear the background of the image and view the statistics of the offers</p>                    
        </div>
        <div id="buttons" style="display: flex; flex-direction: column; justify-content: center; gap: 40px;">
            <h1 v-if="isCookieSet" style="display: flex; justify-content: center;">Options</h1>
            <router-link  v-if="isCookieSet" to="/listing"><button class="btn btn-primary w-100" type="button" style="padding: 0.75rem; font-size: 20px;">Listing offers</button></router-link>
            <router-link  v-if="isCookieSet" to="/edit"><button class="btn btn-primary w-100" type="button" style="padding: 0.75rem; font-size: 20px;">Edit offers</button></router-link>
            <router-link  v-if="isCookieSet" to="/stats"><button class="btn btn-primary w-100" type="button" style="padding: 0.75rem; font-size: 20px;">Statistics</button></router-link>
            <router-link  v-if="!isCookieSet" to="/allegro-credentials"><button class="btn btn-primary w-100" type="button" style="padding: 0.5rem; font-size: 20px;">Enter allegro credentials</button></router-link>
        </div>
    </main>
</template>

<script>
    import TheHeader from "@/components/TheHeader.vue"
    import VueCookies from "vue-cookies"
    export default {
        computed: {
            isCookieSet() {
                return VueCookies.get("allegro-cred") === "true"
            },
        },
        components: {
            TheHeader,
            VueCookies
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