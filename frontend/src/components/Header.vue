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
	<div>header</div>
	<SearchBar placeholder="Поиск"/>
	<Button :callback="test">btn</Button>

	<NavBar>
		<NavItem v-for="n in 10">{{ n }}</NavItem>
	</NavBar>

</template>


<style lang="scss" scoped>
</style>
