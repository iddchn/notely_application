// The logged-in "token" is the userId stored by Login (classic or SSO).
// Logout only clears the app session; the MSAL cache is left so the next
// Microsoft sign-in is one click.
export function isLoggedIn() {
  return !!localStorage.getItem("userId");
}

export function logout() {
  localStorage.removeItem("userId");
}
