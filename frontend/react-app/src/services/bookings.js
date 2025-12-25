import api from '../api'

export async function fetchBookings(){
  return api('/bookings/me')
}

export default {fetchBookings}
