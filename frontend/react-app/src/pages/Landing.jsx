import React from 'react'
import hero from '../assets/hero.jpg'
// Note: hero.jpg is a placeholder image; replace with preferred image assets
import { Link } from 'react-router-dom'

export default function Landing(){
  return (
    <div className="max-w-5xl mx-auto py-16">
      <div className="grid md:grid-cols-2 gap-6 items-center">
        <div>
          <h1 className="text-4xl font-bold">Fly easy — book in minutes</h1>
          <p className="mt-4 text-slate-600">Search flights, pick seats, and manage bookings with ease.</p>
          <div className="mt-6">
            <Link to="/flights" className="inline-block bg-emerald-500 text-white px-5 py-2 rounded">Search Flights</Link>
            <Link to="/login" className="ml-4 inline-block text-emerald-600">Login</Link>
          </div>

          <div className="mt-8 p-4 bg-slate-50 rounded">
            <h3 className="font-semibold">Why choose Airline Reservation System?</h3>
            <ul className="mt-2 text-sm text-slate-600 list-disc list-inside">
              <li>Competitive fares and transparent pricing</li>
              <li>Quick booking flow — find and reserve in minutes</li>
              <li>Secure payments and easy ticket downloads</li>
              <li>24/7 customer support and flexible cancellations</li>
            </ul>
          </div>
        </div>
        <div>
          <img src={hero} alt="airline" className="rounded-lg shadow" />
        </div>
      </div>

      <footer className="mt-12 border-t pt-6 text-sm text-slate-600">
        <div className="flex flex-col md:flex-row md:justify-between items-start md:items-center gap-4">
          <div>
            <div className="font-semibold">Airline Reservation System</div>
            <div className="text-xs">Simple booking, secure payments, and instant tickets.</div>
          </div>
          <div className="flex gap-4 items-center">
            <Link to="/about" className="text-emerald-600">About</Link>
            <Link to="/contact" className="text-emerald-600">Contact</Link>
            <Link to="/privacy" className="text-emerald-600">Privacy</Link>
          </div>
        </div>
        <div className="mt-4 text-xs text-slate-500">© {new Date().getFullYear()} Airline Reservation System. All rights reserved.</div>
      </footer>
    </div>
  )
}
