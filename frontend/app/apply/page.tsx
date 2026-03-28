"use client"
import { useState } from "react"
import { useRouter } from "next/navigation"

export default function ApplyPage() {
  const [step, setStep] = useState(1) // 1: upload, 2: profile, 3: launching
  const [resumeText, setResumeText] = useState("")
  const [profile, setProfile] = useState<{
    full_name: string; email: string; phone: string;
    job_preferences: string; linkedin_url: string; portfolio_url: string;
  }>({
    full_name: "", email: "", phone: "",
    job_preferences: "", linkedin_url: "", portfolio_url: ""
  })
  const router = useRouter()

  const handleResumeUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0]
    const formData = new FormData()
    formData.append("file", file)
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/upload-resume`, {
      method: "POST", body: formData
    })
    const data = await res.json()
    setResumeText(data.resume_text)
    setProfile(p => ({ ...p, ...data })) // auto-fill from resume
    setStep(2)
  }

  const handleLaunchAgent = async () => {
    setStep(3)
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/start-agent`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...profile, resume_text: resumeText })
    })
    const data = await res.json()
    localStorage.setItem("session_id", data.session_id)
    router.push(`/dashboard?session=${data.session_id}`)
  }

  return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center p-8">
      {step === 1 && (
        <div className="max-w-lg w-full text-center">
          <h2 className="text-3xl font-black mb-2">Upload Your CV</h2>
          <p className="text-gray-400 mb-8">PDF or DOCX — we'll extract everything</p>
          <label className="border-2 border-dashed border-green-500 rounded-2xl p-12 block cursor-pointer hover:bg-green-950 transition">
            <input type="file" accept=".pdf,.docx" onChange={handleResumeUpload} className="hidden" />
            <p className="text-5xl mb-4">📄</p>
            <p className="text-green-400 font-bold">Click to upload your resume</p>
          </label>
        </div>
      )}

      {step === 2 && (
        <div className="max-w-lg w-full">
          <h2 className="text-3xl font-black mb-6">Complete Your Profile</h2>
          <div className="space-y-4">
            {[
              { key: "full_name", label: "Full Name", placeholder: "Jean de Dieu Habimana" },
              { key: "email", label: "Email", placeholder: "you@example.com" },
              { key: "phone", label: "Phone", placeholder: "+250 7XX XXX XXX" },
              { key: "job_preferences", label: "Job Preferences", placeholder: "software developer, data analyst, design..." },
              { key: "linkedin_url", label: "LinkedIn URL (optional)", placeholder: "linkedin.com/in/yourname" },
              { key: "portfolio_url", label: "Portfolio URL (optional)", placeholder: "yourportfolio.com" },
            ].map(field => (
              <div key={field.key}>
                <label className="text-sm text-gray-400 mb-1 block">{field.label}</label>
                <input
                  className="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white"
                  placeholder={field.placeholder}
                  value={profile[field.key as keyof typeof profile]}
                  onChange={e => setProfile(p => ({ ...p, [field.key]: e.target.value }))}
                />
              </div>
            ))}
            <button onClick={handleLaunchAgent}
              className="w-full bg-green-500 text-black font-black text-lg py-4 rounded-xl hover:bg-green-400 transition mt-4">
               Launch AI Agent
            </button>
          </div>
        </div>
      )}

      {step === 3 && (
        <div className="text-center">
          <div className="text-6xl mb-4 animate-bounce">🤖</div>
          <h2 className="text-3xl font-black">Agent is live!</h2>
          <p className="text-gray-400 mt-2">Taking you to your dashboard...</p>
        </div>
      )}
    </main>
  )
}
