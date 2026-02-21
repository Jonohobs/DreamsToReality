import { useEffect, useRef } from "react";

const CLAUDE_URL = "https://claude.ai/?utm_source=dreamstoreality";

const PRINT_SERVICES = [
  {
    label: "Craftcloud",
    sub: "Compare prices across services",
    href: "https://craftcloud3d.com",
    color: "#FF6BD6",
  },
  {
    label: "Shapeways",
    sub: "Wide material selection",
    href: "https://www.shapeways.com",
    color: "#A78BFA",
  },
  {
    label: "JLC3DP",
    sub: "Fast turnaround",
    href: "https://jlc3dp.com",
    color: "#22D3EE",
  },
  {
    label: "Sculpteo",
    sub: "Full-colour sandstone prints",
    href: "https://www.sculpteo.com",
    color: "#D4FF00",
  },
];

const PAINT_SERVICES = [
  {
    label: "PaintedFigs",
    sub: "Commission hand-painting",
    href: "https://paintedfigs.com",
    color: "#FF6BD6",
  },
  {
    label: "HeroForge Painting",
    sub: "Full-colour printing + paint",
    href: "https://www.heroforge.com",
    color: "#A78BFA",
  },
];

const FINISHING_TIPS = [
  "Sand with fine grit (400–800) before priming",
  "Acrylic craft paint works great — cheap and forgiving",
  "Nail polish for metallic / glossy accents",
  "Spray primer first for smooth, even coverage",
  "Thin coats > thick coats — always",
  "Wash with soapy water before painting (removes print residue)",
];

const SCANNING_TIPS = [
  "Two-pass capture: scan once with messy paint splatters for geometry, once clean for colour — combine for a textured, accurate model",
  "Full-colour prints skip painting entirely — services like Sculpteo print the texture map straight onto sandstone",
  "Build your own in-Dreams scanner: place gobo spotlight projectors around your sculpt to project tracking patterns onto smooth surfaces — gives photogrammetry something to lock onto",
  "Jonathan's DIY rig: a camera boom arm on a keyframe orbit, pattern confetti emitters that spray coloured shapes onto the sculpt, and a timer to automate the whole capture",
  "Camera settings matter: aperture 0% (everything sharp), FOV 50–60, all post-processing OFF, tiny sharpen boost",
];

