import React, { useState, useEffect } from 'react'
import { resetPassword } from '../api'
import { useNavigate, useLocation } from 'react-router-dom'

export default function ResetPasswordPage(){
  const [email, setEmail] = useState('')
  const [token, setToken] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const navigate = useNavigate()
  const loc = useLocation()

  useEffect(()=>{
    const q = new URLSearchParams(loc.search)
    const e = q.get('email') || ''
    const t = q.get('token') || ''
    setEmail(e)
    setToken(t)
  }, [loc.search])

  async function handleSubmit(e){
    e.preventDefault()
    if (password !== confirm) return alert('Passwords do not match')
    try{
      await resetPassword({email, token, new_password: password})
      alert('Password reset successfully. Please log in with your new password.')
      navigate('/login')
    }catch(err){
      alert('Reset failed: ' + err.message)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 card">
      <h2 className="text-xl font-semibold mb-4">Reset password</h2>
      <form onSubmit={handleSubmit}>
        <input className="w-full p-2 border rounded mb-2" placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="w-full p-2 border rounded mb-2" placeholder="token" value={token} onChange={e=>setToken(e.target.value)} />
        <input className="w-full p-2 border rounded mb-2" placeholder="new password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <input className="w-full p-2 border rounded mb-2" placeholder="confirm password" type="password" value={confirm} onChange={e=>setConfirm(e.target.value)} />
        <button className="w-full bg-emerald-500 text-white py-2 rounded">Reset password</button>
      </form>
    </div>
  )
}