import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";

function AdminPackages() {
  const [features, setFeatures] = useState([]);
  const [packages, setPackages] = useState([]);

  const [featureForm, setFeatureForm] = useState({
    code: "",
    name: "",
    description: "",
  });

  const [packageForm, setPackageForm] = useState({
    name: "",
    description: "",
    price: "",
    credits: "",
    feature_ids: [],
  });

  const [message, setMessage] = useState("");

  const fetchData = async () => {
    try {
      const featureRes = await axiosClient.get("/api/features");
      const packageRes = await axiosClient.get("/api/packages/admin");

      setFeatures(featureRes.data);
      setPackages(packageRes.data);
    } catch (err) {
      setMessage(err.response?.data?.detail || "Failed to load admin data");
    }
  };

  const createFeature = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      await axiosClient.post("/api/features", featureForm);

      setFeatureForm({
        code: "",
        name: "",
        description: "",
      });

      setMessage("Feature created successfully");
      fetchData();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Create feature failed");
    }
  };

  const handlePackageChange = (e) => {
    setPackageForm({
      ...packageForm,
      [e.target.name]: e.target.value,
    });
  };

  const toggleFeatureId = (featureId) => {
    const existed = packageForm.feature_ids.includes(featureId);

    if (existed) {
      setPackageForm({
        ...packageForm,
        feature_ids: packageForm.feature_ids.filter((id) => id !== featureId),
      });
    } else {
      setPackageForm({
        ...packageForm,
        feature_ids: [...packageForm.feature_ids, featureId],
      });
    }
  };

  const createPackage = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      await axiosClient.post("/api/packages", {
        ...packageForm,
        price: Number(packageForm.price),
        credits: Number(packageForm.credits),
      });

      setPackageForm({
        name: "",
        description: "",
        price: "",
        credits: "",
        feature_ids: [],
      });

      setMessage("Package created successfully");
      fetchData();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Create package failed");
    }
  };

  const deletePackage = async (packageId) => {
    try {
      await axiosClient.delete(`/api/packages/${packageId}`);
      setMessage("Package deleted successfully");
      fetchData();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Delete package failed");
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="p-8 bg-slate-100 min-h-[90vh]">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">
          Admin Management
        </h1>

        {message && (
          <div className="bg-blue-100 text-blue-700 p-4 rounded-xl mb-6">
            {message}
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white p-6 rounded-2xl shadow">
            <h2 className="text-xl font-bold mb-4">
              Create Feature
            </h2>

            <form onSubmit={createFeature} className="space-y-3">
              <input
                value={featureForm.code}
                onChange={(e) =>
                  setFeatureForm({ ...featureForm, code: e.target.value })
                }
                placeholder="Code: generate_image"
                className="w-full border rounded-lg px-3 py-2"
                required
              />

              <input
                value={featureForm.name}
                onChange={(e) =>
                  setFeatureForm({ ...featureForm, name: e.target.value })
                }
                placeholder="Name: Generate Image"
                className="w-full border rounded-lg px-3 py-2"
                required
              />

              <textarea
                value={featureForm.description}
                onChange={(e) =>
                  setFeatureForm({
                    ...featureForm,
                    description: e.target.value,
                  })
                }
                placeholder="Description"
                className="w-full border rounded-lg px-3 py-2"
              />

              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg">
                Create Feature
              </button>
            </form>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow">
            <h2 className="text-xl font-bold mb-4">
              Create Package
            </h2>

            <form onSubmit={createPackage} className="space-y-3">
              <input
                name="name"
                value={packageForm.name}
                onChange={handlePackageChange}
                placeholder="Package name"
                className="w-full border rounded-lg px-3 py-2"
                required
              />

              <input
                name="description"
                value={packageForm.description}
                onChange={handlePackageChange}
                placeholder="Description"
                className="w-full border rounded-lg px-3 py-2"
              />

              <input
                name="price"
                type="number"
                value={packageForm.price}
                onChange={handlePackageChange}
                placeholder="Price"
                className="w-full border rounded-lg px-3 py-2"
                required
              />

              <input
                name="credits"
                type="number"
                value={packageForm.credits}
                onChange={handlePackageChange}
                placeholder="Credits"
                className="w-full border rounded-lg px-3 py-2"
                required
              />

              <div>
                <p className="font-medium mb-2">
                  Select Features
                </p>

                <div className="flex flex-wrap gap-2">
                  {features.map((feature) => (
                    <label
                      key={feature.id}
                      className="border rounded-lg px-3 py-1 cursor-pointer"
                    >
                      <input
                        type="checkbox"
                        checked={packageForm.feature_ids.includes(feature.id)}
                        onChange={() => toggleFeatureId(feature.id)}
                        className="mr-2"
                      />
                      {feature.name}
                    </label>
                  ))}
                </div>
              </div>

              <button className="bg-green-600 text-white px-4 py-2 rounded-lg">
                Create Package
              </button>
            </form>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow">
          <h2 className="text-xl font-bold mb-4">
            Packages
          </h2>

          <table className="w-full">
            <thead className="bg-slate-900 text-white">
              <tr>
                <th className="p-3 text-left">ID</th>
                <th className="p-3 text-left">Name</th>
                <th className="p-3 text-left">Price</th>
                <th className="p-3 text-left">Credits</th>
                <th className="p-3 text-left">Active</th>
                <th className="p-3 text-left">Action</th>
              </tr>
            </thead>

            <tbody>
              {packages.map((pkg) => (
                <tr key={pkg.id} className="border-b">
                  <td className="p-3">{pkg.id}</td>
                  <td className="p-3">{pkg.name}</td>
                  <td className="p-3">${pkg.price}</td>
                  <td className="p-3">{pkg.credits}</td>
                  <td className="p-3">{pkg.is_active ? "Yes" : "No"}</td>
                  <td className="p-3">
                    {pkg.is_active && (
                      <button
                        onClick={() => deletePackage(pkg.id)}
                        className="bg-red-500 text-white px-3 py-1 rounded"
                      >
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))}

              {packages.length === 0 && (
                <tr>
                  <td colSpan="6" className="p-6 text-center text-slate-500">
                    No packages.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default AdminPackages;