import React, { useState } from "react";
import { useNavigate } from "react-router";
import api from "../../api/api";
import { msalInstance, loginRequest } from "../../authConfig";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/user/login", { email, password });
      localStorage.setItem("userId", response.data.user_id);
      navigate("/notes");
    } catch (error) {
      alert("Invalid credentials");
    }
  };

  const handleSsoLogin = async () => {
    try {
      const result = await msalInstance.loginPopup(loginRequest);
      const response = await api.post(
        "/user/sso-login",
        {},
        { headers: { Authorization: `Bearer ${result.idToken}` } }
      );
      localStorage.setItem("userId", response.data.user_id);
      navigate("/notes");
    } catch (error) {
      alert("Microsoft sign-in failed");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Login</button>
      </form>
      <button type="button" onClick={handleSsoLogin}>Sign in with Microsoft</button>
    </div>
  );
}

export default Login;
