import React, { useState } from 'react'
import { pay } from '../api'

export default function CheckoutModal({ isOpen, onClose, bookingId, defaultAmount = 100, onPaid }){
  const [amount, setAmount] = useState(defaultAmount)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  if (!isOpen) return null

  async function handlePay(){
    setLoading(true)
    setError(null)
    try{
      await pay(bookingId, parseInt(amount, 10))
      setLoading(false)
      onPaid && onPaid()
      onClose()
    }catch(err){
      setError(err.message || 'Payment failed')
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded p-6 w-full max-w-md">
        <h3 className="text-lg font-semibold mb-2">Complete Payment</h3>
        <div className="text-sm text-slate-600 mb-4">Booking #{bookingId}</div>
        <div className="mb-4">
          <label className="block text-sm text-slate-700 mb-1">Amount (USD)</label>
          <input type="number" value={amount} onChange={e=>setAmount(e.target.value)} className="w-full border p-2 rounded" />
        </div>
        {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
        <div className="flex justify-end gap-2">
          <button onClick={onClose} className="px-4 py-2 rounded border">Cancel</button>
          <button onClick={handlePay} disabled={loading} className="px-4 py-2 bg-emerald-500 text-white rounded">{loading ? 'Processing...' : 'Pay'}</button>
        </div>
      </div>
    </div>
  )
}
