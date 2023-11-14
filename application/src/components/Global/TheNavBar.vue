<template>
  <div class="flex overflow-hidden min-h-screen" v-if="!loading">
    <div
      class="absolute top-0 left-0 z-[10] w-screen h-screen bg-black opacity-60 transition-opacity"
      :class="isOpen ? 'flex ' : 'hidden z-0'"
    ></div>
    <nav
      class="relative bg-primary-gray shadow max-h-full min-w-[90px] flex flex-col justify-between transition-all z-50"
      @mouseenter="changeWidth"
      @mouseleave="resetWidth"
    >
      <div
        class="fixed bg-primary-gray shadow max-h-screen custom-scroll overflow-y-auto h-full overflow-x-hidden shadow-neutral-500 px-2 flex flex-col justify-between py-5 transition-all"
        :class="
          isOpen === false
            ? 'fixed transition-all w-[90px]'
            : 'top-0 left-0 z-50 w-[300px] '
        "
      >
        <div class="flex flex-col gap-8">
          <div
            class="w-full text-center pb-4 lg:text-start text-xl font-semibold flex items-center gap-2 text-white border-b-2 border-white transition-none h-[75px]"
          >
            <span
              class="truncate text-slate-300 rounded-full w-9"
              :class="isOpen === false ? 'hidden' : 'block'"
            >
              <img
                class="h-full cursor-pointer w-12"
                src="../../../logo.ico"
                alt="uk"
                @click="changeLanguage('en')"
              />
            </span>

            Allegro Offers
          </div>
          <div
            class="flex flex-col"
            :class="isOpen === false ? 'sm:px-0' : 'sm:px-3'"
          >
            <div class="group">
              <div
                class="xd group-hover:text-blue-600 font-semibold text-sm truncate"
                :class="isOpen === false ? 'text-center' : 'text-start'"
              >
                {{ $t("headerNavBar.listing") }}
              </div>
              <div class="px-2 flex flex-col gap-1 py-1 items-center">
                <div
                  class="flex gap-3 text-icon hover:text-blue-600 font-semibold leading-tight items-center p-2 rounded-lg cursor-pointer border-2 border-transparent hover:bg-gray-800 hover:border-slate-700 hover:border-3 transition-colors text-[0.9rem] group"
                  @click="option = 'listing'"
                  :class="isOpen === false ? 'w-fit' : 'w-full'"
                >
                  <v-icon name="hi-document-add" scale="1.3" class="x" />
                  <span
                    class="truncate text-slate-300"
                    :class="isOpen === false ? 'hidden' : 'block'"
                    >{{ $t("buttons.listingOffers") }}</span
                  >
                </div>
              </div>
            </div>
            <div class="group">
              <div
                class="xd font-semibold text-sm group-hover:text-blue-600"
                :class="isOpen === false ? 'text-center mt-2' : 'text-start'"
              >
                {{ $t("headerNavBar.editOffers") }}
              </div>
              <div
                class="px-2 flex flex-col gap-1 py-1"
                :class="isOpen ? 'items-start' : 'items-center'"
              >
                <div
                  class="flex gap-3 text-icon hover:text-blue-600 font-semibold leading-tight items-center p-2 rounded-lg cursor-pointer border-2 border-transparent hover:bg-gray-800 hover:border-slate-700 hover:border-3 transition-colors text-[0.9rem] truncate"
                  @click="option = 'specific'"
                  :class="isOpen === false ? 'w-fit' : 'w-full'"
                >
                  <v-icon name="ri-file-edit-line" scale="1.3" />
                  <span
                    class="truncate text-slate-300"
                    :class="isOpen === false ? 'hidden ' : 'block'"
                  >
                    {{ $t("editView.specific") }}</span
                  >
                </div>
                <div
                  class="flex gap-3 text-icon hover:text-blue-600 font-semibold leading-tight items-center p-2 rounded-lg cursor-pointer border-2 border-transparent hover:bg-gray-800 hover:border-slate-700 transition-colors hover:border-3 text-[0.9rem]"
                  @click="option = 'swap'"
                  :class="isOpen === false ? 'w-fit' : 'w-full'"
                >
                  <v-icon name="ri-swap-box-fill" scale="1.3" />
                  <span
                    class="truncate text-slate-300"
                    :class="isOpen === false ? 'hidden' : 'block'"
                  >
                    {{ $t("editView.swap") }}
                  </span>
                </div>
              </div>
            </div>
            <div class="group">
              <div
                class="text-sm xd font-semibold truncate group-hover:text-blue-600"
                :class="isOpen === false ? 'text-center mt-2' : 'text-start'"
              >
                {{ $t("headerNavBar.statistics") }}
              </div>
              <div
                class="px-2 flex flex-col gap-1 py-1"
                :class="isOpen ? 'items-start' : 'items-center'"
              >
                <div
                  class="flex gap-3 text-icon hover:text-blue-600 font-semibold leading-tight items-center p-2 rounded-lg cursor-pointer border-2 border-transparent hover:bg-gray-800 hover:border-slate-700 transition-colors hover:border-3 text-[0.9rem]"
                  @click="option = 'visitors'"
                  :class="isOpen === false ? 'w-fit' : 'w-full'"
                >
                  <v-icon name="md-datathresholding-outlined" scale="1.3" />
                  <span
                    class="truncate text-slate-300"
                    :class="isOpen === false ? 'hidden' : 'block'"
                  >
                    {{ $t("statistics.visitorsViewers") }}</span
                  >
                </div>
                <div
                  class="flex gap-3 text-icon hover:text-blue-600 font-semibold leading-tight items-center p-2 rounded-lg cursor-pointer border-2 border-transparent hover:bg-gray-800 hover:border-slate-700 transition-colors hover:border-3 text-[0.9rem]"
                  @click="option = 'sales'"
                  :class="isOpen === false ? 'w-fit' : 'w-full'"
                >
                  <v-icon name="io-stats-chart" scale="1.3" />
                  <span
                    class="truncate text-slate-300"
                    :class="isOpen === false ? 'hidden' : 'block'"
                    >{{ $t("statistics.sales") }}</span
                  >
                </div>
                <div
                  class="flex gap-3 text-icon hover:text-blue-600 font-semibold leading-tight items-center p-2 rounded-lg cursor-pointer border-2 border-transparent hover:bg-gray-800 hover:border-slate-700 transition-colors hover:border-3 text-[0.9rem]"
                  @click="option = 'genres'"
                  :class="isOpen === false ? 'w-fit' : 'w-full'"
                >
                  <v-icon name="md-legendtoggle-twotone" scale="1.3" />
                  <span
                    class="truncate text-slate-300"
                    :class="isOpen === false ? 'hidden' : 'block'"
                    >{{ $t("statistics.genres") }}</span
                  >
                </div>
              </div>
            </div>
            <div class="group">
              <div
                class="text-sm xd font-semibold group-hover:text-blue-600"
                :class="isOpen === false ? 'text-center mt-2' : 'text-start'"
              >
                {{ $t("headerNavBar.other") }}
              </div>
              <div
                class="px-2 flex flex-col gap-1 py-1"
                :class="isOpen === false ? 'items-center' : 'items-start'"
              >
                <div
                  class="flex gap-3 text-icon hover:text-blue-600 font-semibold leading-tight items-center p-2 rounded-lg cursor-pointer border-2 border-transparent hover:bg-gray-800 hover:border-slate-700 transition-colors hover:border-3 text-[0.9rem]"
                  @click="refreshDatabase"
                  :class="isOpen === false ? 'w-fit' : 'w-full'"
                >
                  <v-icon name="md-payment" scale="1.3" />
                  <span
                    class="truncate text-slate-300"
                    :class="isOpen === false ? 'hidden' : 'block'"
                    >{{ $t("buttons.refresh") }}</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
        <div
          class="flex flex-col gap-5 h-auto mt-6"
          :class="isOpen === false ? 'items-center' : 'items-start mt-0'"
        >
          <div
            class="flex w-fit gap-2 justify-start px-3 z-10"
            :class="isOpen === false ? 'flex-col' : 'h-12'"
          >
            <img
              src="@/assets/poland.png"
              alt="poland"
              @click="changeLanguage('pl')"
              class="h-full cursor-pointer w-12"
            />
            <img
              class="h-full cursor-pointer w-12"
              src="@/assets/uk.png"
              alt="uk"
              @click="changeLanguage('en')"
            />
          </div>
          <div
            class="w-full h-10 flex px-2 gap-3 items-center bg-gray-800 py-7 rounded-lg truncate"
            :class="isOpen ? 'justify-start' : 'justify-center'"
          >
            <div
              class="truncate text-slate-300"
            >
              {{ login }}
            </div>
          </div>
        </div>
      </div>
    </nav>
    <div
      class="overflow-x-auto p-5 w-full"
      :class="isOpen ? 'blur-[2px]' : 'blur-none'"
    >
      <main v-if="!loading">
        <TheListingOptions v-if="option == 'listing'" />
        <TheEditSpecific v-if="option == 'specific'" />
        <TheSwap v-if="option == 'swap'" />
        <TheVisitors v-if="option == 'visitors'" />
        <TheSales v-if="option == 'sales'" />
        <TheGenres v-if="option == 'genres'" />
      </main>

      <TheAlert :alert="alert" />
    </div>
  </div>
  <div id="loading" v-if="loading">
    <img src="@/assets/spinner.gif" alt="loading" />
  </div>
