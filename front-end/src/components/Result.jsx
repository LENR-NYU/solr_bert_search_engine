import React, { useState, useEffect } from 'react';
import { useAnswerContext } from '../contexts/AnswerContextProvider';

const Result = ( { searchTerm, document_link, title, paragraph, id } ) => {
  const { getAnswer, answer, doc, setDoc, loading } = useAnswerContext();
  const [expanded, setExpanded] = useState(id < 5);

  useEffect(() => {
    if (searchTerm && paragraph && expanded) {
      getAnswer(searchTerm, paragraph);
      console.log('answer', answer)
    }
  }, [expanded]);

  return (
    <div className="w-full py-2">
      <a href={document_link} target="_blank" rel="noreferrer">
        {/* <p className="text-sm">{document_link.length > 30 ? document_link.substring(0, 30) : document_link}</p> */}
        <p className="text-lg hover:underline dark:text-blue-300 text-blue-700  ">{title}</p>
      </a>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          {expanded ? (
            <>
              {String(paragraph).split(answer.answer).map((part, idx, array) => {
                return (
                  <React.Fragment key={idx}>
                    {idx > 0 && (
                      <span className="bg-yellow-300" key={`highlight-${idx}`}>
                        {answer.answer}
                      </span>
                    )}
                    <span key={`text-${idx}`}>{part}</span>
                  </React.Fragment>
                );
              })}
            </>
          ) : (
            <button
              onClick={() => setExpanded(!expanded)}
              className="text-blue-500 hover:underline mt-2"
            >
              {expanded ? 'Collapse' : 'Expand'}
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default Result;