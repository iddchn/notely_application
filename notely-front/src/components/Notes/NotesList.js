import React, { useEffect, useState } from "react";
import api from "../../api/api";
import NoteForm from "./NoteForm";
import "../../styles/Notes.css";

function NotesList() {
  const [notes, setNotes] = useState([]);
  const [selectedNote, setSelectedNote] = useState(null); // For editing
  const [showForm, setShowForm] = useState(false); // Toggle form
  const userId = localStorage.getItem("userId");

  useEffect(() => {
    fetchNotes();
  }, [userId]);

  const fetchNotes = async () => {
    try {
      const response = await api.get(`/notes/all/${userId}`);
      setNotes(response.data);
    } catch (error) {
      console.error("Error fetching notes:", error);
    }
  };

  const handleCreateNote = () => {
    setSelectedNote(null);
    setShowForm(true);
  };

  const handleEditNote = (note) => {
    setSelectedNote(note);
    setShowForm(true);
  };

  const handleDeleteNote = async (noteId) => {
    try {
      await api.delete(`/notes/${noteId}`);
      fetchNotes();
    } catch (error) {
      console.error("Error deleting note:", error);
    }
  };

  const handleFormSubmit = () => {
    fetchNotes();
    setShowForm(false);
  };

  return (
    <div className="notes-page">
      <div className="notes-header">
        <h2>Your Notes</h2>
        <button onClick={handleCreateNote}>+ New Note</button>
      </div>
      {showForm && (
        <NoteForm note={selectedNote} onSubmit={handleFormSubmit} />
      )}
      <div className="notes-container">
        {notes.length === 0 && !showForm && (
          <div className="empty-state">No notes yet — create your first one!</div>
        )}
        {notes.map((note) => (
          <div key={note._id} className="note-card">
            <h3>{note.header}</h3>
            <p>{note.body}</p>
            <small>{new Date(note.created_at).toLocaleString()}</small>
            <div className="note-actions">
              <button className="btn-secondary" onClick={() => handleEditNote(note)}>Edit</button>
              <button className="btn-danger" onClick={() => handleDeleteNote(note._id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default NotesList;