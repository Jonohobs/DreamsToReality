import { useEffect, useRef } from "react";


export default function HeroSection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const el = sectionRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) el.classList.add("visible"); },
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative min-h-screen flex items-center justify-center pt-24 pb-20 px-8 md:px-16 lg:px-24 overflow-hidden"
    >
      {/* Abstract blob silhouette behind text */}
      <div
        className="pointer-events-none absolute"
        style={{
          top: "50%",
          left: "55%",
          width: "600px",
          height: "600px",
          background: "radial-gradient(ellipse at 40% 50%, rgba(255,107,214,0.12) 0%, rgba(167,139,250,0.10) 40%, rgba(34,211,238,0.06) 70%, transparent 100%)",
          filter: "blur(60px)",
          borderRadius: "60% 40% 70% 30% / 50% 60% 40% 50%",
          animation: "blob-float 12s ease-in-out infinite",
          transform: "translate(-50%, -50%)",
        }}
      />
      {/* Second blob */}
      <div
        className="pointer-events-none absolute"
        style={{
          top: "45%",
          left: "58%",
          width: "300px",
          height: "300px",
          background: "radial-gradient(ellipse, rgba(167,139,250,0.08) 0%, transparent 70%)",
          filter: "blur(40px)",
          borderRadius: "40% 60% 30% 70%",
          animation: "blob-float 18s ease-in-out infinite reverse",
          transform: "translate(-50%, -50%)",
        }}
      />

      <div className="relative z-10 max-w-4xl mx-auto w-full">
        {/* Centre-aligned title block */}
        <div className="flex flex-col items-center text-center">
          {/* Eyebrow */}
          <p
            className="font-mono-dm text-sm uppercase tracking-[0.25em] reveal visible"
            style={{ color: "#D4FF00", animationDelay: "0ms", marginBottom: "0.6cm" }}
          >
            — Photogrammetry&ensp;for&ensp;Dreams&ensp;Creators
          </p>

          {/* Title — each word on its own line */}
          <div className="mb-10 reveal visible" style={{ animationDelay: "100ms" }}>
            <h1
              className="font-heading leading-[1] tracking-[-0.02em] text-center w-full"
              style={{ fontWeight: 800 }}
            >
              {/* "Dreams" — gold to pink */}
              <span
                className="block text-center"
                style={{
                  fontSize: "clamp(3.5rem, 10vw, 7.5rem)",
                  background: "linear-gradient(90deg, #FFD166 0%, #FF6BD6 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  backgroundClip: "text",
                  padding: "0.05em 0",
                  willChange: "transform",
                }}
              >
                Dreams
              </span>
              {/* "to" — pink, smaller/lighter */}
              <span
                className="block text-center"
                style={{
                  fontSize: "clamp(1.8rem, 5vw, 3.5rem)",
                  fontWeight: 600,
                  color: "#FF6BD6",
                  opacity: 0.9,
                  marginTop: "0.15em",
                  marginBottom: "0.1em",
                }}
              >
                to
              </span>
              {/* "Reality" — violet to green-cyan */}
              <span
                className="block text-center"
                style={{
                  fontSize: "clamp(3.5rem, 10vw, 7.5rem)",
                  background: "linear-gradient(90deg, #A78BFA 0%, #22D3B0 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  backgroundClip: "text",
                  padding: "0.05em 0 0.15em 0",
                  willChange: "transform",
                }}
              >
                Reality
              </span>
            </h1>
          </div>

          {/* BETA badge */}
          <div className="mb-10 reveal visible" style={{ animationDelay: "200ms" }}>
            <span
              className="font-mono-dm uppercase tracking-[0.2em] rounded-full inline-block"
              style={{
                padding: "0.3cm 0.6cm",
                fontSize: "0.75rem",
                color: "#D4FF00",
                border: "1px solid rgba(212,255,0,0.4)",
                background: "rgba(212,255,0,0.08)",
              }}
            >
              Beta
            </span>
          </div>

          {/* Subtitle */}
          <p
            className="font-mono-dm text-base leading-relaxed mb-14 max-w-xl reveal visible"
            style={{ color: "rgba(255,255,255,0.55)", animationDelay: "300ms" }}
          >
            Working toward the most seamless Dreams-to-3D exporting experience possible — for families, hobbyists, artists, and builders. Record your sculpture, run the pipeline, get a model. MIT licensed, community-driven.
          </p>

          {/* CTAs */}
          <div className="flex flex-wrap gap-5 justify-center reveal visible" style={{ animationDelay: "400ms" }}>
            <a
              href="#how-it-works"
              className="font-heading text-sm rounded-full inline-flex items-center gap-3 transition-all duration-500"
              style={{
                padding: "0.4cm 1cm",
                color: "rgba(255,255,255,0.85)",
                border: "1px solid rgba(255,255,255,0.2)",
                fontWeight: 700,
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLAnchorElement).style.borderColor = "rgba(255,255,255,0.5)";
                (e.currentTarget as HTMLAnchorElement).style.transform = "translateY(-2px)";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLAnchorElement).style.borderColor = "rgba(255,255,255,0.2)";
                (e.currentTarget as HTMLAnchorElement).style.transform = "translateY(0)";
              }}
            >
              Learn More&ensp;↓
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
