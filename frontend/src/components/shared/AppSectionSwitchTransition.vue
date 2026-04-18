<template>
	<Transition name="app-section-switch" mode="out-in">
		<slot />
	</Transition>
</template>

<style>
	.app-section-switch-enter-active,
	.app-section-switch-leave-active {
		transition: opacity 0.22s ease, transform 0.22s ease;
	}

	.app-section-switch-enter-from,
	.app-section-switch-leave-to {
		opacity: 0;
		transform: translateY(8px);
	}
</style>
