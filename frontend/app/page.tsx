// Clean, bold landing page
export default function LandingPage() {
  return (
    <main className="min-h-screen bg-black text-white">
      {/* Hero */}
      <section className="flex flex-col items-center justify-center min-h-screen text-center px-4">
        <div className="inline-block bg-green-500 text-black text-sm font-bold px-3 py-1 rounded-full mb-6">
           Built for Rwanda
        </div>
        <h1 className="text-6xl font-black mb-4 leading-tight">
          Your AI Job Agent.<br/>
          <span className="text-green-400">Never Miss an Opportunity.</span>
        </h1>
        <p className="text-xl text-gray-400 mb-8 max-w-xl">
          Upload your CV. Our AI agent browses every Rwanda job board, 
          gig platform, and opportunity — and applies for you. 24/7.
        </p>
        <a href="/apply" className="bg-green-500 hover:bg-green-400 text-black font-bold text-xl px-8 py-4 rounded-full transition-all">
          Start Applying Free →
        </a>
        
        {/* Stats */}
        <div className="flex gap-12 mt-16 text-center">
          <div><p className="text-4xl font-black text-green-400">15+</p><p className="text-gray-500">Job Platforms</p></div>
          <div><p className="text-4xl font-black text-green-400">50+</p><p className="text-gray-500">Apps Per Session</p></div>
          <div><p className="text-4xl font-black text-green-400">24/7</p><p className="text-gray-500">Agent Active</p></div>
        </div>
      </section>
    </main>
  )
}
