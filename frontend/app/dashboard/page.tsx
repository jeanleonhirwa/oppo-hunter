"use client"
import { useEffect, useState, Suspense } from "react"
import { useSearchParams } from "next/navigation"

function DashboardContent() {
  const params = useSearchParams()
  const sessionId = params.get("session")
  const [applications, setApplications] = useState<any[]>([])
  const [isAgentRunning, setIsAgentRunning] = useState(true)

  useEffect(() => {
    if (!sessionId) return
    
    // Poll every 5 seconds for new applications
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/applications/${sessionId}`)
        if (res.ok) {
          const data = await res.json()
          setApplications(data.applications || [])
          if (data.applications && data.applications.length >= 20) setIsAgentRunning(false)
        }
      } catch (err) {
        console.error("Dashboard error:", err)
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [sessionId])

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-black">Your Applications</h1>
        {isAgentRunning && (
          <div className="flex items-center gap-2 bg-green-950 text-green-400 px-4 py-2 rounded-full">
            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
            Agent is searching...
          </div>
        )}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-gray-900 rounded-2xl p-6 text-center">
          <p className="text-4xl font-black text-green-400">{applications.length}</p>
          <p className="text-gray-500">Total Applied</p>
        </div>
        <div className="bg-gray-900 rounded-2xl p-6 text-center">
          <p className="text-4xl font-black text-blue-400">
            {applications.filter(a => a.status === "applied").length}
          </p>
          <p className="text-gray-500">Successful</p>
        </div>
        <div className="bg-gray-900 rounded-2xl p-6 text-center">
          <p className="text-4xl font-black text-yellow-400">
            {[...new Set(applications.map(a => a.platform))].length}
          </p>
          <p className="text-gray-500">Platforms Hit</p>
        </div>
      </div>

      {/* Applications list */}
      <div className="space-y-3">
        {applications.length === 0 && (
          <div className="text-center py-16 text-gray-600">
            <p className="text-5xl mb-4">🔍</p>
            <p>Agent is searching... first applications coming soon</p>
          </div>
        )}
        {applications.map((app, i) => (
          <div key={app.id || i} className="bg-gray-900 rounded-xl p-4 flex items-center justify-between">
            <div>
              <p className="font-bold text-white">{app.job_title}</p>
              <p className="text-gray-400 text-sm">{app.company} · {app.platform}</p>
            </div>
            <div className="flex items-center gap-3">
              <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                app.status === "applied" ? "bg-green-950 text-green-400" : "bg-red-950 text-red-400"
              }`}>
                {app.status === "applied" ? "✓ Applied" : "✗ Failed"}
              </span>
              {app.job_url && (
                <a href={app.job_url} target="_blank" rel="noreferrer"
                   className="text-gray-500 hover:text-white text-xs">View →</a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function Dashboard() {
  return (
    <main className="min-h-screen bg-black text-white p-8">
      <Suspense fallback={<div>Loading dashboard...</div>}>
        <DashboardContent />
      </Suspense>
    </main>
  )
}
