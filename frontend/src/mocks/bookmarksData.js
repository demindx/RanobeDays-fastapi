export const initialBookmarks = [
	{
		id: 'reading-now',
		name: 'Читаю',
		isPublic: true,
		order: 1,
		items: [
			{
				id: 'bm-1',
				novelId: 1,
				title: 'Легенда пепельного трона',
				author: 'Куанг Ли',
				chapterLabel: 'Глава 129',
				rating: 4.8,
				coverStyle: 'from-lime-300 to-emerald-500',
				coverUrl: 'https://tl.rulate.ru/i/book/26/3/29296-100100.jpg',
				href: '/novel/1'
			},
			{
				id: 'bm-2',
				novelId: 4,
				title: 'Путь ледяного феникса',
				author: 'Мин Сон',
				chapterLabel: 'Глава 215',
				rating: 4.9,
				coverStyle: 'from-emerald-300 to-teal-600'
			},
			{
				id: 'bm-3',
				novelId: 5,
				title: 'Тень архивариуса',
				author: 'Рин Араи',
				chapterLabel: 'Глава 34',
				rating: 4.5,
				coverStyle: 'from-green-300 to-emerald-600'
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
				novelId: 2,
				title: 'Хроники небесной башни',
				author: 'Чжан Вэй',
				chapterLabel: 'Глава 78',
				rating: 4.7,
				coverStyle: 'from-lime-300 to-green-500'
			},
			{
				id: 'bm-5',
				novelId: 7,
				title: 'Меч Великой Тан',
				author: 'Сюй Ци',
				chapterLabel: 'Глава 47',
				rating: 4.7,
				coverUrl: 'https://tl.rulate.ru/i/book/26/3/20067-100100.jpg',
				coverStyle: 'from-emerald-300 to-lime-500'
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
				novelId: 3,
				title: 'Алхимик без имени',
				author: 'Андрес Рой',
				chapterLabel: 'Завершено',
				rating: 4.6,
				coverStyle: 'from-emerald-300 to-green-600'
			}
		]
	}
]
