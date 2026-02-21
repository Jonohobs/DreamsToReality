import { useEffect, useRef } from "react";

interface TagProps { label: string; color: string }
function Tag({ label, color }: TagProps) {
  return (
    <span
      className="font-mono-dm text-xs rounded-full"
      style={{
        padding: "0.25cm 0.35cm",
        border: `1px solid ${color}40`,
        color: color,
        background: `${color}10`,
      }}
    >
      {label}
    </span>
  );
}

interface FeatureCardProps {
  title: string;
  desc: string;
  tags: { label: string; color: string }[];
  accent: string;
  span?: string;
  delay: number;
}

function FeatureCard({ title, desc, tags, accent, span, delay }: FeatureCardProps) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setTimeout(() => el.classList.add("visible"), delay);
      },
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [delay]);

  return (
    <div
      ref={ref}
      className={`reveal glass-card shimmer-border flex flex-col gap-6 transition-all duration-500 ${span || ""}`}
      style={{ padding: "1cm" }}
      onMouseEnter={(e) => {
        (e.currentTarget as HTMLDivElement).style.transform = "translateY(-5px)";
        (e.currentTarget as HTMLDivElement).style.boxShadow = `0 20px 60px ${accent}22`;
      }}
      onMouseLeave={(e) => {
        (e.currentTarget as HTMLDivElement).style.transform = "translateY(0)";
        (e.currentTarget as HTMLDivElement).style.boxShadow = "none";
      }}
    >
      {/* Accent bar */}
      <div
        className="w-8 h-1 rounded-full mt-2 ml-2"
        style={{ background: accent }}
      />
      <h3
        className="font-heading text-xl md:text-2xl"
        style={{ fontWeight: 700, color: "rgba(255,255,255,0.95)" }}
      >
        {title}
      </h3>
      <p
        className="font-mono-dm text-sm leading-relaxed flex-1"
        style={{ color: "rgba(255,255,255,0.5)" }}
      >
        {desc}
      </p>
      <div className="flex flex-wrap gap-2">
        {tags.map((t) => <Tag key={t.label} {...t} />)}
      </div>
    </div>
  );
}

const FEATURES = [
  {
    title: "Smart Extraction",
    desc: "Blur detection, duplicate removal, UI overlay filtering. Only the sharpest frames survive — so reconstruction starts with clean input.",
    tags: [
      { label: "Python",  color: "#22D3EE" },
      { label: "OpenCV",  color: "#22D3EE" },
      { label: "CLI",     color: "#A78BFA" },
    ],
    accent: "#22D3EE",
  },
  {
    title: "Automatic Segmentation",
    desc: "U2-Net neural network isolates your creation from the background. No manual masking required.",
    tags: [
      { label: "rembg",   color: "#FF6BD6" },
      { label: "U2-Net",  color: "#FF6BD6" },
      { label: "CPU-only",color: "#A78BFA" },
    ],
    accent: "#FF6BD6",
  },
  {
    title: "Flexible Reconstruction",
    desc: "Choose your engine — COLMAP, Meshroom, RealityScan, or Gaussian Splatting. Run locally or get cloud setup instructions. The pipeline auto-tunes parameters based on your content and hardware.",
    tags: [
      { label: "RealityScan", color: "#A78BFA" },
      { label: "Meshroom",    color: "#FF6BD6" },
      { label: "COLMAP",      color: "#22D3EE" },
      { label: "3DGS",        color: "#22D3EE" },
    ],
    accent: "#A78BFA",
  },
  {
    title: "MIT Licensed, Community First",
    desc: "Core pipeline is open source, MIT licensed. Share results and help make this the most reliable Dreams-to-3D pipeline around.",
    tags: [
      { label: "MIT",       color: "#D4FF00" },
      { label: "Open Source", color: "#D4FF00" },
      { label: "Community", color: "#FF6BD6" },
    ],
    accent: "#D4FF00",
  },
];

export default function FeaturesSection() {
  const headerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = headerRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) el.classList.add("visible"); },
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <section id="features" className="relative z-10 py-16 px-8 md:px-16 lg:px-24">
      <div className="max-w-4xl mx-auto">
        <div ref={headerRef} className="reveal text-center mb-16">
          <p
            className="font-mono-dm text-xs uppercase tracking-[0.25em] mb-4"
            style={{ color: "#D4FF00" }}
          >
            — Features
          </p>
          <h2
            className="font-heading text-4xl md:text-5xl"
            style={{ fontWeight: 800, color: "rgba(255,255,255,0.95)" }}
          >
            Iterating toward reliable, automatic export
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {FEATURES.map((f, i) => (
            <FeatureCard key={f.title} {...f} delay={i * 100} />
          ))}
        </div>
      </div>
    </section>
  );
}
