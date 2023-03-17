<template>
    <TheHeader />
    <main>
        <div id="info">
            <span v-if="!isCookieSet">
                <p>The "Allegro Records Offers" application is a tool designed to help users effectively manage their records offers on Allegro, one of the largest online marketplaces in Poland. Thanks to this application, users can easily list their products on Allegro and edit existing offers.</p>
                <p>The application features a user-friendly interface that allows you to quickly and easily upload your products to the Allegro platform. Users can add product photos, descriptions, prices, and other important details to create engaging and informative listings that will appeal to potential buyers. </p>
                <p>In addition, the user can clear the background of the image and view the statistics of the offers</p>                    
            </span>
            
            <h1 v-if="isCookieSet" style="display: flex; justify-content: center;">Options</h1>
            <router-link v-if="isCookieSet" to="/listing" class="button"><h3>Listing offers</h3></router-link>
            <router-link v-if="isCookieSet"  to="/edit" class="button"><h3>Edit offers</h3></router-link>
            <router-link  v-if="isCookieSet" to="/stats" class="button"><h3>Statistics</h3></router-link>
            <router-link  v-if="!isCookieSet" to="/allegro-credentials" class="button"><h3>Enter allegro credentials</h3></router-link>
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
        },
    }

</script>

<style lang="scss" scoped>
    main{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 100px;

        #info{
            width: 50%;
            font-size: large;

            p{
                font-size: larger;
                margin-bottom: 10px;
            }
            
            .button{
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: large;

                h3{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: rgb(1, 83, 151);
                    border-radius: 12px;
                    height: 50px;
                    margin-top: 38px;
                    outline: 0;
                    text-align: center;
                    width: 30%;

                    &:hover {
                        background-color: rgb(0, 70, 128);
                    }
                }
            }

            a{
                color: rgb(211, 211, 211);

                &:hover{
                    color: white;
                }
            }
        }
    }

    @media only screen and (max-width: 1200px){
        main{

            #info{
                p{
                    font-size: large;    
                }

                .button{

                    h3{
                        width: 50%;
                    }
                }
            }
        }
    }

    @media only screen and (max-width: 700px){
        main{

            #info{
                p{
                    font-size: medium;
                }
                .button{

                    h3{
                        width: 70%;
                    }
                }
            }
        }
    }

    @media only screen and (max-width: 500px){
        main{
            width: 500px;
        }
    }
</style>