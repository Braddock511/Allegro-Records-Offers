import { createApp } from "vue";
import VueCookies from "vue-cookies";
import { createI18n } from "vue-i18n";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "vuetify/styles";
import App from "./App.vue";
import messages from "./messages.js";
import router from "./router";

const i18n = createI18n({
  locale: "pl",
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
