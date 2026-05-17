import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axiosClient from "../api/axiosClient";

function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
    full_name: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await axiosClient.post("/api/auth/register", form);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Register failed");
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center bg-slate-100">
      <div className="bg-white w-full max-w-md p-8 rounded-2xl shadow">
        <h1 className="text-2xl font-bold mb-6 text-center">
          Register
        </h1>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block mb-1 font-medium">
              Full name
            </label>
            <input
              name="full_name"
              value={form.full_name}
              onChange={handleChange}
              className="w-full border rounded-lg px-3 py-2"
              placeholder="Normal User"
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">
              Email
            </label>
            <input
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              className="w-full border rounded-lg px-3 py-2"
              placeholder="user@example.com"
              required
            />
          </div>

          <div>
            <label className="block mb-1 font-medium">
              Password
            </label>
            <input
              name="password"
              type="password"
              value={form.password}
              onChange={handleChange}
              className="w-full border rounded-lg px-3 py-2"
              placeholder="123456"
              required
            />
          </div>

          <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700">
            Register
          </button>
        </form>

        <p className="text-center mt-4 text-sm">
          Already have account?{" "}
          <Link to="/login" className="text-blue-600">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}

export default Register;