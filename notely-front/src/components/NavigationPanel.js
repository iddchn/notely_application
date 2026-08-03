import React from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { isLoggedIn, logout } from "../auth";

function NavigationPanel() {
  const navigate = useNavigate();
  // Re-render on every route change so the auth state is re-read after
  // login/logout navigations.
  useLocation();
  const loggedIn = isLoggedIn();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <Link to={loggedIn ? "/notes" : "/login"} className="navbar-brand">
        📝 Notely
      </Link>
      <div className="navbar-links">
        {loggedIn ? (
          <>
            <Link to="/notes" className="navbar-link">Notes</Link>
            <Link to="/profile" className="navbar-link">Profile</Link>
            <button type="button" className="btn btn-logout" onClick={handleLogout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="navbar-link">Login</Link>
            <Link to="/signup" className="navbar-link">Signup</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default NavigationPanel;
