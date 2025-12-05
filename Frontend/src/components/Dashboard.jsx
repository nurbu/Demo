import { useState, useEffect } from "react";
import { Package, TrendingUp, ShoppingBag, Clock, AlertCircle, Loader2 } from "lucide-react";
import { useItems, useReferenceData } from "../hooks/useInventory";
import { getImageUrl } from "../api/inventory";

export function Dashboard({ onNavigate }) {
  const [filters, setFilters] = useState({ page_size: 100 });
  const { items, total, loading, error } = useItems(filters);
  const { 
    departments, 
    statuses, 
    categories,
    getDepartmentName, 
    getStatusName,
    loading: refLoading 
  } = useReferenceData();

  // Calculate stats
  const today = new Date().toISOString().split('T')[0];
  const itemsAddedToday = items.filter(item => 
    item.date_added?.startsWith(today)
  ).length;
  
  // Find status IDs by name
  const soldStatusId = statuses.find(s => s.status_name?.toLowerCase() === 'sold')?.status_id;
  const processingStatusId = statuses.find(s => s.status_name?.toLowerCase() === 'processing')?.status_id;
  
  const itemsSold = items.filter(item => item.status_id === soldStatusId).length;
  const itemsProcessing = items.filter(item => item.status_id === processingStatusId).length;

  const recentItems = items.slice(0, 4);

  const stats = [
    { label: "Total Items", value: total, icon: Package, color: "bg-[#7a9178]", trend: "+12%" },
    { label: "Added Today", value: itemsAddedToday, icon: TrendingUp, color: "bg-[#4a5c6a]", trend: "+2" },
    { label: "Items Sold", value: itemsSold, icon: ShoppingBag, color: "bg-[#a89080]", trend: "This week" },
    { label: "Processing", value: itemsProcessing, icon: Clock, color: "bg-[#9ba896]", trend: "In queue" },
  ];

  const statusColors = {
    Available: "bg-[#7a9178] text-white",
    Sold: "bg-[#a89080] text-white",
    Processing: "bg-[#4a5c6a] text-white",
    "On Hold": "bg-[#9ba896] text-white",
    Donated: "bg-[#e8dfd1] text-[#6b5d52]",
  };

  // Get primary photo from item
  const getPrimaryPhoto = (item) => {
    if (item.photos && item.photos.length > 0) {
      const primary = item.photos.find(p => p.is_primary) || item.photos[0];
      return getImageUrl(primary.file_path);
    }
    return 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800';
  };

  if (loading || refLoading) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-8 flex items-center justify-center min-h-[400px]">
        <div className="flex items-center gap-3 text-[#7a9178]">
          <Loader2 className="w-6 h-6 animate-spin" />
          <span>Loading dashboard...</span>
        </div>
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
            <p className="text-red-500 text-xs mt-2">Make sure the backend server is running on http://localhost:8000</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="mb-8">
        <h1 className="mb-2">Dashboard</h1>
        <p className="text-[#a89080]">Overview of your inventory</p>
      </div>


      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div
              key={stat.label}
              className="relative bg-[#fefbf6] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] hover:shadow-lg hover:-translate-y-1 transition-all duration-300 overflow-hidden group"
            >
              <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-transparent to-[#e8dfd1]/20 rounded-full -mr-16 -mt-16 group-hover:scale-150 transition-transform duration-500"></div>
              <div className="flex items-start justify-between mb-4 relative z-10">
                <div className="relative">
                  <div className={`relative ${stat.color} w-12 h-12 rounded-xl flex items-center justify-center shadow-md`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs text-[#a89080] uppercase tracking-wide">{stat.trend}</p>
                </div>
              </div>
              <p className="text-xs text-[#a89080] mb-1 uppercase tracking-wider relative z-10">{stat.label}</p>
              <h2 className="m-0 relative z-10">{stat.value}</h2>
            </div>
          );
        })}
      </div>


      <div className="relative bg-gradient-to-br from-[#fefbf6] to-[#f7f4ef] rounded-2xl p-6 shadow-sm border border-[#e8dfd1] mb-8 overflow-hidden">
        <div className="absolute top-0 left-0 w-64 h-64 bg-[#7a9178]/5 rounded-full -ml-32 -mt-32"></div>
        <h3 className="mb-4 relative z-10">Quick Filters</h3>
        <div className="flex flex-wrap gap-3 relative z-10">
          <select 
            className="px-4 py-2 rounded-full border border-[#e8dfd1] bg-white text-[#6b5d52] text-sm focus:outline-none focus:ring-2 focus:ring-[#7a9178] cursor-pointer hover:border-[#a89080] transition-colors shadow-sm"
            onChange={(e) => setFilters(f => ({ ...f, department_id: e.target.value || undefined }))}
          >
            <option value="">All Departments</option>
            {departments.map((dept) => (
              <option key={dept.department_id} value={dept.department_id}>
                {dept.department_name}
              </option>
            ))}
          </select>
          <select 
            className="px-4 py-2 rounded-full border border-[#e8dfd1] bg-white text-[#6b5d52] text-sm focus:outline-none focus:ring-2 focus:ring-[#7a9178] cursor-pointer hover:border-[#a89080] transition-colors shadow-sm"
            onChange={(e) => setFilters(f => ({ ...f, category_id: e.target.value || undefined }))}
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat.category_id} value={cat.category_id}>
                {cat.category_name}
              </option>
            ))}
          </select>
          <select 
            className="px-4 py-2 rounded-full border border-[#e8dfd1] bg-white text-[#6b5d52] text-sm focus:outline-none focus:ring-2 focus:ring-[#7a9178] cursor-pointer hover:border-[#a89080] transition-colors shadow-sm"
            onChange={(e) => setFilters(f => ({ ...f, status_id: e.target.value || undefined }))}
          >
            <option value="">All Statuses</option>
            {statuses.map((status) => (
              <option key={status.status_id} value={status.status_id}>
                {status.status_name}
              </option>
            ))}
          </select>
          <button 
            onClick={() => setFilters({ page_size: 100 })}
            className="px-5 py-2 rounded-full bg-gradient-to-r from-[#7a9178] to-[#6b8167] text-white text-sm hover:shadow-lg transition-all duration-300 hover:scale-105"
          >
            Clear Filters
          </button>
        </div>
      </div>


      <div>
        <div className="flex items-center justify-between mb-6">
          <h2>Recent Items</h2>
          <button
            onClick={() => onNavigate("items")}
            className="text-sm text-[#7a9178] hover:text-[#6b8167] underline"
          >
            View All Items →
          </button>
        </div>

        {recentItems.length === 0 ? (
          <div className="bg-[#fefbf6] rounded-2xl p-12 text-center border border-[#e8dfd1]">
            <Package className="w-12 h-12 text-[#a89080] mx-auto mb-4" />
            <h3 className="text-[#6b5d52] mb-2">No items yet</h3>
            <p className="text-[#a89080] mb-4">Start adding items to your inventory</p>
            <button
              onClick={() => onNavigate("add-item")}
              className="px-6 py-2 rounded-full bg-[#7a9178] text-white hover:bg-[#6b8167] transition-colors"
            >
              Add First Item
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {recentItems.map((item) => {
              const status = getStatusName(item.status_id);

              return (
                <div
                  key={item.item_id}
                  onClick={() => onNavigate("item-detail", item.item_id)}
                  className="bg-[#fefbf6] rounded-2xl overflow-hidden shadow-sm border border-[#e8dfd1] hover:shadow-xl hover:border-[#a89080]/30 hover:-translate-y-1 transition-all duration-300 cursor-pointer group"
                >
                  <div className="aspect-square overflow-hidden bg-gradient-to-br from-[#e8dfd1] to-[#f7f4ef] relative">
                    <img
                      src={getPrimaryPhoto(item)}
                      alt={item.description}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  </div>
                  <div className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="m-0 text-base">{item.brand || 'No Brand'}</h4>
                      <span
                        className={`px-3 py-1 rounded-full text-xs shadow-sm ${
                          statusColors[status] || "bg-[#e8dfd1] text-[#6b5d52]"
                        }`}
                      >
                        {status}
                      </span>
                    </div>
                    <p className="text-sm mb-3 line-clamp-2">
                      {item.description}
                    </p>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-lg m-0">${parseFloat(item.price).toFixed(2)}</p>
                        {item.sale_price && (
                          <p className="text-xs line-through text-[#a89080] m-0">
                            ${parseFloat(item.original_price || item.price).toFixed(2)}
                          </p>
                        )}
                      </div>
                      <p className="text-xs text-[#a89080] uppercase tracking-wide">
                        {getDepartmentName(item.department_id)}
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
