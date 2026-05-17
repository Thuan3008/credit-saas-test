import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";

function Dashboard() {
  const user = JSON.parse(localStorage.getItem("user") || "null");

  const [credits, setCredits] = useState(0);
  const [features, setFeatures] = useState([]);
  const [message, setMessage] = useState("");

  const fetchDashboard = async () => {
    try {
      const creditRes = await axiosClient.get("/api/users/me/credits");
      const featureRes = await axiosClient.get("/api/users/me/features");

      setCredits(creditRes.data.balance);
      setFeatures(featureRes.data);
    } catch (err) {
      console.error(err);
    }
  };

  const useFeature = async (endpoint) => {
    setMessage("");

    try {
      const res = await axiosClient.post(`/api/feature-usage/${endpoint}`);
      setMessage(res.data.message);
    } catch (err) {
      setMessage(err.response?.data?.detail || "Feature failed");
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  return (
    <div className="p-8 bg-slate-100 min-h-[90vh]">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">
          Dashboard
        </h1>

        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div className="bg-white p-6 rounded-2xl shadow">
            <h2 className="text-xl font-semibold mb-2">
              User Info
            </h2>
            <p>
              <strong>Email:</strong> {user?.email}
            </p>
            <p>
              <strong>Role:</strong> {user?.role}
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow">
            <h2 className="text-xl font-semibold mb-2">
              Current Credits
            </h2>
            <p className="text-4xl font-bold text-blue-600">
              {credits}
            </p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow mb-6">
          <h2 className="text-xl font-semibold mb-4">
            Unlocked Features
          </h2>

          {features.length === 0 ? (
            <p className="text-slate-500">
              You have not unlocked any features yet.
            </p>
          ) : (
            <div className="flex flex-wrap gap-3">
              {features.map((feature) => (
                <span
                  key={feature.id}
                  className="bg-green-100 text-green-700 px-3 py-1 rounded-full"
                >
                  {feature.name}
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="bg-white p-6 rounded-2xl shadow">
          <h2 className="text-xl font-semibold mb-4">
            Test Feature Permission
          </h2>

          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => useFeature("generate-image")}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Use Generate Image
            </button>

            <button
              onClick={() => useFeature("auto-post")}
              className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700"
            >
              Use Auto Post
            </button>

            <button
              onClick={() => useFeature("advanced-analytics")}
              className="bg-slate-800 text-white px-4 py-2 rounded-lg hover:bg-slate-900"
            >
              Use Advanced Analytics
            </button>
          </div>

          {message && (
            <div className="mt-4 bg-slate-100 p-3 rounded">
              {message}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;