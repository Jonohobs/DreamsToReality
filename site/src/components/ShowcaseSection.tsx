import { useEffect, useRef } from "react";

const SKETCHFAB_EMBED = "https://sketchfab.com/models/55132b1d53d74942847da4921cbe06c2/embed?autostart=1&ui_theme=dark&ui_infos=0&ui_controls=1&ui_stop=0&ui_watermark=0";

export default function ShowcaseSection() {
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
    <section className="relative z-10 py-16 px-8 md:px-16 lg:px-24">
      <div className="max-w-4xl mx-auto">
        <div ref={ref} className="reveal">
          <div className="text-center mb-12">
            <p
              className="font-mono-dm text-xs uppercase tracking-[0.25em] mb-4"
              style={{ color: "#D4FF00" }}
            >
              — Community Showcase
            </p>
            <h2
              className="font-heading text-4xl md:text-5xl mb-4"
              style={{ fontWeight: 800, color: "rgba(255,255,255,0.95)" }}
            >
              What's possible
            </h2>
            <p
              className="font-mono-dm text-sm max-w-lg mx-auto"
              style={{ color: "rgba(255,255,255,0.45)" }}
            >
              Sculpted in Dreams, exported via photogrammetry. Drag to rotate.
            </p>
          </div>

          <div
            className="glass-card shimmer-border overflow-hidden"
            style={{ borderRadius: "20px" }}
          >
            <div style={{ position: "relative", width: "100%", paddingBottom: "56.25%" }}>
              <iframe
                title="Dreams 3D sculpt by Martinity"
                src={SKETCHFAB_EMBED}
                allow="autoplay; fullscreen; xr-spatial-tracking"
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
            className="font-mono-dm text-xs text-center mt-4"
            style={{ color: "rgba(255,255,255,0.3)" }}
          >
            Model by{" "}
            <a
              href="https://sketchfab.com/Martinity"
              target="_blank"
              rel="noopener noreferrer"
              className="transition-colors duration-300"
              style={{ color: "#A78BFA" }}
              onMouseEnter={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "#D4FF00")}
              onMouseLeave={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "#A78BFA")}
            >
              Martinity
            </a>
            {" "}· Sculpted in Dreams, exported with RealityCapture
          </p>
        </div>
      </div>
    </section>
  );
}
