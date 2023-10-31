import React, { createContext, useContext, useState } from 'react';

const AnswerContext = createContext();
const pyflaskBaseUrl = 'http://127.0.0.1:5000';

export const AnswerContextProvider = ({ children }) => {
  const [answer, setAnswer] = useState([]);
  const [loading, setLoading] = useState(false);
  const [doc, setDoc] = useState('');

  // /search / select
  const getAnswer = async (query, doc) => {
    setLoading(true);

    const res = await fetch(`${pyflaskBaseUrl}/qa?q=${query}&doc=${doc}`, {
      method: 'GET',
    });

    const data = await res.json();
    console.log('qa answer', data)
    setAnswer(data);
    setLoading(false);
  };

  return (
    <AnswerContext.Provider value={{ getAnswer, answer, doc, setDoc, loading }}>
      {children}
    </AnswerContext.Provider>
  );
};

export const useAnswerContext = () => useContext(AnswerContext);