import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";

function History() {
  const [transactions, setTransactions] = useState([]);

  const fetchHistory = async () => {
    try {
      const res = await axiosClient.get("/api/purchases/history");
      setTransactions(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="p-8 bg-slate-100 min-h-[90vh]">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">
          Purchase History
        </h1>

        <div className="bg-white rounded-2xl shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-slate-900 text-white">
              <tr>
                <th className="p-3 text-left">ID</th>
                <th className="p-3 text-left">Package ID</th>
                <th className="p-3 text-left">Amount</th>
                <th className="p-3 text-left">Credits</th>
                <th className="p-3 text-left">Status</th>
                <th className="p-3 text-left">Created At</th>
              </tr>
            </thead>

            <tbody>
              {transactions.map((item) => (
                <tr key={item.id} className="border-b">
                  <td className="p-3">{item.id}</td>
                  <td className="p-3">{item.package_id}</td>
                  <td className="p-3">${item.amount}</td>
                  <td className="p-3">{item.credits}</td>
                  <td className="p-3">
                    <span className="bg-green-100 text-green-700 px-2 py-1 rounded">
                      {item.status}
                    </span>
                  </td>
                  <td className="p-3">
                    {new Date(item.created_at).toLocaleString()}
                  </td>
                </tr>
              ))}

              {transactions.length === 0 && (
                <tr>
                  <td colSpan="6" className="p-6 text-center text-slate-500">
                    No transactions yet.
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

export default History;