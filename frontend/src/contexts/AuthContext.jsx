import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../lib/api'; // Corregido de apiClient a api

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        try {
          const profile = await api.getProfile(token);
          setUser(profile);
        } catch (error) {
          console.error('Error loading user profile:', error);
          setToken(null);
          localStorage.removeItem('token');
        }
      }
      setLoading(false);
    };
    loadUser();
  }, [token]);

  const login = async (email, password) => {
    try {
      const data = await api.login(email, password);
      if (data.access_token) {
        setToken(data.access_token);
        localStorage.setItem('token', data.access_token);
        setUser(data.user); // Usar directamente data.user en lugar de hacer otra petición
        return true;
      } else {
        console.error('Login failed:', data.message);
        return false;
      }
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);


