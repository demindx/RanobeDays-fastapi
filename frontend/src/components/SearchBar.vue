<template>
  <div class="relative w-full">
    <input
      type="text"
      :placeholder="placeholder"
      class="w-full py-2 px-4 pr-10 rounded-full bg-[#B3CB80] text-[#494949] focus:outline-none focus:ring-2 focus:ring-[#C4FF61]"
    />
    <div
      class="absolute right-3 top-1/2 transform -translate-y-1/2 text-[#494949] cursor-pointer"
      @click="onSearchClick"
    >
      <SearchIcon />
    </div>
  </div>
</template>

<script setup>
import SearchIcon from './icons/SearchIcon.vue';

const props = defineProps({
  placeholder: {
    type: String,
    default: 'Search...'
  },
  onSearch: {
    type: Function,
    default: null
  }
});

const onSearchClick = () => {
  if (props.onSearch) {
    props.onSearch();
  }
};
</script>
