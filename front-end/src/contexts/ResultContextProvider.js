import React, { createContext, useContext, useState } from 'react';

const ResultContext = createContext();
const solrBaseUrl = 'http://localhost:8983/solr/search_lenr_0/select?q=';
const pyflaskBaseUrl = 'http://127.0.0.1:5000';

export const ResultContextProvider = ({ children }) => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  // /search / select
  const getResults = async (query, rows) => {
    setLoading(true);

    const res = await fetch(`${pyflaskBaseUrl}/search?q=${query}&rows=${rows}`, {
      method: 'GET',
    });

    const data = await res.json();
    console.log('search results', data)
    setResults(data);
    setLoading(false);
  };

  return (
    <ResultContext.Provider value={{ getResults, results, searchTerm, setSearchTerm, loading }}>
      {children}
    </ResultContext.Provider>
  );
};

export const useResultContext = () => useContext(ResultContext);

