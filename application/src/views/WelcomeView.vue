<template>
  <TheNavBar v-if="!isCookieSet" />
  <!-- <span v-if="!loading && !isCookieSet">
    <TheHeader />
    <main>
      <div id="info">
        <h1>{{ $t("info.title") }}</h1>
        <p>{{ $t("info.description") }}</p>
      </div>
      <div
        id="buttons"
        style="display: flex; flex-direction: column; justify-content: center"
      >
        <router-link to="/allegro-credentials"
          ><button
            class="btn btn-primary w-100"
            type="button"
            style="padding: 0.5rem; font-size: 20px"
          >
            {{ $t("buttons.enterAllegroCredentials") }}
          </button></router-link
        >
      </div>
    </main>
  </span> -->
  <div id="loading" v-if="loading">
    <img src="@/assets/spinner.gif" alt="loading" />
    <h3>{{ $t("loading.loadData") }}</h3>
  </div>
  <TheAlert :alert="alert" />
</template>

<script>
import TheHeader from "@/components/Global/TheHeader.vue";
import TheAlert from "@/components/Global/TheAlert.vue";
import TheNavBar from "@/components/Global/TheNavBar.vue";
export default {
  data() {
    return {
      loading: false,
      alert: {},
    };
  },
  computed: {
    isCookieSet() {
      return this.$cookies.get("allegro-cred").flag === true;
    },
  },
  components: {
    TheHeader,
    TheAlert,
    TheNavBar,
  },
};
</script>
<!-- 
<style lang="scss" scoped>
main {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  margin-top: 100px;
  #info {
    width: 40%;
    p {
      font-size: large;
    }
  }

  #buttons {
    width: 22.5%;
  }
}
@media only screen and (max-width: 1200px) {
  main {
    #info {
      width: 55%;
    }

    #buttons {
      width: 40%;
    }
  }
}
@media only screen and (max-width: 700px) {
  main {
    #info {
      width: 60%;
      p {
        font-size: medium;
      }
    }
    #buttons {
      width: 50%;
    }
  }
}
@media only screen and (max-width: 500px) {
  main {
    width: 500px;
  }
}
</style> -->
