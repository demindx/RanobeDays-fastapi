<script setup>
import { computed } from 'vue'
import { useProfile } from '../../composables/useProfile'

const { calendar } = useProfile()

const MONTHS = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
const DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

const weeks = computed(() => {
  const result = []
  const startDate = new Date(calendar.value[0].date)
  const dayOffset = (startDate.getDay() + 6) % 7

  for (let i = 0; i < dayOffset; i++) {
    result.push(null)
  }

  for (const entry of calendar.value) {
    result.push(entry)
  }

  while (result.length % 7 !== 0) {
    result.push(null)
  }

  const chunked = []
  for (let i = 0; i < result.length; i += 7) {
    chunked.push(result.slice(i, i + 7))
  }
  return chunked
})

const monthLabels = computed(() => {
  const labels = []
  const seenMonths = new Set()
  weeks.value.forEach((week, weekIndex) => {
    const firstDay = week.find((d) => d !== null)
    if (!firstDay) return
    const monthKey = firstDay.date.slice(0, 7)
    if (seenMonths.has(monthKey)) return
    seenMonths.add(monthKey)
    labels.push({
      month: MONTHS[new Date(firstDay.date).getMonth()],
      weekIndex,
    })
  })
  return labels
})

const totalChapters = computed(() => calendar.value.reduce((sum, d) => sum + d.count, 0))

const getColor = (count) => {
  if (count === 0) return 'bg-zinc-800'
  if (count <= 2) return 'bg-emerald-900/70'
  if (count <= 5) return 'bg-emerald-700/80'
  if (count <= 8) return 'bg-emerald-500'
  return 'bg-emerald-300'
}
</script>

<template>
  <div class="rounded-2xl border border-zinc-700/70 bg-zinc-900/80 px-4 py-5 sm:px-6">
    <div class="mb-3 flex items-center justify-between">
      <div>
        <h3 class="text-base font-semibold text-white">Активность чтения</h3>
        <p class="text-sm text-zinc-400">{{ totalChapters }} глав за последние 4 месяца</p>
      </div>
      <div class="hidden items-center gap-1 text-xs text-zinc-500 sm:flex">
        <span>Меньше</span>
        <span class="h-3 w-3 rounded-sm bg-zinc-800" />
        <span class="h-3 w-3 rounded-sm bg-emerald-900/70" />
        <span class="h-3 w-3 rounded-sm bg-emerald-700/80" />
        <span class="h-3 w-3 rounded-sm bg-emerald-500" />
        <span class="h-3 w-3 rounded-sm bg-emerald-300" />
        <span>Больше</span>
      </div>
    </div>

    <div class="overflow-x-auto pb-2">
      <div class="flex" style="min-width: min-content">
        <div class="mr-1 grid grid-rows-7 gap-[2px] pr-2 pt-[18px]">
          <span
            v-for="(day, idx) in DAYS"
            :key="day"
            :class="['text-[10px] leading-3 text-zinc-600', idx % 2 === 1 ? 'invisible' : '']"
            style="height: 12px"
          >
            {{ day }}
          </span>
        </div>

        <div>
          <div class="mb-1 flex text-[10px] text-zinc-600" style="height: 16px">
            <template v-for="(label, idx) in monthLabels" :key="label.month">
              <span
                :style="{
                  marginLeft:
                    idx === 0
                      ? label.weekIndex * 14 + 'px'
                      : (label.weekIndex - monthLabels[idx - 1].weekIndex - 1) * 14 + 'px',
                  marginRight: '2px',
                }"
              >
                {{ label.month }}
              </span>
            </template>
          </div>

          <div class="flex gap-[2px]">
            <div v-for="(week, weekIdx) in weeks" :key="weekIdx" class="grid grid-rows-7 gap-[2px]">
              <div
                v-for="(day, dayIdx) in week"
                :key="dayIdx"
                :class="['h-3 w-3 rounded-sm', day ? getColor(day.count) : 'bg-transparent']"
                :title="day ? `${day.date}: ${day.count} глав(ы)` : ''"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
