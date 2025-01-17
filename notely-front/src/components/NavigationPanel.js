import React from "react";
import { Link } from "react-router-dom";

function NavigationPanel() {
  return (
    <nav style={styles.nav}>
      <Link to="/login" style={styles.link}>
        Login
      </Link>
      <Link to="/signup" style={styles.link}>
        Signup
      </Link>
    </nav>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "center",
    gap: "20px",
    padding: "10px",
    backgroundColor: "#f4f4f9",
    borderBottom: "1px solid #ccc",
  },
  link: {
    textDecoration: "none",
    fontSize: "18px",
    color: "#007bff",
  },
};

export default NavigationPanel;
