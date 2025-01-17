import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./components/Auth/Login";
import Signup from "./components/Auth/Signup";
import NotesList from "./components/Notes/NotesList";
import Profile from "./components/User/Profile";
import NavigationPanel from "./components/NavigationPanel";

function App() {
  return (
    <BrowserRouter>
      <NavigationPanel />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/notes" element={<NotesList />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
