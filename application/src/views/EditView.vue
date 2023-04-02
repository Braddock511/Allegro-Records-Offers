<template>
    <TheHeader />
    <span v-if="edit == ''" style="height: 500px; display: flex; flex-direction: column; justify-content: center;  align-items: center; gap: 20px;">
            <button class="btn btn-primary" type="button" style="width: 30%; padding: 0.5rem; font-size: 20px;" @click="edit='many'">Edit many offers</button>
            <button class="btn btn-primary" type="button" style="width: 30%; padding: 0.5rem; font-size: 20px;" @click="edit='specific'">Edit specific offer</button>
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