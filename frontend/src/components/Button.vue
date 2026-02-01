<script setup>
	const props = defineProps({
		callback: {
			type: Function,
			required: true
		}
	})
</script>


<template>
	<button class="button" @click="props.callback">
		<slot/>
	</button>
</template>


<style lang="scss" scoped>
.button {
	background-color: var(--first-color);
	border-radius: 8px;
	border: none;
	font-family: Inter;
	font-size: 12px;
	color: var(--foreground-color);
	padding: 2px 10px;
	padding-bottom: 3px;
	cursor: pointer;
	transition: all 0.2s ease;

	&:hover {
		background-color: black;
	}

	&:active {
		background-color: var(--first-color);
	}

	// &:hover{
	// 	background-color: darken($first-color, 10%);
	// 	transform: translateY(-0.1px);
	// 	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	// }
	//
	// &:active{
	// 	background-color: darken($first-color, 15%);
	// 	transform: translateY(0);
	// 	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	// }
}
</style>
