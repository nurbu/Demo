import { Home, Package, PlusCircle, Tag, Settings } from "lucide-react";

export function Navigation({ currentPage, onNavigate }) {
  // nav menu items
  const navItems = [
    { id: "dashboard", label: "Home", icon: Home },
    { id: "items", label: "Items", icon: Package },
    { id: "add-item", label: "Add Item", icon: PlusCircle },
    { id: "tags", label: "Tags", icon: Tag },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  return (
    <nav className="bg-[#fefbf6] border-b border-[#e8dfd1] sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="relative w-10 h-10 rounded-full bg-gradient-to-br from-[#7a9178] to-[#6b8167] flex items-center justify-center shadow-lg">
                <Package className="w-5 h-5 text-white" />
              </div>
            </div>
            <div>
              <h1 className="text-xl m-0 p-0 text-[#4a3f35]">Academy Thrift</h1>
              <p className="text-xs m-0 p-0 text-[#a89080] tracking-wider uppercase">Inventory Management</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 relative overflow-hidden group ${isActive ? "bg-gradient-to-r from-[#7a9178] to-[#6b8167] text-white shadow-lg" : "bg-transparent text-[#6b5d52] hover:bg-[#e8dfd1]/50"}`}
                >
                  {!isActive && <div className="absolute inset-0 bg-gradient-to-r from-transparent via-[#e8dfd1]/50 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>}
                  <Icon className={`w-4 h-4 relative z-10 ${isActive ? 'animate-pulse' : ''}`} />
                  <span className="text-sm relative z-10">{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}
