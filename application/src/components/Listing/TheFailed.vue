<template>
  <div
    class="overflow-x-auto w-full custom-scrollbar"
    v-if="dataFailed.length > 0 && !loading.flag"
  >
    <div class="text-center text-3xl text-slate-100 font-semibold">
      {{ $t("table.unlisted") }}
    </div>
    <table class="table table-sm mt-10">
      <thead class="thead-css h-14 text-base">
        <tr>
          <th></th>
          <th>
            {{ $t("table.image") }}
          </th>
          <th>
            {{ $t("table.title") }}
          </th>
          <th>
            {{ $t("table.label") }}
          </th>
          <th>
            {{ $t("table.country") }}
          </th>
          <th>
            {{ $t("table.year") }}
          </th>
          <th>
            {{ $t("table.genre") }}
          </th>
          <th v-if="typeRecord == 'CD'">
            {{ $t("table.barcode") }}
          </th>
          <th>
            {{ $t("table.condition") }}
          </th>
          <th>
            {{ $t("table.price") }}
          </th>
          <th>Allegro</th>
        </tr>
      </thead>
      <tbody class="tab-css">
        <tr
          v-for="index in dataFailed.length"
          :key="index"
          class="mapping odd:bg-lighter-gray even:bg-lighter-gray"
        >
          <th>{{ index }}</th>
          <td>
            <img
              :src="dataFailed[index - 1].images[0]"
              alt="preview image"
              class="w-32 h-32"
            />
          </td>
          <td>{{ dataFailed[index - 1].title }}</td>
          <td>{{ dataFailed[index - 1].label }}</td>
          <td>{{ dataFailed[index - 1].country }}</td>
          <td>{{ dataFailed[index - 1].year }}</td>
          <td>{{ dataFailed[index - 1].genre }}</td>
          <td v-if="typeRecord == 'CD'">{{ dataFailed[index - 1].barcode }}</td>
          <td>{{ dataFailed[index - 1].condition }}</td>
          <td>{{ dataFailed[index - 1].price }}</td>
          <td>
            <button
              class="btn btn-primary w-full allegro"
              type="submit"
              @click="listingOfferAllegro(dataFailed[index - 1])"
            >
              {{ $t("table.send") }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="flex gap-6 mt-5 justify-center flex-wrap">
      <button class="btn btn-primary text-lg w-auto" type="submit">
        <a href="https://allegro.pl/offer/" target="_blank">{{
          $t("table.allegroForm")
        }}</a>
      </button>
      <button class="btn btn-primary text-lg w-auto" type="submit" @click="back">
        {{ $t("table.back") }}
      </button>
    </div>
  </div>

  <div
    v-if="dataFailed.length == 0"
    class="flex flex-col gap-2 text-2xl items-center w-full mt-10 text-white font-semibold"
  >
    {{ $t("listingView.allListed") }}
    <button class="btn btn-primary w-40 text-base" type="submit" @click="back">
      {{ $t("table.back") }}
    </button>
  </div>

  <div id="loading" v-if="loading.flag">
    <img src="@/assets/spinner.gif" alt="loading" />
    <h3>{{ loading.message }}</h3>
  </div>
  <TheAlert :alert="alert" />
</template>

<script>
import axios from "axios";
import TheAlert from "@/components/Global/TheAlert.vue";

export default {
  data() {
    return {
      loading: { flag: false, message: "" },
      alert: {},
    };
  },
  methods: {
    async back() {
      const userKey = this.$cookies.get("allegro-cred").userKey;
      await axios.post(
        `${url}/clear-image-data`,
        { userKey: userKey },
        { headers: { "Content-Type": "application/json" } }
      );
      window.location.reload();
    },
    async listingOfferAllegro(selectedData) {
      this.loading.flag = true;
      const userKey = this.$cookies.get("allegro-cred").userKey;

      axios
        .post(
          `${url}/allegro-listing`,
          {
            userKey: userKey,
            offer_data: selectedData,
            carton: this.carton,
            typeRecord: this.typeRecord,
            typeOffer: this.typeOffer,
            duration: this.duration,
            clear: this.clear,
          },
          {
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*",
            },
          }
        )
        .then((response) => {
          response = response.data;

          if (response.error || response.output.errors) {
            this.alert = {
              variant: "danger",
              message: `${this.$t("alerts.listingFailed")} - ${
                selectedData.title
              }`,
            };
          } else {
            this.alert = {
              variant: "success",
              message: `${this.$t("alerts.listingSuccess")} - ${
                selectedData.title
              }`,
            };
          }
        })
        .finally(() => {
          this.loading.flag = false;
        });
    },
  },
  props: {
    dataFailed: {
      type: Object,
      requried: true,
    },
    typeRecord: {
      type: String,
      requried: true,
    },
    carton: {
      type: String,
      requried: true,
    },
    typeOffer: {
      type: String,
      requried: true,
    },
    duration: {
      type: String,
      requried: true,
    },
    clear: {
      type: Boolean,
      requried: true,
    },
  },
  components: {
    TheAlert,
  },
};
</script>
