import { useEffect, useState, useRef } from "react";

interface ProcessingProps {
  jobId: string;
  onComplete: (data: Record<string, unknown>) => void;
}

const STEP_LABELS: Record<string, string> = {
  waiting: "Queued...",
  extracting_frames: "Extracting frames from video",
  preprocessing: "Filtering blurry frames & removing UI overlays",
  segmenting: "Removing background (isolating sculpt)",
  reconstructing: "Reconstructing 3D geometry (this takes a while)",
  done: "Complete!",
  failed: "Processing failed",
};

export default function Processing({ jobId, onComplete }: ProcessingProps) {
  const [status, setStatus] = useState<Record<string, unknown> | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval>>(undefined);

  useEffect(() => {
    const poll = async () => {
      try {
        const res = await fetch(`/api/status/${jobId}`);
        if (res.ok) {
          const data = await res.json();
          setStatus(data);
          if (data.status === "complete") {
            clearInterval(intervalRef.current);
            onComplete(data);
          }
          if (data.status === "error") {
            clearInterval(intervalRef.current);
          }
        }
      } catch {
        // Server might not be running yet
      }
    };

    poll();
    intervalRef.current = setInterval(poll, 2000);
    return () => clearInterval(intervalRef.current);
  }, [jobId, onComplete]);

  const step = (status?.step as string) || "waiting";
  const progress = (status?.progress as number) || 0;
  const error = status?.error as string | null;

  return (
    <div className="max-w-2xl mx-auto px-6 py-16 text-center">
      <h1 className="text-3xl font-bold mb-2">Processing Your Model</h1>
      <p className="text-neutral-400 mb-12">Job ID: {jobId}</p>

      {/* Progress bar */}
      <div className="mb-8">
        <div className="w-full h-2 bg-neutral-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-red-500 transition-all duration-500 rounded-full"
            style={{ width: `${progress}%` }}
          />
        </div>
        <p className="mt-3 text-sm text-neutral-500">{progress}%</p>
      </div>

      {/* Current step */}
      <div className="p-6 rounded-xl bg-neutral-900 border border-neutral-800 mb-8">
        {step !== "failed" ? (
          <div className="flex items-center justify-center gap-3">
            {step !== "done" && (
              <div className="w-5 h-5 border-2 border-red-500 border-t-transparent rounded-full animate-spin" />
            )}
            <p className="text-lg">
              {STEP_LABELS[step] || step}
            </p>
          </div>
        ) : (
          <div>
            <p className="text-red-400 text-lg mb-2">Processing Failed</p>
            <p className="text-sm text-neutral-500">{error}</p>
          </div>
        )}
      </div>

      {/* Pipeline stages */}
      <div className="space-y-3 text-left max-w-md mx-auto">
        {["extracting_frames", "preprocessing", "segmenting", "reconstructing"].map(
          (s) => {
            const stages = ["extracting_frames", "preprocessing", "segmenting", "reconstructing"];
            const currentIdx = stages.indexOf(step);
            const thisIdx = stages.indexOf(s);
            const isDone = thisIdx < currentIdx || step === "done";
            const isCurrent = s === step;

            return (
              <div
                key={s}
                className={`flex items-center gap-3 text-sm ${
                  isDone
                    ? "text-green-400"
                    : isCurrent
                      ? "text-white"
                      : "text-neutral-600"
                }`}
              >
                <span className="w-5 text-center">
                  {isDone ? "\u2713" : isCurrent ? "\u25CB" : "\u00B7"}
                </span>
                {STEP_LABELS[s]}
              </div>
            );
          }
        )}
      </div>
    </div>
  );
}
