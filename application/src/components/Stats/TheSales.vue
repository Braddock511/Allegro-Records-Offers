<template>
  <span v-if="!loading" style="flex-direction: column; width: 100%">
    <div
      class="data"
      style="
        width: 100%;
        flex-direction: row;
        justify-content: center;
        flex-wrap: wrap;
      "
    >
      <img :src="saleBarplot" alt="bar plot" style="width: 100%" />
    </div>
  </span>
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
      saleBarplot: "",
      loading: false,
      alert: {},
    };
  },
  async beforeMount() {
    if (this.saleBarplot == "") {
      this.loading = true;
      const userKey = this.$cookies.get("allegro-cred").userKey;
      const response = (
        await axios.post(`${url}/sale-barplot`, { userKey: userKey })
      ).data;
      if (response.error || response.errors) {
        this.alert = {
          variant: "danger",
          message: this.$t("alerts.someWrong"),
        };
      } else {
        this.saleBarplot = response.output;
        this.alert = {
          variant: "success",
          message: this.$t("alerts.statistics"),
        };
      }
      this.loading = false;
    }
  },
  components: {
    TheAlert,
  },
};
</script>
