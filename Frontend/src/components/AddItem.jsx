import { useState, useEffect } from "react";
import { Plus, Save, X, Loader2, ArrowLeft } from "lucide-react";
import { useReferenceData } from "../hooks/useInventory";
import { createItem, addItemPhoto, uploadItemPhoto } from "../api/inventory";
import { PhotoUploader } from "./PhotoUploader";

export function AddItem({ onNavigate }) {
  const {
    departments,
    categories,
    itemTypes,
    sizes,
    colors,
    conditions,
    statuses,
    tags,
    locations,
    loading,
    refetch,
    getCategoriesByDepartment,
    getItemTypesByCategory
  } = useReferenceData();

  const [formData, setFormData] = useState({
    department_id: "",
    category_id: "",
    item_type_id: "",
    brand: "",
    size_id: "",
    color_primary_id: "",
    color_secondary_id: "",
    material: "",
    condition_id: "",
    status_id: "",
    current_location_id: "",
    price: "",
    original_price: "",
    on_sale: false,
    sale_price: "",
    description: "",
    internal_notes: "",
    customer_notes: "",
    season: "",
  });

  const [selectedTags, setSelectedTags] = useState([]);
  const [photos, setPhotos] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [filteredCategories, setFilteredCategories] = useState([]);
  const [filteredItemTypes, setFilteredItemTypes] = useState([]);

  // Effect to filter categories when department changes
  useEffect(() => {
    if (formData.department_id) {
      const cats = getCategoriesByDepartment(parseInt(formData.department_id));
      setFilteredCategories(cats);
    } else {
      setFilteredCategories([]);
    }
  }, [formData.department_id, getCategoriesByDepartment]);

  // Effect to filter item types when category changes
  useEffect(() => {
    if (formData.category_id) {
      const types = getItemTypesByCategory(parseInt(formData.category_id));
      setFilteredItemTypes(types);
    } else {
      setFilteredItemTypes([]);
    }
  }, [formData.category_id, getItemTypesByCategory]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleTagToggle = (tagId) => {
    setSelectedTags((prev) =>
      prev.includes(tagId)
        ? prev.filter((id) => id !== tagId)
        : [...prev, tagId]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      // 1. Create the item
      const itemData = {
        ...formData,
        department_id: parseInt(formData.department_id),
        category_id: parseInt(formData.category_id),
        item_type_id: parseInt(formData.item_type_id),
        size_id: parseInt(formData.size_id),
        color_primary_id: parseInt(formData.color_primary_id),
        color_secondary_id: formData.color_secondary_id ? parseInt(formData.color_secondary_id) : null,
        condition_id: parseInt(formData.condition_id),
        status_id: parseInt(formData.status_id),
        current_location_id: formData.current_location_id ? parseInt(formData.current_location_id) : null,
        price: parseFloat(formData.price),
        original_price: formData.original_price ? parseFloat(formData.original_price) : null,
        sale_price: formData.sale_price ? parseFloat(formData.sale_price) : null,
        tag_ids: selectedTags,
      };

      const newItem = await createItem(itemData);

      // 2. Add photos
      if (newItem && photos.length > 0) {
        await Promise.all(photos.map(async (photo, index) => {
          if (photo instanceof File) {
            await uploadItemPhoto(newItem.item_id, photo, index === 0, index + 1);
          }
        }));
      }

      console.log('Item created:', newItem);
      alert("Item created successfully!");
      onNavigate("items"); // Ensure we go back to the list ('items' seems to be the page key in App.jsx for ItemList)
    } catch (err) {
      console.error('Failed to create item:', err);
      alert("Error: " + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 text-[#7a9178] animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-4">
          <button
            onClick={() => onNavigate("items")}
            className="p-2 rounded-full hover:bg-[#e8dfd1] transition-colors"
          >
            <ArrowLeft className="w-6 h-6 text-[#6b5d52]" />
          </button>
          <div>
            <h1 className="m-0">Add New Item</h1>
            <p className="text-[#a89080]">Create a new inventory listing</p>
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">

        <section className="bg-white rounded-2xl p-6 shadow-sm border border-[#e8dfd1]">
          <h3 className="text-[#6b5d52] mb-4">Photos</h3>
          <PhotoUploader
            currentPhotos={photos}
            onPhotosChange={setPhotos}
          />
        </section>


        <section className="bg-white rounded-2xl p-6 shadow-sm border border-[#e8dfd1]">
          <h3 className="text-[#6b5d52] mb-6">Basic Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Department *</label>
              <select
                name="department_id"
                required
                value={formData.department_id}
                onChange={handleInputChange}
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">Select Department</option>
                {departments.map(d => (
                  <option key={d.department_id} value={d.department_id}>{d.department_name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Category *</label>
              <select
                name="category_id"
                required
                value={formData.category_id}
                onChange={handleInputChange}
                disabled={!formData.department_id}
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178] disabled:opacity-50"
              >
                <option value="">Select Category</option>
                {filteredCategories.map(c => (
                  <option key={c.category_id} value={c.category_id}>{c.category_name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Item Type *</label>
              <select
                name="item_type_id"
                required
                value={formData.item_type_id}
                onChange={handleInputChange}
                disabled={!formData.category_id}
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178] disabled:opacity-50"
              >
                <option value="">Select Item Type</option>
                {filteredItemTypes.map(t => (
                  <option key={t.item_type_id} value={t.item_type_id}>{t.item_type_name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Brand</label>
              <input
                type="text"
                name="brand"
                value={formData.brand}
                onChange={handleInputChange}
                placeholder="e.g. Nike, Zara"
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              />
            </div>
          </div>
        </section>


        <section className="bg-white rounded-2xl p-6 shadow-sm border border-[#e8dfd1]">
          <h3 className="text-[#6b5d52] mb-6">Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Size *</label>
              <select
                name="size_id"
                required
                value={formData.size_id}
                onChange={handleInputChange}
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">Select Size</option>
                {sizes.map(s => (
                  <option key={s.size_id} value={s.size_id}>{s.size_value} ({s.size_system})</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Material</label>
              <input
                type="text"
                name="material"
                value={formData.material}
                onChange={handleInputChange}
                placeholder="e.g. Cotton, Silk"
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              />
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Primary Color *</label>
              <select
                name="color_primary_id"
                required
                value={formData.color_primary_id}
                onChange={handleInputChange}
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">Select Color</option>
                {colors.map(c => (
                  <option key={c.color_id} value={c.color_id}>{c.color_name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Secondary Color</label>
              <select
                name="color_secondary_id"
                value={formData.color_secondary_id}
                onChange={handleInputChange}
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">None</option>
                {colors.map(c => (
                  <option key={c.color_id} value={c.color_id}>{c.color_name}</option>
                ))}
              </select>
            </div>
          </div>
        </section>


        <section className="bg-white rounded-2xl p-6 shadow-sm border border-[#e8dfd1]">
          <h3 className="text-[#6b5d52] mb-6">Status & Price</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Condition *</label>
              <select
                name="condition_id"
                required
                value={formData.condition_id}
                onChange={handleInputChange}
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">Select Condition</option>
                {conditions.map(c => (
                  <option key={c.condition_id} value={c.condition_id}>{c.condition_name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Status *</label>
              <select
                name="status_id"
                required
                value={formData.status_id}
                onChange={handleInputChange}
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">Select Status</option>
                {statuses.map(s => (
                  <option key={s.status_id} value={s.status_id}>{s.status_name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Location</label>
              <select
                name="current_location_id"
                value={formData.current_location_id}
                onChange={handleInputChange}
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              >
                <option value="">Select Location</option>
                {locations.map(l => (
                  <option key={l.location_id} value={l.location_id}>{l.location_name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Season</label>
              <input
                type="text"
                name="season"
                value={formData.season}
                onChange={handleInputChange}
                placeholder="e.g. SS24, FW23"
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
              />
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Price *</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-[#a89080]">$</span>
                <input
                  type="number"
                  name="price"
                  required
                  min="0"
                  step="0.01"
                  value={formData.price}
                  onChange={handleInputChange}
                  className="w-full pl-8 pr-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Original Price</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-[#a89080]">$</span>
                <input
                  type="number"
                  name="original_price"
                  min="0"
                  step="0.01"
                  value={formData.original_price}
                  onChange={handleInputChange}
                  className="w-full pl-8 pr-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                />
              </div>
            </div>
          </div>
        </section>


        <section className="bg-white rounded-2xl p-6 shadow-sm border border-[#e8dfd1]">
          <h3 className="text-[#6b5d52] mb-4">Tags</h3>
          <div className="flex flex-wrap gap-2">
            {tags.map(tag => (
              <button
                key={tag.tag_id}
                type="button"
                onClick={() => handleTagToggle(tag.tag_id)}
                className={`px-4 py-2 rounded-full text-sm transition-colors border ${selectedTags.includes(tag.tag_id)
                  ? "bg-[#7a9178] text-white border-[#7a9178]"
                  : "bg-[#fefbf6] text-[#6b5d52] border-[#e8dfd1] hover:bg-[#e8dfd1]"
                  }`}
              >
                {tag.tag_name}
              </button>
            ))}
          </div>
        </section>


        <section className="bg-white rounded-2xl p-6 shadow-sm border border-[#e8dfd1]">
          <h3 className="text-[#6b5d52] mb-6">Notes</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Description *</label>
              <textarea
                name="description"
                required
                rows={4}
                value={formData.description}
                onChange={handleInputChange}
                className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178] resize-y"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Internal Notes</label>
                <textarea
                  name="internal_notes"
                  rows={3}
                  value={formData.internal_notes}
                  onChange={handleInputChange}
                  placeholder="Only visible to staff"
                  className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178] resize-none"
                />
              </div>

              <div>
                <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Customer Notes</label>
                <textarea
                  name="customer_notes"
                  rows={3}
                  value={formData.customer_notes}
                  onChange={handleInputChange}
                  placeholder="Visible on receipt/online"
                  className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-[#fefbf6] text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178] resize-none"
                />
              </div>
            </div>
          </div>
        </section>

        <div className="flex items-center justify-end gap-4 pt-4">
          <button
            type="button"
            onClick={() => onNavigate("items")}
            className="px-8 py-3 rounded-xl border border-[#e8dfd1] text-[#6b5d52] hover:bg-[#e8dfd1] transition-colors font-medium"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="px-8 py-3 rounded-xl bg-[#7a9178] text-white hover:bg-[#6b8167] transition-colors shadow-lg shadow-[#7a9178]/20 flex items-center gap-2 font-medium disabled:opacity-50"
          >
            {submitting ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Saving...
              </>
            ) : (
              <>
                <Save className="w-5 h-5" />
                Save Item
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
