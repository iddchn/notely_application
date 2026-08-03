import { PublicClientApplication } from "@azure/msal-browser";

// Entra app registration identifiers — public values, not secrets.
const TENANT_ID = "504483c6-ab3b-408a-b4d3-152fa58976df";
const CLIENT_ID = "9c775da3-1c31-4ab4-9940-76d45b7d9a71";

export const msalInstance = new PublicClientApplication({
  auth: {
    clientId: CLIENT_ID,
    authority: `https://login.microsoftonline.com/${TENANT_ID}`,
    redirectUri: window.location.origin,
  },
  cache: {
    cacheLocation: "localStorage",
  },
});

export const loginRequest = {
  scopes: ["openid", "profile", "email"],
};
