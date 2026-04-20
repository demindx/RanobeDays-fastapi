<script setup>
	import SearchBar from './SearchBar.vue';
	import Button from './Button.vue';

	import NavBar from './NavBar.vue';
	import NavItem from './NavItem.vue';

	function test() {
		console.log("Hello");
	}
</script>


<template>
	<div class="header">
		<SearchBar placeholder="Поиск"/>
		<Button :callback="test">btn</Button>

		<NavBar>
			<NavItem v-for="n in 10">{{ n }}</NavItem>
		</NavBar>

	</div>
</template>


<style lang="scss">
.header {
  width: 100%;
  // Any additional header-specific styles
}
</style>
