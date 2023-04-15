<template>
    <h1 style="width: 100%; margin-top: 10px; text-align: center;">{{ $t("table.unlisted") }}</h1>
    <div class="data">
        <table v-if="dataFailed">
            <tr>
                <td><h2>{{ $t("table.image") }}</h2></td>
                <td><h2>{{ $t("table.title") }}</h2></td>
                <td><h2>{{ $t("table.label") }}</h2></td>
                <td><h2>{{ $t("table.country") }}</h2></td>
                <td><h2>{{ $t("table.year") }}</h2></td>
                <td><h2>{{ $t("table.genre") }}</h2></td>
                <td v-if="type == 'CD'"><h2>{{ $t("table.barcode") }}</h2></td>
                <td><h2>{{ $t("table.condition") }}</h2></td>
                <td><h2>{{ $t("table.price") }}</h2></td>
            </tr>
            
            <tbody >
                <tr v-for="index in dataFailed.condition.length" :key="index">
                    <td><img :src="dataFailed.img[index-1]" alt="preview image"  style="width: 150px; height: 150px;"></td>
                    <td>{{ dataFailed.data[index-1].title }}</td>
                    <td>{{ dataFailed.data[index-1].label }}</td>
                    <td>{{ dataFailed.data[index-1].country }}</td>
                    <td>{{ dataFailed.data[index-1].year }}</td>
                    <td>{{ dataFailed.data[index-1].genre }}</td>
                    <td v-if="type == 'CD'">{{ dataFailed.data[index-1].barcode }}</td>
                    <td>{{ dataFailed.condition[index-1] }}</td>
                    <td>{{ dataFailed.data[index-1].price }}</td>
                </tr>
            </tbody>
        </table>

        <button class="btn btn-primary w-50" type="submit" style="padding: 0.5rem; font-size: 20px;"><a href="https://allegro.pl/offer/" style="color: white" target="_blank">{{ $t("table.allegroForm") }}</a></button>
        <button class="btn btn-primary w-50" type="submit" style="padding: 0.5rem; font-size: 20px;" @click="back">{{ $t("table.back") }}</button>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        props:{
            dataFailed:{
                type: Object,
                requried: true
            },
            type:{
                type: String,
                requried: true
            }
        },
        methods:{
            async back(){
                await axios.get('http://127.0.0.1:8000/truncate', {headers: {'Content-Type': 'application/json'}})
                this.$router.push('/')
            }
        }
    }
</script>