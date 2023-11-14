<template>
  <Transition name="slide" class="flex justify-between">
    <div v-if="alert.message" :class="['alert', `alert-${alert.variant}`, 'position-fixed', 'top-0', 'end-0', 'm-3', 'fade', 'show', 'w-25' ]" role="alert">
      {{ alert.message }}
      <button type="button" @click="alert = {}">
        <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </Transition>
</template>

<script>
  import { Transition } from 'vue';
  export default {
    props: {
      alert: {
        type: Object,
        default: {},
      },
    },
    updated(){
      setTimeout(() => {this.alert.message = ""}, 5000)
    },
    components:{
      Transition
    }
  };
</script>

<style scoped>
.alert{
  color: white;
}
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s ease-out, opacity 0.5s ease-out;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.slide-leave-active {
  opacity: 0;
}
</style>