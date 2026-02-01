<script setup>
	import SearchIcon from './icons/SearchIcon.vue';
</script>


<template>
	<div class="searchbar">
		<input id="searchbar__input" type="text" class="searchbar__input inset-shadow-sm">
		<SearchIcon class="searchbar__icon"/>
	</div>
</template>


<style lang="scss" scoped>
.searchbar {
	display: flex;

	&__input {
		background-color: var(--secondary-color);
		border: none;
		border-radius: 16px;
		width: 340px;
		height: 25px;

		padding: 0px 10px;

		color: var(--foreground-color);

		box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1) inset;

		&:focus {
			border: none;
			outline: none;
		}

	}

	&__icon {
		position: relative;
		right: 30px;
	}

}
</style>
