<template>
    <TheHeader />
    <span v-if="edit == ''" style="height: 500px; display: flex; flex-direction: column; justify-content: center;  align-items: center; gap: 20px;">
            <button class="btn btn-primary" type="button" style="width: 30%; padding: 0.5rem; font-size: 20px;" @click="edit='many'">{{ $t("editView.many") }}</button>
            <button class="btn btn-primary" type="button" style="width: 30%; padding: 0.5rem; font-size: 20px;" @click="edit='specific'">{{ $t("editView.specific") }}</button>
            <button class="btn btn-primary" type="button" style="width: 30%; padding: 0.5rem; font-size: 20px;" @click="edit='swap'">{{ $t("editView.swap") }}</button>
    </span>
    <TheEditMany v-if="edit=='many'"/>
    <TheEditSpecific v-if="edit=='specific'"/>
    <TheSwap v-if="edit=='swap'"/>
</template>

<script>
    import TheHeader from '@/components/Global/TheHeader.vue'
    import TheEditMany from '@/components/Edit/TheEditMany.vue'
    import TheEditSpecific from '@/components/Edit/TheEditSpecific.vue'
    import TheSwap from '@/components/Edit/TheSwap.vue'

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
            TheEditSpecific,
            TheSwap
        }
    }
</script>