import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Layouts & Shared
import Navbar from './components/Navbar';

// Public Pages
import Home from './pages/public/Home';
import Login from './pages/public/Login';
import Register from './pages/public/Register';
import ContainerLookup from './pages/public/ContainerLookup';

// Customer Pages
import CustomerDashboard from './pages/customer/Dashboard';

// Seller Pages
import SellerDashboard from './pages/seller/Dashboard';

// Admin Pages
import AdminDashboard from './pages/admin/Dashboard';

const ProtectedRoute = ({ children, allowedRoles }) => {
  const { user, loading } = useAuth();
  
  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />; // Or unauthorized page
  }
  
  return children;
};

const RoleBasedRedirect = () => {
  const { user, loading } = useAuth();
  
  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (!user) return <Navigate to="/login" replace />;
  
  if (user.role === 'customer') return <Navigate to="/dashboard" replace />;
  if (user.role === 'seller') return <Navigate to="/seller/dashboard" replace />;
  if (user.role === 'admin') return <Navigate to="/admin/dashboard" replace />;
  
  return <Navigate to="/" replace />;
};

function AppRoutes() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      <Navbar />
      <main className="flex-1 p-4 md:p-8">
        <Routes>
          {/* Public */}
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/containers/:code" element={<ContainerLookup />} />
          
          {/* Dashboard Redirector */}
          <Route path="/dashboard-redirect" element={<RoleBasedRedirect />} />

          {/* Customer */}
          <Route path="/dashboard" element={
            <ProtectedRoute allowedRoles={['customer']}>
              <CustomerDashboard />
            </ProtectedRoute>
          } />

          {/* Seller */}
          <Route path="/seller/dashboard" element={
            <ProtectedRoute allowedRoles={['seller']}>
              <SellerDashboard />
            </ProtectedRoute>
          } />

          {/* Admin */}
          <Route path="/admin/dashboard" element={
            <ProtectedRoute allowedRoles={['admin']}>
              <AdminDashboard />
            </ProtectedRoute>
          } />
          
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;
