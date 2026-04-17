<template>
	<footer class="rounded-2xl border border-zinc-700/70 bg-zinc-900/80 p-4 sm:p-5">
		<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
			<div>
				<h3 class="text-sm font-semibold text-white">RanobeDays</h3>
				<p class="mt-1 text-xs text-zinc-400">Читай любимые новелы каждый день.</p>
			</div>

			<div>
				<p class="text-xs font-semibold uppercase tracking-wide text-zinc-500">Навигация</p>
				<div class="mt-2 space-y-1 text-sm text-zinc-300">
					<a href="#" class="block transition hover:text-white">Главная</a>
					<a href="#" class="block transition hover:text-white">Каталог</a>
					<a href="#" class="block transition hover:text-white">Закладки</a>
				</div>
			</div>

			<div>
				<p class="text-xs font-semibold uppercase tracking-wide text-zinc-500">Поддержка</p>
				<div class="mt-2 space-y-1 text-sm text-zinc-300">
					<a href="#" class="block transition hover:text-white">FAQ</a>
					<a href="#" class="block transition hover:text-white">Контакты</a>
					<a href="#" class="block transition hover:text-white">Политика</a>
				</div>
			</div>

			<div class="sm:col-span-2 lg:col-span-1">
				<p class="text-xs font-semibold uppercase tracking-wide text-zinc-500">Соцсети</p>
				<div class="mt-2 flex gap-2 text-sm text-zinc-300">
					<a href="#" class="rounded-md border border-zinc-700 px-2 py-1 transition hover:bg-zinc-800 hover:text-white">TG</a>
					<a href="#" class="rounded-md border border-zinc-700 px-2 py-1 transition hover:bg-zinc-800 hover:text-white">VK</a>
					<a href="#" class="rounded-md border border-zinc-700 px-2 py-1 transition hover:bg-zinc-800 hover:text-white">YT</a>
				</div>
			</div>
		</div>

		<div class="mt-5 border-t border-zinc-800 pt-3 text-center text-xs text-zinc-500">
			© {{ new Date().getFullYear() }} RanobeDays. Все права защищены.
		</div>
	</footer>
</template>
