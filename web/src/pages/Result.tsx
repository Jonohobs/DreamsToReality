interface ResultProps {
  jobId: string;
  data: Record<string, unknown> | null;
}

export default function Result({ jobId, data }: ResultProps) {
  const handleDownload = () => {
    window.open(`/api/download/${jobId}`, "_blank");
  };

  return (
    <div className="max-w-2xl mx-auto px-6 py-16 text-center">
      <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-green-600/20 border border-green-600/30 flex items-center justify-center text-3xl">
        {"\u2713"}
      </div>

      <h1 className="text-3xl font-bold mb-2">Model Ready</h1>
      <p className="text-neutral-400 mb-10">
        Your 3D model has been reconstructed from the Dreams capture.
      </p>

      <button
        onClick={handleDownload}
        className="px-8 py-3 bg-red-600 hover:bg-red-500 rounded-lg font-medium transition-colors cursor-pointer mb-8"
      >
        Download 3D Model
      </button>

      {data?.result != null && (
        <div className="p-6 rounded-xl bg-neutral-900 border border-neutral-800 text-left text-sm">
          <h3 className="font-semibold mb-3">Details</h3>
          <div className="space-y-2 text-neutral-400">
            <p>
              <span className="text-neutral-500">Job ID:</span> {jobId}
            </p>
            <p>
              <span className="text-neutral-500">Output:</span>{" "}
              {String(data.result as string).split(/[\\/]/).pop()}
            </p>
          </div>
        </div>
      )}

      {/* Next steps */}
      <div className="mt-12 p-6 rounded-xl bg-neutral-900/50 border border-neutral-800/50 text-left">
        <h3 className="font-semibold mb-3">What to do next</h3>
        <ul className="text-sm text-neutral-400 space-y-2 list-disc list-inside">
          <li>
            Open the .ply file in <strong>Blender</strong> (File &gt; Import &gt; PLY) or{" "}
            <strong>MeshLab</strong> for inspection
          </li>
          <li>
            Run Poisson Surface Reconstruction in MeshLab for a watertight mesh
          </li>
          <li>
            Export as .obj or .stl for 3D printing, or .fbx for game engines
          </li>
          <li>
            If you captured a texture pass, the clean color data can be projected
            onto the mesh in Blender
          </li>
        </ul>
      </div>
    </div>
  );
}
