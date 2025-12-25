import React from 'react'

export default function Contact(){
  return (
    <div className="max-w-5xl mx-auto py-10">
      <div className="card">
        <h2 className="text-2xl font-semibold">Contact Us</h2>
        <p className="mt-4 text-slate-600">Need help? Reach us at <a href="mailto:support@example.com" className="text-emerald-600">support@example.com</a> or call <span className="font-medium">1-800-555-0100</span>.</p>
        <p className="mt-2 text-slate-600">For partnership inquiries, please use the same contact email.</p>
      </div>
    </div>
  )
}