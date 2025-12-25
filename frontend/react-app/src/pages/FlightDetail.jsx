import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../api'
import CheckoutModal from '../components/CheckoutModal'
import { fetchBookings } from '../services/bookings'

export default function FlightDetail(){
  const { id } = useParams()
  const [flight, setFlight] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [modalBookingId, setModalBookingId] = useState(null)
  const [userBooking, setUserBooking] = useState(null)
  const navigate = useNavigate()

  useEffect(()=>{
    api(`/flights/${id}`).then(setFlight).catch(()=>setFlight(null))
  }, [id])

  useEffect(()=>{
    async function checkBooking(){
      try{
        const bookings = await fetchBookings()
        const b = bookings?.find(x => x.flight_id === flight.id)
        setUserBooking(b || null)
      }catch(err){
        setUserBooking(null)
      }
    }
    if (flight) checkBooking()
  }, [flight])

  if (!flight) return <div className="max-w-5xl mx-auto py-10">Flight not found.</div>

  return (
    <div className="max-w-5xl mx-auto py-10">
      <div className="card">
        <h2 className="text-2xl font-semibold">Flight {flight.flight_number}</h2>
        <div className="mt-3 grid grid-cols-2 gap-4">
          <div>
            <div className="text-sm text-slate-600">Route</div>
            <div className="font-medium">{flight.origin} → {flight.destination}</div>

            <div className="mt-3 text-sm text-slate-600">Departure</div>
            <div className="font-medium">{new Date(flight.departure_time).toLocaleString()}</div>

            <div className="mt-3 text-sm text-slate-600">Arrival</div>
            <div className="font-medium">{new Date(flight.arrival_time).toLocaleString()}</div>
          </div>
          <div>
            <div className="text-sm text-slate-600">Seats</div>
            <div className="font-medium">Total: {flight.total_seats}</div>
            <div className="font-medium">Available: {flight.seats_available}</div>
            <div className="mt-4">
              {userBooking ? (
                <div className="text-slate-600">You already have a booking for this flight (#{userBooking.id}).</div>
              ) : (
                <button disabled={processing} onClick={async()=>{
                  try{
                    setProcessing(true)
                    const booking = await api('/bookings/', {method:'POST', body: JSON.stringify({flight_id: flight.id})})
                    alert('Booking created: #' + booking.id)
                    // open checkout modal
                    setModalBookingId(booking.id)
                  }catch(err){
                    alert('Booking failed: ' + err.message)
                  }finally{
                    setProcessing(false)
                  }
                }} className="bg-emerald-500 text-white px-4 py-2 rounded">{processing ? 'Booking...' : 'Book this flight'}</button>
              )}
              <CheckoutModal isOpen={!!modalBookingId} bookingId={modalBookingId} onClose={() => { setModalBookingId(null); navigate('/dashboard') }} onPaid={() => { navigate('/dashboard') }} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
