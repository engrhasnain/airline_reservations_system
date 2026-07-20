import React, { useState } from 'react'
import { login } from '../api'
import { setToken } from '../utils/auth'
import { useNavigate } from 'react-router-dom'

export default function LoginPage(){
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const [loadingLogin, setLoadingLogin] = useState(false)
  const navigate = useNavigate()

  async function handleLogin(e){
    e.preventDefault()
    setLoadingLogin(true)
    try{
      const res = await login({email,password})
      if (res?.access_token){
        setToken(res.access_token)
        navigate('/dashboard')
      } else {
        alert('Login failed')
      }
    }catch(err){
      alert('Login failed: ' + err.message)
    }finally{
      setLoadingLogin(false)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 card">
      <h2 className="text-xl font-semibold mb-4">Sign in</h2>
      <form onSubmit={handleLogin}>
        <input className="w-full p-2 border rounded mb-2" placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} disabled={loadingLogin} />
        <input className="w-full p-2 border rounded mb-2" placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} disabled={loadingLogin} />
        <button type="submit" disabled={loadingLogin} className="w-full bg-emerald-500 text-white py-2 rounded disabled:opacity-50 flex items-center justify-center">
          {loadingLogin ? (<><span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin inline-block mr-2" /> Logging in...</>) : 'Login'}
        </button>
        <div className="text-center text-sm mt-2"><a href="/forgot-password" className="text-slate-600">Forgot password?</a></div>
      </form>
    </div>
  )
}
