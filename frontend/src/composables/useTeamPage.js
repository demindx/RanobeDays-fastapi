import { computed, ref } from 'vue'
import { teamPageData, teamMembers, teamNovels } from '../mocks/teamPageData'

const roleLabel = (role) => {
  const labels = { creator: 'Создатель', manager: 'Менеджер', translator: 'Переводчик' }
  return labels[role] || role
}

export const useTeamPage = (teamIdRef) => {
  const team = computed(() => {
    if (String(teamPageData.id) !== String(teamIdRef.value)) return null
    return {
      ...teamPageData,
      members: teamMembers,
      novels: teamNovels,
    }
  })

  const members = computed(() => team.value?.members ?? [])
  const novels = computed(() => team.value?.novels ?? [])

  const activeTab = ref('about')

  const tabs = computed(() => [
    { key: 'about', label: 'О команде' },
    { key: 'members', label: 'Участники', count: members.value.length },
    { key: 'novels', label: 'Новеллы', count: novels.value.length },
  ])

  const setActiveTab = (tab) => {
    activeTab.value = tab
  }

  return {
    team,
    members,
    novels,
    tabs,
    activeTab,
    setActiveTab,
    roleLabel,
  }
}
