import { useState } from "react";
import { Navigation } from "./components/Navigation";
import { Dashboard } from "./components/Dashboard";
import { ItemList } from "./components/ItemList";
import { ItemDetail } from "./components/ItemDetail";
import { AddItem } from "./components/AddItem";
import { EditItem } from "./components/EditItem";
import { TagManagement } from "./components/TagManagement";
import { ReferenceManagement } from "./components/ReferenceManagement";

export default function App() {
  const [currentPage, setCurrentPage] = useState("dashboard");
  const [selectedItemId, setSelectedItemId] = useState(null);

  const handleNavigate = (page, itemId) => {
    setCurrentPage(page);
    if (itemId !== undefined) setSelectedItemId(itemId);
  };

  return (
    <div className="min-h-screen bg-[#f7f4ef]">
      <Navigation currentPage={currentPage} onNavigate={handleNavigate} />

      {currentPage === "dashboard" && <Dashboard onNavigate={handleNavigate} />}
      {currentPage === "items" && <ItemList onNavigate={handleNavigate} />}
      {currentPage === "item-detail" && selectedItemId && (
        <ItemDetail itemId={selectedItemId} onNavigate={handleNavigate} />
      )}
      {currentPage === "add-item" && <AddItem onNavigate={handleNavigate} />}
      {currentPage === "edit-item" && selectedItemId && (
        <EditItem itemId={selectedItemId} onNavigate={handleNavigate} />
      )}
      {currentPage === "tags" && <TagManagement />}
      {currentPage === "settings" && <ReferenceManagement />}
    </div>
  );
}
