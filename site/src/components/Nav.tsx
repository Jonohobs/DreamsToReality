import { useState, useEffect } from "react";

const GITHUB_URL = "https://github.com/Jonohobs/DreamsToReality";

export default function Nav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const scrollTo = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <nav
      className="fixed top-0 left-0 right-0 z-50 transition-all duration-500"
      style={{
        background: scrolled
          ? "rgba(10, 10, 15, 0.75)"
          : "rgba(10, 10, 15, 0.3)",
        backdropFilter: "blur(16px)",
        WebkitBackdropFilter: "blur(16px)",
        borderBottom: scrolled ? "1px solid rgba(255,255,255,0.06)" : "1px solid transparent",
      }}
    >
      <div
        className="w-full h-16 flex items-center justify-between"
        style={{ paddingLeft: "0.6cm", paddingRight: "0.6cm", gap: "0.8cm" }}
      >
        {/* Left: wisp dot + brand — clickable home link */}
        <a
          href="#"
          onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: "smooth" }); }}
          className="flex items-center flex-shrink-0 transition-opacity duration-300 hover:opacity-80"
          style={{ gap: "0.5cm", textDecoration: "none" }}
        >
          <span
            className="block w-2.5 h-2.5 rounded-full flex-shrink-0"
            style={{
              background: "radial-gradient(circle, #D4FF00 30%, #FF6BD6 100%)",
              animation: "wisp-pulse 2.5s ease-in-out infinite",
            }}
          />
          <span
            className="font-heading text-sm tracking-[-0.01em] flex-shrink-0"
            style={{ color: "rgba(255,255,255,0.9)", fontWeight: 700 }}
          >
            Dreams <span className="font-mono-dm" style={{ fontSize: "0.65em", opacity: 0.5, verticalAlign: "middle" }}>to</span> Reality
          </span>
          <span
            className="font-mono-dm text-xs uppercase tracking-[0.15em] rounded-full flex-shrink-0"
            style={{
              padding: "2px 8px",
              color: "#D4FF00",
              border: "1px solid rgba(212,255,0,0.3)",
              fontSize: "0.6rem",
            }}
          >
            Beta
          </span>
        </a>

        {/* Right: nav links */}
        <div className="flex items-center gap-6 overflow-hidden flex-shrink min-w-0" style={{ whiteSpace: "nowrap" }}>
          {[
            { label: "How It Works", id: "how-it-works" },
            { label: "Features",     id: "features" },
            { label: "Community",    id: "community" },
          ].map((link) => (
            <button
              key={link.id}
              onClick={() => scrollTo(link.id)}
              className="font-mono-dm text-sm text-white/60 hover:text-white transition-colors duration-300 flex-shrink-0"
              style={{ background: "none", border: "none", cursor: "pointer" }}
            >
              {link.label}
            </button>
          ))}
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="font-mono-dm text-sm rounded-full border transition-all duration-300 flex-shrink-0"
            style={{
              padding: "0.25cm 0.5cm",
              borderColor: "rgba(255,255,255,0.15)",
              color: "rgba(255,255,255,0.7)",
            }}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLAnchorElement).style.borderColor = "#D4FF00";
              (e.currentTarget as HTMLAnchorElement).style.color = "#D4FF00";
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLAnchorElement).style.borderColor = "rgba(255,255,255,0.15)";
              (e.currentTarget as HTMLAnchorElement).style.color = "rgba(255,255,255,0.7)";
            }}
          >
            GitHub ↗
          </a>
        </div>
      </div>
    </nav>
  );
}
