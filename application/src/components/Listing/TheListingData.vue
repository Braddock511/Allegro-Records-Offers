<template>
  <div class="w-full">
    <div
      v-if="!cartonFlag && !loading.flag"
      id="carton"
      class="flex flex-col gap-2 text-center items-center justify-center"
    >
      <span class="text-xl font-semibold">{{ $t("carton.enter_carton") }}</span>
      <input
        type="text"
        name="carton"
        v-model="carton"
        class="p-1 font-semibold bg-darker-gray rounded-lg px-2 max-w-xs min-w-[300px]"
      />
      <button
        class="btn btn-primary w-[300px] p-2 text-xl"
        type="button"
        @click="confirmCarton"
      >
        {{ $t("carton.confirm") }}
      </button>
    </div>
    <div v-if="cartonFlag && !failedFlag && !loading.flag">
      <div class="flex flex-col items-center mb-16">
        <TheSlider :images="offerImages"></TheSlider>
        <span class="text-xl mt-5 mb-5">
          {{ $t("table.condition") }}:
          {{ conditions[currentIndex / numberImages] }}
        </span>
        <div class="w-full flex justify-center">
          <button
            class="btn btn-primary w-1/2 p-2 text-xl"
            type="submit"
            @click="
              activeRequests += 1;
              failed.push({
                id: '',
                title: '-',
                label: '-',
                country: '-',
                year: '-',
                genre: '-',
                price: '-',
                barcode: '-',
                condition: this.condition,
                images: this.offerImages,
              });
              next();
            "
          >
            {{ $t("table.next") }}
          </button>
        </div>
      </div>
      <div class="overflow-x-auto w-full custom-scrollbar">
        <table class="table table-sm">
          <thead class="thead-css h-14 text-base">
            <tr>
              <th></th>
              <th>{{ $t("table.title") }}</th>
              <th>{{ $t("table.label") }}</th>
              <th>{{ $t("table.country") }}</th>
              <th>{{ $t("table.year") }}</th>
              <th>{{ $t("table.genre") }}</th>
              <th :class="typeRecord === 'CD' ? 'display' : 'hidden'">
                {{ $t("table.barcode") }}
              </th>
              <th class="w-[100px]">
                <div class="flex items-center gap-1">
                  {{ $t("table.enter_price") }}
                  <div class="relative">
                    <label
                      for="head-price"
                      class="absolute flex justify-center items-center -top-0 text-gray-300 left-1 h-[1.5px] bg-oceans px-1 text-xs font-semibold"
                      >{{ $t("table.condition") }}</label
                    >
                    <select
                      v-model="condition"
                      id="head-price"
                      class="select-css h-8 w-full p-1 rounded-md text-gray-100 placeholder:text-center border-none bg-oceans text-sm truncate outline-none"
                    >
                      <option value="Near Mint (NM or M-)">
                        {{ $t("table.mintMinus") }}
                      </option>
                      <option value="Mint (M)">{{ $t("table.mint") }}</option>
                      <option value="Excellent (EX)">
                        {{ $t("table.ex") }}
                      </option>
                      <option value="Very Good Plus (VG+)">
                        {{ $t("table.veryGoodPlus") }}
                      </option>
                      <option value="Very Good (VG)">
                        {{ $t("table.veryGood") }}
                      </option>
                      <option value="Good (G)">{{ $t("table.good") }}</option>
                      <option value="Fair (F)">{{ $t("table.fair") }}</option>
                    </select>
                  </div>
                </div>
              </th>
              <th>Allegro</th>
              <th>Discogs</th>
            </tr>
          </thead>
          <tbody class="tab-css">
            <tr className="bg-darker-gray">
              <th class="text-transparent"></th>
              <td>
                <input
                  type="text"
                  name="title"
                  class="h-7 rounded-md placeholder:text-center border-none bg-oceans px-1 font-semibold"
                  v-model="title"
                />
              </td>
              <td>
                <input
                  type="text"
                  name="label"
                  class="h-7 rounded-md placeholder:text-center border-none bg-oceans px-1 font-semibold"
                  placeholder="-"
                  v-model="label"
                />
              </td>
              <td>
                <input
                  type="text"
                  name="country"
                  class="h-7 rounded-md placeholder:text-center border-none bg-oceans px-1 font-semibold"
                  placeholder="-"
                  v-model="country"
                />
              </td>
              <td>
                <input
                  type="text"
                  name="year"
                  class="h-7 rounded-md placeholder:text-center border-none bg-oceans px-1 font-semibold"
                  placeholder="-"
                  v-model="year"
                />
              </td>
              <td>
                <select
                  v-model="genre"
                  class="select-css h-7 p-1 rounded-md text-gray-100 placeholder:text-center border-none bg-oceans px-1 font-semibold"
                >
                  <option value="ballad">
                    {{ $t("genre_options.ballad") }}
                  </option>
                  <option value="blues">{{ $t("genre_options.blues") }}</option>
                  <option value="country">
                    {{ $t("genre_options.country") }}
                  </option>
                  <option value="dance">{{ $t("genre_options.dance") }}</option>
                  <option value="disco">{{ $t("genre_options.disco") }}</option>
                  <option value="children's">
                    {{ $t("genre_options.children") }}
                  </option>
                  <option value="ethno">{{ $t("genre_options.ethno") }}</option>
                  <option value="jazz">{{ $t("genre_options.jazz") }}</option>
                  <option value="carols">
                    {{ $t("genre_options.carols") }}
                  </option>
                  <option value="metal">{{ $t("genre_options.metal") }}</option>
                  <option value="alternative">
                    {{ $t("genre_options.alternative") }}
                  </option>
                  <option value="electronic">
                    {{ $t("genre_options.electronic") }}
                  </option>
                  <option value="film">{{ $t("genre_options.film") }}</option>
                  <option value="classical">
                    {{ $t("genre_options.classical") }}
                  </option>
                  <option value="religious">
                    {{ $t("genre_options.religious") }}
                  </option>
                  <option value="new">{{ $t("genre_options.new") }}</option>
                  <option value="opera">{{ $t("genre_options.opera") }}</option>
                  <option value="pop">{{ $t("genre_options.pop") }}</option>
                  <option value="hip hop">{{ $t("genre_options.rap") }}</option>
                  <option value="reggae">
                    {{ $t("genre_options.reggae") }}
                  </option>
                  <option value="rock">{{ $t("genre_options.rock") }}</option>
                  <option value="rock'n'roll">
                    {{ $t("genre_options.rock_and_roll") }}
                  </option>
                  <option value="single">
                    {{ $t("genre_options.single") }}
                  </option>
                  <option value="compilations">
                    {{ $t("genre_options.compilations") }}
                  </option>
                  <option value="soul">{{ $t("genre_options.soul") }}</option>
                  <option value="synth-pop">
                    {{ $t("genre_options.synth_pop") }}
                  </option>
                  <option value="other">{{ $t("genre_options.other") }}</option>
                  <option value="sets">{{ $t("genre_options.sets") }}</option>
                </select>
              </td>
              <td :class="typeRecord === 'CD' ? 'display' : 'hidden'">
                <input
                  type="text"
                  name="barcode"
                  class="h-7 rounded-md placeholder:text-center border-none bg-oceans px-1 font-semibold"
                  placeholder="-"
                  v-model="barcode"
                />
              </td>
              <td>
                <input
                  type="number"
                  name="price"
                  class="text-center h-7 rounded-md placeholder:text-center text-gray-100 border-none bg-oceans px-1 font-semibold"
                  min="1"
                  v-model="price"
                />
              </td>
              <td>
                <button
                  class="btn btn-primary w-full"
                  type="submit"
                  style="
                    max-height: 1.75rem !important;
                    min-height: 1.75rem !important;
                  "
                  @click="listingOfferAllegro"
                >
                  {{ $t("table.send") }}
                </button>
              </td>
              <td>
                <div class="relative">
                  <label
                    for="head-sleeve"
                    class="absolute flex justify-center items-center -top-[2px] text-gray-300 left-1 h-[1.5px] bg-oceans px-1 text-xs font-semibold"
                    >{{ $t("table.sleeveCondition") }}</label
                  >
                  <select
                    id="head-sleeve"
                    v-model="sleeveCondition"
                    class="select-css font-semibold h-8 p-1 rounded-md text-gray-100 placeholder:text-center border-none bg-oceans px-1 outline-none"
                  >
                    <option value="Near Mint (NM or M-)">
                      {{ $t("table.mintMinus") }}
                    </option>
                    <option value="Mint (M)">{{ $t("table.mint") }}</option>
                    <option value="Excellent (EX)">{{ $t("table.ex") }}</option>
                    <option value="Very Good Plus (VG+)">
                      {{ $t("table.veryGoodPlus") }}
                    </option>
                    <option value="Very Good (VG)">
                      {{ $t("table.veryGood") }}
                    </option>
                    <option value="Good (G)">{{ $t("table.good") }}</option>
                    <option value="Fair (F)">{{ $t("table.fair") }}</option>
                  </select>
                </div>
              </td>
            </tr>
            <tr
              v-for="(data, index) in discogsData[recordIndex].information"
              class="mapping odd:bg-dark-gray even:bg-lighter-gray"
            >
              <th class="number-css">{{ index + 1 }}</th>
              <td>
                <a :href="data.uri" target="_blank">{{ data.title }}</a>
              </td>
              <td>
                <span v-if="data.label !== '-'">{{ data.label }}</span>
                <input
                  v-else
                  type="text"
                  name="label"
                  class="h-8 rounded-md placeholder:text-center border-none bg-oceans px-1 font-semibold hover:bg-opacity-0"
                  placeholder="Label"
                  v-model="label"
                />
              </td>
              <td>
                <span v-if="data.country !== '-'">{{ data.country }}</span>
                <input
                  v-else
                  type="text"
                  name="country"
                  class="h-8 rounded-md placeholder:text-center border-none bg-oceans px-1 font-semibold"
                  placeholder="Country"
                  v-model="country"
                />
              </td>
              <td>
                <span v-if="data.year !== '-'">{{ data.year }}</span>
                <input
                  v-else
                  type="text"
                  name="year"
                  class="h-8 rounded-md placeholder:text-center border-none bg-oceans px-1 font-semibold"
                  placeholder="Year"
                  v-model="year"
                />
              </td>
              <td>{{ data.genre }}</td>
              <td v-if="typeRecord == 'CD'">
                <span v-if="data.barcode !== '-'">{{ data.barcode }}</span>
                <input
                  v-else
                  type="text"
                  name="barcode"
                  class="h-8 rounded-md placeholder:text-center border-none bg-oceans px-1 font-semibold"
                  placeholder="-"
                  v-model="barcode"
                />
              </td>
              <td class="hidden">
                {{ $t("table.condition") }}
                <select v-model="condition">
                  <option value="Near Mint (NM or M-)">
                    {{ $t("table.mintMinus") }}
                  </option>
                  <option value="Mint (M)">{{ $t("table.mint") }}</option>
                  <option value="Excellent (EX)">{{ $t("table.ex") }}</option>
                  <option value="Very Good Plus (VG+)">
                    {{ $t("table.veryGoodPlus") }}
                  </option>
                  <option value="Very Good (VG)">
                    {{ $t("table.veryGood") }}
                  </option>
                  <option value="Good (G)">{{ $t("table.good") }}</option>
                  <option value="Fair (F)">{{ $t("table.fair") }}</option>
                </select>
              </td>
              <td
                v-if="
                  data.price[
                    condition == 'Excellent (EX)'
                      ? 'Very Good Plus (VG+)'
                      : condition
                  ] !== undefined
                "
              >
                <label
                  >Want : {{ data.community.want }} | Have:
                  {{ data.community.have }}</label
                >
                <input
                  type="number"
                  name="price"
                  class="text-center h-8 rounded-md placeholder:text-center text-gray-100 border-none bg-oceans px-1 font-semibold"
                  min="1"
                  :placeholder="
                    roundedPriceToPLN(
                      data.price[
                        condition == 'Excellent (EX)'
                          ? 'Very Good Plus (VG+)'
                          : condition
                      ]
                    )
                  "
                  v-model="price"
                  @click="
                    price = roundedPriceToPLN(
                      data.price[
                        condition == 'Excellent (EX)'
                          ? 'Very Good Plus (VG+)'
                          : condition
                      ]
                    )
                  "
                />
              </td>
              <td v-else>
                <div class="relative">
                  <label
                    :for="`price-${index}`"
                    :class="
                      index % 2 === 0 ? 'bg-lighter-gray  ' : 'bg-dark-gray'
                    "
                    class="absolute flex justify-center items-center h-1 text-gray-300 left-1 bg-oceans px-1 text-sm font-semibold"
                    >Want: ? | Have: ?</label
                  >
                  <input
                    type="number"
                    name="price"
                    :id="`price-${index}`"
                    class="h-8 rounded-md placeholder:text-center border-none bg-oceans px-1 font-semibold"
                    min="1"
                    v-model="price"
                  />
                </div>
              </td>
              <td class="text-center">
                <button
                  class="btn btn-primary w-full"
                  type="submit"
                  style="
                    max-height: 1.75rem !important;
                    min-height: 1.75rem !important;
                  "
                  @click="listingOfferAllegro(data)"
                >
                  {{ $t("table.send") }}
                </button>
              </td>
              <td class="text-center">
                <button
                  class="btn btn-primary w-[100px]"
                  type="submit"
                  style="
                    max-height: 1.75rem !important;
                    min-height: 1.75rem !important;
                  "
                  @click="listingOfferDiscogs(data)"
                >
                  {{ $t("table.send") }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex flex-col justify-center items-center mt-10 gap-3">
        <label
          for="searcher"
          class="text-[1.5rem] font-bold leading-tight tracking-tight text-center"
        >
          {{ $t("table.notFound") }}
        </label>
        <input
          type="text"
          id="searcher"
          class="h-8 rounded-md placeholder:text-center border-none bg-lighter-black px-1 font-semibold"
          v-model="newSearch"
          placeholder="-"
        />
        <button class="btn btn-primary" type="submit" @click="search">
          {{ $t("table.search") }}
        </button>
      </div>
    </div>
    <div id="loading" v-if="loading.flag">
      <img src="@/assets/spinner.gif" alt="loading" />
      <h3>{{ loading.message }}</h3>
    </div>
    <TheAlert :alert="alert" />

    <TheFailed
      :dataFailed="failed"
      :typeRecord="typeRecord"
      :carton="carton"
      :typeOffer="this.typeOffer"
      :duration="this.duration"
      :clear="this.clear"
      v-if="failedFlag"
    />
  </div>
</template>

<script>
import TheSlider from "@/components/Global/TheSlider.vue";
import TheAlert from "@/components/Global/TheAlert.vue";
import TheFailed from "@/components/Listing/TheFailed.vue";
import axios from "axios";
export default {
  data() {
    return {
      discogsData: "",
      condition: "Near Mint (NM or M-)",
      sleeveCondition: "Near Mint (NM or M-)",
      carton: "",
      title: "",
      label: "",
      country: "",
      year: "",
      genre: "rock",
      barcode: "",
      price: "",
      currentIndex: 0,
      recordIndex: this.typeRecord == "Vinyl" ? 0 : 1,
      offerImages: [],
      failed: [],
      alert: {},
      cartonFlag: false,
      visible: false,
      failedFlag: false,
      loading: { flag: false, message: "" },
      activeRequests: 0,
      newSearch: "",
      userKey: this.$cookies.get("allegro-cred").userKey,
    };
  },
  methods: {
    resetVariables() {
      this.title = "";
      this.label = "";
      this.country = "";
      this.year = "";
      this.price = "";
      this.barcode = "";
      this.condition = "Near Mint (NM or M-)";
    },
    async listingOfferDiscogs(data) {
      if (this.price === "") {
        this.alert = {
          variant: "warning",
          message: this.$t("alerts.complete"),
        };
        return;
      }

      let selectedData = {
        id: data.id,
        condition: this.condition,
        price: this.price,
      };

      // Send data
      this.loading.flag = true;
      this.loading.message = this.$t("loading.listingOffer");

      await axios
        .post(
          `${url}/discogs-listing`,
          {
            userKey: this.userKey,
            listing_id: data.id,
            mediaCondition: this.condition,
            carton: this.carton,
            sleeveCondition: this.sleeveCondition,
            price: this.roundedPriceToEUR(this.price),
          },
          { headers: { "Content-Type": "application/json" } }
        )
        .then((response) => {
          response = response.data;

          if (response.error || response.output.errors) {
            this.failed.push(selectedData);
            this.alert = {
              variant: "danger",
              message: this.$t("alerts.listingFailed"),
            };
          } else {
            this.alert = {
              variant: "success",
              message: this.$t("alerts.listingSuccess"),
            };
          }
        })
        .finally(() => {
          this.activeRequests += 1;
        });

      this.resetVariables();
      await this.next();
    },
    async listingOfferAllegro(data) {
      let selectedData = {};

      if (this.price === "") {
        this.alert = {
          variant: "warning",
          message: this.$t("alerts.complete"),
        };
        return;
      }

      if (data.title !== undefined) {
        selectedData = {
          id: data.id,
          title: data.title,
          label: data.label,
          country: data.country,
          year: data.year,
          genre: data.genre,
          price: this.price,
          barcode: data.barcode,
          quantity: data.quantity,
          images: this.offerImages,
          condition: this.condition,
        };
      } else {
        if (this.title === "" || this.price === "") {
          this.alert = {
            variant: "warning",
            message: this.$t("alerts.complete"),
          };
          return;
        }

        if (this.title.length + 3 >= 50) {
          this.alert = {
            variant: "warning",
            message: this.$t("alerts.toLong"),
          };
          return;
        }

        selectedData = {
          id: "",
          title: this.title,
          label: this.label ? this.label : "-",
          country: this.country ? this.country : "-",
          year: this.year ? this.year : "-",
          genre: this.genre,
          price: this.price,
          barcode: this.barcode ? this.barcode : "-",
          quantity: "",
          images: this.offerImages,
          condition: this.condition,
        };
      }

      // Send data
      this.loading.flag = true;
      this.next();
      const requestData = {
        userKey: this.userKey,
        offer_data: selectedData,
        carton: this.carton,
        typeRecord: this.typeRecord,
        typeOffer: this.typeOffer,
        duration: this.duration,
        clear: this.clear,
      };
      axios
        .post(`${url}/allegro-listing`, requestData)
        .then((response) => {
          response = response.data;
          if (response.error || response.output.errors) {
            this.failed.push(selectedData);
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
          this.activeRequests += 1;

          // Last offer
          if (this.activeRequests == this.numberFiles / this.numberImages) {
            this.next();
          }
        });

      this.resetVariables();
    },
    async next() {
      this.loading.flag = true;
      this.loading.message = this.$t("loading.loadData");
      this.currentIndex += this.numberImages;

      if (this.currentIndex >= this.numberFiles) {
        this.loading.message = "";
        if (this.activeRequests == this.numberFiles / this.numberImages) {
          this.loading.flag = false;
          this.failedFlag = true;
        }
      } else {
        this.offerImages = [];
        axios
          .post(
            `${url}/discogs-information-image`,
            {
              userKey: this.userKey,
              typeRecord: this.typeRecord,
              index: this.currentIndex,
              numberImages: this.numberImages,
            },
            { headers: { "Content-Type": "application/json" } }
          )
          .then((response) => {
            this.discogsData = response.data.output;

            for (let i = 0; i < this.numberImages; i++) {
              this.offerImages.push(this.discogsData[i].url);
            }

            this.offerImages.reverse();
          })
          .catch((error) => {
            console.error("Error:", error);
          })
          .finally(() => {
            this.loading.message = "";
            this.loading.flag = false;
          });
      }
    },
    async search() {
      this.loading.flag = true;
      this.loading.message = this.$t("loading.loadData");

      axios
        .post(
          `${url}/discogs-information-new-search`,
          {
            userKey: this.userKey,
            newSearch: this.newSearch,
            typeRecord: this.typeRecord,
          },
          { headers: { "Content-Type": "application/json" } }
        )
        .then((response) => {
          this.discogsData = response.data.output;

          this.newSearch = "";
          this.loading.message = "";
          this.loading.flag = false;
        });
    },
    roundedPriceToPLN(price) {
      let finalValue;
      if (price) {
        const roundedValue = Math.round((price.value * 3) / 10) * 10 - 0.01;
        finalValue = roundedValue < 19.99 ? 19.99 : roundedValue;
      } else {
        finalValue = 0;
      }
      return finalValue;
    },
    roundedPriceToEUR(price) {
      let finalValue;
      if (price) {
        const roundedValue = Math.round((price * 0.3) / 10) * 10 - 0.01;
        finalValue = roundedValue < 3.99 ? 3.99 : roundedValue;
      } else {
        finalValue = 0;
      }
      return finalValue;
    },
    confirmCarton() {
      if (this.carton != ""){
        this.cartonFlag = true;
      }
    },
    showImage() {
      this.show();
    },
    show() {
      this.visible = true;
    },
    handleHide() {
      this.visible = false;
    },
  },
  async beforeMount() {
    this.loading.flag = false;
    this.loading.message = this.$t("loading.loadData");
    await axios
      .post(
        `${url}/discogs-information-image`,
        {
          userKey: this.userKey,
          typeRecord: this.typeRecord,
          index: 0,
          numberImages: this.numberImages,
        },
        { headers: { "Content-Type": "application/json" } }
      )
      .then((response) => {
        this.discogsData = response.data.output;
        for (let i = 0; i < this.numberImages; i++) {
          this.offerImages.push(this.discogsData[i].url);
        }
        this.offerImages.reverse();
      })
      .catch((error) => {
        this.alert = {
          variant: "danger",
          message: this.$t("alerts.someWrong"),
        };
        console.error("Error:", error);
      })
      .finally(() => {
        this.loading.message = "";
        this.loading.flag = false;
      });
  },
  props: {
    typeRecord: {
      type: String,
      required: true,
    },
    typeOffer: {
      type: String,
      required: true,
    },
    duration: {
      type: String,
      required: true,
    },
    clear: {
      type: Boolean,
      required: true,
    },
    numberImages: {
      type: Number,
      required: true,
      integer: true,
    },
    numberFiles: {
      type: Number,
      required: true,
      integer: true,
    },
    conditions: {
      type: Array,
      required: false,
    },
  },
  components: {
    TheSlider,
    TheAlert,
    TheFailed,
  },
};
</script>
