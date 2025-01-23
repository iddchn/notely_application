import axios from "axios";

const api = axios.create({
  baseURL: "http://notely-flask.notely.svc.cluster.local:5001",
  headers: {
    "Content-Type": "application/json",
  }
});

export default api;
