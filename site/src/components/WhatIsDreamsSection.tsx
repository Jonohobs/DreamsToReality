import { useEffect, useRef } from "react";

const YOUTUBE_ID = "Btj6Ziu_QpU"; // Dreams Launch Trailer — PlayStation

export default function WhatIsDreamsSection() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) el.classList.add("visible"); },
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <section id="what-is-dreams" className="relative z-10 py-16 px-8 md:px-16 lg:px-24">
      <div className="max-w-4xl mx-auto">
        <div ref={ref} className="reveal">
          <div className="text-center mb-10">
            <p
              className="font-mono-dm text-xs uppercase tracking-[0.25em] mb-4"
              style={{ color: "#FF6BD6" }}
            >
              — The Starting Point
            </p>
            <h2
              className="font-heading text-4xl md:text-5xl mb-4"
              style={{ fontWeight: 800, color: "rgba(255,255,255,0.95)" }}
            >
              What is Dreams?
            </h2>
            <p
              className="font-mono-dm text-sm max-w-xl mx-auto leading-relaxed"
              style={{ color: "rgba(255,255,255,0.5)" }}
            >
              Dreams is a game creation system developed by{" "}
              <span style={{ color: "rgba(255,255,255,0.75)" }}>Media Molecule</span>{" "}
              and published by{" "}
              <span style={{ color: "rgba(255,255,255,0.75)" }}>Sony Interactive Entertainment</span>{" "}
              for PlayStation. It lets you sculpt, paint, animate, and build entire games
              using intuitive motion controls — all running on a unique SDF rendering engine
              that makes everything look like nothing else.
            </p>
          </div>

          {/* YouTube embed */}
          <div
            className="glass-card overflow-hidden"
            style={{ borderRadius: "16px" }}
          >
            <div
              style={{
                position: "relative",
                paddingBottom: "56.25%",
                height: 0,
                overflow: "hidden",
              }}
            >
              <iframe
                src={`https://www.youtube.com/embed/${YOUTUBE_ID}?rel=0&modestbranding=1`}
                title="Dreams — Launch Trailer"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                loading="lazy"
                style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  width: "100%",
                  height: "100%",
                  border: "none",
                }}
              />
            </div>
          </div>

          <p
            className="font-mono-dm text-xs text-center mt-6 leading-relaxed"
            style={{ color: "rgba(255,255,255,0.3)" }}
          >
            Dreams to Reality extracts these creations as real 3D models
            using photogrammetry — capturing what was never meant to leave the engine.
          </p>
        </div>
      </div>
    </section>
  );
}
