import { useState, useEffect } from "react";
import { ArrowLeft, Clock, Loader2, Save } from "lucide-react";
import { useItem, useReferenceData } from "../hooks/useInventory";
import { updateItem, getImageUrl, addItemPhoto, deleteItemPhoto, uploadItemPhoto } from "../api/inventory";
import { PhotoUploader } from "./PhotoUploader";

export function EditItem({ itemId, onNavigate }) {
  const { item, loading: itemLoading, error: itemError, refetch: refetchItem } = useItem(itemId);
  const {
    departments,
    categories,
    itemTypes,
    sizes,
    colors,
    conditions,
    statuses,
    locations,
    tags,
    getCategoriesByDepartment,
    getItemTypesByCategory,
    loading: refLoading
  } = useReferenceData();

  const [selectedDepartment, setSelectedDepartment] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedTags, setSelectedTags] = useState([]);
  const [photos, setPhotos] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({
    brand: "",
    material: "",
    description: "",
    item_type_id: "",
    size_id: "",
    color_primary_id: "",
    color_secondary_id: "",
    condition_id: "",
    status_id: "",
    current_location_id: "",
    price: "",
    original_price: "",
    sale_price: "",
    on_sale: false,
    season: "",
    customer_notes: "",
    internal_notes: "",
  });

  // Initialize form when item loads
  useEffect(() => {
    if (item) {
      setSelectedDepartment(item.department_id);
      setSelectedCategory(item.category_id);
      setSelectedTags(item.tags?.map(t => t.tag_id) || []);
      setPhotos(item.photos?.map(p => ({
        ...p,
        url: getImageUrl(p.file_path)
      })) || []);
      setFormData({
        brand: item.brand || "",
        material: item.material || "",
        description: item.description || "",
        item_type_id: item.item_type_id || "",
        size_id: item.size_id || "",
        color_primary_id: item.color_primary_id || "",
        color_secondary_id: item.color_secondary_id || "",
        condition_id: item.condition_id || "",
        status_id: item.status_id || "",
        current_location_id: item.current_location_id || "",
        price: item.price || "",
        original_price: item.original_price || "",
        sale_price: item.sale_price || "",
        on_sale: item.on_sale || false,
        season: item.season || "",
        customer_notes: item.customer_notes || "",
        internal_notes: item.internal_notes || "",
      });
    }
  }, [item]);

  const filteredCategories = selectedDepartment
    ? getCategoriesByDepartment(parseInt(selectedDepartment))
    : [];

  const filteredItemTypes = selectedCategory
    ? getItemTypesByCategory(parseInt(selectedCategory))
    : [];

  const toggleTag = (tagId) => {
    setSelectedTags(prev =>
      prev.includes(tagId) ? prev.filter(id => id !== tagId) : [...prev, tagId]
    );
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handlePhotosChange = async (updatedPhotos) => {
    // Check for deletions
    const deletedPhotos = photos.filter(p => !updatedPhotos.includes(p));

    for (const photo of deletedPhotos) {
      if (photo.photo_id) {
        if (window.confirm("Are you sure you want to delete this photo?")) {
          try {
            await deleteItemPhoto(photo.photo_id);
          } catch (err) {
            console.error("Error deleting photo:", err);
            alert("Failed to delete photo");
            return; // Don't update state if delete failed
          }
        } else {
          return; // Cancelled
        }
      }
    }

    setPhotos(updatedPhotos);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      // 1. Update item details
      const itemData = {
        department_id: parseInt(selectedDepartment),
        category_id: parseInt(selectedCategory),
        item_type_id: parseInt(formData.item_type_id),
        brand: formData.brand || null,
        size_id: parseInt(formData.size_id),
        color_primary_id: parseInt(formData.color_primary_id),
        color_secondary_id: formData.color_secondary_id ? parseInt(formData.color_secondary_id) : null,
        material: formData.material || null,
        condition_id: parseInt(formData.condition_id),
        status_id: parseInt(formData.status_id),
        current_location_id: formData.current_location_id ? parseInt(formData.current_location_id) : null,
        price: parseFloat(formData.price),
        original_price: formData.original_price ? parseFloat(formData.original_price) : null,
        on_sale: formData.on_sale,
        sale_price: formData.sale_price ? parseFloat(formData.sale_price) : null,
        description: formData.description,
        internal_notes: formData.internal_notes || null,
        customer_notes: formData.customer_notes || null,
        season: formData.season || null,
        tag_ids: selectedTags,
      };

      await updateItem(itemId, itemData);

      // 2. Upload new photos
      const newPhotosToUpload = photos.filter(p => p instanceof File);
      if (newPhotosToUpload.length > 0) {
        await Promise.all(newPhotosToUpload.map(async (photo) => {
          const index = photos.indexOf(photo);
          await uploadItemPhoto(itemId, photo, index === 0, index + 1);
        }));
      }

      alert('Item updated');
      refetchItem(); 
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (itemLoading || refLoading) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-8 flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 text-[#7a9178] animate-spin" />
        <span className="ml-3 text-[#6b5d52]">Loading item...</span>
      </div>
    );
  }

  if (itemError) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="bg-red-50 border border-red-200 rounded-2xl p-6">
          <h3 className="text-red-800 font-medium">Error loading item</h3>
          <p className="text-red-600 text-sm">{itemError}</p>
        </div>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-8">
        <p>Item not found</p>
      </div>
    );
  }

  const history = item.history || [];

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="mb-8">
        <button
          onClick={() => onNavigate("item-detail", itemId)}
          className="flex items-center gap-2 text-[#6b5d52] hover:text-[#4a3f35] transition-colors mb-4"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back to Item Details</span>
        </button>
        <h1 className="mb-2">Edit Item</h1>
        <p className="text-[#a89080]">Update item information</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-4 mb-6">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <form onSubmit={handleSubmit}>
            <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] mb-6">
              <h3 className="mb-4 text-[#6b5d52]">Photos</h3>
              <PhotoUploader
                currentPhotos={photos}
                onPhotosChange={handlePhotosChange}
              />
            </div>

            <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] mb-6">
              <h3 className="mb-4 text-[#6b5d52]">Basic Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Brand</label>
                  <input
                    type="text"
                    name="brand"
                    value={formData.brand}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  />
                </div>
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Material</label>
                  <input
                    type="text"
                    name="material"
                    value={formData.material}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Description</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178] resize-none"
                  />
                </div>
              </div>
            </div>

            <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] mb-6">
              <h3 className="mb-4 text-[#6b5d52]">Classification</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Department</label>
                  <select
                    value={selectedDepartment || ""}
                    onChange={(e) => {
                      setSelectedDepartment(parseInt(e.target.value) || null);
                      setSelectedCategory(null);
                    }}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  >
                    {departments.map((dept) => (
                      <option key={dept.department_id} value={dept.department_id}>
                        {dept.department_name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Category</label>
                  <select
                    value={selectedCategory || ""}
                    onChange={(e) => setSelectedCategory(parseInt(e.target.value) || null)}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  >
                    {filteredCategories.map((cat) => (
                      <option key={cat.category_id} value={cat.category_id}>
                        {cat.category_name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Item Type</label>
                  <select
                    name="item_type_id"
                    value={formData.item_type_id}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  >
                    {filteredItemTypes.map((type) => (
                      <option key={type.item_type_id} value={type.item_type_id}>
                        {type.item_type_name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] mb-6">
              <h3 className="mb-4 text-[#6b5d52]">Size & Colors</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Size</label>
                  <select
                    name="size_id"
                    value={formData.size_id}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  >
                    {sizes.map((size) => (
                      <option key={size.size_id} value={size.size_id}>
                        {size.size_value} ({size.size_system})
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Primary Color</label>
                  <select
                    name="color_primary_id"
                    value={formData.color_primary_id}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  >
                    {colors.map((color) => (
                      <option key={color.color_id} value={color.color_id}>
                        {color.color_name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Secondary Color</label>
                  <select
                    name="color_secondary_id"
                    value={formData.color_secondary_id}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  >
                    <option value="">None</option>
                    {colors.map((color) => (
                      <option key={color.color_id} value={color.color_id}>
                        {color.color_name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] mb-6">
              <h3 className="mb-4 text-[#6b5d52]">Condition & Status</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Condition</label>
                  <select
                    name="condition_id"
                    value={formData.condition_id}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  >
                    {conditions.map((cond) => (
                      <option key={cond.condition_id} value={cond.condition_id}>
                        {cond.condition_name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Status</label>
                  <select
                    name="status_id"
                    value={formData.status_id}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  >
                    {statuses.map((status) => (
                      <option key={status.status_id} value={status.status_id}>
                        {status.status_name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Location</label>
                  <select
                    name="current_location_id"
                    value={formData.current_location_id}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  >
                    <option value="">None</option>
                    {locations.map((loc) => (
                      <option key={loc.location_id} value={loc.location_id}>
                        {loc.location_name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] mb-6">
              <h3 className="mb-4 text-[#6b5d52]">Pricing</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Price</label>
                  <div className="relative">
                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-[#a89080]">$</span>
                    <input
                      type="number"
                      step="0.01"
                      name="price"
                      value={formData.price}
                      onChange={handleInputChange}
                      className="w-full pl-8 pr-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Original Price</label>
                  <div className="relative">
                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-[#a89080]">$</span>
                    <input
                      type="number"
                      step="0.01"
                      name="original_price"
                      value={formData.original_price}
                      onChange={handleInputChange}
                      className="w-full pl-8 pr-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Season</label>
                  <select
                    name="season"
                    value={formData.season}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                  >
                    <option value="">Select season</option>
                    <option>Spring</option>
                    <option>Summer</option>
                    <option>Fall</option>
                    <option>Winter</option>
                    <option>All Season</option>
                    <option>Fall/Winter</option>
                    <option>Spring/Summer</option>
                  </select>
                </div>
              </div>
              <div className="mt-4 p-4 rounded-xl bg-[#7a9178]/10 border border-[#7a9178]/20">
                <div className="flex items-center gap-4 mb-4">
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      name="on_sale"
                      checked={formData.on_sale}
                      onChange={handleInputChange}
                      className="rounded"
                    />
                    <span className="text-sm text-[#6b5d52]">Item is on sale</span>
                  </label>
                </div>
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Sale Price</label>
                  <div className="relative">
                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-[#a89080]">$</span>
                    <input
                      type="number"
                      step="0.01"
                      name="sale_price"
                      value={formData.sale_price}
                      onChange={handleInputChange}
                      className="w-full pl-8 pr-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] mb-6">
              <h3 className="mb-4 text-[#6b5d52]">Tags</h3>
              <div className="flex flex-wrap gap-2">
                {tags.map((tag) => {
                  const isSelected = selectedTags.includes(tag.tag_id);
                  return (
                    <button
                      key={tag.tag_id}
                      type="button"
                      onClick={() => toggleTag(tag.tag_id)}
                      className={`px-4 py-2 rounded-full text-sm border transition-colors ${isSelected
                        ? "bg-[#7a9178] text-white border-[#7a9178]"
                        : "bg-white text-[#6b5d52] border-[#e8dfd1] hover:bg-[#e8dfd1]"
                        }`}
                    >
                      {tag.tag_name}
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] mb-6">
              <h3 className="mb-4 text-[#6b5d52]">Notes</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Customer Notes</label>
                  <textarea
                    name="customer_notes"
                    value={formData.customer_notes}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178] resize-none"
                  />
                </div>
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Internal Notes</label>
                  <textarea
                    name="internal_notes"
                    value={formData.internal_notes}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178] resize-none"
                  />
                </div>
              </div>
            </div>

            <div className="flex gap-4 justify-end">
              <button
                type="button"
                onClick={() => onNavigate("item-detail", itemId)}
                className="px-8 py-3 rounded-xl border border-[#e8dfd1] text-[#6b5d52] hover:bg-[#e8dfd1] transition-colors font-medium"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="px-8 py-3 rounded-xl bg-[#7a9178] text-white hover:bg-[#6b8167] transition-colors disabled:opacity-50 flex items-center gap-2 font-medium shadow-lg shadow-[#7a9178]/20"
              >
                {submitting && <Loader2 className="w-5 h-5 animate-spin" />}
                {submitting ? "Saving..." : "Save Changes"}
              </button>
            </div>
          </form>
        </div>

        <div className="lg:col-span-1">
          <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] sticky top-8">
            <div className="flex items-center gap-2 mb-4">
              <Clock className="w-5 h-5 text-[#7a9178]" />
              <h3 className="m-0 text-[#6b5d52]">Audit History</h3>
            </div>
            <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-[#e8dfd1] scrollbar-track-transparent">
              {history.length > 0 ? (
                history.map((event) => (
                  <div key={event.history_id} className="pb-3 border-b border-[#e8dfd1] last:border-0 last:pb-0">
                    <p className="text-sm font-medium text-[#6b5d52] m-0 mb-1">{event.action}</p>
                    <p className="text-xs text-[#a89080] mb-1">
                      {new Date(event.action_date).toLocaleDateString()} at {new Date(event.action_date).toLocaleTimeString()}
                    </p>
                    {event.old_value && (
                      <div className="text-xs text-[#6b5d52] bg-white p-2 rounded-lg border border-[#e8dfd1] mt-1">
                        <span className="font-medium">Previous:</span> {event.old_value}
                      </div>
                    )}
                    {event.notes && (
                      <p className="text-xs text-[#a89080] mt-1 italic">{event.notes}</p>
                    )}
                  </div>
                ))
              ) : (
                <p className="text-sm text-[#a89080]">No history available</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
