import axios from "axios";

const api = axios.create({
  baseURL:
    process.env.NEXT_PUBLIC_API_BASE_URL ||
    (typeof window === "undefined" ? "http://localhost:5000" : ""),
  withCredentials: false,
});

export default api;
