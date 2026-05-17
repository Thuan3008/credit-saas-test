import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";

function Packages() {
  const [packages, setPackages] = useState([]);
  const [message, setMessage] = useState("");

  const fetchPackages = async () => {
    try {
      const res = await axiosClient.get("/api/packages");
      setPackages(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const buyPackage = async (packageId) => {
    setMessage("");

    try {
      const res = await axiosClient.post(`/api/purchases/${packageId}`);
      setMessage(
        `Purchase successful! Added ${res.data.credits_added} credits. Current balance: ${res.data.current_balance}`
      );
    } catch (err) {
      setMessage(err.response?.data?.detail || "Purchase failed");
    }
  };

  useEffect(() => {
    fetchPackages();
  }, []);

  return (
    <div className="p-8 bg-slate-100 min-h-[90vh]">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">
          Credit Packages
        </h1>

        {message && (
          <div className="bg-blue-100 text-blue-700 p-4 rounded-xl mb-6">
            {message}
          </div>
        )}

        <div className="grid md:grid-cols-3 gap-6">
          {packages.map((pkg) => (
            <div
              key={pkg.id}
              className="bg-white p-6 rounded-2xl shadow flex flex-col"
            >
              <h2 className="text-2xl font-bold mb-2">
                {pkg.name}
              </h2>

              <p className="text-slate-500 mb-4">
                {pkg.description}
              </p>

              <p className="text-3xl font-bold text-blue-600 mb-2">
                ${pkg.price}
              </p>

              <p className="mb-4">
                <strong>{pkg.credits}</strong> credits
              </p>

              <div className="mb-6">
                <h3 className="font-semibold mb-2">
                  Features:
                </h3>

                <ul className="space-y-1">
                  {pkg.features.map((feature) => (
                    <li key={feature.id} className="text-sm">
                      ✅ {feature.name}
                    </li>
                  ))}
                </ul>
              </div>

              <button
                onClick={() => buyPackage(pkg.id)}
                className="mt-auto bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
              >
                Buy Now
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Packages;