export const initialBookmarks = [
	{
		id: 'reading-now',
		name: 'Читаю',
		isPublic: true,
		order: 1,
		items: [
			{
				id: 'bm-1',
				title: 'Легенда пепельного трона',
				author: 'Куанг Ли',
				chapterLabel: 'Глава 129',
				rating: 4.8,
				coverStyle: 'from-lime-300 to-emerald-500',
				coverUrl: 'https://tl.rulate.ru/i/book/26/3/29296-100100.jpg',
				href: '#'
			},
			{
				id: 'bm-2',
				title: 'Путь ледяного феникса',
				author: 'Мин Сон',
				chapterLabel: 'Глава 215',
				rating: 4.9,
				coverStyle: 'from-emerald-300 to-teal-600',
				href: '#'
			},
			{
				id: 'bm-3',
				title: 'Тень архивариуса',
				author: 'Рин Араи',
				chapterLabel: 'Глава 34',
				rating: 4.5,
				coverStyle: 'from-green-300 to-emerald-600',
				href: '#'
			}
		]
	},
	{
		id: 'plan-to-read',
		name: 'Планирую',
		isPublic: true,
		order: 2,
		items: [
			{
				id: 'bm-4',
				title: 'Хроники небесной башни',
				author: 'Чжан Вэй',
				chapterLabel: 'Глава 78',
				rating: 4.7,
				coverStyle: 'from-lime-300 to-green-500',
				href: '#'
			},
			{
				id: 'bm-5',
				title: 'Меч Великой Тан',
				author: 'Сюй Ци',
				chapterLabel: 'Глава 47',
				rating: 4.7,
				coverUrl: 'https://tl.rulate.ru/i/book/26/3/20067-100100.jpg',
				coverStyle: 'from-emerald-300 to-lime-500',
				href: '#'
			}
		]
	},
	{
		id: 'completed',
		name: 'Прочитано',
		isPublic: true,
		order: 3,
		items: [
			{
				id: 'bm-6',
				title: 'Алхимик без имени',
				author: 'Андрес Рой',
				chapterLabel: 'Завершено',
				rating: 4.6,
				coverStyle: 'from-emerald-300 to-green-600',
				href: '#'
			}
		]
	}
]
