import React from 'react';
import Result from './Result'; // Import the SearchResult component

// Sample array of search results
const sampleResults = [
  {
    document_link: 'https://example.com/document1',
    abstract: 'Lorem ipsum dolor sit amet.',
    all_authors: ['Author 1', 'Author 2'],
    title: 'Sample Title 1',
    publisher: 'Publisher 1',
    year_published: '2023',
    keywords: ['Keyword 1', 'Keyword 2'],
  },
  {
    document_link: 'https://example.com/document2',
    abstract: 'Consectetur adipiscing elit.',
    all_authors: ['Author 3'],
    title: 'Sample Title 2',
    publisher: 'Publisher 2',
    year_published: '2022',
    keywords: ['Keyword 3'],
  },
  // Add more result objects as needed
];

export const Results = () => (
  <div>
    {sampleResults.map((result, index) => (
      <Result key={index} result={result} />
    ))}
  </div>
);
