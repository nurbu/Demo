import { useState, useEffect, useCallback } from 'react';
import * as api from '../api/inventory';
export function useApiData(fetchFunction, dependencies = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetchFunction();
      setData(result);
    } catch (err) {
      setError(err.message);
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  }, [fetchFunction, ...dependencies]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}


export function useItems(filters = {}) {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchItems = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.getItems(filters);
      setItems(result.items || []);
      setTotal(result.total || 0);
      setTotalPages(result.total_pages || 0);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching items:', err);
    } finally {
      setLoading(false);
    }
  }, [JSON.stringify(filters)]);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  return { items, total, totalPages, loading, error, refetch: fetchItems };
}


export function useItem(itemId) {
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchItem = useCallback(async () => {
    if (!itemId) return;
    setLoading(true);
    setError(null);
    try {
      const result = await api.getItem(itemId);
      setItem(result);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching item:', err);
    } finally {
      setLoading(false);
    }
  }, [itemId]);

  useEffect(() => {
    fetchItem();
  }, [fetchItem]);

  return { item, loading, error, refetch: fetchItem };
}


export function useReferenceData() {
  const [departments, setDepartments] = useState([]);
  const [categories, setCategories] = useState([]);
  const [itemTypes, setItemTypes] = useState([]);
  const [sizes, setSizes] = useState([]);
  const [colors, setColors] = useState([]);
  const [tags, setTags] = useState([]);
  const [conditions, setConditions] = useState([]);
  const [statuses, setStatuses] = useState([]);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAllReferenceData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [
        deptRes,
        catRes,
        typeRes,
        sizeRes,
        colorRes,
        tagRes,
        condRes,
        statusRes,
        locRes
      ] = await Promise.all([
        api.getDepartments(),
        api.getCategories(),
        api.getItemTypes(),
        api.getSizes(),
        api.getColors(),
        api.getTags(),
        api.getConditions(),
        api.getStatuses(),
        api.getLocations()
      ]);

      setDepartments(deptRes.departments || []);
      setCategories(catRes.categories || []);
      setItemTypes(typeRes.item_types || []);
      setSizes(sizeRes.sizes || []);
      setColors(colorRes.colors || []);
      setTags(tagRes.tags || []);
      setConditions(condRes.conditions || []);
      setStatuses(statusRes.statuses || []);
      setLocations(locRes.locations || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching reference data:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAllReferenceData();
  }, [fetchAllReferenceData]);


  const getDepartmentName = (id) => departments.find(d => d.department_id === id)?.department_name || '';
  const getCategoryName = (id) => categories.find(c => c.category_id === id)?.category_name || '';
  const getItemTypeName = (id) => itemTypes.find(t => t.item_type_id === id)?.item_type_name || '';
  const getSizeName = (id) => sizes.find(s => s.size_id === id)?.size_value || '';
  const getSizeSystem = (id) => sizes.find(s => s.size_id === id)?.size_system || '';
  const getColorName = (id) => colors.find(c => c.color_id === id)?.color_name || '';
  const getConditionName = (id) => conditions.find(c => c.condition_id === id)?.condition_name || '';
  const getStatusName = (id) => statuses.find(s => s.status_id === id)?.status_name || '';
  const getLocationName = (id) => locations.find(l => l.location_id === id)?.location_name || '';
  const getTagName = (id) => tags.find(t => t.tag_id === id)?.tag_name || '';


  const getCategoriesByDepartment = (deptId) => 
    categories.filter(c => c.department_id === deptId);
  
  const getItemTypesByCategory = (catId) => 
    itemTypes.filter(t => t.category_id === catId);

  return {
    departments,
    categories,
    itemTypes,
    sizes,
    colors,
    tags,
    conditions,
    statuses,
    locations,
    loading,
    error,
    refetch: fetchAllReferenceData,
    // Helper functions
    getDepartmentName,
    getCategoryName,
    getItemTypeName,
    getSizeName,
    getSizeSystem,
    getColorName,
    getConditionName,
    getStatusName,
    getLocationName,
    getTagName,
    getCategoriesByDepartment,
    getItemTypesByCategory
  };
}
