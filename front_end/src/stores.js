import { writable } from 'svelte/store';

export const FLAVOR_CUISINE_URL = 'http://localhost:8000';
export let authToken = writable(0);

export async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST',
    mode: 'cors',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  })

  let result = await response.json().then(data => ({
    data:data,
    status:response.status,
  })); // parses JSON response into native JavaScript objects
  
  return result
}

export async function getData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'GET',
    mode: 'cors',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
  })

  let result = await response.json().then(data => ({
    data:data,
    status:response.status,
  })); // parses JSON response into native JavaScript objects
  
  return result
}

// export async function getData(url = '', opts) {
//   let response = await fetch(url, {
//     method: 'GET',
//     mode: 'cors',
//     credentials: 'same-origin',
//     redirect: 'follow', // manual, *follow, error
//     referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
//   });

//   for (const field of opts) {
//     const [key, val] = field
//     response[key] = val
//   }
//   let result = await response.json().then(data => ({
//     data:data,
//     status:response.status,
//   })); // parses JSON response into native JavaScript objects
  
//   return result
// }
