import { useState, useRef } from "react";
import { Upload, X, Image as ImageIcon, Loader2 } from "lucide-react";

export function PhotoUploader({ currentPhotos = [], onPhotosChange, maxPhotos = 5 }) {
    const [dragActive, setDragActive] = useState(false);
    const inputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFiles(e.dataTransfer.files);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFiles(e.target.files);
        }
    };

    const handleFiles = (files) => {
        const newPhotos = Array.from(files);
        // Validate file type and size here if needed
        onPhotosChange(newPhotos);
    };

    const removePhoto = (index) => {
        const updatedPhotos = [...currentPhotos];
        updatedPhotos.splice(index, 1);
        onPhotosChange(updatedPhotos, true); // true indicates deletion
    };

    return (
        <div className="space-y-4">
            <div
                className={`relative border-2 border-dashed rounded-2xl p-8 text-center transition-colors ${dragActive
                    ? "border-[#7a9178] bg-[#7a9178]/5"
                    : "border-[#e8dfd1] bg-[#fefbf6] hover:bg-[#e8dfd1]/30"
                    }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <input
                    ref={inputRef}
                    type="file"
                    multiple
                    accept="image/*"
                    className="hidden"
                    onChange={handleChange}
                />

                <div className="flex flex-col items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-[#e8dfd1] flex items-center justify-center text-[#6b5d52]">
                        <Upload className="w-6 h-6" />
                    </div>
                    <div>
                        <p className="text-[#6b5d52] font-medium mb-1">
                            Click to upload or drag and drop
                        </p>
                        <p className="text-sm text-[#a89080]">
                            SVG, PNG, JPG or GIF (max. 5MB)
                        </p>
                    </div>
                    <button
                        type="button"
                        onClick={() => inputRef.current?.click()}
                        className="px-6 py-2 rounded-full border border-[#7a9178] text-[#7a9178] text-sm hover:bg-[#7a9178] hover:text-white transition-colors"
                    >
                        Select Photos
                    </button>
                </div>
            </div>

            {currentPhotos.length > 0 && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {currentPhotos.map((photo, index) => (
                        <div key={index} className="relative aspect-square rounded-xl overflow-hidden border border-[#e8dfd1] group bg-white">
                            <img
                                src={
                                    photo instanceof File
                                        ? URL.createObjectURL(photo)
                                        : (typeof photo === 'string' ? photo : (photo.file_path || photo.url))
                                }
                                alt={`Upload ${index + 1}`}
                                className="w-full h-full object-cover"
                            />
                            <button
                                type="button"
                                onClick={() => removePhoto(index)}
                                className="absolute top-2 right-2 p-1.5 rounded-full bg-black/50 text-white hover:bg-red-500 transition-colors opacity-0 group-hover:opacity-100"
                            >
                                <X className="w-4 h-4" />
                            </button>
                            {index === 0 && (
                                <div className="absolute bottom-2 left-2 px-2 py-1 rounded bg-black/50 text-white text-xs backdrop-blur-sm">
                                    Primary
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
