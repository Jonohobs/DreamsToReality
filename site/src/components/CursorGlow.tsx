import { useEffect, useRef } from "react";

export default function CursorGlow() {
  const glowRef = useRef<HTMLDivElement>(null);
  const pos = useRef({ x: -300, y: -300 });
  const target = useRef({ x: -300, y: -300 });
  const animId = useRef<number>(0);

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      target.current = { x: e.clientX, y: e.clientY };
    };

    const tick = () => {
      const dx = target.current.x - pos.current.x;
      const dy = target.current.y - pos.current.y;

      // Skip RAF if barely moving to save CPU
      if (Math.abs(dx) > 0.2 || Math.abs(dy) > 0.2) {
        pos.current.x += dx * 0.08;
        pos.current.y += dy * 0.08;

        if (glowRef.current) {
          glowRef.current.style.transform = `translate3d(${pos.current.x - 150}px, ${pos.current.y - 150}px, 0)`;
        }
      }

      animId.current = requestAnimationFrame(tick);
    };

    window.addEventListener("mousemove", onMove, { passive: true });
    animId.current = requestAnimationFrame(tick);

    return () => {
      window.removeEventListener("mousemove", onMove);
      cancelAnimationFrame(animId.current);
    };
  }, []);

  return (
    <div
      ref={glowRef}
      className="pointer-events-none fixed z-10 w-[300px] h-[300px] rounded-full"
      style={{
        background: "radial-gradient(circle, rgba(255,107,214,0.10) 0%, rgba(212,255,0,0.05) 45%, transparent 70%)",
        filter: "blur(24px)",
        transition: "none",
        willChange: "transform",
        top: 0,
        left: 0,
      }}
    />
  );
}
