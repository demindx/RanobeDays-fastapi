<template>
	<div class="grid gap-4 lg:grid-cols-12">
		<aside class="lg:col-span-4 xl:col-span-3">
			<slot name="sidebar" />
		</aside>
		<section class="lg:col-span-8 xl:col-span-9">
			<slot name="content" />
		</section>
	</div>
</template>
