<template>
  <div v-if="!read">
    <section
      v-if="!loading"
      class="w-full flex justify-center items-center h-full"
    >
      <form
        @submit.prevent="getImageData"
        class="bg-darker-gray rounded-lg p-4 px-6 flex flex-col gap-8"
      >
        <div class="text-2xl text-slate-200 font-semibold">
          {{ $t("listingView.upload") }}
        </div>
        <div class="px-4 flex flex-col gap-7">
          <div class="relative">
            <label
              for="files"
              class="absolute flex justify-center items-center text-gray-300 left-2 h-[1.5px] bg-lighter-black text-sm font-semibold"
              >{{ $t("listingView.images") }} &nbsp;</label
            >
            <label
              class="absolute flex justify-center items-center text-gray-300 right-2 h-[1.5px] bg-lighter-black px-1 text-sm font-semibold"
            >
              Uploaded: {{ images.length }}</label
            >
            <input
              @change="handleImagesFiles"
              class="bg-lighter-black w-full rounded-md text-white px-2 h-auto min-h-[28px] hidden"
              id="files"
              type="file"
              ref="fileInput"
              multiple
              required
            />
            <button
              class="bg-lighter-black w-full rounded-md text-white px-2 h-10 min-h-[28px] border-css"
              type="button"
              @click="openFileInput"
            >
              <span
                class="bg-gray-400 px-4 text-black rounded-xl text-base font-semibold"
              >
                {{ $t("table.inputFile") }}</span
              >
            </button>
          </div>
          <div class="relative">
            <div
              class="absolute flex justify-center items-center text-gray-300 left-2 h-[1.5px] bg-lighter-black px-1 text-sm font-semibold"
            >
              {{ $t("vinyl") }} / CD
            </div>
            <select
              v-model="typeRecord"
              class="select-css h-10 w-full p-1 rounded-md placeholder:text-center bg-lighter-black text-sm truncate outline-none"
            >
              <option value="Vinyl">{{ $t("vinyl") }}</option>
              <option value="CD">CD</option>
            </select>
          </div>
          <div class="relative flex flex-col gap-2 items-center">
            <div
              class="absolute flex justify-center items-center text-gray-300 left-2 h-[1.5px] bg-lighter-black px-1 text-sm font-semibold"
            >
              Offer type
            </div>
            <select
              v-model="typeOffer"
              class="select-css h-10 w-full p-1 rounded-md placeholder:text-center bg-lighter-black text-sm truncate outline-none"
            >
              <option value="BUY_NOW">{{ $t("listingView.buyNow") }}</option>
              <option value="AUCTION">{{ $t("listingView.auction") }}</option>
            </select>
            <select
              v-if="typeOffer == 'AUCTION'"
              v-model="duration"
              class="select-css h-10 w-3/4 p-1 rounded-md placeholder:text-center bg-lighter-black text-sm truncate outline-none"
            >
              <option value="P1D">1 {{ $t("listingView.day") }}</option>
              <option value="P3D">3 {{ $t("listingView.day") }}</option>
              <option value="P5D">5 {{ $t("listingView.day") }}</option>
              <option value="P7D">7 {{ $t("listingView.day") }}</option>
              <option value="P10D">10 {{ $t("listingView.day") }}</option>
            </select>
          </div>
          <label class="label cursor-pointer gap-1 w-fit">
            <span class="label-text text-base">
              {{ $t("listingView.clearFirstImage") }}</span
            >
            <input
              type="checkbox"
              checked="checked"
              v-model="clear"
              class="checkbox h-5 w-5 checkbox-primary bg-gray-600"
            />
          </label>
          <div class="relative">
            <label
              for="number-images"
              class="absolute flex justify-center items-center text-gray-300 left-2 h-[1.5px] bg-lighter-black px-1 text-sm font-semibold"
              >{{ $t("listingView.numberImages") }}</label
            >
            <input
              v-model="numberImages"
              id="number-images"
              type="number"
              min="2"
              class="bg-lighter-black font-semibold h-10 w-full p-1 rounded-md placeholder:text-center px-1 outline-none border-css"
              required
            />
          </div>
          <div class="relative">
            <label
              for="number-images"
              class="absolute flex justify-center items-center text-gray-300 left-2 h-[1.5px] bg-lighter-black px-1 text-sm font-semibold"
              >{{ $t("conditionFile") }}&nbsp;</label
            >
            <input
              type="file"
              @change="handleConditionFile"
              accept=".txt"
              class="bg-lighter-black w-full rounded-md text-white px-2 min-h-[28px] h-10 hidden"
            />
            <button
              class="bg-lighter-black w-full rounded-md text-white px-2 h-10 min-h-[28px] border-css"
              type="button"
              @click="openFileInput"
            >
              <span
                class="bg-gray-400 px-4 text-black rounded-xl text-base font-semibold"
              >
                {{ $t("table.inputFile") }}</span
              >
            </button>
          </div>
          <div class="flex flex-col gap-1 px-2">
            <p>1. {{ $t("listingView.imageOrder") }}</p>
            <p>2. {{ $t("listingView.paymentLocationDelivery") }}</p>
            <p>3. {{ $t("listingView.description") }}</p>
          </div>
        </div>
        <button type="submit" class="btn btn-primary">
          {{ $t("listingView.sendImages") }}
        </button>
      </form>
    </section>
    <div id="loading" v-if="loading">
      <img src="@/assets/spinner.gif" alt="loading" />
      <h3>{{ $t("loading.readImage") }}</h3>
    </div>
  </div>
  <TheListingData
    v-if="read"
    :typeRecord="typeRecord"
    :typeOffer="typeOffer"
    :duration="duration"
    :clear="clear"
    :numberImages="numberImages"
    :numberFiles="files.length"
    :conditions="conditions"
  />
