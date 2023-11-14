<template>
  <header
    class="h-20 bg-darker-gray flex justify-between items-center relative"
  >
    <span class="text-2xl title-css text-white font-semibold text-start ml-4"
      >Allegro Offers</span
    >
    <div
      class="h-full w-fit flex items-center py-4 gap-3 mr-5 absolute right-0"
    >
      <img
        src="@/assets/poland.png"
        alt="poland"
        class="h-full cursor-pointer"
        @click="changeLanguage('pl')"
      />
      <img
        src="@/assets/uk.png"
        alt="uk"
        @click="changeLanguage('en')"
        class="h-full cursor-pointer"
      />
    </div>
  </header>
</template>

<script>
export default {
  methods: {
    changeLanguage(locale) {
      this.$i18n.locale = locale;
    },
  },
};
</script>
