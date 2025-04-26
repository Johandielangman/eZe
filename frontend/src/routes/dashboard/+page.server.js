// +page.server.js
import { kindeAuthClient } from '@kinde-oss/kinde-auth-sveltekit';

export async function load({ fetch, request }) {
  const access_token = await kindeAuthClient.getToken(request);

  const response = await fetch('http://127.0.0.1:8000/kinde', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${access_token}`
    }
  });

  const data = await response.text();

  return {
    pingResponse: data
  };
}
