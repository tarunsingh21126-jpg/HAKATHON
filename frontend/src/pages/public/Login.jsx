import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate('/dashboard-redirect');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 bg-white p-8 rounded-2xl shadow-sm border border-slate-100">
      <h2 className="text-2xl font-bold text-center mb-6">Welcome Back</h2>
      {error && <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">{error}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <input 
            type="email" 
            className="w-full p-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:outline-none"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required 
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
          <input 
            type="password" 
            className="w-full p-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:outline-none"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required 
          />
        </div>
        <button type="submit" className="w-full bg-brand-600 text-white font-medium py-2.5 rounded-lg hover:bg-brand-700 transition-colors">
          Sign In
        </button>
      </form>
      <p className="mt-4 text-center text-sm text-slate-500">
        Don't have an account? <Link to="/register" className="text-brand-600 hover:underline">Register here</Link>
      </p>
      
      <div className="mt-8 pt-4 border-t border-slate-100 text-xs text-slate-400">
        <p>Demo Logins:</p>
        <p>Customer: tarun@example.com / customer123</p>
        <p>Seller: greenleaf@packback.app / seller123</p>
        <p>Admin: admin@packback.app / admin123</p>
      </div>
    </div>
  );
}
