import { getJSON } from './api.js'

export async function listFlights() {
  return getJSON('/flights')
}
