import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getToken, logout, getCurrentUser } from '../utils/auth'

export default function Navbar(){
  const navigate = useNavigate()
  const [token, setTokenState] = React.useState(getToken())
  const [isAdmin, setIsAdmin] = React.useState(false)

  React.useEffect(()=>{
    function onAuthChange(){
      setTokenState(getToken())
      const user = getCurrentUser()
      setIsAdmin(!!(user && user.is_admin))
    }
    onAuthChange()
    window.addEventListener('auth:change', onAuthChange)
    window.addEventListener('storage', onAuthChange)
    return ()=>{
      window.removeEventListener('auth:change', onAuthChange)
      window.removeEventListener('storage', onAuthChange)
    }
  }, [])

  function handleLogout(){
    logout()
    navigate('/')
  }

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="header-brand">Airline</Link>
        <div>
          <Link to="/flights" className="mr-4 text-slate-600 hover:text-slate-900">Flights</Link>
          <Link to="/about" className="mr-4 text-slate-600 hover:text-slate-900">About</Link>
          <Link to="/contact" className="mr-4 text-slate-600 hover:text-slate-900">Contact</Link>
          {isAdmin && <Link to="/admin" className="mr-4 text-rose-600 hover:text-rose-900">Admin</Link>}
          {token ? (
            <>
              <Link to="/dashboard" className="mr-4 text-slate-600 hover:text-slate-900">Dashboard</Link>
              <button onClick={handleLogout} className="btn btn-sm bg-emerald-500 text-white px-3 py-1 rounded">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="mr-4 text-slate-600 hover:text-slate-900">Login</Link>
              <Link to="/register" className="btn btn-sm bg-emerald-500 text-white px-3 py-1 rounded">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
