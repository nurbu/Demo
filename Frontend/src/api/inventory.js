import { get, post, patch, del, API_BASE_URL } from './config';

export async function getItems(params = {}) {
  const queryParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      if (Array.isArray(value)) {
        value.forEach(v => queryParams.append(key, v));
      } else {
        queryParams.append(key, value);
      }
    }
  });

  const queryString = queryParams.toString();
  const endpoint = queryString ? `/items/?${queryString}` : '/items/';
  return get(endpoint);
}

export async function getItem(itemId) {
  return get(`/items/${itemId}`);
}

export async function createItem(itemData) {
  return post('/items/', itemData);
}

export async function updateItem(itemId, itemData) {
  return patch(`/items/${itemId}`, itemData);
}

export async function deleteItem(itemId) {
  return del(`/items/${itemId}`);
}

export async function getDepartments() {
  return get('/departments/');
}

export async function getCategories(departmentId = null) {
  const endpoint = departmentId
    ? `/categories/?department_id=${departmentId}`
    : '/categories/';
  return get(endpoint);
}

export async function getItemTypes(categoryId = null) {
  const endpoint = categoryId
    ? `/item-types/?category_id=${categoryId}`
    : '/item-types/';
  return get(endpoint);
}

export async function getSizes() {
  return get('/sizes/');
}

export async function getColors() {
  return get('/colors/');
}

export async function getTags() {
  return get('/tags/');
}

export async function getConditions() {
  return get('/conditions/');
}

export async function getStatuses() {
  return get('/item-statuses/');
}

export async function getLocations() {
  return get('/locations/');
}


export async function createDepartment(data) {
  return post('/departments/', data);
}

export async function updateDepartment(id, data) {
  return patch(`/departments/${id}`, data);
}

export async function deleteDepartment(id) {
  return del(`/departments/${id}`);
}


export async function createCategory(data) {
  return post('/categories/', data);
}

export async function updateCategory(id, data) {
  return patch(`/categories/${id}`, data);
}

export async function deleteCategory(id) {
  return del(`/categories/${id}`);
}


export async function createItemType(data) {
  return post('/item-types/', data);
}

export async function updateItemType(id, data) {
  return patch(`/item-types/${id}`, data);
}

export async function deleteItemType(id) {
  return del(`/item-types/${id}`);
}


export async function createSize(data) {
  return post('/sizes/', data);
}

export async function updateSize(id, data) {
  return patch(`/sizes/${id}`, data);
}

export async function deleteSize(id) {
  return del(`/sizes/${id}`);
}


export async function createColor(data) {
  return post('/colors/', data);
}

export async function updateColor(id, data) {
  return patch(`/colors/${id}`, data);
}

export async function deleteColor(id) {
  return del(`/colors/${id}`);
}


export async function createTag(data) {
  return post('/tags/', data);
}

export async function updateTag(id, data) {
  return patch(`/tags/${id}`, data);
}

export async function deleteTag(id) {
  return del(`/tags/${id}`);
}


export async function createCondition(data) {
  return post('/conditions/', data);
}

export async function updateCondition(id, data) {
  return patch(`/conditions/${id}`, data);
}

export async function deleteCondition(id) {
  return del(`/conditions/${id}`);
}


export async function createStatus(data) {
  return post('/item-statuses/', data);
}

export async function updateStatus(id, data) {
  return patch(`/item-statuses/${id}`, data);
}

export async function deleteStatus(id) {
  return del(`/item-statuses/${id}`);
}


export async function createLocation(data) {
  return post('/locations/', data);
}

export async function updateLocation(id, data) {
  return patch(`/locations/${id}`, data);
}

export async function deleteLocation(id) {
  return del(`/locations/${id}`);
}

export async function bulkUpdateStatus(itemIds, statusId, notes = null) {
  return post('/items/bulk/update-status', { item_ids: itemIds, status_id: statusId, notes });
}

export async function bulkUpdateLocation(itemIds, locationId, notes = null) {
  return post('/items/bulk/update-location', { item_ids: itemIds, location_id: locationId, notes });
}

export async function bulkUpdatePrice(itemIds, price = null, onSale = null, salePrice = null) {
  return post('/items/bulk/update-price', {
    item_ids: itemIds,
    price,
    on_sale: onSale,
    sale_price: salePrice
  });
}

export async function bulkDeleteItems(itemIds, reason = null) {
  return post('/items/bulk/delete', { item_ids: itemIds, reason });
}

export async function getItemPhotos(itemId) {
  return get(`/items/${itemId}/photos`);
}

export async function addItemPhoto(itemId, photoData) {
  return post(`/items/${itemId}/photos`, photoData);
}

export async function uploadItemPhoto(itemId, file, isPrimary = false, sortOrder = 1) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('is_primary', isPrimary);
  formData.append('sort_order', sortOrder);

  // Use generic post but let browser handle headers for FormData
  // The fetch wrapper in config.js might set Content-Type: application/json automatically
  // We need to bypass that.

  // Checking config.js implementation...
  // Assuming config.js sets 'Content-Type': 'application/json' by default.
  // We'll write a specific fetch for this or modify config.js.
  // Let's modify config.js instead or just use raw fetch here for safety if config is rigid.

  // Actually, let's peek at config.js first to be safe.
  return fetch(`${API_BASE_URL}/items/${itemId}/photos/upload`, {
    method: 'POST',
    body: formData,
  }).then(async res => {
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(errorText || 'Upload failed');
    }
    return res.json();
  });
}

export async function updateItemPhoto(photoId, photoData) {
  return patch(`/items/photos/${photoId}`, photoData);
}

export async function deleteItemPhoto(photoId) {
  return del(`/items/photos/${photoId}`);
}

export async function getItemHistory(itemId) {
  return get(`/items/${itemId}/history`);
}

export function getImageUrl(filePath) {
  if (!filePath) return null;
  if (filePath.startsWith('http')) return filePath;
  return `${API_BASE_URL}${filePath.startsWith('/') ? '' : '/'}${filePath}`;
}

export async function checkHealth() {
  return get('/health');
}