</template>

<script>
import TheListingData from "@/components/Listing/TheListingData.vue";
import VueCookies from "vue-cookies";
import axios from "axios";
export default {
  data() {
    return {
      images: [],
      numberImages: 3,
      read: "asd",
      files: "",
      typeRecord: "Vinyl",
      typeOffer: "BUY_NOW",
      duration: "P1D",
      conditionFile: null,
      conditions: [],
      clear: false,
      loading: false,
      alert: {},
    };
  },
  methods: {
    openFileInput() {
      this.$refs.fileInput.click();
    },

    handleImagesFiles(event) {
      // Get an array of the selected files and sort them by name
      const files = Array.from(event.target.files);
      this.files = files;
      let loadedCount = 0;

      // Loop through the files and read each one as a data URL
      for (let i = 0; i < files.length; i++) {
        const reader = new FileReader();
        reader.readAsDataURL(files[i]);
        reader.onload = () => {
          this.images[i] = reader.result;
          loadedCount++;
          if (loadedCount === files.length) {
            // All files have been loaded, sort the data array
            this.images.sort(
              (a, b) =>
                files.findIndex(
                  (file) => file.name === a.split(",")[0].split(";")[1]
                ) -
                files.findIndex(
                  (file) => file.name === b.split(",")[0].split(";")[1]
                )
            );
          }
        };
      }
    },
    handleConditionFile(event) {
      const file = event.target.files[0];
      this.conditionFile = file;
      const reader = new FileReader();
      reader.onload = () => {
        const content = reader.result;
        this.validateAndSave(content);
      };
      reader.readAsText(this.conditionFile);
    },
    validateAndSave(content) {
      const lines = content.includes("\n")
        ? content.split("\n")
        : content.split(" ");
      const processedLines = lines.map((line) => line.trim());
      this.conditions = this.conditions.concat(processedLines).reverse();
    },
    splitImages(images, numberImages) {
      const chunks = [];

      for (let i = 0; i < images.length; i += numberImages) {
        const chunk = images.slice(i, i + numberImages);
        chunks.push(chunk);
      }

      return chunks;
    },
    async getImageData() {
      this.loading = true;
      const splitImages = this.splitImages(this.images, this.numberImages);
      const userKey = this.$cookies.get("allegro-cred").userKey;
      const endpoint =
        this.typeRecord === "Vinyl" ? "read-vinyl-image" : "read-cd-image";

      this.read = await axios.post(
        `${url}/${endpoint}`,
        { userKey, images: splitImages },
        { headers: { "Content-Type": "application/json" } }
      );
      this.loading = false;
    },
  },
  components: {
    TheListingData,
    VueCookies,
  },
};
</script>
