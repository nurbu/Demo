import { useState } from "react";
import { ArrowLeft, Edit, Trash2, ChevronLeft, ChevronRight, Loader2, AlertCircle } from "lucide-react";
import { useItem, useReferenceData } from "../hooks/useInventory";
import { deleteItem, getImageUrl } from "../api/inventory";

export function ItemDetail({ itemId, onNavigate }) {
  const { item, loading, error } = useItem(itemId);
  const {
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
    loading: refLoading
  } = useReferenceData();
  
  const [currentPhotoIndex, setCurrentPhotoIndex] = useState(0);

  if (loading || refLoading) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-8 flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 text-[#7a9178] animate-spin" />
        <span className="ml-3 text-[#6b5d52]">Loading item details...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="bg-red-50 border border-red-200 rounded-2xl p-6 flex items-center gap-4">
          <AlertCircle className="w-6 h-6 text-red-500" />
          <div>
            <h3 className="text-red-800 font-medium">Error loading item</h3>
            <p className="text-red-600 text-sm">{error}</p>
          </div>
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

  const allPhotos = item.photos && item.photos.length > 0 
    ? item.photos.map(p => getImageUrl(p.file_path))
    : ['https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800'];
  
  const itemTags = item.tags?.map((tag) => tag.tag_name).filter(Boolean) || [];
  const history = item.history || [];

  const nextPhoto = () => {
    setCurrentPhotoIndex((prev) => (prev + 1) % allPhotos.length);
  };

  const prevPhoto = () => {
    setCurrentPhotoIndex((prev) => (prev - 1 + allPhotos.length) % allPhotos.length);
  };

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this item?")) {
      try {
        await deleteItem(itemId);
        onNavigate("items");
      } catch (err) {
        alert("Error deleting item: " + err.message);
      }
    }
  };

  const statusColors = {
    Available: "bg-[#7a9178] text-white",
    Sold: "bg-[#a89080] text-white",
    Processing: "bg-[#4a5c6a] text-white",
    "On Hold": "bg-[#9ba896] text-white",
    Donated: "bg-[#e8dfd1] text-[#6b5d52]",
  };

  const status = getStatusName(item.status_id);

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <button
          onClick={() => onNavigate("items")}
          className="flex items-center gap-2 text-[#6b5d52] hover:text-[#4a3f35] transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back to Items</span>
        </button>
        <div className="flex gap-3">
          <button
            onClick={() => onNavigate("edit-item", itemId)}
            className="flex items-center gap-2 px-6 py-2 rounded-full bg-[#7a9178] text-white hover:bg-[#6b8167] transition-colors"
          >
            <Edit className="w-4 h-4" />
            Edit Item
          </button>
          <button 
            onClick={handleDelete}
            className="flex items-center gap-2 px-6 py-2 rounded-full border border-[#e8dfd1] text-[#a89080] hover:bg-[#e8dfd1] transition-colors"
          >
            <Trash2 className="w-4 h-4" />
            Delete
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Photo Gallery */}
        <div>
          <div className="bg-[#fefbf6] rounded-2xl overflow-hidden shadow-sm border border-[#e8dfd1] mb-4">
            <div className="aspect-square relative bg-[#e8dfd1]">
              <img
                src={allPhotos[currentPhotoIndex]}
                alt={item.brand}
                className="w-full h-full object-cover"
              />
              {allPhotos.length > 1 && (
                <>
                  <button
                    onClick={prevPhoto}
                    className="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-white/95 flex items-center justify-center hover:bg-white transition-colors shadow-md"
                  >
                    <ChevronLeft className="w-5 h-5 text-[#6b5d52]" />
                  </button>
                  <button
                    onClick={nextPhoto}
                    className="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-white/95 flex items-center justify-center hover:bg-white transition-colors shadow-md"
                  >
                    <ChevronRight className="w-5 h-5 text-[#6b5d52]" />
                  </button>
                  <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
                    {allPhotos.map((_, index) => (
                      <button
                        key={index}
                        onClick={() => setCurrentPhotoIndex(index)}
                        className={`w-2 h-2 rounded-full transition-all ${
                          index === currentPhotoIndex
                            ? "bg-white w-6"
                            : "bg-white/50 hover:bg-white/75"
                        }`}
                      />
                    ))}
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Thumbnail Gallery */}
          {allPhotos.length > 1 && (
            <div className="grid grid-cols-4 gap-3">
              {allPhotos.map((photo, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentPhotoIndex(index)}
                  className={`aspect-square rounded-xl overflow-hidden border-2 transition-all ${
                    index === currentPhotoIndex
                      ? "border-[#7a9178] shadow-md"
                      : "border-[#e8dfd1] hover:border-[#a89080]"
                  }`}
                >
                  <img src={photo} alt={`View ${index + 1}`} className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Item Details */}
        <div>
          <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] mb-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h1 className="mb-2">{item.brand || 'No Brand'}</h1>
                <p className="text-[#a89080]">{getItemTypeName(item.item_type_id)}</p>
              </div>
              <span
                className={`px-4 py-2 rounded-full text-sm ${
                  statusColors[status] || "bg-[#e8dfd1] text-[#6b5d52]"
                }`}
              >
                {status}
              </span>
            </div>

            {/* Price Section */}
            <div className="mb-6 pb-6 border-b border-[#e8dfd1]">
              <div className="flex items-baseline gap-3">
                <h2 className="m-0">${parseFloat(item.price).toFixed(2)}</h2>
                {item.on_sale && item.sale_price && (
                  <span className="text-lg line-through text-[#a89080]">
                    ${parseFloat(item.original_price || item.price).toFixed(2)}
                  </span>
                )}
              </div>
              {item.original_price && (
                <p className="text-sm text-[#7a9178] mt-2">
                  Originally ${parseFloat(item.original_price).toFixed(2)}
                </p>
              )}
            </div>

            {/* Description */}
            <div className="mb-6">
              <h4 className="mb-2">Description</h4>
              <p className="text-[#6b5d52]">{item.description}</p>
            </div>

            {/* Tags */}
            {itemTags.length > 0 && (
              <div className="mb-6">
                <h4 className="mb-3">Tags</h4>
                <div className="flex flex-wrap gap-2">
                  {itemTags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 rounded-full bg-[#e8dfd1] text-[#6b5d52] text-sm border border-[#a89080]/20"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Customer Notes */}
            {item.customer_notes && (
              <div className="mb-6 p-4 rounded-xl bg-[#7a9178]/10 border border-[#7a9178]/20">
                <h4 className="mb-2 text-sm">Customer Notes</h4>
                <p className="text-sm text-[#6b5d52]">{item.customer_notes}</p>
              </div>
            )}

            {/* Internal Notes */}
            {item.internal_notes && (
              <div className="p-4 rounded-xl bg-[#4a5c6a]/10 border border-[#4a5c6a]/20">
                <h4 className="mb-2 text-sm">Internal Notes</h4>
                <p className="text-sm text-[#6b5d52]">{item.internal_notes}</p>
              </div>
            )}
          </div>

          {/* Detailed Specifications */}
          <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1]">
            <h3 className="mb-4">Item Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-[#a89080] mb-1">Department</p>
                <p className="text-[#6b5d52]">{getDepartmentName(item.department_id)}</p>
              </div>
              <div>
                <p className="text-sm text-[#a89080] mb-1">Category</p>
                <p className="text-[#6b5d52]">{getCategoryName(item.category_id)}</p>
              </div>
              <div>
                <p className="text-sm text-[#a89080] mb-1">Item Type</p>
                <p className="text-[#6b5d52]">{getItemTypeName(item.item_type_id)}</p>
              </div>
              <div>
                <p className="text-sm text-[#a89080] mb-1">Size</p>
                <p className="text-[#6b5d52]">
                  {getSizeName(item.size_id)} ({getSizeSystem(item.size_id)})
                </p>
              </div>
              <div>
                <p className="text-sm text-[#a89080] mb-1">Primary Color</p>
                <p className="text-[#6b5d52]">{getColorName(item.color_primary_id)}</p>
              </div>
              {item.color_secondary_id && (
                <div>
                  <p className="text-sm text-[#a89080] mb-1">Secondary Color</p>
                  <p className="text-[#6b5d52]">{getColorName(item.color_secondary_id)}</p>
                </div>
              )}
              <div>
                <p className="text-sm text-[#a89080] mb-1">Material</p>
                <p className="text-[#6b5d52]">{item.material || 'Not specified'}</p>
              </div>
              <div>
                <p className="text-sm text-[#a89080] mb-1">Condition</p>
                <p className="text-[#6b5d52]">{getConditionName(item.condition_id)}</p>
              </div>
              <div>
                <p className="text-sm text-[#a89080] mb-1">Season</p>
                <p className="text-[#6b5d52]">{item.season || 'Not specified'}</p>
              </div>
              <div>
                <p className="text-sm text-[#a89080] mb-1">Date Added</p>
                <p className="text-[#6b5d52]">{new Date(item.date_added).toLocaleDateString()}</p>
              </div>
              <div className="col-span-2">
                <p className="text-sm text-[#a89080] mb-1">Current Location</p>
                <p className="text-[#6b5d52]">{getLocationName(item.current_location_id) || 'Not assigned'}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Item History Timeline */}
      <div className="bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1]">
        <h3 className="mb-6">Item History</h3>
        <div className="space-y-4">
          {history.length > 0 ? (
            history.map((event, index) => (
              <div key={event.history_id} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-3 h-3 rounded-full bg-[#7a9178]" />
                  {index < history.length - 1 && (
                    <div className="w-0.5 h-full bg-[#e8dfd1] flex-1 mt-2" />
                  )}
                </div>
                <div className="flex-1 pb-6">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h4 className="m-0 text-base">{event.action}</h4>
                      <p className="text-sm text-[#a89080] mt-1">
                        {new Date(event.action_date).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  {event.old_value && (
                    <p className="text-sm text-[#6b5d52]">{event.old_value}</p>
                  )}
                  {event.notes && (
                    <p className="text-xs text-[#a89080] mt-1">{event.notes}</p>
                  )}
                </div>
              </div>
            ))
          ) : (
            <p className="text-[#a89080] text-center py-8">No history available for this item</p>
          )}
        </div>
      </div>
    </div>
  );
}
