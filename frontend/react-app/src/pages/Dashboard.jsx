import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getToken } from '../utils/auth'
import { fetchBookings } from '../services/bookings'
import api, { pay } from '../api'
import CheckoutModal from '../components/CheckoutModal'

export default function Dashboard(){
  const [bookings, setBookings] = useState([])
  const [processing, setProcessing] = useState(null)
  const [modalBookingId, setModalBookingId] = useState(null)
  const [downloadProcessing, setDownloadProcessing] = useState(null)
  const navigate = useNavigate()

  useEffect(()=>{
    const token = getToken()
    if (!token) return navigate('/login')
    fetchBookings().then(setBookings).catch(()=>setBookings([]))
  }, [])

  async function downloadTicket(b){
    try{
      setDownloadProcessing(b.id)
      const ticket = await api(`/tickets/${b.id}`)
      const content = `Ticket #${b.id}\nTicket number: ${ticket.ticket_number}\nFlight: ${ticket.flight_number}\nFrom: ${ticket.source} → ${ticket.destination}\nDeparture: ${new Date(ticket.departure_time).toLocaleString()}\nSeat: ${ticket.seat_number}\nPassenger: ${ticket.passenger_email}\n`
      const blob = new Blob([content], {type: 'text/plain'})
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `ticket_${b.id}.txt`
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)
    }catch(err){
      alert('Download failed: ' + err.message)
    }finally{
      setDownloadProcessing(null)
    }
  }

  return (
    <div className="max-w-5xl mx-auto py-10">
      <h2 className="text-2xl font-semibold mb-4">Your Bookings</h2>
      {bookings.length === 0 ? (
        <div className="card">You have no bookings yet. Search flights to book.</div>
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="text-sm text-slate-600">
                <th className="py-2">Booking #</th>
                <th className="py-2">Flight</th>
                <th className="py-2">Seat</th>
                <th className="py-2">Date</th>
                <th className="py-2">Status</th>
                <th className="py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {bookings.map(b=> (
                <tr key={b.id} className="border-t">
                  <td className="py-2">#{b.id}</td>
                  <td className="py-2">{b.flight_number} <div className="text-xs text-slate-500">{b.origin} → {b.destination}</div></td>
                  <td className="py-2">{b.seat_id}</td>
                  <td className="py-2">{new Date(b.booked_at).toLocaleString()}</td>
                  <td className="py-2">{b.payment_status}</td>
                  <td className="py-2">
                    <a href={`/flights/${b.flight_id}`} className="text-emerald-600 mr-3">View flight</a>
                    {b.payment_status === 'PAID' ? (
                      <button disabled={downloadProcessing === b.id} onClick={()=>downloadTicket(b)} className="text-slate-600">{downloadProcessing === b.id ? 'Downloading...' : 'Download ticket'}</button>
                    ) : (
                      <>
                        <button disabled={processing === b.id} onClick={()=>{
                          setProcessing(b.id)
                          setModalBookingId(b.id)
                        }} className="text-emerald-600">Pay</button>
                        <CheckoutModal isOpen={modalBookingId === b.id} bookingId={b.id} onClose={() => { setModalBookingId(null); setProcessing(null) }} onPaid={() => { fetchBookings().then(setBookings).catch(()=>setBookings([])) }} />
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
