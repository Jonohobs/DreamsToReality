export default function NebulaBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden">
      {/* Grain overlay */}
      <svg
        className="absolute inset-0 w-full h-full opacity-[0.03]"
        xmlns="http://www.w3.org/2000/svg"
      >
        <filter id="grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>

      {/* Nebula orb 1 — Dreams Pink */}
      <div
        className="nebula-1 absolute"
        style={{
          top: "5%",
          left: "10%",
          width: "600px",
          height: "600px",
          background: "radial-gradient(circle, rgba(255,107,214,0.18) 0%, transparent 70%)",
          filter: "blur(80px)",
          borderRadius: "50%",
        }}
      />

      {/* Nebula orb 2 — Violet */}
      <div
        className="nebula-2 absolute"
        style={{
          top: "20%",
          right: "5%",
          width: "700px",
          height: "700px",
          background: "radial-gradient(circle, rgba(167,139,250,0.14) 0%, transparent 70%)",
          filter: "blur(100px)",
          borderRadius: "50%",
        }}
      />

      {/* Nebula orb 3 — Cyan */}
      <div
        className="nebula-3 absolute"
        style={{
          bottom: "10%",
          left: "20%",
          width: "500px",
          height: "500px",
          background: "radial-gradient(circle, rgba(34,211,238,0.12) 0%, transparent 70%)",
          filter: "blur(90px)",
          borderRadius: "50%",
        }}
      />

      {/* Nebula orb 4 — Lime (faint) */}
      <div
        className="nebula-4 absolute"
        style={{
          bottom: "30%",
          right: "15%",
          width: "400px",
          height: "400px",
          background: "radial-gradient(circle, rgba(212,255,0,0.07) 0%, transparent 70%)",
          filter: "blur(80px)",
          borderRadius: "50%",
        }}
      />
    </div>
  );
}
