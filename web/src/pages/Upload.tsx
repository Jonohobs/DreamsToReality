import { useState, useRef } from "react";

interface UploadProps {
  onUploaded: (jobId: string) => void;
}

export default function Upload({ onUploaded }: UploadProps) {
  const [geoFile, setGeoFile] = useState<File | null>(null);
  const [texFile, setTexFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const geoRef = useRef<HTMLInputElement>(null);
  const texRef = useRef<HTMLInputElement>(null);

  const handleUpload = async () => {
    if (!geoFile) return;
    setUploading(true);
    setError(null);

    try {
      const form = new FormData();
      form.append("geometry_video", geoFile);
      if (texFile) {
        form.append("texture_video", texFile);
      }

      const res = await fetch("/api/upload", { method: "POST", body: form });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Upload failed");
      }

      const { job_id } = await res.json();

      // Auto-start processing
      const procRes = await fetch(`/api/process/${job_id}`, { method: "POST" });
      if (!procRes.ok) {
        throw new Error("Failed to start processing");
      }

      onUploaded(job_id);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-6 py-16">
      <h1 className="text-3xl font-bold mb-2">Upload Capture Videos</h1>
      <p className="text-neutral-400 mb-10">
        Upload the recordings from your Dreams capture session. The geometry
        pass (with tracking patterns) is required. The texture pass (clean
        colors) is optional but recommended.
      </p>

      {/* Geometry video (required) */}
      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">
          Geometry Pass Video
          <span className="text-red-400 ml-1">*</span>
        </label>
        <div
          onClick={() => geoRef.current?.click()}
          className={`
            border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors
            ${geoFile ? "border-red-500 bg-red-600/10" : "border-neutral-700 hover:border-neutral-500 bg-neutral-900/50"}
          `}
        >
          <input
            ref={geoRef}
            type="file"
            accept="video/*"
            className="hidden"
            onChange={(e) => setGeoFile(e.target.files?.[0] || null)}
          />
          {geoFile ? (
            <div>
              <p className="font-medium text-red-400">{geoFile.name}</p>
              <p className="text-sm text-neutral-500 mt-1">
                {(geoFile.size / (1024 * 1024)).toFixed(1)} MB
              </p>
            </div>
          ) : (
            <div>
              <p className="text-neutral-400 mb-1">
                Click to select the geometry pass recording
              </p>
              <p className="text-sm text-neutral-600">
                The video with tracking patterns applied to your sculpt
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Texture video (optional) */}
      <div className="mb-8">
        <label className="block text-sm font-medium mb-2">
          Texture Pass Video
          <span className="text-neutral-600 ml-1">(optional)</span>
        </label>
        <div
          onClick={() => texRef.current?.click()}
          className={`
            border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors
            ${texFile ? "border-blue-500 bg-blue-600/10" : "border-neutral-700 hover:border-neutral-500 bg-neutral-900/50"}
          `}
        >
          <input
            ref={texRef}
            type="file"
            accept="video/*"
            className="hidden"
            onChange={(e) => setTexFile(e.target.files?.[0] || null)}
          />
          {texFile ? (
            <div>
              <p className="font-medium text-blue-400">{texFile.name}</p>
              <p className="text-sm text-neutral-500 mt-1">
                {(texFile.size / (1024 * 1024)).toFixed(1)} MB
              </p>
            </div>
          ) : (
            <div>
              <p className="text-neutral-400 mb-1">
                Click to select the texture pass recording
              </p>
              <p className="text-sm text-neutral-600">
                The clean video without patterns — used for color data
              </p>
            </div>
          )}
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-lg bg-red-900/50 border border-red-700 text-red-300 text-sm">
          {error}
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!geoFile || uploading}
        className={`
          w-full py-3 rounded-lg font-medium transition-colors cursor-pointer
          ${!geoFile || uploading
            ? "bg-neutral-700 text-neutral-500 cursor-not-allowed"
            : "bg-red-600 hover:bg-red-500 text-white"}
        `}
      >
        {uploading ? "Uploading..." : "Upload & Process"}
      </button>

      {/* Help text */}
      <div className="mt-12 p-6 rounded-xl bg-neutral-900/50 border border-neutral-800/50">
        <h3 className="font-semibold mb-3">How to get videos from PS5</h3>
        <ol className="text-sm text-neutral-400 space-y-2 list-decimal list-inside">
          <li>
            After the capture tool runs in Dreams, find the recordings in your
            PS5 Media Gallery
          </li>
          <li>
            Transfer to USB drive (Settings &gt; Storage &gt; Media Gallery &gt;
            Copy to USB) or use the PS App
          </li>
          <li>Copy the .mp4 files to your computer and upload them here</li>
        </ol>
      </div>
    </div>
  );
}
