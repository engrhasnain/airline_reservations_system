const API_BASE = '/api';

async function getJSON(path) {
  const res = await fetch(API_BASE + path);
  return res.json();
}

export { getJSON };
