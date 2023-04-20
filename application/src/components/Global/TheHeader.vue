<template>
    <header>
        <router-link to="/" id="home"><h1><span>Allegro Offers</span></h1></router-link>
        <div id="languages">
            <img src="@/assets/poland.png" alt="poland" @click="changeLanguage('pl')">
            <img src="@/assets/uk.png" alt="uk" @click="changeLanguage('en')">
        </div>
    </header>
</template>

<script>
    export default {
        methods: {
            changeLanguage(locale) {
                this.$i18n.locale = locale
            }
        }
    }
</script>

<style scoped lang="scss">
    header{
        display: flex;
        justify-content: center;
        text-align: center;
        background-color: rgb(34, 36, 35);
        padding: 15px;
        #home{
            display: block;
            width: 250px;
            span:hover{
                opacity: 0.8;
            }
        }
        #github{
            position: absolute;
            top: 0;
            left: 0;
            padding: 20px;
            &:hover{
                opacity: 0.8;
            }
        }
        #languages{
            position: absolute;
            right: 0;
            display: flex;
            gap:10px;
            img{
                cursor: pointer;
                width: 50px;
                height: 50px;

                &:hover{
                    opacity: 0.9;
                }
            }
        }
    }
    @media only screen and (max-width: 500px){
        header{
            width: 500px;

            #languages{
                position: static;
            }
        }
    }
</style>
  