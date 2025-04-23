import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [packages, setPackages] = useState([]);
  const [query, setQuery] = useState('');
  const [aiSuggestions, setAiSuggestions] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchPackages = async () => {
    try {
      const response = await axios.get('http://localhost:4000/api/npm/list');
      setPackages(response.data.dependencies || []);
    } catch (error) {
      console.error('Error fetching packages:', error);
    }
  };

  const installPackage = async (packageName) => {
    setLoading(true);
    try {
      await axios.post('http://localhost:4000/api/npm/install', { packageName });
      alert(`${packageName} installed successfully!`);
      fetchPackages();
    } catch (error) {
      console.error('Error installing package:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchPackagesWithAI = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:4000/api/ai/search', { query });
      setAiSuggestions(response.data.suggestions);
    } catch (error) {
      console.error('Error searching with AI:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-800">
      <header className="bg-blue-500 text-white py-4 text-center">
        <h1 className="text-2xl font-bold">Modern NPM Manager with AI Portal</h1>
      </header>
      <div className="p-6">
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Installed Packages</h2>
          <button
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
            onClick={fetchPackages}
          >
            Load Packages
          </button>
          <ul className="mt-4">
            {Object.keys(packages).map((pkg) => (
              <li key={pkg} className="py-2 border-b">
                {pkg} - {packages[pkg].version}
              </li>
            ))}
          </ul>
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Install a Package</h2>
          <input
            type="text"
            placeholder="Enter package name"
            className="border p-2 rounded mr-2"
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            onClick={() => installPackage(query)}
            disabled={loading}
          >
            {loading ? 'Installing...' : 'Install'}
          </button>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">AI-Powered Package Suggestions</h2>
          <input
            type="text"
            placeholder="Search for npm packages"
            className="border p-2 rounded mr-2"
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
            onClick={searchPackagesWithAI}
            disabled={loading}
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
          <div className="mt-4">
            <pre className="bg-gray-200 p-4 rounded">{aiSuggestions}</pre>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;