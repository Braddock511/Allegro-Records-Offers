<template>
  <section v-if="!loading && !displaySpecific">
    <form>
      <div class="text-3xl text-white font-semibold text-center">
        {{ $t("swap.title") }}
      </div>
      <div class="text-xl text-center w-full">{{ $t("swap.info") }}</div>
      <div
        class="w-full justify-center items-center flex-wrap md:flex-nowrap flex-col flex md:flex-row md:gap-10"
      >
        <div class="mt-5 flex flex-col gap-1 items-center">
          <span class="text-base text-slate-100 h-auto min-h-[28px]">{{
            $t("swap.swap")
          }}</span>
          <input
            type="text"
            name="swap"
            v-model="swapCarton"
            class="bg-lighter-black w-52 rounded-md text-white px-2 h-auto min-h-[28px]"
          />
          <button
            class="btn btn-primary w-full"
            type="submit"
            @click="swap"
            style="
              max-height: 1.75rem !important;
              min-height: 1.75rem !important;
            "
          >
            {{ $t("swap.swapAll") }}
          </button>
        </div>
        <div class="h-auto min-h-[28px] mt-6">
          <v-icon name="co-swap-horizontal" class="text-white" scale="1.2" />
        </div>
        <div class="mt-5 flex flex-col gap-2 items-center">
          <span class="text-base h-auto text-slate-100 min-h-[28px]">{{
            $t("swap.with")
          }}</span>
          <input
            type="text"
            name="with"
            v-model="withCarton"
            class="bg-lighter-black w-52 rounded-md text-white px-2 h-auto min-h-[28px]"
          />
          <button
            class="btn btn-primary w-full"
            type="submit"
            @click="displaySpecific = true"
            style="max-height: 1.7rem !important; min-height: 1.7rem !important"
          >
            {{ $t("swap.swapSpecific") }}
          </button>
        </div>
      </div>
    </form>
  </section>

  <section v-if="!loading && displaySpecific">
    <form class="mt-10">
      <div class="text-3xl text-white font-semibold text-center">
        {{ $t("swap.title") }}
      </div>
      <div class="text-xl text-center">
        {{ $t("swap.info") }}
      </div>
      <div
        class="w-full justify-center items-center flex-wrap md:flex-nowrap flex-col flex md:flex-row md:gap-10"
      >
        <div class="mt-5 flex flex-col gap-1 items-center">
          <span class="text-base h-auto min-h-[28px] text-slate-100">
            {{ $t("editSpecific.offerId") }}</span
          >
          <input
            type="text"
            name="offer-id"
            v-model="offerId"
            class="bg-lighter-black w-52 rounded-md text-white px-2 h-auto min-h-[28px]"
          />
          <button
            class="btn btn-primary w-full"
            type="submit"
            @click="swapSpecific"
            style="max-height: 1.7rem !important; min-height: 1.7rem !important"
          >
            {{ $t("swap.swapOffer") }}
          </button>
        </div>
        <div class="h-auto min-h-[28px] mt-6">
          <v-icon name="co-swap-horizontal" class="text-white" scale="1.2" />
        </div>
        <div class="mt-5 flex flex-col gap-2 items-center h-auto">
          <span class="text-base h-auto min-h-[28px] text-slate-100">
            {{ $t("swap.orFile") }}</span
          >
          <input
            type="file"
            name="with"
            accept=".txt"
            ref="fileInput"
            @change="handleIdsFile"
            class="bg-lighter-black w-full rounded-md text-white px-2 h-auto min-h-[28px] hidden"
          />
          <button
            class="bg-lighter-black w-full rounded-md text-white px-2 h-auto min-h-[28px]"
            type="button"
            @click="openFileInput"
          >
            <span
              class="bg-gray-400 px-4 text-black rounded-xl text-base font-semibold"
            >
              {{ $t("table.inputFile") }}</span
            >
          </button>
          <button
            class="btn btn-primary w-full"
            type="submit"
            @click="displaySpecific = false"
            style="max-height: 1.7rem !important; min-height: 1.7rem !important"
          >
            {{ $t("table.back") }}
          </button>
        </div>
      </div>
    </form>
  </section>

  <div id="loading" v-if="loading">
    <img src="@/assets/spinner.gif" alt="loading" />
  </div>
  <TheAlert :alert="alert" />
</template>

<script>
import TheAlert from "@/components/Global/TheAlert.vue";
import axios from "axios";
export default {
  data() {
    return {
      swapCarton: "",
      withCarton: "",
      offerId: "",
      offersId: [],
      displaySpecific: false,
      alert: {},
      loading: false,
      userKey: this.$cookies.get("allegro-cred").userKey,
    };
  },
  methods: {
    openFileInput() {
      this.$refs.fileInput.click();
    },

    async swap() {
      this.loading = true;
      const response = (
        await axios.post(`${url}/swap-all`, {
          userKey: this.userKey,
          swapCarton: this.swapCarton,
          withCarton: this.withCarton,
        })
      ).data;
      if (response.error || response.errors) {
        this.alert = {
          variant: "danger",
          message: this.$t("alerts.someWrong"),
        };
      } else {
        this.alert = { variant: "success", message: this.$t("alerts.success") };
      }
      this.loading = false;
    },
    async swapSpecific() {
      this.loading = true;
      if (this.offersId.length == 0) {
        const response = (
          await axios.post(`${url}/swap-specific`, {
            userKey: this.userKey,
            swapCarton: this.swapCarton,
            withCarton: this.withCarton,
            offerId: this.offerId,
          })
        ).data;
        if (response.error || response.errors) {
          this.alert = {
            variant: "danger",
            message: this.$t("alerts.someWrong"),
          };
        } else {
          this.alert = {
            variant: "success",
            message: this.$t("alerts.success"),
          };
        }
      } else {
        for (let i = 0; i < this.offersId.length; i++) {
          const id = this.offersId[i];
          const response = (
            await axios.post(`${url}/swap-specific`, {
              userKey: userKey,
              swapCarton: this.swapCarton,
              withCarton: this.withCarton,
              offerId: id,
            })
          ).data;

          if (response.error || response.errors) {
            this.alert = {
              variant: "danger",
              message: this.$t("alerts.someWrong"),
            };
          } else {
            this.alert = {
              variant: "success",
              message: this.$t("alerts.success"),
            };
          }
        }
      }

      this.offerId = "";
      this.offersId = [];
      this.loading = false;
    },
    handleIdsFile(event) {
      const file = event.target.files[0];
      this.idsFile = file;
      const reader = new FileReader();
      reader.onload = () => {
        const content = reader.result;
        this.validateAndSave(content);
      };
      reader.readAsText(this.idsFile);
    },
    validateAndSave(content) {
      const lines = content.includes("\n")
        ? content.split("\n")
        : content.split(" ");
      const processedLines = lines.map((line) => line.trim());
      this.offersId = this.offersId.concat(processedLines).reverse();
    },
  },
  components: {
    TheAlert,
  },
};
</script>
