import { useState } from "react";
import Landing from "./pages/Landing";
import Upload from "./pages/Upload";
import Processing from "./pages/Processing";
import Result from "./pages/Result";

type Page = "landing" | "upload" | "processing" | "result";

export default function App() {
  const [page, setPage] = useState<Page>("landing");
  const [jobId, setJobId] = useState<string | null>(null);
  const [resultData, setResultData] = useState<Record<string, unknown> | null>(null);

  return (
    <div className="min-h-screen bg-neutral-950 text-white">
      <nav className="fixed top-0 w-full z-50 bg-neutral-950/80 backdrop-blur border-b border-neutral-800">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <button
            onClick={() => setPage("landing")}
            className="text-lg font-bold tracking-tight hover:text-red-400 transition-colors cursor-pointer"
          >
            Dreams to Reality
          </button>
          <button
            onClick={() => setPage("upload")}
            className="px-4 py-2 bg-red-600 hover:bg-red-500 rounded-lg text-sm font-medium transition-colors cursor-pointer"
          >
            Extract Model
          </button>
        </div>
      </nav>

      <main className="pt-20">
        {page === "landing" && (
          <Landing onGetStarted={() => setPage("upload")} />
        )}
        {page === "upload" && (
          <Upload
            onUploaded={(id) => {
              setJobId(id);
              setPage("processing");
            }}
          />
        )}
        {page === "processing" && jobId && (
          <Processing
            jobId={jobId}
            onComplete={(data) => {
              setResultData(data);
              setPage("result");
            }}
          />
        )}
        {page === "result" && jobId && (
          <Result jobId={jobId} data={resultData} />
        )}
      </main>
    </div>
  );
}
