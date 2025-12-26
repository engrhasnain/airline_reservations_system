import React, { useState } from 'react'
import { login, verifyOtp } from '../api'
import { setToken } from '../utils/auth'
import { useNavigate } from 'react-router-dom'

export default function LoginPage(){
  // ensure old simple Login.jsx is removed and this page is used

  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const [otpMode, setOtpMode] = useState(false)
  const [code, setCode] = useState('')
  const navigate = useNavigate()

  async function handleLogin(e){
    e.preventDefault()
    try{
      const res = await login({email,password})
      if (res?.detail === 'otp_sent'){
        setOtpMode(true)
        return
      }
      if (res?.access_token){
        setToken(res.access_token)
        navigate('/dashboard')
      } else {
        alert('Login failed')
      }
    }catch(err){
      alert('Login failed: ' + err.message)
    }
  }

  async function handleVerify(e){
    e.preventDefault()
    try{
      const res = await verifyOtp({email, code})
      if (res?.access_token){
        setToken(res.access_token)
        navigate('/dashboard')
      } else {
        alert('Verify failed')
      }
    }catch(err){
      alert('Verify failed: ' + err.message)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 card">
      <h2 className="text-xl font-semibold mb-4">Sign in</h2>
      {!otpMode ? (
        <form onSubmit={handleLogin}>
          <input className="w-full p-2 border rounded mb-2" placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
          <input className="w-full p-2 border rounded mb-2" placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
          <button className="w-full bg-emerald-500 text-white py-2 rounded">Login</button>
        </form>
      ) : (
        <form onSubmit={handleVerify}>
          <div className="text-sm text-slate-600 mb-2">A verification code was sent to your email. Enter it below to complete login.</div>
          <input className="w-full p-2 border rounded mb-2" placeholder="6-digit code" value={code} onChange={e=>setCode(e.target.value)} />
          <button className="w-full bg-emerald-500 text-white py-2 rounded">Verify</button>
        </form>
      )}
    </div>
  )
}
