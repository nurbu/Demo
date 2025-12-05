import { useState } from "react";
import { Plus, Edit, Trash2, X, Loader2, Tag } from "lucide-react";
import { useReferenceData } from "../hooks/useInventory";
import { createTag, deleteTag } from "../api/inventory";

export function TagManagement() {
  const [showAddModal, setShowAddModal] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const { tags, refetch, loading } = useReferenceData();

  const handleAddTag = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    const formData = new FormData(e.target);
    const tagName = formData.get("tag_name");

    try {
      await createTag({
        tag_name: tagName,
        tag_category: "General",
        active: true
      });
      await refetch();
      setShowAddModal(false);
    } catch (err) {
      alert("Error adding tag: " + err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteTag = async (tagId) => {
    if (window.confirm("Are you sure you want to delete this tag?")) {
      try {
        await deleteTag(tagId);
        refetch();
      } catch (err) {
        alert("Error deleting tag: " + err.message);
      }
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-8 flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 text-[#7a9178] animate-spin" />
        <span className="ml-3 text-[#6b5d52]">Loading tags...</span>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="mb-2">Tag Management</h1>
          <p className="text-[#a89080]">Organize and manage your inventory tags</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 px-6 py-3 rounded-full bg-[#7a9178] text-white hover:bg-[#6b8167] transition-colors shadow-lg shadow-[#7a9178]/20"
        >
          <Plus className="w-5 h-5" />
          Add New Tag
        </button>
      </div>

      {tags.length === 0 ? (
        <div className="bg-[#fefbf6] rounded-2xl p-12 text-center border border-[#e8dfd1] flex flex-col items-center">
          <div className="w-16 h-16 rounded-full bg-[#e8dfd1]/50 flex items-center justify-center mb-4">
            <Tag className="w-8 h-8 text-[#a89080]" />
          </div>
          <h3 className="text-[#6b5d52] mb-2">No tags found</h3>
          <p className="text-[#a89080] mb-4">Create tags to organize your inventory</p>
          <button
            onClick={() => setShowAddModal(true)}
            className="px-6 py-2 rounded-full border border-[#7a9178] text-[#7a9178] hover:bg-[#7a9178] hover:text-white transition-colors"
          >
            Create First Tag
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tags.map((tag) => (
            <div
              key={tag.tag_id}
              className="flex items-center justify-between p-4 rounded-xl border border-[#e8dfd1] bg-white hover:bg-[#f7f4ef] transition-colors group"
            >
              <div className="flex items-center gap-3">
                <span className="w-8 h-8 rounded-full bg-[#e8dfd1]/30 flex items-center justify-center text-[#6b5d52]">
                  <Tag className="w-4 h-4" />
                </span>
                <span className="text-[#6b5d52] font-medium">{tag.tag_name}</span>
              </div>
              <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={() => handleDeleteTag(tag.tag_id)}
                  className="p-2 hover:bg-[#e8dfd1] rounded-lg transition-colors text-[#a89080] hover:text-red-500"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Tag Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-6 backdrop-blur-sm">
          <div className="bg-[#fefbf6] rounded-2xl p-8 max-w-md w-full shadow-2xl transform transition-all">
            <div className="flex items-center justify-between mb-6">
              <h2 className="m-0 text-[#6b5d52]">Add New Tag</h2>
              <button
                onClick={() => setShowAddModal(false)}
                className="p-2 hover:bg-[#e8dfd1] rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-[#6b5d52]" />
              </button>
            </div>

            <form onSubmit={handleAddTag}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-[#6b5d52] mb-2 font-medium">
                    Tag Name <span className="text-[#a89080]">*</span>
                  </label>
                  <input
                    type="text"
                    name="tag_name"
                    required
                    placeholder="e.g., Vintage, Boho, Summer"
                    className="w-full px-4 py-3 rounded-xl border border-[#e8dfd1] bg-white text-[#6b5d52] focus:outline-none focus:ring-2 focus:ring-[#7a9178] placeholder-[#a89080]/50"
                  />
                </div>
              </div>

              <div className="flex gap-3 mt-8">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="flex-1 px-6 py-3 rounded-xl border border-[#e8dfd1] text-[#6b5d52] hover:bg-[#e8dfd1] transition-colors font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex-1 px-6 py-3 rounded-xl bg-[#7a9178] text-white hover:bg-[#6b8167] transition-colors font-medium flex items-center justify-center gap-2"
                >
                  {submitting && <Loader2 className="w-4 h-4 animate-spin" />}
                  Add Tag
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
