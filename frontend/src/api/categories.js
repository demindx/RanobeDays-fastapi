import { get, post, patch, del } from './client'

export function fetchCategories() {
  return get('/category/')
}

export function fetchCategoryById(id) {
  return get(`/category/${id}`)
}

export function createCategory(data) {
  return post('/category/', data)
}

export function updateCategory(id, data) {
  return patch(`/category/${id}`, data)
}

export function deleteCategory(id) {
  return del(`/category/${id}`)
}
