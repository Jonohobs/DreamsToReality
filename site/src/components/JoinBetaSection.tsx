import { useEffect, useRef, useState } from "react";

const GITHUB_URL = "https://github.com/Jonohobs/DreamsToReality";
const ISSUES_URL = "https://github.com/Jonohobs/DreamsToReality/issues";

const PATREON_URL = "https://patreon.com/DreamsToReality";

const LINKS = [
  {
    label: "GitHub",
    sub: "Star, fork, contribute",
    href: GITHUB_URL,
    color: "#D4FF00",
  },
  {
    label: "Support on Patreon",
    sub: "Help fund development",
    href: PATREON_URL,
    color: "#FF6BD6",
  },
  {
    label: "Report a Bug",
    sub: "Help us squash issues",
    href: ISSUES_URL,
    color: "#22D3EE",
  },
];

function LinkRow({ label, sub, href, color }: { label: string; sub: string; href: string; color: string }) {
  const [hovered, setHovered] = useState(false);

  return (
    <a
      href={href}
      target={href === "#" ? undefined : "_blank"}
      rel="noopener noreferrer"
      className="group flex items-center justify-between py-5 border-b transition-all duration-500"
      style={{
        borderColor: hovered ? `${color}40` : "rgba(255,255,255,0.06)",
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div>
        <span
          className="font-heading text-xl block mb-0.5 transition-colors duration-300"
          style={{
            fontWeight: 700,
            color: hovered ? color : "rgba(255,255,255,0.85)",
          }}
        >
          {label}
        </span>
        <span
          className="font-mono-dm text-xs"
          style={{ color: "rgba(255,255,255,0.35)" }}
        >
          {sub}
        </span>
      </div>
      <span
        className="font-mono-dm text-xl transition-all duration-300"
        style={{
          color: color,
          transform: hovered ? "translateX(8px)" : "translateX(0)",
          opacity: hovered ? 1 : 0.3,
        }}
      >
        →
      </span>
    </a>
  );
}

export default function JoinBetaSection() {
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
    <section id="community" className="relative z-10 py-16 px-8 md:px-16 lg:px-24">
      <div className="max-w-4xl mx-auto">
        <div
          ref={ref}
          className="reveal glass-card relative overflow-hidden flex flex-col gap-6"
          style={{
            padding: "1.5cm",
            background: "rgba(17,17,24,0.5)",
            border: "1px solid rgba(167,139,250,0.2)",
          }}
        >
          {/* Always-on gradient border glow */}
          <div
            className="absolute inset-0 pointer-events-none rounded-[20px]"
            style={{
              background: "linear-gradient(135deg, rgba(255,107,214,0.06) 0%, rgba(167,139,250,0.08) 50%, rgba(34,211,238,0.06) 100%)",
            }}
          />
          {/* Subtle inner radial glow */}
          <div
            className="absolute pointer-events-none"
            style={{
              top: "-20%",
              right: "-10%",
              width: "60%",
              height: "60%",
              background: "radial-gradient(ellipse, rgba(167,139,250,0.08) 0%, transparent 70%)",
              filter: "blur(40px)",
            }}
          />

          {/* Gradient accent bar */}
          <div
            className="relative w-16 h-1 rounded-full"
            style={{
              background: "linear-gradient(90deg, #FF6BD6, #A78BFA, #22D3EE)",
            }}
          />

          <p
            className="relative font-mono-dm text-xs uppercase tracking-[0.25em]"
            style={{ color: "#D4FF00" }}
          >
            — Join the Beta
          </p>

          <h2
            className="relative font-heading text-3xl md:text-5xl"
            style={{ fontWeight: 800, color: "rgba(255,255,255,0.95)" }}
          >
            Shape the Future of<br />
            <span className="gradient-text-dreams">Dreams Photogrammetry</span>
          </h2>

          <p
            className="relative font-mono-dm text-sm leading-relaxed max-w-xl"
            style={{ color: "rgba(255,255,255,0.45)" }}
          >
            A growing community of Dreams creators, 3D artists, and developers working toward stress-free model exporting. Share your exports, vote on favourites, earn community badges.
          </p>

          {/* Community awards teaser */}
          <div className="relative flex flex-wrap gap-3">
            {[
              { label: "🏆 Most Seamless — Martinity", desc: "Closest 1-to-1 export" },
              { label: "✨ Most Wow — Martinity", desc: "The one that makes you go 'oh wow'" },
              { label: "🎖️ OG — DrSecksy", desc: "Built the in-Dreams photogrammetry export recorder" },
            ].map((award) => (
              <span
                key={award.label}
                className="font-mono-dm text-xs rounded-full"
                title={award.desc}
                style={{
                  padding: "0.25cm 0.4cm",
                  border: "1px solid rgba(212,255,0,0.25)",
                  color: "#D4FF00",
                  background: "rgba(212,255,0,0.06)",
                }}
              >
                {award.label}
              </span>
            ))}
            <span
              className="font-mono-dm text-xs rounded-full"
              style={{
                padding: "0.25cm 0.4cm",
                color: "rgba(255,255,255,0.3)",
                border: "1px solid rgba(255,255,255,0.08)",
              }}
            >
              More badges coming...
            </span>
          </div>

          <div className="relative flex flex-col">
            {LINKS.map((link) => (
              <LinkRow key={link.label} {...link} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
