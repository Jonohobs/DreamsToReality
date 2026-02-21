const GITHUB_URL = "https://github.com/Jonohobs";
const INSTAGRAM_URL = "https://instagram.com/jonathanhobman";
const X_URL = "https://x.com/JonathanHobman";

export default function Footer() {
  return (
    <footer
      className="relative z-10 px-8 md:px-16 lg:px-24 border-t"
      style={{ borderColor: "rgba(255,255,255,0.06)", paddingTop: "0.5cm", paddingBottom: "1cm" }}
    >
      <div className="max-w-4xl mx-auto flex flex-col items-center gap-8 text-center">
        {/* Credit */}
        <p
          className="font-mono-dm text-sm"
          style={{ color: "rgba(255,255,255,0.5)" }}
        >
          Built by{" "}
          <span style={{ color: "#FF6BD6" }}>Jonathan Hobman</span>{" "}
          — open source, MIT licensed
        </p>

        {/* Personal links */}
        <div className="flex items-center gap-6">
          <a
            href={INSTAGRAM_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="font-mono-dm text-sm transition-colors duration-300"
            style={{ color: "rgba(255,255,255,0.45)" }}
            onMouseEnter={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "#FF6BD6")}
            onMouseLeave={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "rgba(255,255,255,0.45)")}
          >
            Instagram ↗
          </a>
          <span style={{ color: "rgba(255,255,255,0.15)" }}>·</span>
          <a
            href={X_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="font-mono-dm text-sm transition-colors duration-300"
            style={{ color: "rgba(255,255,255,0.45)" }}
            onMouseEnter={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "#A78BFA")}
            onMouseLeave={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "rgba(255,255,255,0.45)")}
          >
            X ↗
          </a>
          <span style={{ color: "rgba(255,255,255,0.15)" }}>·</span>
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="font-mono-dm text-sm transition-colors duration-300"
            style={{ color: "rgba(255,255,255,0.45)" }}
            onMouseEnter={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "#22D3EE")}
            onMouseLeave={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "rgba(255,255,255,0.45)")}
          >
            GitHub ↗
          </a>
        </div>

        {/* Original credit */}
        <p
          className="font-mono-dm text-xs"
          style={{ color: "rgba(255,255,255,0.35)" }}
        >
          Inspired by the original Dreams photogrammetry work of{" "}
          <a
            href="https://indreams.me/DrSecksy"
            target="_blank"
            rel="noopener noreferrer"
            className="transition-colors duration-300"
            style={{ color: "#A78BFA" }}
            onMouseEnter={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "#D4FF00")}
            onMouseLeave={(e) => ((e.currentTarget as HTMLAnchorElement).style.color = "#A78BFA")}
          >
            DrSecksy
          </a>
        </p>

        {/* Disclaimer */}
        <p
          className="font-mono-dm text-xs mt-4"
          style={{ color: "rgba(255,255,255,0.3)", marginBottom: "1cm" }}
        >
          Not affiliated with Sony Interactive Entertainment or Media Molecule
        </p>
      </div>
    </footer>
  );
}
