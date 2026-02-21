const STEPS = [
  {
    num: "1",
    title: "Capture in Dreams",
    desc: "Place your sculpt on the capture platform. Our in-Dreams tool automatically applies tracking patterns and records two camera passes.",
  },
  {
    num: "2",
    title: "Upload Your Videos",
    desc: "Transfer the two recordings from your PS5 and upload them here. One for geometry, one for color.",
  },
  {
    num: "3",
    title: "Get Your 3D Model",
    desc: "Our pipeline extracts frames, removes backgrounds, and reconstructs a full 3D mesh ready for Blender, Unity, or 3D printing.",
  },
];

const FEATURES = [
  {
    title: "Dreams-Tuned Pipeline",
    desc: "Custom-built for Dreams' unique SDF rendering. We handle the soft edges, painterly flecks, and baked lighting that break standard tools.",
  },
  {
    title: "Two-Pass Capture",
    desc: "Geometry pass with tracking patterns for accurate shape. Texture pass with clean colors for faithful materials. Best of both worlds.",
  },
  {
    title: "Runs Locally",
    desc: "Your creations never leave your machine. All processing happens on your hardware. No cloud uploads, no data collection.",
  },
  {
    title: "Open Source",
    desc: "The entire pipeline is open. Inspect, modify, and improve it. Built by the Dreams community, for the Dreams community.",
  },
];

export default function Landing({ onGetStarted }: { onGetStarted: () => void }) {
  return (
    <div>
      {/* Hero */}
      <section className="max-w-5xl mx-auto px-6 py-24 text-center">
        <div className="inline-block mb-6 px-3 py-1 rounded-full bg-red-600/20 text-red-400 text-sm font-medium border border-red-600/30">
          PlayStation Dreams
        </div>
        <h1 className="text-5xl sm:text-6xl font-bold tracking-tight mb-6 leading-tight">
          Break your creations
          <br />
          <span className="text-red-500">out of Dreams</span>
        </h1>
        <p className="text-lg text-neutral-400 max-w-2xl mx-auto mb-10">
          Extract 3D models from PlayStation Dreams using photogrammetry.
          Capture a video inside Dreams, upload it here, and get a real 3D mesh
          you can use in Blender, Unity, Unreal, or 3D print.
        </p>
        <div className="flex gap-4 justify-center">
          <button
            onClick={onGetStarted}
            className="px-6 py-3 bg-red-600 hover:bg-red-500 rounded-lg font-medium transition-colors cursor-pointer"
          >
            Extract a Model
          </button>
          <a
            href="#how-it-works"
            className="px-6 py-3 bg-neutral-800 hover:bg-neutral-700 rounded-lg font-medium transition-colors"
          >
            How It Works
          </a>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="max-w-5xl mx-auto px-6 py-20">
        <h2 className="text-3xl font-bold text-center mb-16">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {STEPS.map((step) => (
            <div
              key={step.num}
              className="relative p-6 rounded-xl bg-neutral-900 border border-neutral-800"
            >
              <div className="w-10 h-10 rounded-full bg-red-600 flex items-center justify-center text-lg font-bold mb-4">
                {step.num}
              </div>
              <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
              <p className="text-neutral-400 text-sm leading-relaxed">
                {step.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="max-w-5xl mx-auto px-6 py-20">
        <h2 className="text-3xl font-bold text-center mb-16">
          Built for Dreams
        </h2>
        <div className="grid md:grid-cols-2 gap-6">
          {FEATURES.map((f) => (
            <div
              key={f.title}
              className="p-6 rounded-xl bg-neutral-900/50 border border-neutral-800/50"
            >
              <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
              <p className="text-neutral-400 text-sm leading-relaxed">
                {f.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-5xl mx-auto px-6 py-20 text-center">
        <div className="p-12 rounded-2xl bg-gradient-to-br from-red-600/20 to-neutral-900 border border-red-600/20">
          <h2 className="text-3xl font-bold mb-4">Ready to extract?</h2>
          <p className="text-neutral-400 mb-8 max-w-lg mx-auto">
            Record your Dreams creation using the capture tool, then upload the
            video here. Your 3D model will be ready in minutes.
          </p>
          <button
            onClick={onGetStarted}
            className="px-8 py-3 bg-red-600 hover:bg-red-500 rounded-lg font-medium transition-colors cursor-pointer"
          >
            Get Started
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-neutral-800 py-8 text-center text-neutral-500 text-sm">
        Dreams to Reality — Open source photogrammetry for PlayStation Dreams
      </footer>
    </div>
  );
}
