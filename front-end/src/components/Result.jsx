import React from 'react';

const SearchResult = ({ result }) => {
  const {
    document_link,
    abstract,
    all_authors,
    title,
    publisher,
    year_published,
    keywords,
  } = result;

  return (
    <div className="search-result">
      {document_link && (
        <a href={document_link} target="_blank" rel="noopener noreferrer">
          Document Link
        </a>
      )}

      {abstract && <p>Abstract: {abstract}</p>}

      {all_authors && all_authors.length > 0 && (
        <p>Authors: {all_authors.join(', ')}</p>
      )}

      {title && <p>Title: {title}</p>}

      {publisher && <p>Publisher: {publisher}</p>}

      {year_published && <p>Year Published: {year_published}</p>}

      {keywords && keywords.length > 0 && (
        <p>Keywords: {keywords.join(', ')}</p>
      )}
    </div>
  );
};

export default SearchResult;