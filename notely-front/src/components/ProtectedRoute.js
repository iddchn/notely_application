import React from "react";
import { Navigate } from "react-router-dom";
import { isLoggedIn } from "../auth";

function ProtectedRoute({ children }) {
  return isLoggedIn() ? children : <Navigate to="/login" replace />;
}

export default ProtectedRoute;
