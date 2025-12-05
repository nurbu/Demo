import { useState, useEffect } from "react";
import { Search, Grid3x3, List, Eye, Edit, Trash2, SlidersHorizontal, X, Loader2, AlertCircle, CheckSquare, Square, MapPin, Tag as TagIcon, DollarSign } from "lucide-react";
import { useItems, useReferenceData } from "../hooks/useInventory";
import { deleteItem, getImageUrl, bulkUpdateStatus, bulkUpdateLocation, bulkDeleteItems } from "../api/inventory";

export function ItemList({ onNavigate }) {
  const [viewMode, setViewMode] = useState("grid");
  const [searchQuery, setSearchQuery] = useState("");
  const [showFilters, setShowFilters] = useState(false);
  const [selectedDepartment, setSelectedDepartment] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedStatus, setSelectedStatus] = useState(null);
  const [selectedCondition, setSelectedCondition] = useState(null);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [selectedSize, setSelectedSize] = useState(null);
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [selectedTags, setSelectedTags] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(20);

  // Bulk Selection State
  const [selectedItems, setSelectedItems] = useState([]);
  const [bulkActionLoading, setBulkActionLoading] = useState(false);

  // Bulk Action Inputs
  const [bulkStatusId, setBulkStatusId] = useState("");
  const [bulkLocationId, setBulkLocationId] = useState("");

  // Build filters object
  const filters = {
    page: currentPage,
    page_size: pageSize,
    search: searchQuery || undefined,
    department_id: selectedDepartment || undefined,
    category_id: selectedCategory || undefined,
    status_id: selectedStatus || undefined,
    condition_id: selectedCondition || undefined,
    location_id: selectedLocation || undefined,
    size_id: selectedSize || undefined,
    min_price: minPrice || undefined,
    max_price: maxPrice || undefined,
    tag_ids: selectedTags.length > 0 ? selectedTags : undefined,
  };

  const { items, total, totalPages, loading, error, refetch } = useItems(filters);
  const {
    departments,
    categories,
    sizes,
    colors,
    conditions,
    statuses,
    locations,
    tags,
    getDepartmentName,
    getCategoryName,
    getItemTypeName,
    getSizeName,
    getColorName,
    getConditionName,
    getStatusName,
    getLocationName,
    getCategoriesByDepartment,
    loading: refLoading
  } = useReferenceData();

  const filteredCategories = selectedDepartment
    ? getCategoriesByDepartment(parseInt(selectedDepartment))
    : categories;

  // Clear selection when filters or page changes
  useEffect(() => {
    setSelectedItems([]);
  }, [currentPage, searchQuery, selectedDepartment, selectedCategory, selectedStatus, selectedCondition, selectedLocation, selectedSize, minPrice, maxPrice, selectedTags]);

  const toggleTag = (tagId) => {
    setSelectedTags(prev =>
      prev.includes(tagId) ? prev.filter(id => id !== tagId) : [...prev, tagId]
    );
  };

  const clearFilters = () => {
    setSearchQuery("");
    setSelectedDepartment(null);
    setSelectedCategory(null);
    setSelectedStatus(null);
    setSelectedCondition(null);
    setSelectedLocation(null);
    setSelectedSize(null);
    setMinPrice("");
    setMaxPrice("");
    setSelectedTags([]);
    setCurrentPage(1);
  };

  const handleDelete = async (itemId, e) => {
    e.stopPropagation();
    if (window.confirm("Are you sure you want to delete this item?")) {
      try {
        await deleteItem(itemId);
        refetch();
      } catch (err) {
        alert("Error deleting item: " + err.message);
      }
    }
  };

  // Bulk Operations Handlers
  const handleSelectAll = () => {
    if (selectedItems.length === items.length) {
      setSelectedItems([]);
    } else {
      setSelectedItems(items.map(i => i.item_id));
    }
  };

  const handleSelectOne = (itemId, e) => {
    e.stopPropagation(); // Prevent navigation
    setSelectedItems(prev =>
      prev.includes(itemId) ? prev.filter(id => id !== itemId) : [...prev, itemId]
    );
  };

  const handleBulkStatusUpdate = async () => {
    if (!bulkStatusId) return;
    if (!window.confirm(`Update status for ${selectedItems.length} items?`)) return;

    setBulkActionLoading(true);
    try {
      await bulkUpdateStatus(selectedItems, parseInt(bulkStatusId));
      setSelectedItems([]);
      setBulkStatusId("");
      refetch();
      alert(`Status updated for ${selectedItems.length} items`);
    } catch (err) {
      alert("Error updating status: " + err.message);
    } finally {
      setBulkActionLoading(false);
    }
  };

  const handleBulkLocationUpdate = async () => {
    if (!bulkLocationId) return;
    if (!window.confirm(`Update location for ${selectedItems.length} items?`)) return;

    setBulkActionLoading(true);
    try {
      await bulkUpdateLocation(selectedItems, parseInt(bulkLocationId));
      setSelectedItems([]);
      setBulkLocationId("");
      refetch();
      alert(`Location updated for ${selectedItems.length} items`);
    } catch (err) {
      alert("Error updating location: " + err.message);
    } finally {
      setBulkActionLoading(false);
    }
  };

  const handleBulkDelete = async () => {
    if (!window.confirm(`Are you sure you want to delete ${selectedItems.length} items? This cannot be undone.`)) return;

    setBulkActionLoading(true);
    try {
      await bulkDeleteItems(selectedItems);
      setSelectedItems([]);
      refetch();
      alert(`Deleted ${selectedItems.length} items`);
    } catch (err) {
      alert("Error deleting items: " + err.message);
    } finally {
      setBulkActionLoading(false);
    }
  };

  const getPrimaryPhoto = (item) => {
    if (item.photos && item.photos.length > 0) {
      const primary = item.photos.find(p => p.is_primary) || item.photos[0];
      return getImageUrl(primary.file_path);
    }
    return 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800';
  };

  const statusColors = {
    Available: "bg-[#7a9178] text-white",
    Sold: "bg-[#a89080] text-white",
    Processing: "bg-[#4a5c6a] text-white",
    "On Hold": "bg-[#9ba896] text-white",
    Donated: "bg-[#e8dfd1] text-[#6b5d52]",
  };

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="bg-red-50 border border-red-200 rounded-2xl p-6 flex items-center gap-4">
          <AlertCircle className="w-6 h-6 text-red-500" />
          <div>
            <h3 className="text-red-800 font-medium">Error loading items</h3>
            <p className="text-red-600 text-sm">{error}</p>
            <p className="text-red-500 text-xs mt-2">Make sure the backend server is running on http://localhost:8000</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-8 pb-32"> {/* Added pb-32 for floating bar space */}
      <div className="mb-8">
        <h1 className="mb-2">Item Inventory</h1>
        <p className="text-[#a89080]">Browse and manage all inventory items</p>
      </div>


      <div className="flex flex-col md:flex-row gap-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[#a89080]" />
          <input
            type="text"
            placeholder="Search by brand, description, or item type..."
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setCurrentPage(1);
            }}
            className="w-full pl-12 pr-4 py-3 rounded-full border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
          />
        </div>
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="px-6 py-3 rounded-full border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] hover:bg-[#e8dfd1] transition-colors flex items-center gap-2"
        >
          <SlidersHorizontal className="w-5 h-5" />
          Filters
        </button>
        <div className="flex gap-2 bg-[#fefbf6] rounded-full p-1 border border-[#e8dfd1]">
          <button
            onClick={() => setViewMode("grid")}
            className={`p-2 rounded-full transition-colors ${viewMode === "grid" ? "bg-[#7a9178] text-white" : "text-[#6b5d52] hover:bg-[#e8dfd1]"
              }`}
          >
            <Grid3x3 className="w-5 h-5" />
          </button>
          <button
            onClick={() => setViewMode("list")}
            className={`p-2 rounded-full transition-colors ${viewMode === "list" ? "bg-[#7a9178] text-white" : "text-[#6b5d52] hover:bg-[#e8dfd1]"
              }`}
          >
            <List className="w-5 h-5" />
          </button>
        </div>
      </div>


      {showFilters && (
        <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] mb-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="m-0">Advanced Filters</h3>
            <button onClick={() => setShowFilters(false)} className="text-[#a89080] hover:text-[#6b5d52]">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div>
              <label className="block text-sm text-[#6b5d52] mb-2">Department</label>
              <select
                value={selectedDepartment || ""}
                onChange={(e) => {
                  setSelectedDepartment(e.target.value || null);
                  setSelectedCategory(null);
                  setCurrentPage(1);
                }}
                className="w-full px-4 py-2 rounded-full border border-[#e8dfd1] bg-white text-[#6b5d52] text-sm focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">All Departments</option>
                {departments.map((dept) => (
                  <option key={dept.department_id} value={dept.department_id}>
                    {dept.department_name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2">Category</label>
              <select
                value={selectedCategory || ""}
                onChange={(e) => {
                  setSelectedCategory(e.target.value || null);
                  setCurrentPage(1);
                }}
                className="w-full px-4 py-2 rounded-full border border-[#e8dfd1] bg-white text-[#6b5d52] text-sm focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">All Categories</option>
                {filteredCategories.map((cat) => (
                  <option key={cat.category_id} value={cat.category_id}>
                    {cat.category_name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2">Size</label>
              <select
                value={selectedSize || ""}
                onChange={(e) => {
                  setSelectedSize(e.target.value || null);
                  setCurrentPage(1);
                }}
                className="w-full px-4 py-2 rounded-full border border-[#e8dfd1] bg-white text-[#6b5d52] text-sm focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">All Sizes</option>
                {sizes.map((size) => (
                  <option key={size.size_id} value={size.size_id}>
                    {size.size_value} ({size.size_system})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2">Condition</label>
              <select
                value={selectedCondition || ""}
                onChange={(e) => {
                  setSelectedCondition(e.target.value || null);
                  setCurrentPage(1);
                }}
                className="w-full px-4 py-2 rounded-full border border-[#e8dfd1] bg-white text-[#6b5d52] text-sm focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">All Conditions</option>
                {conditions.map((cond) => (
                  <option key={cond.condition_id} value={cond.condition_id}>
                    {cond.condition_name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2">Status</label>
              <select
                value={selectedStatus || ""}
                onChange={(e) => {
                  setSelectedStatus(e.target.value || null);
                  setCurrentPage(1);
                }}
                className="w-full px-4 py-2 rounded-full border border-[#e8dfd1] bg-white text-[#6b5d52] text-sm focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">All Statuses</option>
                {statuses.map((status) => (
                  <option key={status.status_id} value={status.status_id}>
                    {status.status_name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2">Location</label>
              <select
                value={selectedLocation || ""}
                onChange={(e) => {
                  setSelectedLocation(e.target.value || null);
                  setCurrentPage(1);
                }}
                className="w-full px-4 py-2 rounded-full border border-[#e8dfd1] bg-white text-[#6b5d52] text-sm focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">All Locations</option>
                {locations.map((loc) => (
                  <option key={loc.location_id} value={loc.location_id}>
                    {loc.location_name}
                  </option>
                ))}
              </select>
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm text-[#6b5d52] mb-2">Price Range</label>
              <div className="flex items-center gap-4">
                <input
                  type="number"
                  placeholder="Min"
                  value={minPrice}
                  onChange={(e) => {
                    setMinPrice(e.target.value);
                    setCurrentPage(1);
                  }}
                  className="flex-1 px-4 py-2 rounded-full border border-[#e8dfd1] bg-white text-[#6b5d52] text-sm focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                />
                <span className="text-[#a89080]">to</span>
                <input
                  type="number"
                  placeholder="Max"
                  value={maxPrice}
                  onChange={(e) => {
                    setMaxPrice(e.target.value);
                    setCurrentPage(1);
                  }}
                  className="flex-1 px-4 py-2 rounded-full border border-[#e8dfd1] bg-white text-[#6b5d52] text-sm focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                />
              </div>
            </div>
          </div>

    
          <div>
            <label className="block text-sm text-[#6b5d52] mb-3">Tags</label>
            <div className="flex flex-wrap gap-2">
              {tags.map((tag) => {
                const isSelected = selectedTags.includes(tag.tag_id);
                return (
                  <button
                    key={tag.tag_id}
                    onClick={() => {
                      toggleTag(tag.tag_id);
                      setCurrentPage(1);
                    }}
                    className={`px-4 py-2 rounded-full text-sm border transition-colors ${isSelected
                        ? "bg-[#7a9178] text-white border-[#7a9178]"
                        : "bg-[#fefbf6] text-[#6b5d52] border-[#e8dfd1] hover:bg-[#e8dfd1]"
                      }`}
                  >
                    {tag.tag_name}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="flex gap-3 mt-6">
            <button
              onClick={clearFilters}
              className="px-6 py-2 rounded-full border border-[#e8dfd1] text-[#6b5d52] hover:bg-[#e8dfd1] transition-colors"
            >
              Clear All
            </button>
          </div>
        </div>
      )}


      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 text-[#7a9178] animate-spin" />
          <span className="ml-3 text-[#6b5d52]">Loading items...</span>
        </div>
      ) : items.length === 0 ? (
        <div className="bg-[#fefbf6] rounded-2xl p-12 text-center border border-[#e8dfd1]">
          <h3 className="text-[#6b5d52] mb-2">No items found</h3>
          <p className="text-[#a89080] mb-4">Try adjusting your filters or add new items</p>
          <button
            onClick={() => onNavigate("add-item")}
            className="px-6 py-2 rounded-full bg-[#7a9178] text-white hover:bg-[#6b8167] transition-colors"
          >
            Add New Item
          </button>
        </div>
      ) : (
        <>

          <div className="mb-4 flex items-center justify-between bg-white p-3 rounded-xl border border-[#e8dfd1] shadow-sm">
            <div className="flex items-center gap-3">
              <button onClick={handleSelectAll} className="flex items-center gap-2 text-[#6b5d52] hover:text-[#4a3f35] font-medium">
                {selectedItems.length === items.length && items.length > 0 ? (
                  <CheckSquare className="w-5 h-5 text-[#7a9178]" />
                ) : (
                  <Square className="w-5 h-5 text-[#a89080]" />
                )}
                Select All ({items.length})
              </button>
              <span className="text-[#a89080] text-sm">
                {selectedItems.length} selected
              </span>
            </div>
          </div>


          {viewMode === "grid" && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {items.map((item) => {
                const status = getStatusName(item.status_id);
                const isSelected = selectedItems.includes(item.item_id);
                return (
                  <div
                    key={item.item_id}
                    className={`bg-[#fefbf6] rounded-2xl overflow-hidden shadow-sm border transition-all group ${isSelected ? "border-[#7a9178] ring-2 ring-[#7a9178]/20" : "border-[#e8dfd1] hover:shadow-md"
                      }`}
                  >
                    <div className="aspect-square overflow-hidden bg-[#e8dfd1] relative">
                      <img
                        src={getPrimaryPhoto(item)}
                        alt={item.description}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
          
                      <button
                        onClick={(e) => handleSelectOne(item.item_id, e)}
                        className="absolute top-3 left-3 w-8 h-8 rounded-lg bg-white/90 backdrop-blur-sm shadow-sm flex items-center justify-center hover:bg-white transition-colors"
                      >
                        {isSelected ? <CheckSquare className="w-5 h-5 text-[#7a9178]" /> : <Square className="w-5 h-5 text-[#a89080]" />}
                      </button>

                      <div className="absolute top-3 right-3 flex flex-col gap-2">
                        <button
                          onClick={() => onNavigate("item-detail", item.item_id)}
                          className="w-9 h-9 rounded-full bg-white/95 flex items-center justify-center hover:bg-white transition-colors shadow-sm"
                        >
                          <Eye className="w-4 h-4 text-[#6b5d52]" />
                        </button>
                        <button
                          onClick={() => onNavigate("edit-item", item.item_id)}
                          className="w-9 h-9 rounded-full bg-white/95 flex items-center justify-center hover:bg-white transition-colors shadow-sm"
                        >
                          <Edit className="w-4 h-4 text-[#6b5d52]" />
                        </button>
                        <button
                          onClick={(e) => handleDelete(item.item_id, e)}
                          className="w-9 h-9 rounded-full bg-white/95 flex items-center justify-center hover:bg-white transition-colors shadow-sm"
                        >
                          <Trash2 className="w-4 h-4 text-[#a89080]" />
                        </button>
                      </div>
                    </div>
                    <div className="p-4">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h4 className="m-0 text-base">{item.brand || 'No Brand'}</h4>
                          <p className="text-xs text-[#a89080] mt-1">
                            {getDepartmentName(item.department_id)} · {getSizeName(item.size_id)}
                          </p>
                        </div>
                        <span
                          className={`px-2 py-1 rounded-full text-xs ${statusColors[status] || "bg-[#e8dfd1] text-[#6b5d52]"
                            }`}
                        >
                          {status}
                        </span>
                      </div>
                      <p className="text-sm mb-3 line-clamp-2">{item.description}</p>
                      <div className="flex items-center justify-between">
                        <p className="text-lg m-0">${parseFloat(item.price).toFixed(2)}</p>
                        <p className="text-xs text-[#a89080]">{getConditionName(item.condition_id)}</p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}


          {viewMode === "list" && (
            <div className="bg-[#fefbf6] rounded-2xl shadow-sm border border-[#e8dfd1] overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-[#e8dfd1]">
                    <tr>
                      <th className="px-4 py-3 w-12">
                        {/* Header Checkbox handled by Select All bar/button above, but can put one here too */}
                      </th>
                      <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Photo</th>
                      <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Brand</th>
                      <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Description</th>
                      <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Size</th>
                      <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Color</th>
                      <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Condition</th>
                      <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Price</th>
                      <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Department</th>
                      <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Status</th>
                      <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Location</th>
                      <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {items.map((item) => {
                      const status = getStatusName(item.status_id);
                      const isSelected = selectedItems.includes(item.item_id);
                      return (
                        <tr key={item.item_id} className={`border-t border-[#e8dfd1] hover:bg-[#f7f4ef] transition-colors ${isSelected ? 'bg-[#7a9178]/5' : ''}`}>
                          <td className="px-4 py-3">
                            <button onClick={(e) => handleSelectOne(item.item_id, e)} className="flex items-center justify-center">
                              {isSelected ? <CheckSquare className="w-5 h-5 text-[#7a9178]" /> : <Square className="w-5 h-5 text-[#a89080]" />}
                            </button>
                          </td>
                          <td className="px-4 py-3">
                            <img
                              src={getPrimaryPhoto(item)}
                              alt={item.brand}
                              className="w-12 h-12 rounded-lg object-cover"
                            />
                          </td>
                          <td className="px-4 py-3 text-sm">{item.brand || 'No Brand'}</td>
                          <td className="px-4 py-3 text-sm max-w-xs truncate">{item.description}</td>
                          <td className="px-4 py-3 text-sm">{getSizeName(item.size_id)}</td>
                          <td className="px-4 py-3 text-sm">{getColorName(item.color_primary_id)}</td>
                          <td className="px-4 py-3 text-sm">{getConditionName(item.condition_id)}</td>
                          <td className="px-4 py-3 text-sm">${parseFloat(item.price).toFixed(2)}</td>
                          <td className="px-4 py-3 text-sm">{getDepartmentName(item.department_id)}</td>
                          <td className="px-4 py-3">
                            <span
                              className={`px-2 py-1 rounded-full text-xs ${statusColors[status] || "bg-[#e8dfd1] text-[#6b5d52]"
                                }`}
                            >
                              {status}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-sm">{getLocationName(item.current_location_id)}</td>
                          <td className="px-4 py-3">
                            <div className="flex gap-2">
                              <button
                                onClick={() => onNavigate("item-detail", item.item_id)}
                                className="p-1 hover:bg-[#e8dfd1] rounded-lg transition-colors"
                              >
                                <Eye className="w-4 h-4 text-[#6b5d52]" />
                              </button>
                              <button
                                onClick={() => onNavigate("edit-item", item.item_id)}
                                className="p-1 hover:bg-[#e8dfd1] rounded-lg transition-colors"
                              >
                                <Edit className="w-4 h-4 text-[#6b5d52]" />
                              </button>
                              <button
                                onClick={(e) => handleDelete(item.item_id, e)}
                                className="p-1 hover:bg-[#e8dfd1] rounded-lg transition-colors"
                              >
                                <Trash2 className="w-4 h-4 text-[#a89080]" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}


          <div className="flex items-center justify-between px-6 py-4 mt-4 bg-[#fefbf6] rounded-2xl border border-[#e8dfd1]">
            <p className="text-sm text-[#a89080]">
              Showing {((currentPage - 1) * pageSize) + 1}-{Math.min(currentPage * pageSize, total)} of {total} items
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className="px-4 py-2 rounded-full border border-[#e8dfd1] text-[#6b5d52] text-sm hover:bg-[#e8dfd1] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                const pageNum = i + 1;
                return (
                  <button
                    key={pageNum}
                    onClick={() => setCurrentPage(pageNum)}
                    className={`px-4 py-2 rounded-full text-sm ${currentPage === pageNum
                        ? "bg-[#7a9178] text-white"
                        : "border border-[#e8dfd1] text-[#6b5d52] hover:bg-[#e8dfd1]"
                      } transition-colors`}
                  >
                    {pageNum}
                  </button>
                );
              })}
              <button
                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
                className="px-4 py-2 rounded-full border border-[#e8dfd1] text-[#6b5d52] text-sm hover:bg-[#e8dfd1] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </div>
        </>
      )}


      {selectedItems.length > 0 && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 w-[90%] max-w-4xl bg-[#6b5d52] text-white p-4 rounded-2xl shadow-xl flex flex-col md:flex-row items-center justify-between gap-4 z-50 animate-in slide-in-from-bottom-5">
          <div className="flex items-center gap-4">
            <div className="bg-white/10 px-3 py-1 rounded-full text-sm font-medium">
              {selectedItems.length} selected
            </div>
            <div className="h-8 w-px bg-white/20 hidden md:block"></div>
          </div>

          <div className="flex flex-1 items-center gap-2 w-full md:w-auto overflow-x-auto">

            <div className="flex items-center gap-2 bg-white/5 p-1 rounded-xl">
              <select
                value={bulkStatusId}
                onChange={(e) => setBulkStatusId(e.target.value)}
                className="bg-transparent text-white text-sm border-none focus:ring-0 w-32 md:w-40 [&>option]:text-black cursor-pointer"
              >
                <option value="">Set Status...</option>
                {statuses.map(s => <option key={s.status_id} value={s.status_id}>{s.status_name}</option>)}
              </select>
              <button
                onClick={handleBulkStatusUpdate}
                disabled={!bulkStatusId || bulkActionLoading}
                className="p-2 hover:bg-white/10 rounded-lg transition-colors disabled:opacity-50"
                title="Update Status"
              >
                <TagIcon className="w-4 h-4" />
              </button>
            </div>


            <div className="flex items-center gap-2 bg-white/5 p-1 rounded-xl">
              <select
                value={bulkLocationId}
                onChange={(e) => setBulkLocationId(e.target.value)}
                className="bg-transparent text-white text-sm border-none focus:ring-0 w-32 md:w-40 [&>option]:text-black cursor-pointer"
              >
                <option value="">Set Location...</option>
                {locations.map(l => <option key={l.location_id} value={l.location_id}>{l.location_name}</option>)}
              </select>
              <button
                onClick={handleBulkLocationUpdate}
                disabled={!bulkLocationId || bulkActionLoading}
                className="p-2 hover:bg-white/10 rounded-lg transition-colors disabled:opacity-50"
                title="Update Location"
              >
                <MapPin className="w-4 h-4" />
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleBulkDelete}
              disabled={bulkActionLoading}
              className="flex items-center gap-2 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-200 rounded-xl transition-colors text-sm font-medium disabled:opacity-50"
            >
              {bulkActionLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trash2 className="w-4 h-4" />}
              <span>Delete Selected</span>
            </button>
            <button
              onClick={() => setSelectedItems([])}
              className="p-2 hover:bg-white/10 rounded-xl transition-colors text-white/60 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
