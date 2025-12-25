const TOKEN_KEY = 'ARS_TOKEN'

export function setToken(token){
  localStorage.setItem(TOKEN_KEY, token)
  // notify other components in this window
  window.dispatchEvent(new Event('auth:change'))
}
export function getToken(){
  return localStorage.getItem(TOKEN_KEY)
}

export function getCurrentUser(){
  const token = getToken()
  if (!token) return null
  try{
    const payload = token.split('.')[1]
    // base64 url -> base64
    const b64 = payload.replace(/-/g, '+').replace(/_/g, '/')
    const json = JSON.parse(atob(b64))
    return json
  }catch(e){
    return null
  }
}
export function logout(){
  localStorage.removeItem(TOKEN_KEY)
  window.dispatchEvent(new Event('auth:change'))
}
