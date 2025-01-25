import React, { useState, useEffect } from "react";
import api from "../../api/api";

function NoteForm({ note, onSubmit }) {
  const [header, setHeader] = useState("");
  const [body, setBody] = useState("");

  useEffect(() => {
    if (note) {
      setHeader(note.header);
      setBody(note.body);
    }
  }, [note]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitting note form");

    const payload = { header, body, user_id: localStorage.getItem("userId") };
    console.log("Payload:", payload);
    try {
      if (note) {
        // Editing existing note
        console.log("Updating note:", note._id);
        await api.put(`/notes/${note._id}`, payload);
      } else {
        // Creating a new note
        console.log("Creating new note");
        await api.post("/notes", payload);
      }
      onSubmit(); // Callback to refresh the notes list
    } catch (error) {
      console.error("Error saving note:", error);
    }
  };

  return (
    <div>
      <h2>{note ? "Edit Note" : "New Note"}</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Header"
          value={header}
          onChange={(e) => setHeader(e.target.value)}
          required
        />
        <textarea
          placeholder="Body"
          value={body}
          onChange={(e) => setBody(e.target.value)}
          rows="5"
          required
        />
        <button type="submit">{note ? "Update Note" : "Create Note"}</button>
      </form>
    </div>
  );
}

export default NoteForm;
