import { createApp } from "vue";
import router from "./router";
import App from "./App.vue";
import VueCookies from "vue-cookies";
import { createI18n } from "vue-i18n";
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import messages from "./messages.js";

const i18n = createI18n({
  locale: "en",
  messages,
});

const vuetify = createVuetify({
  components,
  directives,
});

const app = createApp(App);

app.use(vuetify);
app.use(router);
app.use(VueCookies);
app.use(i18n);
app.mount("#app");

// import 'bootstrap/dist/js/bootstrap.js'
import "./assets/main.scss";
