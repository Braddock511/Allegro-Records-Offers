<template>
  <template v-if="listings.length > 0">
    <div v-if="!listing_data" className="overflow-x-auto w-full custom-scrollbar">
        <table class="table table-sm">
            <thead class="thead-css h-14 text-base">
                <tr>
                    <th>{{ $t("carton.enter_carton") }}</th>
                    <th>{{ $t("history.date") }}</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
            <tr v-for="listing in listings" v-if="listings" class="mapping odd:bg-dark-gray even:bg-lighter-gray h-10">
                <td class="text-slate-200 text-base">{{ listing[1] }}</td>
                <td class="text-slate-200 text-base">{{ listing[2] }}</td>
                <td class="text-slate-200 text-base flex justify-between"><button @click="load(listing[0])" class="btn btn-primary">{{ $t("history.load") }}</button><img @click="deleteListing(listing[0])" src="@/assets/delete.png" style="width: 50px; min-width: 50px; cursor: pointer;"></td>
            </tr>
        </tbody>
        </table>
    </div>
  </template>
  <div v-else class="flex flex-col gap-2 text-2xl items-center w-full mt-10 text-white font-semibold" >{{ $t("history.empty") }}</div>

  <TheListingData v-if="listing_data"
    :typeRecord="listing_data.typeRecord"
    :typeOffer="listing_data.typeOffer"
    :duration="listing_data.duration"
    :clear="listing_data.clear"
    :numberImages="listing_data.numberImages"
    :numberFiles="listing_data.numberFiles"
    :conditions="listing_data.conditions"
    :imageData="imageData"
    :carton="listing_data.carton"/> 

</template>

<script>
import TheListingData from "@/components/Listing/TheListingData.vue";
import VueCookies from "vue-cookies";
import axios from "axios";
export default {
  data() {
    return {
      listings: [],
      listing_data: null,
      listing_id: null
    };
  },
  methods: {
    async load(id){
      this.listing_id = id
      const response = (await axios.post(`${baseUrl}/load-listing`, { listing: id}, { headers: { "Content-Type": "application/json" }})).data
      this.listing_data = response.output
      this.imageData = response.image_data
    },
    async deleteListing(id){
      await axios.post(`${baseUrl}/clear-image-data`, { listing: id}, { headers: { "Content-Type": "application/json" }})
      const indexToDelete = this.listings.findIndex(listing => listing[0] === id);

      if (indexToDelete !== -1) {
        this.listings.splice(indexToDelete, 1);
      }
    }
  },
  async beforeMount() {
    const userKey = this.$cookies.get("allegro-cred").userKey;
    this.listings = (await axios.post(`${baseUrl}/listing-ids`, { userKey}, { headers: { "Content-Type": "application/json" }})).data.output
  },
  components: {
    VueCookies,
    TheListingData
  },
};
</script>