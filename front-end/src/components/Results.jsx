import React, { useState, useEffect } from 'react';
import Result from './Result'; // Import the SearchResult component
// import { useLocation } from 'react-router-dom';
import { useResultContext } from '../contexts/ResultContextProvider';
import { AnswerContextProvider } from '../contexts/AnswerContextProvider';
import { Loading } from './Loading';
import { Facets } from './Facets';

export const Results = () => {
  const { results, loading, getResults, searchTerm } = useResultContext();
  const [ filteredResults, setFilteredResults] = useState([]);
  const [ selectedFilters, setSelectedFilters ] = useState({
    all_authors: [],
    publisher: [],
    year_published: [],
  });

  useEffect(() => {
    if (searchTerm !== '') {
      getResults(searchTerm, 40);
    }
  }, [searchTerm]);

  useEffect(() => {
    // Apply selected filters to the copied results
    var filteredDocs = results?.response?.docs || []
    if (selectedFilters.all_authors.length != 0 || selectedFilters.publisher.length != 0 || selectedFilters.year_published.length != 0){
      filteredDocs = filteredDocs.filter((doc) => {
        // Replace these conditions with your filter logic based on selectedFilters
        return (
          selectedFilters.all_authors.some((author) =>
            doc.all_authors.includes(author)) ||
          selectedFilters.publisher.includes(doc.publisher) ||
          selectedFilters.year_published.includes(doc.year_published)
        );
      });
    }
    setFilteredResults(filteredDocs);
  }, [selectedFilters, results]);

  if(loading) return <Loading />;

  return(
    <div className="flex flex-wrap justify-between space-y-6">
      <div className="md:block md:w-1/5 hidden p-2">
        <Facets 
          all_authors={results?.facet_counts?.facet_fields.all_authors || [] }
          publisher={results?.facet_counts?.facet_fields.publisher || []}
          year_publsihed={results?.facet_counts?.facet_fields.year_published || []}
          setSelectedFilters={setSelectedFilters}
        />
      </div>

      <div className='block w-4/5 xs:w-full'>
        {filteredResults.map((element, index) => (
          <AnswerContextProvider>
            <Result 
              searchTerm={searchTerm}
              document_link={element.document_link}
              title={element.title}
              paragraph={element.paragraph}
              id={index}
              key={index}
              />
          </AnswerContextProvider>
        ))}
      </div>
    </div>
  );
};
