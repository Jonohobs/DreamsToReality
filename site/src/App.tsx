import NebulaBackground from './components/NebulaBackground'
import ParticleCanvas from './components/ParticleCanvas'
import CursorGlow from './components/CursorGlow'
import Nav from './components/Nav'
import HeroSection from './components/HeroSection'
import HowItWorksSection from './components/HowItWorksSection'
import FeaturesSection from './components/FeaturesSection'
import GetHelpSection from './components/GetHelpSection'
import JoinBetaSection from './components/JoinBetaSection'
import WhatIsDreamsSection from './components/WhatIsDreamsSection'
import ShowcaseSection from './components/ShowcaseSection'
import ProcessSection from './components/ProcessSection'
import Footer from './components/Footer'

function App() {
  return (
    <div className="min-h-screen relative" style={{ background: '#0A0A0F' }}>
      <NebulaBackground />
      <ParticleCanvas />
      <CursorGlow />
      <Nav />
      <main className="relative z-10 flex flex-col" style={{ gap: "1cm" }}>
        <HeroSection />
        <WhatIsDreamsSection />
        <HowItWorksSection />
        <ShowcaseSection />
        <ProcessSection />
        <GetHelpSection />
        <JoinBetaSection />
        <FeaturesSection />
      </main>
      <div style={{ height: "1cm" }} />
      <Footer />
    </div>
  )
}

export default App
