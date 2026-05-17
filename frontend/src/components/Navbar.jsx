import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");
  const user = JSON.parse(localStorage.getItem("user") || "null");

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <nav className="bg-slate-900 text-white px-6 py-4 flex justify-between items-center">
      <Link to="/" className="text-xl font-bold">
        Credit SaaS
      </Link>

      <div className="flex items-center gap-4">
        {token ? (
          <>
            <Link to="/dashboard" className="hover:text-blue-300">
              Dashboard
            </Link>

            <Link to="/packages" className="hover:text-blue-300">
              Packages
            </Link>

            <Link to="/history" className="hover:text-blue-300">
              History
            </Link>

            {user?.role === "admin" && (
              <Link to="/admin/packages" className="hover:text-blue-300">
                Admin
              </Link>
            )}

            <span className="text-sm text-slate-300">
              {user?.email}
            </span>

            <button
              onClick={handleLogout}
              className="bg-red-500 px-3 py-1 rounded hover:bg-red-600"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:text-blue-300">
              Login
            </Link>
            <Link to="/register" className="hover:text-blue-300">
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;