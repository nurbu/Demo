import { useState } from "react";
import { Plus, Edit, Trash2, X, Settings as SettingsIcon, Loader2, AlertCircle } from "lucide-react";
import { useReferenceData } from "../hooks/useInventory";
import * as api from "../api/inventory";

export function ReferenceManagement() {
  const [activeTab, setActiveTab] = useState("departments");
  const [showAddModal, setShowAddModal] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const {
    departments,
    categories,
    itemTypes,
    sizes,
    colors,
    locations,
    conditions,
    statuses,
    loading,
    error,
    refetch,
    getDepartmentName,
    getCategoryName
  } = useReferenceData();

  const tabs = [
    { id: "departments", label: "Departments" },
    { id: "categories", label: "Categories" },
    { id: "itemTypes", label: "Item Types" },
    { id: "sizes", label: "Sizes" },
    { id: "colors", label: "Colors" },
    { id: "locations", label: "Locations" },
    { id: "conditions", label: "Conditions" },
    { id: "statuses", label: "Statuses" },
  ];

  const handleAdd = async (formData) => {
    setSubmitting(true);
    try {
      switch (activeTab) {
        case "departments":
          await api.createDepartment({
            department_name: formData.department_name,
            sort_order: departments.length + 1,
            active: true
          });
          break;
        case "categories":
          await api.createCategory({
            category_name: formData.category_name,
            department_id: parseInt(formData.department_id),
            sort_order: categories.length + 1,
            active: true
          });
          break;
        case "itemTypes":
          await api.createItemType({
            item_type_name: formData.item_type_name,
            category_id: parseInt(formData.category_id),
            sort_order: itemTypes.length + 1,
            active: true
          });
          break;
        case "sizes":
          await api.createSize({
            size_value: formData.size_value,
            size_system: formData.size_system,
            sort_order: parseInt(formData.sort_order) || sizes.length + 1,
            notes: formData.notes || null
          });
          break;
        case "colors":
          await api.createColor({
            color_name: formData.color_name,
            color_family: formData.color_family || "Neutral",
            hex_code: formData.hex_code || null,
            sort_order: parseInt(formData.sort_order) || colors.length + 1
          });
          break;
        case "locations":
          await api.createLocation({
            location_name: formData.location_name,
            location_type: formData.location_type || "Floor",
            description: formData.description || null,
            active: true
          });
          break;
        case "conditions":
          await api.createCondition({
            condition_name: formData.condition_name,
            description: formData.description || null,
            sort_order: parseInt(formData.sort_order) || conditions.length + 1
          });
          break;
        case "statuses":
          await api.createStatus({
            status_name: formData.status_name,
            description: formData.description || null,
            is_available_for_sale: formData.is_available_for_sale === 'true',
            sort_order: parseInt(formData.sort_order) || statuses.length + 1
          });
          break;
      }
      await refetch();
      setShowAddModal(false);
    } catch (err) {
      alert("Error adding item: " + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this item?")) return;

    try {
      switch (activeTab) {
        case "departments": await api.deleteDepartment(id); break;
        case "categories": await api.deleteCategory(id); break;
        case "itemTypes": await api.deleteItemType(id); break;
        case "sizes": await api.deleteSize(id); break;
        case "colors": await api.deleteColor(id); break;
        case "locations": await api.deleteLocation(id); break;
        case "conditions": await api.deleteCondition(id); break;
        case "statuses": await api.deleteStatus(id); break;
      }
      await refetch();
    } catch (err) {
      alert("Error deleting item: " + err.message);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-8 flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 text-[#7a9178] animate-spin" />
        <span className="ml-3 text-[#6b5d52]">Loading reference data...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="bg-red-50 border border-red-200 rounded-2xl p-6 flex items-center gap-4">
          <AlertCircle className="w-6 h-6 text-red-500" />
          <div>
            <h3 className="text-red-800 font-medium">Error loading data</h3>
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <SettingsIcon className="w-8 h-8 text-[#7a9178]" />
          <h1 className="m-0">Reference Tables</h1>
        </div>
        <p className="text-[#a89080]">Manage system reference data</p>
      </div>

      <div className="flex gap-2 mb-6 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-[#e8dfd1] scrollbar-track-transparent">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-6 py-3 rounded-full text-sm whitespace-nowrap transition-colors flex-shrink-0 ${activeTab === tab.id
                ? "bg-[#7a9178] text-white shadow-lg shadow-[#7a9178]/20"
                : "bg-[#fefbf6] text-[#6b5d52] border border-[#e8dfd1] hover:bg-[#e8dfd1]"
              }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="bg-[#fefbf6] rounded-2xl shadow-sm border border-[#e8dfd1]">
        <div className="p-6 border-b border-[#e8dfd1] flex items-center justify-between">
          <h3 className="m-0">{tabs.find((t) => t.id === activeTab)?.label}</h3>
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-full bg-[#7a9178] text-white text-sm hover:bg-[#6b8167] transition-colors"
          >
            <Plus className="w-4 h-4" />
            Add New
          </button>
        </div>

        <div className="p-6">
          {activeTab === "departments" && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {departments.map((dept) => (
                <div
                  key={dept.department_id}
                  className="flex items-center justify-between p-4 rounded-xl border border-[#e8dfd1] bg-white hover:bg-[#f7f4ef] transition-colors group"
                >
                  <span className="text-[#6b5d52] font-medium">{dept.department_name}</span>
                  <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => handleDelete(dept.department_id)}
                      className="p-2 hover:bg-[#e8dfd1] rounded-lg transition-colors text-[#a89080] hover:text-red-500"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === "categories" && (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-[#e8dfd1]">
                    <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Category Name</th>
                    <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Department</th>
                    <th className="px-4 py-3 text-right text-sm text-[#6b5d52]">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {categories.map((cat) => (
                    <tr key={cat.category_id} className="border-b border-[#e8dfd1] hover:bg-[#f7f4ef] transition-colors">
                      <td className="px-4 py-3 text-sm">{cat.category_name}</td>
                      <td className="px-4 py-3 text-sm text-[#a89080]">{getDepartmentName(cat.department_id)}</td>
                      <td className="px-4 py-3 text-right">
                        <button
                          onClick={() => handleDelete(cat.category_id)}
                          className="p-2 hover:bg-[#e8dfd1] rounded-lg transition-colors text-[#a89080] hover:text-red-500"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === "itemTypes" && (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-[#e8dfd1]">
                    <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Item Type</th>
                    <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Category</th>
                    <th className="px-4 py-3 text-right text-sm text-[#6b5d52]">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {itemTypes.map((type) => (
                    <tr key={type.item_type_id} className="border-b border-[#e8dfd1] hover:bg-[#f7f4ef] transition-colors">
                      <td className="px-4 py-3 text-sm">{type.item_type_name}</td>
                      <td className="px-4 py-3 text-sm text-[#a89080]">{getCategoryName(type.category_id)}</td>
                      <td className="px-4 py-3 text-right">
                        <button
                          onClick={() => handleDelete(type.item_type_id)}
                          className="p-2 hover:bg-[#e8dfd1] rounded-lg transition-colors text-[#a89080] hover:text-red-500"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === "sizes" && (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-[#e8dfd1]">
                    <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Size Value</th>
                    <th className="px-4 py-3 text-left text-sm text-[#6b5d52]">Size System</th>
                    <th className="px-4 py-3 text-right text-sm text-[#6b5d52]">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {sizes.map((size) => (
                    <tr key={size.size_id} className="border-b border-[#e8dfd1] hover:bg-[#f7f4ef] transition-colors">
                      <td className="px-4 py-3 text-sm">{size.size_value}</td>
                      <td className="px-4 py-3 text-sm text-[#a89080]">{size.size_system}</td>
                      <td className="px-4 py-3 text-right">
                        <button
                          onClick={() => handleDelete(size.size_id)}
                          className="p-2 hover:bg-[#e8dfd1] rounded-lg transition-colors text-[#a89080] hover:text-red-500"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === "colors" && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {colors.map((color) => (
                <div
                  key={color.color_id}
                  className="flex items-center justify-between p-4 rounded-xl border border-[#e8dfd1] bg-white hover:bg-[#f7f4ef] transition-colors group"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className="w-8 h-8 rounded-full border-2 border-[#e8dfd1]"
                      style={{ backgroundColor: color.hex_code || '#ccc' }}
                    />
                    <div>
                      <span className="text-sm font-medium">{color.color_name}</span>
                      <p className="text-xs text-[#a89080]">{color.color_family}</p>
                    </div>
                  </div>
                  <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => handleDelete(color.color_id)}
                      className="p-2 hover:bg-[#e8dfd1] rounded-lg transition-colors text-[#a89080] hover:text-red-500"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === "locations" && (
            <div className="space-y-2">
              {locations.map((location) => (
                <div
                  key={location.location_id}
                  className="flex items-center justify-between p-4 rounded-xl border border-[#e8dfd1] bg-white hover:bg-[#f7f4ef] transition-colors group"
                >
                  <div>
                    <span className="text-sm font-medium">{location.location_name}</span>
                    <p className="text-xs text-[#a89080]">{location.location_type}</p>
                  </div>
                  <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => handleDelete(location.location_id)}
                      className="p-2 hover:bg-[#e8dfd1] rounded-lg transition-colors text-[#a89080] hover:text-red-500"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === "conditions" && (
            <div className="space-y-2">
              {conditions.map((condition) => (
                <div
                  key={condition.condition_id}
                  className="flex items-center justify-between p-4 rounded-xl border border-[#e8dfd1] bg-white hover:bg-[#f7f4ef] transition-colors group"
                >
                  <div>
                    <p className="text-sm m-0 mb-1 font-medium">{condition.condition_name}</p>
                    <p className="text-xs text-[#a89080] m-0">{condition.description}</p>
                  </div>
                  <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => handleDelete(condition.condition_id)}
                      className="p-2 hover:bg-[#e8dfd1] rounded-lg transition-colors text-[#a89080] hover:text-red-500"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === "statuses" && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {statuses.map((status) => (
                <div
                  key={status.status_id}
                  className="flex items-center justify-between p-4 rounded-xl border border-[#e8dfd1] bg-white hover:bg-[#f7f4ef] transition-colors group"
                >
                  <div>
                    <span className="text-sm font-medium">{status.status_name}</span>
                    <p className="text-xs text-[#a89080]">
                      {status.is_available_for_sale ? "Available for sale" : "Not for sale"}
                    </p>
                  </div>
                  <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => handleDelete(status.status_id)}
                      className="p-2 hover:bg-[#e8dfd1] rounded-lg transition-colors text-[#a89080] hover:text-red-500"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-6 backdrop-blur-sm">
          <div className="bg-[#fefbf6] rounded-2xl p-8 max-w-md w-full shadow-2xl transform transition-all">
            <div className="flex items-center justify-between mb-6">
              <h2 className="m-0 text-[#6b5d52]">Add {tabs.find(t => t.id === activeTab)?.label.slice(0, -1)}</h2>
              <button
                onClick={() => setShowAddModal(false)}
                className="p-2 hover:bg-[#e8dfd1] rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-[#6b5d52]" />
              </button>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                const formData = Object.fromEntries(new FormData(e.target));
                handleAdd(formData);
              }}
            >
              <div className="space-y-4">
                {activeTab === "departments" && (
                  <div>
                    <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Department Name *</label>
                    <input
                      type="text"
                      name="department_name"
                      required
                      placeholder="e.g., Women's"
                      className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                    />
                  </div>
                )}

                {activeTab === "categories" && (
                  <>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Category Name *</label>
                      <input
                        type="text"
                        name="category_name"
                        required
                        placeholder="e.g., Tops"
                        className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                      />
                    </div>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Department *</label>
                      <select
                        name="department_id"
                        required
                        className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                      >
                        <option value="">Select department</option>
                        {departments.map(d => (
                          <option key={d.department_id} value={d.department_id}>{d.department_name}</option>
                        ))}
                      </select>
                    </div>
                  </>
                )}

                {activeTab === "itemTypes" && (
                  <>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Item Type Name *</label>
                      <input
                        type="text"
                        name="item_type_name"
                        required
                        placeholder="e.g., Blouse"
                        className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                      />
                    </div>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Category *</label>
                      <select
                        name="category_id"
                        required
                        className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                      >
                        <option value="">Select category</option>
                        {categories.map(c => (
                          <option key={c.category_id} value={c.category_id}>{c.category_name}</option>
                        ))}
                      </select>
                    </div>
                  </>
                )}

                {activeTab === "sizes" && (
                  <>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Size Value *</label>
                      <input
                        type="text"
                        name="size_value"
                        required
                        placeholder="e.g., XS, M, 8, 10"
                        className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]"
                      />
                    </div>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Size System *</label>
                      <select name="size_system" required className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]">
                        <option value="">Select system</option>
                        <option>Standard</option>
                        <option>Numeric</option>
                        <option>Universal</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2">Sort Order</label>
                      <input type="number" name="sort_order" placeholder="1" className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]" />
                    </div>
                  </>
                )}

                {activeTab === "colors" && (
                  <>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Color Name *</label>
                      <input type="text" name="color_name" required placeholder="e.g., Navy, Beige" className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]" />
                    </div>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2">Color Family</label>
                      <select name="color_family" className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]">
                        <option value="Neutral">Neutral</option>
                        <option value="Warm">Warm</option>
                        <option value="Cool">Cool</option>
                        <option value="Earth">Earth</option>
                        <option value="Bright">Bright</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2">Hex Code</label>
                      <input type="text" name="hex_code" placeholder="#000000" className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]" />
                    </div>
                  </>
                )}

                {activeTab === "locations" && (
                  <>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Location Name *</label>
                      <input type="text" name="location_name" required placeholder="e.g., Floor - Women's Section" className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]" />
                    </div>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2">Location Type</label>
                      <select name="location_type" className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]">
                        <option value="Floor">Floor</option>
                        <option value="Storage">Storage</option>
                        <option value="Display">Display</option>
                        <option value="Online">Online</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2">Description</label>
                      <textarea name="description" rows={2} placeholder="Brief description..." className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178] resize-none" />
                    </div>
                  </>
                )}

                {activeTab === "conditions" && (
                  <>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Condition Name *</label>
                      <input type="text" name="condition_name" required placeholder="e.g., Excellent, Good" className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]" />
                    </div>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2">Description</label>
                      <textarea name="description" rows={2} placeholder="Brief description..." className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178] resize-none" />
                    </div>
                  </>
                )}

                {activeTab === "statuses" && (
                  <>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2 font-medium">Status Name *</label>
                      <input type="text" name="status_name" required placeholder="e.g., Available, Sold" className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]" />
                    </div>
                    <div>
                      <label className="block text-sm text-[#6b5d52] mb-2">Available for Sale</label>
                      <select name="is_available_for_sale" className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178]">
                        <option value="true">Yes</option>
                        <option value="false">No</option>
                      </select>
                    </div>
                  </>
                )}
              </div>

              <div className="flex gap-3 mt-8">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="flex-1 px-6 py-3 rounded-xl border border-[#e8dfd1] text-[#6b5d52] hover:bg-[#e8dfd1] transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex-1 px-6 py-3 rounded-xl bg-[#7a9178] text-white hover:bg-[#6b8167] transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
                  Add
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
