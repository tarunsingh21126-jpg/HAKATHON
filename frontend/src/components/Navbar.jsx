import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Package, User as UserIcon, LogOut } from 'lucide-react';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-white shadow-sm border-b border-slate-200 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <Package className="text-brand-600 w-8 h-8" />
        <Link to="/" className="text-xl font-bold text-slate-900 tracking-tight">Pack<span className="text-brand-600">Back</span></Link>
      </div>
      
      <div className="flex items-center gap-6">
        {user ? (
          <>
            <Link to="/dashboard-redirect" className="text-sm font-medium text-slate-600 hover:text-brand-600">Dashboard</Link>
            <div className="flex items-center gap-3">
              <span className="text-sm text-slate-500">{user.name} ({user.role})</span>
              <button onClick={logout} className="p-2 text-slate-400 hover:text-red-500 rounded-full hover:bg-red-50 transition-colors">
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </>
        ) : (
          <>
            <Link to="/login" className="text-sm font-medium text-slate-600 hover:text-brand-600">Login</Link>
            <Link to="/register" className="text-sm font-medium bg-brand-600 text-white px-4 py-2 rounded-lg hover:bg-brand-700 transition-colors shadow-sm">Get Started</Link>
          </>
        )}
      </div>
    </nav>
  );
}
