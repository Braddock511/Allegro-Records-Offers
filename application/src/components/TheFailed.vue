<template>
    <h1 style="width: 100%; margin-top: 10px; text-align: center;">Unlisted offers</h1>
    <div class="data">
        <table v-if="dataFailed">
            <tr>
                <td><h2>Image</h2></td>
                <td><h2>Title</h2></td>
                <td><h2>Label</h2></td>
                <td><h2>Country</h2></td>
                <td><h2>Year</h2></td>
                <td><h2>Genre</h2></td>
                <td v-if="type == 'CD'"><h2>Barcode</h2></td>
                <td><h2>Condition</h2></td>
                <td><h2>Price</h2></td>
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

        <button class="btn btn-primary w-50" type="submit" style="padding: 0.5rem; font-size: 20px;"><a href="https://allegro.pl/offer/" style="color: white" target="_blank">Go to allegro form</a></button>
        <button class="btn btn-primary w-50" type="submit" style="padding: 0.5rem; font-size: 20px;" @click="this.$router.push('/')">Back</button>
    </div>
</template>

<script>
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
        }
    }
</script>