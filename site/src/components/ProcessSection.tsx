import { useEffect, useRef } from "react";

const PROCESS_IMAGES = [
  {
    src: "/process/env-01.jpg",
    caption: "The Dreams capture environment — sculpt on platform with purple void backdrop",
    tag: "Environment",
  },
  {
    src: "/process/original-01.jpg",
    caption: "Dreams sculpt on capture platform — gobo spotlights projecting tracking patterns",
    tag: "In-Dreams Setup",
  },
  {
    src: "/process/original-02.jpg",
    caption: "Close-up of gobo light patterns giving photogrammetry something to lock onto",
    tag: "Gobo Detail",
  },
  {
    src: "/process/env-04.jpg",
    caption: "Different orbit angle — mushroom details and origami crane visible on the sculpt",
    tag: "Orbit View",
  },
  {
    src: "/process/capture-01.jpg",
    caption: "Paint-mess geometry pass — segmented and ready for reconstruction",
    tag: "Segmented",
  },
  {
    src: "/process/capture-04.jpg",
    caption: "Different angle of the same capture — the pipeline needs coverage from all sides",
    tag: "Multi-Angle",
  },
  {
    src: "/process/env-03.jpg",
    caption: "Close-up of the origami crane — Dreams' soft SDF rendering makes surfaces tricky for photogrammetry",
    tag: "Detail Shot",
  },
  {
    src: "/process/original-04.jpg",
    caption: "Original Dreams footage before segmentation — camera orbits the sculpt",
    tag: "Raw Capture",
  },
];

export default function ProcessSection() {
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
              — Building in Public
            </p>
            <h2
              className="font-heading text-4xl md:text-5xl mb-4"
              style={{ fontWeight: 800, color: "rgba(255,255,255,0.95)" }}
            >
              The Process
            </h2>
            <p
              className="font-mono-dm text-sm max-w-lg mx-auto"
              style={{ color: "rgba(255,255,255,0.45)" }}
            >
              From Dreams sculpt to 3D model — paint it, capture it, process it. Here's what that actually looks like.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {PROCESS_IMAGES.map((img, i) => (
              <div
                key={img.src}
                className="glass-card overflow-hidden group"
                style={{
                  borderRadius: "16px",
                  animationDelay: `${i * 80}ms`,
                }}
              >
                <div className="relative overflow-hidden">
                  <img
                    src={img.src}
                    alt={img.caption}
                    loading="lazy"
                    className="w-full h-auto block transition-transform duration-700 group-hover:scale-105"
                  />
                  <span
                    className="absolute top-3 left-3 font-mono-dm text-xs rounded-full"
                    style={{
                      padding: "4px 10px",
                      background: "rgba(10,10,15,0.7)",
                      backdropFilter: "blur(8px)",
                      color: "#D4FF00",
                      border: "1px solid rgba(212,255,0,0.2)",
                    }}
                  >
                    {img.tag}
                  </span>
                </div>
                <div style={{ padding: "0.4cm 0.5cm" }}>
                  <p
                    className="font-mono-dm text-xs leading-relaxed"
                    style={{ color: "rgba(255,255,255,0.5)" }}
                  >
                    {img.caption}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <p
            className="font-mono-dm text-xs text-center mt-6"
            style={{ color: "rgba(255,255,255,0.25)" }}
          >
            More process shots coming as the pipeline evolves
          </p>
        </div>
      </div>
    </section>
  );
}