</template>

<script>
import axios from "axios";
import TheAlert from "@/components/Global/TheAlert.vue";
import TheListingOptions from "@/components/Listing/TheListingOptions.vue";
import TheEditSpecific from "@/components/Edit/TheEditSpecific.vue";
import TheSwap from "@/components/Edit/TheSwap.vue";
import TheVisitors from "@/components/Stats/TheVisitors.vue";
import TheGenres from "@/components/Stats/TheGenres.vue";
import TheSales from "@/components/Stats/TheSales.vue";

export default {
  data() {
    return {
      option: "listing",
      login: this.$cookies.get("allegro-cred").login,
      loading: false,
      alert: {},
      divWidth: 90,
      isOpen: false,
    };
  },
  mounted() {
    window.addEventListener("resize", this.handleWindowResize);

    this.handleWindowResize();
  },
  destroyed() {
    window.removeEventListener("resize", this.handleWindowResize);
  },
  methods: {
    handleWindowResize() {
      if (window.innerWidth < 1024 && this.isOpen) {
        this.changeWidth();
      } else if (window.innerWidth < 1024 && !this.isOpen) {
        this.resetWidth();
      }
    },
    changeWidth() {
      this.divWidth = 300;
      this.isOpen = true;
    },
    resetWidth() {
      this.divWidth = 90;
      this.isOpen = false;
    },
    async refreshDatabase() {
      this.loading = true;
      const userKey = this.$cookies.get("allegro-cred").userKey;

      await axios.post(`${url}/refresh-database`, { userKey: userKey });
      await axios.post(`${url}/store-all-offers`, { userKey: userKey });
      await axios.post(`${url}/store-all-payments`, { userKey: userKey })
      .finally(() => {
          this.loading = false;
      });

    },
    changeLanguage(locale) {
      this.$i18n.locale = locale;
    },
  },
  components: {
    TheAlert,
    TheListingOptions,
    TheEditSpecific,
    TheSwap,
    TheVisitors,
    TheGenres,
    TheSales,
  },
};
</script>
