import React, { useState } from "react";
import api from "../../api/api";

function Profile() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const userId = localStorage.getItem("userId");

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await api.put("/user", { id: userId, name, email, password });
      alert("Profile updated successfully");
    } catch (error) {
      alert("Profile update failed");
    }
  };

  return (
    <div>
      <h2>Update Profile</h2>
      <form onSubmit={handleUpdate}>
        <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Update</button>
      </form>
    </div>
  );
}

export default Profile;
