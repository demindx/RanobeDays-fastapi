import { get, post, patch, del } from './client'

export function fetchCategories() {
  return get('/api/v1/category/')
}

export function fetchCategoryById(id) {
  return get(`/api/v1/category/${id}`)
}

export function createCategory(data) {
  return post('/api/v1/category/', data)
}

export function updateCategory(id, data) {
  return patch(`/api/v1/category/${id}`, data)
}

export function deleteCategory(id) {
  return del(`/api/v1/category/${id}`)
}
