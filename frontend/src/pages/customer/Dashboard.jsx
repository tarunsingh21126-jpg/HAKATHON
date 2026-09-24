import { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import api from '../../api/axios';
import { Package, CheckCircle2, RotateCcw } from 'lucide-react';

export default function CustomerDashboard() {
  const { user } = useAuth();
  const [containers, setContainers] = useState([]);
  const [rewards, setRewards] = useState({ balance: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [containersRes, rewardsRes] = await Promise.all([
          api.get('/containers/'),
          api.get('/rewards/')
        ]);
        setContainers(containersRes.data.results || containersRes.data);
        setRewards(rewardsRes.data);
      } catch (error) {
        console.error("Error fetching dashboard data", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleReturn = async (containerId) => {
    try {
      await api.post('/returns/', {
        container: containerId,
        method: 'dropoff' // default method
      });
      // Refresh data
      const [containersRes, rewardsRes] = await Promise.all([
        api.get('/containers/'),
        api.get('/rewards/')
      ]);
      setContainers(containersRes.data.results || containersRes.data);
      setRewards(rewardsRes.data);
      alert('Return requested successfully!');
    } catch (err) {
      console.error(err);
      alert('Failed to request return');
    }
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;

  const activeContainers = containers.filter(c => ['assigned', 'delivered'].includes(c.status));
  const returnedContainers = containers.filter(c => ['return_requested', 'pickup_assigned', 'collected', 'completed'].includes(c.status));

  return (
    <div className="max-w-4xl mx-auto space-y-8 mt-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-slate-900">Welcome, {user?.name?.split(' ')[0]}</h1>
        <div className="bg-brand-50 text-brand-700 px-4 py-2 rounded-lg font-medium border border-brand-100 flex items-center gap-2">
          <span>⭐️</span> {rewards.balance} Points
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Active Packaging */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="border-b border-slate-100 bg-slate-50 px-6 py-4 font-semibold text-slate-700 flex items-center gap-2">
            <Package className="w-5 h-5" /> Active Packaging
          </div>
          <div className="p-6 space-y-4">
            {activeContainers.length === 0 ? (
              <p className="text-slate-500 text-sm text-center py-4">No active packaging right now.</p>
            ) : (
              activeContainers.map(container => (
                <div key={container.id} className="border border-slate-100 rounded-xl p-4 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold font-mono text-slate-800">{container.container_code}</h3>
                    <span className="text-xs font-medium bg-blue-50 text-blue-600 px-2.5 py-1 rounded-full">
                      {container.status.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-sm text-slate-500 mb-4">Deposit: ₹{container.deposit_amount}</p>
                  <button 
                    onClick={() => handleReturn(container.id)}
                    className="w-full bg-brand-600 text-white font-medium py-2 rounded-lg hover:bg-brand-700 transition-colors flex items-center justify-center gap-2">
                    <RotateCcw className="w-4 h-4" /> Return Packaging
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Return History */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="border-b border-slate-100 bg-slate-50 px-6 py-4 font-semibold text-slate-700 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-green-600" /> Return History
          </div>
          <div className="p-6">
             {returnedContainers.length === 0 ? (
              <p className="text-slate-500 text-sm text-center py-4">No return history yet.</p>
            ) : (
              <div className="space-y-3">
                {returnedContainers.slice(0, 5).map(container => (
                  <div key={container.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100">
                    <span className="font-mono text-sm font-medium">{container.container_code}</span>
                    <span className="text-xs text-brand-600 font-medium flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" /> Returned
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
