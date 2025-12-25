import React, { useState } from 'react'
import { register, login } from '../api'
import { setToken } from '../utils/auth'
import { useNavigate } from 'react-router-dom'

export default function RegisterPage(){
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  async function handleRegister(e){
    e.preventDefault()
    try{
      await register({ full_name: fullName, email, password })
      // auto-login
      const res = await login({ email, password })
      if (res?.access_token){
        setToken(res.access_token)
        navigate('/dashboard')
      } else {
        navigate('/login')
      }
    }catch(err){
      alert('Registration failed: ' + err.message)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 card">
      <h2 className="text-xl font-semibold mb-4">Create Account</h2>
      <form onSubmit={handleRegister}>
        <input className="w-full p-2 border rounded mb-2" placeholder="Full name" value={fullName} onChange={e=>setFullName(e.target.value)} />
        <input className="w-full p-2 border rounded mb-2" placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="w-full p-2 border rounded mb-2" placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="w-full bg-emerald-500 text-white py-2 rounded">Register</button>
      </form>
    </div>
  )
}
