<template>
  <table class="mt-10 table table-sm" v-for="(order, index) in orders" v-if="orders">
    <thead class="thead-css h-14 text-base">
      <tr>
        <th>{{ $t("table.image") }}</th>
        <th>{{ $t("table.title") }}</th>
        <th>{{ $t("orders.details") }}</th>
      </tr>
    </thead>
    <tbody class="tab-css">
      <tr v-for="items in order.items" class="mapping odd:bg-dark-gray even:bg-lighter-gray">
        <td class="w-4/12"><TheSlider :images="items.images" :sliderStyle="'width: 350px;'"></TheSlider></td>
        <td class="w-4/12 text-left">{{ items.name }}</td>
        <td class="w-4/12 text-left">{{ orders[index].city }} {{ orders[index].street }} - {{ orders[index].pickup_id }}</td>
      </tr>
    </tbody>
  </table>
  <div v-else class="flex flex-col gap-2 text-2xl items-center w-full mt-10 text-white font-semibold" >{{ $t("orders.allSent") }}</div>
  <div id="loading" v-if="loading">
    <img src="@/assets/spinner.gif" alt="loading" />
  </div>
</template>
  
<script setup>
    import { ref, onMounted } from 'vue';
    import axios from 'axios';
    import TheSlider from "@/components/Global/TheSlider.vue";

    const orders = ref([]);
    const userKey = $cookies.get("allegro-cred").userKey;
    let loading = ref(false);

    onMounted(async () => {
      try {
          loading.value = true;
          const response = await axios.post(`${baseUrl}/get-orders-detail`, { userKey: userKey });
          orders.value = response.data.output;
          loading.value = false;
      } catch (error) {
          console.error('There was a problem fetching the orders:', error);
      }
    });
</script>