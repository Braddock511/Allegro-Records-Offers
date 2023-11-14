import { createApp } from "vue";
import router from "./router";
import App from "./App.vue";
import VueCookies from "vue-cookies";
import { createI18n } from "vue-i18n";
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { OhVueIcon, addIcons } from "oh-vue-icons";
import {
  MdDatathresholdingOutlined,
  FaFlag,
  RiZhihuFill,
  MdQuerystats,
  IoStatsChart,
  RiFileEditLine,
  HiDocumentAdd,
  RiSwapBoxFill,
  MdLegendtoggleTwotone,
  MdPayment,
  SiAllegro,
  AiAcademiaSquare,
  CoSwapHorizontal,
} from "oh-vue-icons/icons";
import messages from "./messages.js";

addIcons(
  FaFlag,
  RiZhihuFill,
  MdDatathresholdingOutlined,
  IoStatsChart,
  MdQuerystats,
  RiFileEditLine,
  HiDocumentAdd,
  RiSwapBoxFill,
  MdLegendtoggleTwotone,
  MdPayment,
  SiAllegro,
  AiAcademiaSquare,
  CoSwapHorizontal
);

const i18n = createI18n({
  locale: "en",
  messages,
});

const vuetify = createVuetify({
  components,
  directives,
});

const app = createApp(App);
app.component("v-icon", OhVueIcon);
app.use(vuetify);
app.use(router);
app.use(VueCookies);
app.use(i18n);
app.mount("#app");

// import 'bootstrap/dist/js/bootstrap.js'
import "./assets/main.scss";
