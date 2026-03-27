function Hero() {
  return (
    <div className="relative h-[500px] overflow-hidden">
      {/* Video Background */}
      <video 
        autoPlay 
        loop 
        muted 
        playsInline
        className="absolute inset-0 w-full h-full object-cover"
      >
        <source src="/cable2.mp4" type="video/mp4" />
        {/* Fallback for browsers that don't support video */}
      </video>
      
      {/* Optional: Add a subtle dark overlay for text readability */}
      <div className="absolute inset-0 bg-black/30" />
      
      {/* Content */}
      <div className="relative z-10 h-full flex items-center justify-center">
        <div className="text-center max-w-4xl px-8">
          <h1 className="font-serif text-5xl font-semibold text-white mb-4 tracking-wider leading-tight">
            Global Digital Infrastructure Political Economy Observatory
          </h1>
          <p className="font-sans text-xl font-light text-white/95 mb-2 tracking-wider">
            Phase 1: Submarine Cable Analysis
          </p>
          <p className="font-sans text-base font-light text-white/75 tracking-wider">
            Research Platform | Professor Shen's Research Group, Northeastern University
          </p>
        </div>
      </div>
    </div>
  )
}

export default Hero