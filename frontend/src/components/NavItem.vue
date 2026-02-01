<script setup>
	const props = defineProps({
		url: {
			type: String,
			default: "#"
		}
	})
</script>


<template>
	<a :href="props.url"><slot/></a>
</template>


<style lang="scss" scoped>
a {
	color: white;
	margin: 10px 40px;
	font-family: Inter;
}
</style>
