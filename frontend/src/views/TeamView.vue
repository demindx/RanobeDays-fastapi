<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppTabs from '../components/shared/AppTabs.vue'
import AppPanel from '../components/shared/AppPanel.vue'
import AppEmptyState from '../components/shared/AppEmptyState.vue'
import AppSectionSwitchTransition from '../components/shared/AppSectionSwitchTransition.vue'
import NovelGridCard from '../components/cards/NovelGridCard.vue'
import { useTeamPage } from '../composables/useTeamPage'

const route = useRoute()
const teamId = computed(() => String(route.params.id || 'team-1'))
const { team, members, novels, tabs, activeTab, setActiveTab, roleLabel } = useTeamPage(teamId)

const roleBadgeClass = (role) => {
  const map = {
    creator: 'border-emerald-300/40 bg-emerald-400/15 text-emerald-200',
    manager: 'border-blue-300/40 bg-blue-400/15 text-blue-200',
    translator: 'border-violet-300/40 bg-violet-400/15 text-violet-200',
  }
  return map[role] || 'border-zinc-600 bg-zinc-800 text-zinc-200'
}

const currentTabComponent = computed(() => {
  switch (activeTab.value) {
    case 'about':
      return 'about-section'
    case 'members':
      return 'members-section'
    case 'novels':
      return 'novels-section'
    default:
      return 'about-section'
  }
})
</script>

<template>
  <div>
    <AppEmptyState v-if="!team"> Команда не найдена. </AppEmptyState>

    <template v-else>
      <AppPanel as="section" class="mb-4 rounded-2xl p-4 sm:p-6">
        <div class="flex flex-col items-center gap-3 text-center sm:flex-row sm:text-left">
          <div
            class="flex h-16 w-16 shrink-0 items-center justify-center rounded-full text-2xl font-bold text-white shadow-lg sm:h-20 sm:w-20 sm:text-3xl"
            :class="team.avatarColorClass"
          >
            {{ team.name.slice(0, 1).toUpperCase() }}
          </div>
          <div class="min-w-0">
            <div class="flex flex-wrap items-center justify-center gap-2 sm:justify-start">
              <h1 class="text-xl font-semibold text-white sm:text-2xl">{{ team.name }}</h1>
              <span
                class="rounded-full border border-zinc-600 bg-zinc-800 px-2.5 py-0.5 text-xs text-zinc-300"
              >
                {{ team.typeLabel }}
              </span>
            </div>
            <p class="mt-1 text-sm text-zinc-400">{{ team.shortDescription }}</p>
            <p class="mt-2 text-xs text-zinc-500">
              {{ team.stats.membersCount }} участников · {{ team.stats.novelsCount }} новелл ·
              {{ team.stats.chaptersTotal }} глав
            </p>
          </div>
        </div>
      </AppPanel>

      <AppTabs v-model:model-value="activeTab" :tabs="tabs" />

      <AppSectionSwitchTransition>
        <template v-if="activeTab === 'about'">
          <div key="about" class="mt-3 space-y-3">
            <AppPanel as="section" class="rounded-2xl space-y-3">
              <h3 class="text-base font-semibold text-white">О команде</h3>
              <p class="whitespace-pre-line text-sm leading-6 text-zinc-300">
                {{ team.description }}
              </p>
              <div class="flex flex-wrap gap-4 text-xs text-zinc-500">
                <span>Создана: {{ team.createdAt }}</span>
                <span>Тип: {{ team.typeLabel }}</span>
              </div>
            </AppPanel>
          </div>
        </template>

        <template v-else-if="activeTab === 'members'">
          <div key="members" class="mt-3">
            <AppEmptyState v-if="!members.length" compact>
              В команде пока нет участников.
            </AppEmptyState>
            <div v-else class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
              <div
                v-for="member in members"
                :key="member.id"
                class="flex flex-col items-center gap-2 rounded-2xl border border-zinc-700/70 bg-zinc-900/70 p-4"
              >
                <div
                  class="flex h-14 w-14 items-center justify-center rounded-full text-lg font-bold text-white shadow-md"
                  :class="member.avatarColorClass"
                >
                  {{ member.nickname.slice(0, 1).toUpperCase() }}
                </div>
                <span class="text-sm font-medium text-white">{{ member.nickname }}</span>
                <span
                  class="rounded-full border px-2 py-0.5 text-[11px]"
                  :class="roleBadgeClass(member.role)"
                >
                  {{ roleLabel(member.role) }}
                </span>
              </div>
            </div>
          </div>
        </template>

        <template v-else-if="activeTab === 'novels'">
          <div key="novels" class="mt-3">
            <AppEmptyState v-if="!novels.length" compact>
              У команды пока нет новелл.
            </AppEmptyState>
            <div
              v-else
              class="grid grid-cols-2 gap-2 min-[480px]:gap-2.5 sm:gap-3 lg:grid-cols-4 xl:grid-cols-5"
            >
              <NovelGridCard v-for="item in novels" :key="item.id" :novel="item" />
            </div>
          </div>
        </template>
      </AppSectionSwitchTransition>
    </template>
  </div>
</template>
