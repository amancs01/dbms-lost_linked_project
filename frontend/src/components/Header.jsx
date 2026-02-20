import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export const Header = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight hover:text-blue-100 transition-colors">
              LostLinked
            </h1>
          </Link>
          
          <nav className="flex items-center space-x-4">
            <Link
              to="/"
              className="px-4 py-2 rounded-md hover:bg-blue-500 transition-colors"
            >
              Home
            </Link>
            <Link
              to="/report/lost"
              className="px-4 py-2 rounded-md hover:bg-blue-500 transition-colors"
            >
              Report Lost
            </Link>
            <Link
              to="/report/found"
              className="px-4 py-2 rounded-md hover:bg-blue-500 transition-colors"
            >
              Report Found
            </Link>
            
            {isAuthenticated ? (
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-red-500 rounded-md hover:bg-red-600 transition-colors"
              >
                Logout ({user?.username})
              </button>
            ) : (
              <Link
                to="/login"
                className="px-4 py-2 bg-green-500 rounded-md hover:bg-green-600 transition-colors"
              >
                Admin Login
              </Link>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
};


