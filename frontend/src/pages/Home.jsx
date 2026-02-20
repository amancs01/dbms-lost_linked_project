import React, { useState, useEffect } from 'react';
import ItemCard from '../components/ItemCard';
import Spinner from '../components/Spinner';
import api from '../services/api';
import toast from 'react-hot-toast';

const Home = () => {
  const [lostItems, setLostItems] = useState([]);
  const [foundItems, setFoundItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const [lostResponse, foundResponse] = await Promise.all([
        api.get('/lost-items'),
        api.get('/found-items'),
      ]);
      setLostItems(lostResponse.data);
      setFoundItems(foundResponse.data);
    } catch (error) {
      toast.error('Failed to fetch items');
      console.error('Error fetching items:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteLost = (itemId) => {
    setLostItems(lostItems.filter(item => item.lost_id !== itemId));
  };

  const handleDeleteFound = (itemId) => {
    setFoundItems(foundItems.filter(item => item.found_id !== itemId));
  };

  if (loading) {
    return <Spinner />;
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Lost & Found Items
          </h1>
          <p className="text-gray-600">
            Help reunite people with their belongings
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Lost Items Section */}
          <div>
            <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded">
              <h2 className="text-2xl font-bold text-red-800 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                Lost Items ({lostItems.length})
              </h2>
              <p className="text-red-700 mt-1">Items that people have lost</p>
            </div>

            <div className="space-y-4">
              {lostItems.length === 0 ? (
                <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
                  <p>No lost items reported yet</p>
                </div>
              ) : (
                lostItems.map((item) => (
                  <ItemCard
                    key={item.lost_id}
                    item={item}
                    type="lost"
                    onDelete={handleDeleteLost}
                  />
                ))
              )}
            </div>
          </div>

          {/* Found Items Section */}
          <div>
            <div className="bg-green-50 border-l-4 border-green-500 p-4 mb-6 rounded">
              <h2 className="text-2xl font-bold text-green-800 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Found Items ({foundItems.length})
              </h2>
              <p className="text-green-700 mt-1">Items that have been found</p>
            </div>

            <div className="space-y-4">
              {foundItems.length === 0 ? (
                <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
                  <p>No found items reported yet</p>
                </div>
              ) : (
                foundItems.map((item) => (
                  <ItemCard
                    key={item.found_id}
                    item={item}
                    type="found"
                    onDelete={handleDeleteFound}
                  />
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
