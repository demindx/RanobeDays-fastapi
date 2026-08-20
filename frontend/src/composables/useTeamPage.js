import { computed, ref, watch } from 'vue'
import { fetchTeam, fetchTeamUsers, fetchTeamNovels } from '../api/teams'
import { mapNovelsList } from '../api/mapper'
import { useAsyncState } from './useAsyncState'

const TYPE_LABELS = {
  publishers: 'Издательства',
  authors: 'Авторы',
  translators: 'Переводчики',
}

const roleLabel = (role) => {
  const labels = { creator: 'Создатель', manager: 'Менеджер', newbie: 'Новичок' }
  return labels[role] || role
}

export const useTeamPage = (teamIdRef) => {
  const team = ref(null)
  const members = ref([])
  const novels = ref([])
  const { loading, error, run } = useAsyncState()

  watch(
    teamIdRef,
    async (id) => {
      team.value = null
      members.value = []
      novels.value = []
      if (!id) return
      const result = await run(() =>
        Promise.all([fetchTeam(id), fetchTeamUsers(id), fetchTeamNovels(id)]),
      )
      if (!result) return
      const [teamData, membersData, novelsData] = result
      team.value = {
        id: teamData.id,
        name: teamData.name,
        slug: '',
        avatarColorClass: 'bg-orange-500',
        type: teamData.type,
        typeLabel: TYPE_LABELS[teamData.type] || teamData.type,
        shortDescription: '',
        description: '',
        createdAt: '',
        stats: {
          membersCount: membersData.length,
          novelsCount: novelsData.length,
          chaptersTotal: 0,
        },
      }
      members.value = membersData.map((m) => ({
        id: m.nickname,
        nickname: m.nickname,
        role: m.role,
        avatarColorClass: 'bg-lime-500',
      }))
      novels.value = mapNovelsList(novelsData)
    },
    { immediate: true },
  )

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
    loading,
    error,
    setActiveTab,
    roleLabel,
  }
}
