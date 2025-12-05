export const API_BASE_URL = 'http://localhost:8000';
export async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const response = await fetch(url, { ...defaultOptions, ...options });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }
  
  // Handle 204 No Content
  if (response.status === 204) {
    return null;
  }
  
  return response.json();
}


export async function get(endpoint) {
  return apiRequest(endpoint, { method: 'GET' });
}


export async function post(endpoint, data) {
  return apiRequest(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}


export async function patch(endpoint, data) {
  return apiRequest(endpoint, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}


export async function del(endpoint) {
  return apiRequest(endpoint, { method: 'DELETE' });
}
