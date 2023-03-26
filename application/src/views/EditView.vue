<template>
    <TheHeader />
    <span v-if="edit == ''" style="width: 100%; height: 500px; display: flex; justify-content: center;  align-items: center; flex-direction: column;">
        <button  class="blue-button" @click="edit='many'" style="width: 33%;">Edit many offers</button>
        <button  class="blue-button" @click="edit='specific'" style="width: 33%;">Edit specific offer</button>
    </span>
    <TheEditMany v-if="edit=='many'"/>
    <TheEditSpecific v-if="edit=='specific'"/>
</template>

<script>
    import TheHeader from '@/components/TheHeader.vue'
    import TheEditMany from '@/components/TheEdItMany.vue'
    import TheEditSpecific from '@/components/TheEditSpecific.vue'
    export default {
        data(){
            return{
                edit: "",
                loading: false,
            }
        },
        components:{
            TheHeader,
            TheEditMany,
            TheEditSpecific
        }
    }
</script>