import { useEffect, useRef } from "react";

const STEPS = [
  {
    num: "01",
    icon: "🎥",
    title: "Record",
    desc: "Orbit your Dreams creation on screen while recording. PS5 Share, OBS, or a phone pointed at your TV all work perfectly.",
    accent: "#FF6BD6",
  },
  {
    num: "02",
    icon: "⚙️",
    title: "Process",
    desc: "The pipeline extracts frames, detects blur, and removes backgrounds automatically. Then choose your reconstruction engine — local or cloud.",
    accent: "#A78BFA",
  },
  {
    num: "03",
    icon: "📦",
    title: "Export",
    desc: "Download your model export — ready for printing, game engines, Blender, or sharing with the community.",
    accent: "#22D3EE",
  },
];

function useReveal(ref: React.RefObject<HTMLElement>, delay = 0) {
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setTimeout(() => el.classList.add("visible"), delay);
        }
      },
      { threshold: 0.15 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [ref, delay]);
}

function StepCard({ num, icon, title, desc, accent, delay }: { num: string; icon: string; title: string; desc: string; accent: string; delay: number }) {
  const ref = useRef<HTMLDivElement>(null);
  useReveal(ref as React.RefObject<HTMLElement>, delay);

  return (
    <div
      ref={ref}
      className="reveal glass-card shimmer-border flex flex-col gap-5 transition-all duration-500 group relative overflow-hidden"
      style={{
        padding: "1cm",
        background: "rgba(17,17,24,0.6)",
      }}
      onMouseEnter={(e) => {
        (e.currentTarget as HTMLDivElement).style.transform = "translateY(-6px)";
        (e.currentTarget as HTMLDivElement).style.boxShadow = `0 20px 60px ${accent}15`;
      }}
      onMouseLeave={(e) => {
        (e.currentTarget as HTMLDivElement).style.transform = "translateY(0)";
        (e.currentTarget as HTMLDivElement).style.boxShadow = "none";
      }}
    >
      {/* Large faded step number */}
      <span
        className="absolute font-heading select-none pointer-events-none"
        aria-hidden="true"
        style={{
          top: "-0.6cm",
          right: "-0.3cm",
          fontSize: "8rem",
          fontWeight: 800,
          lineHeight: 1,
          color: accent,
          opacity: 0.06,
        }}
      >
        {num}
      </span>

      {/* Accent bar */}
      <div
        className="w-8 h-1 rounded-full"
        style={{ background: accent }}
      />

      <span className="text-2xl" aria-hidden="true">{icon}</span>

      <h3
        className="font-heading text-xl"
        style={{ fontWeight: 700, color: "rgba(255,255,255,0.95)" }}
      >
        {title}
      </h3>
      <p
        className="font-mono-dm text-sm leading-relaxed"
        style={{ color: "rgba(255,255,255,0.5)" }}
      >
        {desc}
      </p>
    </div>
  );
}

export default function HowItWorksSection() {
  const headerRef = useRef<HTMLDivElement>(null);
  useReveal(headerRef as React.RefObject<HTMLElement>, 0);

  return (
    <section id="how-it-works" className="relative z-10 py-16 px-8 md:px-16 lg:px-24 overflow-hidden">
      <div className="max-w-4xl mx-auto">
        <div ref={headerRef} className="reveal text-center mb-16">
          <p
            className="font-mono-dm text-xs uppercase tracking-[0.25em] mb-4"
            style={{ color: "#D4FF00" }}
          >
            — How It Works
          </p>
          <h2
            className="font-heading text-4xl md:text-5xl"
            style={{ fontWeight: 800, color: "rgba(255,255,255,0.95)" }}
          >
            Three steps to a real 3D model
          </h2>
        </div>

        {/* Step cards with connecting lines */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          {/* Connecting line (desktop only) */}
          <div
            className="hidden md:block absolute top-1/2 left-0 right-0 -translate-y-1/2 pointer-events-none"
            style={{
              height: "1px",
              background: "linear-gradient(90deg, transparent 10%, rgba(255,255,255,0.08) 20%, rgba(255,255,255,0.08) 80%, transparent 90%)",
            }}
          />
          {STEPS.map((step, i) => (
            <StepCard key={step.title} {...step} delay={i * 120} />
          ))}
        </div>
      </div>
    </section>
  );
}
