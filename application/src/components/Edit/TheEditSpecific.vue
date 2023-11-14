<template>
  <span>
    <section class="" v-if="!discogsData && !loading">
      <form class="flex flex-col items-center gap-2">
        <div class="text-2xl text-white font-bold">
          {{ $t("editSpecific.offerId") }}
        </div>
        <div class="">
          <input
            type="text"
            name="offer-id"
            v-model="offerId"
            required
            class="text-center bg-light-black rounded-lg px-10"
          />
        </div>
        <div class="flex gap-2 flex-wrap justify-center flex-column">
          <label class="label cursor-pointer gap-1">
            <span class="label-text text-base">
              {{ $t("editSpecific.editPrice") }}</span
            >
            <input
              type="checkbox"
              checked="checked"
              v-model="editPrice"
              class="checkbox h-5 w-5 checkbox-primary bg-gray-600"
            />
          </label>
          <label class="label cursor-pointer gap-1">
            <span class="label-text text-base">
              {{ $t("editSpecific.editDescription") }}</span
            >
            <input
              type="checkbox"
              v-model="editDescription"
              checked="checked"
              class="checkbox h-5 w-5 checkbox-primary bg-gray-600"
            />
          </label>
          <label class="label cursor-pointer gap-1">
            <span class="label-text text-base tracking-tight">
              {{ $t("editSpecific.toBuy") }}</span
            >
            <input
              type="checkbox"
              v-model="toBuy"
              checked="checked"
              class="checkbox h-5 w-5 checkbox-primary bg-gray-600"
            />
          </label>
        </div>
        <button class="btn btn-primary w-40" type="submit" @click="getOffer">
          {{ $t("editSpecific.edit") }}
        </button>
      </form>
    </section>
  </span>
  <span v-if="!loading">
    <div class="flex flex-col items-center mt-10" v-if="discogsData">
      <TheSlider :images="img.slice()" @click="displayTable"></TheSlider>
      <div class="flex gap-4">
        <button class="btn btn-primary w-32" type="type" @click="editImage">
          {{ $t("editSpecific.clearImage") }}
        </button>
        <button
          class="btn btn-primary w-32"
          type="type"
          @click="
            discogsData = '';
            alert = {};
          "
        >
          {{ $t("table.back") }}
        </button>
      </div>
      <div id="tableData" className="overflow-x-auto w-full custom-scrollbar">
        <table class="mt-10 table table-sm">
          <thead class="thead-css h-14 text-base">
            <tr>
              <th></th>
              <th>
                {{ $t("table.label") }}
              </th>
              <th>
                {{ $t("table.country") }}
              </th>
              <th>
                {{ $t("table.year") }}
              </th>
              <th v-if="!editPrice">
                <div class="relative">
                  <label
                    for="condition"
                    class="absolute flex justify-center items-center -top-[2px] left-1 h-[1.5px] bg-oceans px-1 text-xs font-semibold"
                    >{{ $t("table.price") }}</label
                  >
                  <select
                    id="condition"
                    v-model="condition"
                    @change="this.price = ''"
                    class="select-css font-semibold h-8 p-1 rounded-md placeholder:text-center border-1 bg-oceans px- outline-none"
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
              </th>
              <th>{{ $t("table.price") }}</th>
              <th>{{ $t("editSpecific.editOffer") }}</th>
              <th>
                {{ $t("editSpecific.listingSimilar") }}
              </th>
            </tr>
          </thead>
          <tbody class="tab-css">
            <tr class="bg-darker-gray">
              <th class="text-transparent"></th>
              <td>
                <input
                  type="text"
                  name="label"
                  class="h-8 rounded-md placeholder:text-center bg-oceans px-1 font-semibold hover:bg-opacity-0"
                  placeholder="Label"
                  v-model="label"
                />
              </td>
              <td>
                <input
                  type="text"
                  name="country"
                  class="h-8 rounded-md placeholder:text-center bg-oceans px-1 font-semibold hover:bg-opacity-0"
                  placeholder="Country"
                  v-model="country"
                />
              </td>
              <td>
                <input
                  type="text"
                  name="year"
                  class="h-8 rounded-md placeholder:text-center bg-oceans px-1 font-semibold hover:bg-opacity-0"
                  placeholder="Year"
                  v-model="year"
                />
              </td>
              <td v-if="editPrice">
                <input
                  type="text"
                  name="price"
                  class="h-8 rounded-md placeholder:text-center bg-oceans px-1 font-semibold hover:bg-opacity-0"
                  placeholder="Price"
                  v-model="price"
                />
              </td>
              <td>
                <button
                  class="btn btn-primary w-full"
                  type="type"
                  style="
                    max-height: 2rem !important;
                    min-height: 2rem !important;
                  "
                  @click="editOffer"
                >
                  {{ $t("editSpecific.edit") }}
                </button>
              </td>
              <td>
                <button
                  class="btn btn-primary w-full"
                  type="type"
                  style="
                    max-height: 2rem !important;
                    min-height: 2rem !important;
                  "
                  @click="
                    listing_similar = true;
                    editOffer({});
                  "
                >
                  {{ $t("table.send") }}
                </button>
              </td>
            </tr>
            <tr
              v-for="(data, index) in discogsData.output[0].information"
              v-if="discogsData && discogsData.output"
              class="mapping odd:bg-dark-gray even:bg-lighter-gray"
            >
              <th class="number-css">{{ index + 1 }}</th>
              <td>
                <span v-if="data.label !== '-'">{{ data.label }}</span>
                <input
                  v-else
                  type="text"
                  name="label"
                  placeholder="Label"
                  class="h-8 rounded-md placeholder:text-center bg-oceans px-1 font-semibold hover:bg-opacity-0"
                  v-model="label"
                />
              </td>
              <td>
                <span v-if="data.country !== '-'">{{ data.country }}</span>
                <input
                  v-else
                  type="text"
                  name="country"
                  placeholder="Country"
                  v-model="country"
                  class="h-8 rounded-md placeholder:text-center bg-oceans px-1 font-semibold hover:bg-opacity-0"
                />
              </td>
              <td>
                <span v-if="data.year !== '-'">{{ data.year }}</span>
                <input
                  v-else
                  type="text"
                  name="year"
                  placeholder="Year"
                  v-model="year"
                  class="h-8 rounded-md placeholder:text-center bg-oceans px-1 font-semibold hover:bg-opacity-0"
                />
              </td>
              <td
                v-if="
                  editPrice &&
                  data.price[
                    condition == 'Excellent (EX)'
                      ? 'Very Good Plus (VG+)'
                      : condition
                  ] !== undefined
                "
              >
                <div class="relative">
                  <label
                    :for="`price-${index}`"
                    :class="
                      index % 2 === 0 ? 'bg-lighter-gray  ' : 'bg-dark-gray'
                    "
                    class="absolute flex justify-center items-center h-1 text-gray-300 left-1 bg-oceans px-1 text-sm font-semibold"
                  >
                    Want: {{ data.community.want }} | Have:
                    {{ data.community.have }}</label
                  >
                  <input
                    type="number"
                    name="price"
                    :id="`price-${index}`"
                    class="h-8 rounded-md placeholder:text-center bg-oceans px-1 font-semibold"
                    min="1"
                    :placeholder="
                      roundedPrice(
                        data.price[
                          condition == 'Excellent (EX)'
                            ? 'Very Good Plus (VG+)'
                            : condition
                        ]
                      )
                    "
                    v-model="price"
                    @click="
                      price = roundedPrice(
                        data.price[
                          condition == 'Excellent (EX)'
                            ? 'Very Good Plus (VG+)'
                            : condition
                        ]
                      )
                    "
                  />
                </div>
              </td>
              <td
                v-if="
                  editPrice &&
                  data.price[
                    condition == 'Excellent (EX)'
                      ? 'Very Good Plus (VG+)'
                      : condition
                  ] === undefined
                "
              >
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
                    min="1"
                    v-model="price"
                    :id="`price-${index}`"
                    class="h-8 rounded-md placeholder:text-center bg-oceans px-1 font-semibold"
                  />
                </div>
              </td>
              <td>
                <button
                  class="btn btn-primary w-full"
                  style="
                    max-height: 1.75rem !important;
                    min-height: 1.75rem !important;
                  "
                  type="type"
                  @click="editOffer(data)"
                >
                  {{ $t("editSpecific.edit") }}
                </button>
              </td>
              <td>
                <button
                  class="btn btn-primary w-full"
                  style="
                    max-height: 1.75rem !important;
                    min-height: 1.75rem !important;
                  "
                  type="type"
                  @click="
                    listing_similar = true;
                    editOffer(data);
                  "
                >
                  {{ $t("table.send") }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
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
    </div>
  </span>
  <div id="loading" v-if="loading">
    <img src="@/assets/spinner.gif" alt="loading" />
  </div>
  <TheAlert :alert="alert" />
</template>

<script>
import TheAlert from "@/components/Global/TheAlert.vue";
import TheSlider from "@/components/Global/TheSlider.vue";
import axios from "axios";
export default {
  data() {
    return {
      allegroData: "",
      discogsData: "",
      offerId: "",
      img: "s",
      label: "",
      country: "",
      year: "",
      price: "",
      condition: "Near Mint (NM or M-)",
      newSearch: "",
      loading: false,
      listing_similar: false,
      alert: {},
      userKey: this.$cookies.get("allegro-cred").userKey,
      editPrice: false,
      editDescription: false,
      toBuy: false,
    };
  },
  methods: {
    async getOffer() {
      this.loading = true;
      this.allegroData = (
        await axios.post(`${url}/allegro-offer`, {
          userKey: this.userKey,
          offerId: this.offerId,
        })
      ).data;
      if (this.allegroData.error || this.allegroData.errors) {
        this.alert = {
          variant: "danger",
          message: this.$t("alerts.someWrong"),
        };
      } else {
        this.allegroData = this.allegroData.output;
        await axios
          .post(`${url}/discogs-information`, {
            userKey: this.userKey,
            index: 0,
            allegroData: this.allegroData,
          })
          .then((response) => {
            this.discogsData = response.data;

            if (this.discogsData.status == 500) {
              this.alert = {
                variant: "danger",
                message: `${this.$t("alerts.failed")} - ${
                  this.discogsData.error
                }`,
              };
              this.discogsData = "";
            } else {
              this.img = this.discogsData.offer.images;
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }
      this.loading = false;
    },
    async editOffer(data) {
      let selectedData = {};
      selectedData = {
        id: data.id,
        label: data.label != "-" ? data.label : this.label,
        country: data.country != "-" ? data.country : this.country,
        year: data.year != "-" ? data.year : this.year,
        price: this.price,
      };

      if (selectedData.id === undefined) {
        selectedData = {
          id: "-",
          label: this.label ? this.label : "-",
          country: this.country ? this.country : "-",
          year: this.year ? this.year : "-",
          price: this.price,
        };
      }
      // Edit offer
      this.loading = true;
      axios
        .post(`${url}/allegro-edit`, {
          userKey: this.userKey,
          offerId: this.offerId,
          images: this.img,
          newEditData: selectedData,
          listingSimilar: this.listing_similar,
          editPrice: this.editPrice,
          editDescription: this.editDescription,
          toBuy: this.toBuy,
        })
        .then((response) => {
          const responseData = response.data;
          if (responseData.status == 500) {
            this.alert = {
              variant: "danger",
              message: `${this.$t("alerts.failed")} - ${
                responseData.error.errors[0].userMessage
              }`,
            };
          } else {
            this.alert = {
              variant: "success",
              message: this.$t("alerts.success"),
            };
            this.discogsData = "";
            this.offerId = "";
            this.label = "";
            this.country = "";
            this.year = "";
            this.price = "";
          }
          this.loading = false;
        })
        .catch((error) => {
          this.alert = {
            variant: "danger",
            message: `${this.$t("alerts.failed")} - ${error}`,
          };
          this.loading = false;
        });
      this.listing_similar = false;
    },
    async editImage() {
      this.loading = true;

      axios
        .post(`${url}/clear-image`, {
          userKey: this.userKey,
          image: this.img[0],
        })
        .then((response) => {
          this.clearImage = response.data.output;
        })
        .catch((error) => {
          console.error("Error:", error);
        });

      let otherImages = this.img.slice(1, this.img.length);
      let newImages = [this.clearImage, otherImages].flat();
      axios
        .post(`${url}/allegro-edit-image`, {
          userKey: this.userKey,
          offerId: this.offerId,
          images: newImages,
        })
        .then((response) => {
          const responseData = response.data;
          if (responseData.status == 500) {
            this.alert = {
              variant: "danger",
              message: `${this.$t("alerts.failed")} - ${
                responseData.error.errors[0].userMessage
              }`,
            };
          } else {
            this.alert = {
              variant: "success",
              message: this.$t("alerts.imageSuccess"),
            };
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    roundedPrice(price) {
      let finalValue;
      if (price) {
        const roundedValue = Math.round((price.value * 3) / 10) * 10 - 0.01;
        finalValue = roundedValue < 19.99 ? 19.99 : roundedValue;
      } else {
        finalValue = 0;
      }
      return finalValue;
    },
    async search() {
      this.loading = true;
      axios
        .post(
          `${url}/discogs-information-new-search`,
          {
            userKey: this.userKey,
            newSearch: this.newSearch,
            typeRecord: "",
            allegroData: this.allegroData,
          },
          { headers: { "Content-Type": "application/json" } }
        )
        .then((response) => {
          this.discogsData = response.data;

          this.newSearch = "";
          this.loading = false;
        });
    },
  },
  components: {
    TheSlider,
    TheAlert,
  },
};
</script>