export default function GetHelpSection() {
  const ref = useRef<HTMLDivElement>(null);
  const printRef = useRef<HTMLDivElement>(null);
  const finishRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observers: IntersectionObserver[] = [];
    [ref.current, printRef.current, finishRef.current].forEach((el, i) => {
      if (!el) return;
      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) setTimeout(() => el.classList.add("visible"), i * 120);
        },
        { threshold: 0.1 }
      );
      observer.observe(el);
      observers.push(observer);
    });
    return () => observers.forEach((o) => o.disconnect());
  }, []);

  return (
    <section className="relative z-10 py-16 px-8 md:px-16 lg:px-24">
      {/* Top row: Help + Print */}
      <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">

        {/* Get Help card */}
        <div
          ref={ref}
          className="reveal glass-card shimmer-border flex flex-col gap-6 relative overflow-visible"
          style={{ padding: "1cm" }}
        >
          {/* Claude sparkle icon */}
          <div className="flex items-start gap-4">
            <div className="relative flex-shrink-0" style={{ width: 52, height: 52 }}>
              <svg
                className="claude-sparkle"
                width="52"
                height="52"
                viewBox="0 0 48 48"
                fill="none"
                aria-hidden="true"
              >
                <path
                  d="M24 2L26.5 19L46 24L26.5 29L24 46L21.5 29L2 24L21.5 19Z"
                  fill="#E07A3A"
                />
                <path
                  d="M24 8L25.5 20L40 24L25.5 28L24 40L22.5 28L8 24L22.5 20Z"
                  fill="#F4A574"
                  opacity="0.5"
                />
              </svg>
              {/* Tiny companion sparkle */}
              <svg
                className="claude-sparkle-mini absolute"
                style={{ top: -4, right: -6 }}
                width="16"
                height="16"
                viewBox="0 0 48 48"
                fill="none"
                aria-hidden="true"
              >
                <path
                  d="M24 2L26.5 19L46 24L26.5 29L24 46L21.5 29L2 24L21.5 19Z"
                  fill="#E07A3A"
                />
              </svg>
            </div>
            <div className="flex flex-col">
              <p
                className="font-mono-dm text-xs uppercase tracking-[0.25em] mb-2"
                style={{ color: "#D4FF00" }}
              >
                — Pipeline support
              </p>
              <h3
                className="font-heading text-2xl mb-3"
                style={{ fontWeight: 700, color: "rgba(255,255,255,0.95)" }}
              >
                Stuck? Ask Claude
              </h3>
            </div>
          </div>
          <p
            className="font-mono-dm text-sm leading-relaxed"
            style={{ color: "rgba(255,255,255,0.5)" }}
          >
            Open Claude, paste the context file below, then ask your question. Claude will understand the full pipeline.
          </p>

          <div className="flex flex-wrap gap-3">
            <a
              href={CLAUDE_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="font-heading text-lg px-10 py-5 rounded-full inline-flex items-center gap-3 self-start transition-all duration-500"
              style={{
                background: "#D4FF00",
                color: "#0A0A0F",
                fontWeight: 700,
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLAnchorElement).style.boxShadow = "0 0 30px rgba(212,255,0,0.4)";
                (e.currentTarget as HTMLAnchorElement).style.transform = "translateY(-2px)";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLAnchorElement).style.boxShadow = "none";
                (e.currentTarget as HTMLAnchorElement).style.transform = "translateY(0)";
              }}
            >
              Open Claude ↗
            </a>
          </div>

          <div className="flex flex-col gap-2">
            <a
              href="/dreams-to-reality-context.md"
              download
              className="font-mono-dm text-xs inline-flex items-center gap-2 transition-colors duration-300"
              style={{ color: "#E07A3A" }}
              onMouseEnter={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "#F4A574")}
              onMouseLeave={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "#E07A3A")}
            >
              ↓ Download pipeline context file — paste into Claude for full support
            </a>
            <a
              href="/claude-code-quick-start.md"
              download
              className="font-mono-dm text-xs inline-flex items-center gap-2 transition-colors duration-300"
              style={{ color: "rgba(255,255,255,0.35)" }}
              onMouseEnter={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "#A78BFA")}
              onMouseLeave={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "rgba(255,255,255,0.35)")}
            >
              ↓ Claude Code quick start guide — get more out of every session
            </a>
          </div>

          <p
            className="font-mono-dm text-xs"
            style={{ color: "rgba(255,255,255,0.25)" }}
          >
            Free to use — create a Claude account for longer conversations.
          </p>
        </div>

        {/* Print + Paint services card */}
        <div
          ref={printRef}
          className="reveal glass-card shimmer-border flex flex-col gap-6"
          style={{ padding: "1cm" }}
        >
          <div
            className="w-8 h-1 rounded-full mt-2 ml-2"
            style={{ background: "#22D3EE" }}
          />
          <div>
            <p
              className="font-mono-dm text-xs uppercase tracking-[0.25em] mb-2"
              style={{ color: "#D4FF00" }}
            >
              — Got your model?
            </p>
            <h3
              className="font-heading text-2xl mb-3"
              style={{ fontWeight: 700, color: "rgba(255,255,255,0.95)" }}
            >
              Print &amp; paint it
            </h3>
            <p
              className="font-mono-dm text-sm leading-relaxed"
              style={{ color: "rgba(255,255,255,0.5)" }}
            >
              Send your export to a print service, then bring it to life with paint.
            </p>
          </div>

          <p
            className="font-mono-dm text-xs uppercase tracking-[0.15em]"
            style={{ color: "rgba(255,255,255,0.3)" }}
          >
            Printing
          </p>
          <div className="flex flex-col gap-0" style={{ marginTop: "-0.3cm" }}>
            {PRINT_SERVICES.map((s) => (
              <a
                key={s.label}
                href={s.href}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-center justify-between py-3 border-b transition-all duration-300"
                style={{ borderColor: "rgba(255,255,255,0.06)" }}
                onMouseEnter={(e) => {
                  const row = e.currentTarget as HTMLAnchorElement;
                  row.style.borderColor = `${s.color}40`;
                  const label = row.querySelector(".srv-label") as HTMLElement;
                  if (label) label.style.color = s.color;
                  const arrow = row.querySelector(".srv-arrow") as HTMLElement;
                  if (arrow) { arrow.style.transform = "translateX(6px)"; arrow.style.opacity = "1"; }
                }}
                onMouseLeave={(e) => {
                  const row = e.currentTarget as HTMLAnchorElement;
                  row.style.borderColor = "rgba(255,255,255,0.06)";
                  const label = row.querySelector(".srv-label") as HTMLElement;
                  if (label) label.style.color = "rgba(255,255,255,0.85)";
                  const arrow = row.querySelector(".srv-arrow") as HTMLElement;
                  if (arrow) { arrow.style.transform = "translateX(0)"; arrow.style.opacity = "0.3"; }
                }}
              >
                <div>
                  <span
                    className="srv-label font-heading text-base block mb-0.5 transition-colors duration-300"
                    style={{ fontWeight: 700, color: "rgba(255,255,255,0.85)" }}
                  >
                    {s.label}
                  </span>
                  <span className="font-mono-dm text-xs" style={{ color: "rgba(255,255,255,0.35)" }}>
                    {s.sub}
                  </span>
                </div>
                <span
                  className="srv-arrow font-mono-dm text-xl transition-all duration-300"
                  style={{ color: s.color, transform: "translateX(0)", opacity: 0.3 }}
                >
                  →
                </span>
              </a>
            ))}
          </div>

          <p
            className="font-mono-dm text-xs uppercase tracking-[0.15em]"
            style={{ color: "rgba(255,255,255,0.3)" }}
          >
            Painting
          </p>
          <div className="flex flex-col gap-0" style={{ marginTop: "-0.3cm" }}>
            {PAINT_SERVICES.map((s) => (
              <a
                key={s.label}
                href={s.href}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-center justify-between py-3 border-b transition-all duration-300"
                style={{ borderColor: "rgba(255,255,255,0.06)" }}
                onMouseEnter={(e) => {
                  const row = e.currentTarget as HTMLAnchorElement;
                  row.style.borderColor = `${s.color}40`;
                  const label = row.querySelector(".srv-label") as HTMLElement;
                  if (label) label.style.color = s.color;
                  const arrow = row.querySelector(".srv-arrow") as HTMLElement;
                  if (arrow) { arrow.style.transform = "translateX(6px)"; arrow.style.opacity = "1"; }
                }}
                onMouseLeave={(e) => {
                  const row = e.currentTarget as HTMLAnchorElement;
                  row.style.borderColor = "rgba(255,255,255,0.06)";
                  const label = row.querySelector(".srv-label") as HTMLElement;
                  if (label) label.style.color = "rgba(255,255,255,0.85)";
                  const arrow = row.querySelector(".srv-arrow") as HTMLElement;
                  if (arrow) { arrow.style.transform = "translateX(0)"; arrow.style.opacity = "0.3"; }
                }}
              >
                <div>
                  <span
                    className="srv-label font-heading text-base block mb-0.5 transition-colors duration-300"
                    style={{ fontWeight: 700, color: "rgba(255,255,255,0.85)" }}
                  >
                    {s.label}
                  </span>
                  <span className="font-mono-dm text-xs" style={{ color: "rgba(255,255,255,0.35)" }}>
                    {s.sub}
                  </span>
                </div>
                <span
                  className="srv-arrow font-mono-dm text-xl transition-all duration-300"
                  style={{ color: s.color, transform: "translateX(0)", opacity: 0.3 }}
                >
                  →
                </span>
              </a>
            ))}
          </div>
        </div>
      </div>

      {/* Finishing tips card — full width below */}
      <div className="max-w-4xl mx-auto mt-8">
        <div
          ref={finishRef}
          className="reveal glass-card shimmer-border flex flex-col gap-5"
          style={{ padding: "1cm" }}
        >
          <div
            className="w-8 h-1 rounded-full mt-2 ml-2"
            style={{ background: "#FF6BD6" }}
          />
          <div>
            <p
              className="font-mono-dm text-xs uppercase tracking-[0.25em] mb-2"
              style={{ color: "#D4FF00" }}
            >
              — DIY finishing
            </p>
            <h3
              className="font-heading text-2xl mb-3"
              style={{ fontWeight: 700, color: "rgba(255,255,255,0.95)" }}
            >
              Make it look amazing
            </h3>
            <p
              className="font-mono-dm text-sm leading-relaxed mb-4"
              style={{ color: "rgba(255,255,255,0.5)" }}
            >
              Some services print in full colour straight from your textured model — no painting needed. Otherwise, craft paint, spray primer, and a bit of patience go a long way.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-3">
            {FINISHING_TIPS.map((tip) => (
              <div key={tip} className="flex items-start gap-3">
                <span style={{ color: "#FF6BD6", flexShrink: 0 }}>→</span>
                <span
                  className="font-mono-dm text-sm"
                  style={{ color: "rgba(255,255,255,0.6)" }}
                >
                  {tip}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Scanning & capture tips card — full width */}
      <div className="max-w-4xl mx-auto mt-8">
        <div
          className="glass-card shimmer-border flex flex-col gap-5"
          style={{ padding: "1cm" }}
        >
          <div
            className="w-8 h-1 rounded-full mt-2 ml-2"
            style={{ background: "#22D3EE" }}
          />
          <div>
            <p
              className="font-mono-dm text-xs uppercase tracking-[0.25em] mb-2"
              style={{ color: "#D4FF00" }}
            >
              — Better captures
            </p>
            <h3
              className="font-heading text-2xl mb-3"
              style={{ fontWeight: 700, color: "rgba(255,255,255,0.95)" }}
            >
              Get the best scan possible
            </h3>
            <p
              className="font-mono-dm text-sm leading-relaxed mb-4"
              style={{ color: "rgba(255,255,255,0.5)" }}
            >
              Photogrammetry needs surface detail to work. Dreams' smooth surfaces are its biggest challenge — here's how to beat it.
            </p>
          </div>
          <div className="flex flex-col gap-4">
            {SCANNING_TIPS.map((tip) => (
              <div key={tip} className="flex items-start gap-3">
                <span style={{ color: "#22D3EE", flexShrink: 0 }}>→</span>
                <span
                  className="font-mono-dm text-sm leading-relaxed"
                  style={{ color: "rgba(255,255,255,0.6)" }}
                >
                  {tip}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
