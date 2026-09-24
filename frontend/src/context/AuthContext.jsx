import { createContext, useState, useEffect, useContext } from 'react';
import api from '../api/axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const storedUser = localStorage.getItem('user');
      const token = localStorage.getItem('access_token');
      
      if (storedUser && token) {
        try {
          setUser(JSON.parse(storedUser));
          // Optionally verify token or fetch profile if needed
        } catch (error) {
          console.error("Auth init error:", error);
          logout();
        }
      }
      setLoading(false);
    };
    initAuth();
  }, []);

  const login = async (email, password) => {
    const response = await api.post('/auth/login/', { email, password });
    const { access, refresh, user: userData } = response.data;
    
    // We decode basic info from token if needed, or use the returned user data
    // The CustomTokenObtainPairView returns data['user'] = UserSerializer
    // Wait, the default TokenObtainPair doesn't return user, but our Custom one does.
    // Let's assume we decode token or get user from response. Let's use standard approach:
    // we get token, and fetch profile.
    
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    
    // Let's fetch the full profile
    const profileRes = await api.get('/auth/profile/', {
      headers: { Authorization: `Bearer ${access}` }
    });
    
    localStorage.setItem('user', JSON.stringify(profileRes.data));
    setUser(profileRes.data);
    return profileRes.data;
  };

  const register = async (userData) => {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
