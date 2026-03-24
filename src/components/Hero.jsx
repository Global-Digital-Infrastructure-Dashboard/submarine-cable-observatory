function Hero() {
  return (
    <div className="relative h-[400px] flex items-center justify-center overflow-hidden bg-gradient-to-br from-[#0D47A1] to-[#00695C]">
      {/* Circuit pattern overlay */}
      <div 
        className="absolute inset-0 opacity-40"
        style={{
          backgroundImage: `linear-gradient(rgba(13, 71, 161, 0.85), rgba(0, 105, 92, 0.85)),
            url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400"><defs><pattern id="circuit" x="0" y="0" width="120" height="120" patternUnits="userSpaceOnUse"><path d="M20,20 L100,20 M20,40 L80,40 M40,60 L100,60 M20,80 L60,80 M80,100 L100,100" stroke="rgba(255,255,255,0.1)" stroke-width="2" fill="none"/><circle cx="20" cy="20" r="3" fill="rgba(255,255,255,0.2)"/><circle cx="100" cy="60" r="3" fill="rgba(255,255,255,0.2)"/><circle cx="80" cy="100" r="3" fill="rgba(255,255,255,0.2)"/></pattern></defs><rect width="1200" height="400" fill="url(%23circuit)"/></svg>')`,
          backgroundSize: 'cover'
        }}
      />

      {/* Content */}
      <div className="relative z-10 text-center max-w-[900px] px-8">
        <h1 className="font-serif text-5xl font-bold text-white mb-4 tracking-tight">
          Global Digital Infrastructure Political Economy Observatory
        </h1>
        <p className="font-sans text-xl font-normal text-white/90 mb-2">
          Phase 1: Submarine Cable Analysis
        </p>
        <p className="font-sans text-[0.95rem] font-light text-white/70">
          Research Platform | Northeastern University
        </p>
      </div>
    </div>
  )
}

export default Hero