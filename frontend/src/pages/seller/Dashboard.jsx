import { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import api from '../../api/axios';
import { Package, Plus, ShoppingCart } from 'lucide-react';

export default function SellerDashboard() {
  const { user } = useAuth();
  const [containers, setContainers] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Form states
  const [depositAmount, setDepositAmount] = useState(100);
  const [condition, setCondition] = useState('excellent');
  
  const [selectedContainer, setSelectedContainer] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState('');

  const fetchData = async () => {
    try {
      setLoading(true);
      const [containersRes, usersRes] = await Promise.all([
        api.get('/containers/'),
        api.get('/auth/users/')
      ]);
      setContainers(containersRes.data.results || containersRes.data);
      const allUsers = usersRes.data.results || usersRes.data;
      setCustomers(allUsers.filter(u => u.role === 'customer'));
    } catch (error) {
      console.error("Error fetching data", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreatePackage = async (e) => {
    e.preventDefault();
    try {
      await api.post('/containers/', {
        seller: user?.seller_profile?.id,
        deposit_amount: depositAmount,
        condition: condition,
        notes: 'Created via dashboard'
      });
      alert('Package created successfully!');
      fetchData();
    } catch (err) {
      console.error(err);
      alert('Failed to create package');
    }
  };

  const [customerAddress, setCustomerAddress] = useState('');

  const handleSellPackage = async (e) => {
    e.preventDefault();
    if (!selectedContainer || !selectedCustomer || !customerAddress) {
      alert('Please fill out all fields.');
      return;
    }
    try {
      await api.post('/orders/', {
        customer: selectedCustomer,
        container: selectedContainer,
        customer_address: customerAddress,
        notes: 'Sold via dashboard'
      });
      alert('Package assigned to customer successfully!');
      setSelectedContainer('');
      setSelectedCustomer('');
      setCustomerAddress('');
      fetchData();
    } catch (err) {
      console.error(err);
      alert('Failed to sell package');
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-500">Loading Seller Dashboard...</div>;

  const availableContainers = containers.filter(c => c.status === 'available');

  return (
    <div className="max-w-6xl mx-auto space-y-8 mt-8 pb-16">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Seller Dashboard</h1>
          <p className="text-slate-500 mt-1">{user?.seller_profile?.business_name || user?.name}</p>
        </div>
        <div className="bg-brand-50 text-brand-700 px-4 py-3 rounded-xl font-medium border border-brand-100 flex items-center gap-2 shadow-sm">
          <Package className="w-5 h-5" /> 
          Total Packages: {containers.length}
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        
        {/* Forms Column */}
        <div className="lg:col-span-1 space-y-8">
          
          {/* Create Package */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="border-b border-slate-100 bg-slate-50 px-6 py-4 font-semibold text-slate-700 flex items-center gap-2">
              <Plus className="w-5 h-5 text-brand-600" /> Create New Package
            </div>
            <form onSubmit={handleCreatePackage} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Deposit Amount (₹)</label>
                <input 
                  type="number" 
                  value={depositAmount}
                  onChange={(e) => setDepositAmount(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all"
                  required
                  min="0"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Condition</label>
                <select 
                  value={condition}
                  onChange={(e) => setCondition(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all bg-white"
                >
                  <option value="excellent">Excellent</option>
                  <option value="good">Good</option>
                  <option value="fair">Fair</option>
                </select>
              </div>
              <button type="submit" className="w-full bg-brand-600 text-white font-medium py-2.5 rounded-lg hover:bg-brand-700 transition-colors shadow-sm">
                Create Package
              </button>
            </form>
          </div>

          {/* Sell/Assign Package */}
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="border-b border-slate-100 bg-slate-50 px-6 py-4 font-semibold text-slate-700 flex items-center gap-2">
              <ShoppingCart className="w-5 h-5 text-brand-600" /> Sell / Assign Package
            </div>
            <form onSubmit={handleSellPackage} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Select Available Package</label>
                <select 
                  value={selectedContainer}
                  onChange={(e) => setSelectedContainer(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all bg-white"
                  required
                >
                  <option value="">-- Select Package --</option>
                  {availableContainers.map(c => (
                    <option key={c.id} value={c.id}>{c.container_code} (₹{c.deposit_amount})</option>
                  ))}
                </select>
                {availableContainers.length === 0 && (
                  <p className="text-xs text-amber-600 mt-1">No available packages to sell. Create one first.</p>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Select Customer</label>
                <select 
                  value={selectedCustomer}
                  onChange={(e) => setSelectedCustomer(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all bg-white"
                  required
                >
                  <option value="">-- Select Customer --</option>
                  {customers.map(c => (
                    <option key={c.id} value={c.id}>{c.name} ({c.email})</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Customer Address</label>
                <textarea 
                  value={customerAddress}
                  onChange={(e) => setCustomerAddress(e.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-3 py-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all resize-none"
                  rows="2"
                  placeholder="Enter delivery address"
                  required
                ></textarea>
              </div>
              <button 
                type="submit" 
                disabled={availableContainers.length === 0}
                className="w-full bg-slate-900 text-white font-medium py-2.5 rounded-lg hover:bg-slate-800 transition-colors shadow-sm disabled:bg-slate-300 disabled:cursor-not-allowed">
                Complete Sale
              </button>
            </form>
          </div>

        </div>

        {/* Packages List Column */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden h-full">
            <div className="border-b border-slate-100 bg-slate-50 px-6 py-4 font-semibold text-slate-700 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Package className="w-5 h-5" /> Your Packages
              </div>
            </div>
            
            <div className="p-6">
              {containers.length === 0 ? (
                <div className="text-center py-12 text-slate-500 bg-slate-50 rounded-xl border border-dashed border-slate-200">
                  <Package className="w-12 h-12 mx-auto text-slate-300 mb-3" />
                  <p>You haven't created any packages yet.</p>
                  <p className="text-sm mt-1">Use the form to create your first package.</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm text-slate-600">
                    <thead className="text-xs text-slate-500 uppercase bg-slate-50 border-b border-slate-200">
                      <tr>
                        <th className="px-4 py-3 rounded-tl-lg">Code</th>
                        <th className="px-4 py-3">Status</th>
                        <th className="px-4 py-3">Customer</th>
                        <th className="px-4 py-3 text-right">Deposit</th>
                      </tr>
                    </thead>
                    <tbody>
                      {containers.map(container => (
                        <tr key={container.id} className="border-b border-slate-100 hover:bg-slate-50/50 transition-colors">
                          <td className="px-4 py-3 font-mono font-medium text-slate-800">{container.container_code}</td>
                          <td className="px-4 py-3">
                            <span className={`px-2.5 py-1 rounded-full text-xs font-medium 
                              ${container.status === 'available' ? 'bg-green-100 text-green-700' : 
                                container.status === 'assigned' ? 'bg-blue-100 text-blue-700' : 
                                container.status === 'return_requested' ? 'bg-amber-100 text-amber-700' :
                                'bg-slate-100 text-slate-700'}`}>
                              {container.status.replace('_', ' ').toUpperCase()}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-slate-500">{container.customer_name || '-'}</td>
                          <td className="px-4 py-3 text-right font-medium text-slate-700">₹{container.deposit_amount}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
