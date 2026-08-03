import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Auth/Login";
import Signup from "./components/Auth/Signup";
import NotesList from "./components/Notes/NotesList";
import Profile from "./components/User/Profile";
import NavigationPanel from "./components/NavigationPanel";
import ProtectedRoute from "./components/ProtectedRoute";
import { isLoggedIn } from "./auth";

function RedirectIfAuthed({ children }) {
  return isLoggedIn() ? <Navigate to="/notes" replace /> : children;
}

function App() {
  return (
    <BrowserRouter>
      <NavigationPanel />
      <Routes>
        <Route path="/" element={<RedirectIfAuthed><Login /></RedirectIfAuthed>} />
        <Route path="/login" element={<RedirectIfAuthed><Login /></RedirectIfAuthed>} />
        <Route path="/signup" element={<RedirectIfAuthed><Signup /></RedirectIfAuthed>} />
        <Route path="/notes" element={<ProtectedRoute><NotesList /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
