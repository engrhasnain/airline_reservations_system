import React, { useEffect, useState } from 'react'
import api from '../api'
import { getCurrentUser } from '../utils/auth'

export default function Admin(){
  const [stats, setStats] = useState([])
  const [bookings, setBookings] = useState([])
  const [flights, setFlights] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [newFlight, setNewFlight] = useState({
    flight_number: '', origin: '', destination: '', departure_time: '', arrival_time: '', total_seats: 100, status: 'ACTIVE'
  })
  const [creating, setCreating] = useState(false)

  useEffect(()=>{
    const user = getCurrentUser()
    if (!user || !user.is_admin){
      setError('Admin access required')
      setLoading(false)
      return
    }

    async function load(){
      setLoading(true)
      try{
        const [s, b, f] = await Promise.all([api('/flights/stats'), api('/bookings/'), api('/flights/')])
        setStats(s || [])
        setBookings(b || [])
        setFlights(f || [])
      }catch(err){
        setError(err.message || 'Failed to load')
      }finally{
        setLoading(false)
      }
    }
    load()
  }, [])

  async function refresh(){
    setLoading(true)
    try{
      const [s, b, f] = await Promise.all([api('/flights/stats'), api('/bookings/'), api('/flights/')])
      setStats(s || [])
      setBookings(b || [])
      setFlights(f || [])
    }catch(err){
      setError(err.message || 'Failed to load')
    }finally{
      setLoading(false)
    }
  }

  async function createFlight(e){
    e.preventDefault()
    try{
      setCreating(true)
      // convert datetime-local to ISO strings
      const payload = {
        ...newFlight,
        departure_time: new Date(newFlight.departure_time).toISOString(),
        arrival_time: new Date(newFlight.arrival_time).toISOString(),
        total_seats: parseInt(newFlight.total_seats, 10)
      }
      await api('/flights/', { method: 'POST', body: JSON.stringify(payload) })
      setNewFlight({flight_number: '', origin: '', destination: '', departure_time: '', arrival_time: '', total_seats: 100, status: 'ACTIVE'})
      await refresh()
    }catch(err){
      alert('Create failed: ' + err.message)
    }finally{
      setCreating(false)
    }
  }

  async function deleteFlight(id){
    if (!confirm('Delete flight #' + id + '?')) return
    try{
      await api(`/flights/${id}`, { method: 'DELETE' })
      await refresh()
    }catch(err){
      alert('Delete failed: ' + err.message)
    }
  }

  async function changeStatus(id, status){
    try{
      await api(`/flights/${id}/status?status=${encodeURIComponent(status)}`, { method: 'PATCH' })
      await refresh()
    }catch(err){
      alert('Status update failed: ' + err.message)
    }
  }

  if (loading) return <div className="max-w-5xl mx-auto py-10">Loading admin data…</div>
  if (error) return <div className="max-w-5xl mx-auto py-10 text-red-600">Error: {error}</div>

  return (
    <div className="max-w-6xl mx-auto py-10">
      <h2 className="text-2xl font-semibold mb-4">Admin Dashboard</h2>

      <div className="card mb-6">
        <h3 className="font-semibold mb-2">Manage Flights</h3>
        <form className="grid grid-cols-1 md:grid-cols-3 gap-2 mb-4" onSubmit={createFlight}>
          <input required placeholder="Flight #" value={newFlight.flight_number} onChange={e=>setNewFlight({...newFlight, flight_number: e.target.value})} className="p-2 border rounded" />
          <input required placeholder="Origin" value={newFlight.origin} onChange={e=>setNewFlight({...newFlight, origin: e.target.value})} className="p-2 border rounded" />
          <input required placeholder="Destination" value={newFlight.destination} onChange={e=>setNewFlight({...newFlight, destination: e.target.value})} className="p-2 border rounded" />
          <input required type="datetime-local" value={newFlight.departure_time} onChange={e=>setNewFlight({...newFlight, departure_time: e.target.value})} className="p-2 border rounded" />
          <input required type="datetime-local" value={newFlight.arrival_time} onChange={e=>setNewFlight({...newFlight, arrival_time: e.target.value})} className="p-2 border rounded" />
          <input required type="number" value={newFlight.total_seats} onChange={e=>setNewFlight({...newFlight, total_seats: e.target.value})} className="p-2 border rounded" />
          <select value={newFlight.status} onChange={e=>setNewFlight({...newFlight, status: e.target.value})} className="p-2 border rounded">
            <option>ACTIVE</option>
            <option>SCHEDULED</option>
            <option>CANCELLED</option>
          </select>
          <div className="md:col-span-3">
            <button disabled={creating} className="bg-emerald-500 text-white px-4 py-2 rounded">{creating ? 'Creating...' : 'Create Flight'}</button>
          </div>
        </form>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="text-sm text-slate-600">
                <th className="py-2">ID</th>
                <th className="py-2">Flight</th>
                <th className="py-2">When</th>
                <th className="py-2">Seats</th>
                <th className="py-2">Status</th>
                <th className="py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {flights.map(f=> (
                <tr key={f.id} className="border-t">
                  <td className="py-2">{f.id}</td>
                  <td className="py-2">{f.flight_number} <div className="text-xs text-slate-500">{f.origin} → {f.destination}</div></td>
                  <td className="py-2">{new Date(f.departure_time).toLocaleString()} → {new Date(f.arrival_time).toLocaleString()}</td>
                  <td className="py-2">{f.total_seats}</td>
                  <td className="py-2">
                    <select value={f.status} onChange={e=>changeStatus(f.id, e.target.value)} className="p-1 border rounded text-sm">
                      <option>ACTIVE</option>
                      <option>SCHEDULED</option>
                      <option>CANCELLED</option>
                    </select>
                  </td>
                  <td className="py-2">
                    <button onClick={()=>deleteFlight(f.id)} className="text-rose-600">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card mb-6">
        <h3 className="font-semibold mb-2">Flight Stats</h3>
        {stats.length === 0 ? (
          <div className="text-slate-600">No data</div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="text-sm text-slate-600">
                <th className="py-2">Flight</th>
                <th className="py-2">Total Bookings</th>
              </tr>
            </thead>
            <tbody>
              {stats.map(s => (
                <tr key={s.flight_number} className="border-t">
                  <td className="py-2">{s.flight_number}</td>
                  <td className="py-2">{s.total_bookings}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card">
        <h3 className="font-semibold mb-2">All Bookings</h3>
        {bookings.length === 0 ? (
          <div className="text-slate-600">No bookings</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="text-sm text-slate-600">
                  <th className="py-2">#</th>
                  <th className="py-2">User</th>
                  <th className="py-2">Flight</th>
                  <th className="py-2">Seat</th>
                  <th className="py-2">Status</th>
                  <th className="py-2">Booked At</th>
                </tr>
              </thead>
              <tbody>
                {bookings.map(b=> (
                  <tr key={b.id} className="border-t">
                    <td className="py-2">#{b.id}</td>
                    <td className="py-2">{b.user_email}</td>
                    <td className="py-2">{b.flight_number} <div className="text-xs text-slate-500">{b.origin} → {b.destination}</div></td>
                    <td className="py-2">{b.seat_id}</td>
                    <td className="py-2">{b.payment_status}</td>
                    <td className="py-2">{new Date(b.booked_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}