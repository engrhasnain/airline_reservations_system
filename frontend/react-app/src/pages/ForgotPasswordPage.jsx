import React, { useState } from 'react'
import { forgotPassword } from '../api'

export default function ForgotPasswordPage(){
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e){
    e.preventDefault()
    setLoading(true)
    try{
      await forgotPassword({email})
      alert('If the email exists, a reset link has been sent.')
    }catch(err){
      alert('Request failed: ' + err.message)
    }finally{
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 card">
      <h2 className="text-xl font-semibold mb-4">Forgot password</h2>
      <form onSubmit={handleSubmit}>
        <input className="w-full p-2 border rounded mb-2" placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
        <button className="w-full bg-emerald-500 text-white py-2 rounded">Send reset link</button>
      </form>
    </div>
  )
}