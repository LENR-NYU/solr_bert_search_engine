import React, { useState, useEffect } from 'react';
import { useResultContext } from '../contexts/ResultContextProvider';

export const Facets  = ({all_authors, publisher, year_published, setSelectedFilters}) => {

    const [isAuthorSectionExpanded, setAuthorSectionExpanded] = useState(false);
    const [isPublisherSectionExpanded, setPublisherSectionExpanded] = useState(false);

    const handleFilterChange = (filterType, value) => {
        // Toggle the filter value in the selectedFilters array
        setSelectedFilters((prevFilters) => {
          const updatedFilters = { ...prevFilters };
          const index = updatedFilters[filterType].indexOf(value);
    
          if (index === -1) {
            updatedFilters[filterType].push(value);
          } else {
            updatedFilters[filterType].splice(index, 1);
          }
    
          return updatedFilters;
        });
    };

    const resetFilters = () => {
        setSelectedFilters({
            all_authors: [],
            publisher: [],
            year_published: [],
          });
    };

    const extractValues = (facetData) => {
        const values = [];
        for (let i = 0; i < facetData.length; i += 2) {
            const author = facetData[i];
            const count = facetData[i + 1];
            if (count !== 0) {
              values.push([author, count]);
            }
        }
        return values;
    };

    return(
        <div className="facet-filter">

        {/* All_authors */}
        <h2 
            className='display: block text-lg'
            onClick={() => setAuthorSectionExpanded(!isAuthorSectionExpanded)}>
            Author
        </h2>
        {isAuthorSectionExpanded && (
          <div>
            <ul>
              {extractValues(all_authors).map((authorData) => (
                <li key={authorData[0]} className='pr-6 py-1'>
                  <label className="cursor-pointer flex">
                    <input
                        type="checkbox"
                        value={authorData[0]}
                        // checked={selectedFilters.all_authors.includes(
                        // authorData[0]
                        // )}
                        onChange={() =>
                        handleFilterChange('all_authors', authorData[0])
                        }
                    />
                    <span className="ml-1">{authorData[0]}</span>
                    <span className="ml-auto text-gray-300">{authorData[1]}</span>
                  </label>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Publishers */}
        <h2 
            className='display: block text-lg'
            onClick={() => setPublisherSectionExpanded(!isPublisherSectionExpanded)}>
            Publisher
        </h2>
        {isPublisherSectionExpanded && (
          <div>
            <ul>
              {extractValues(publisher).map((publisherData) => (
                <li key={publisherData[0]} className='pr-6 py-1'>
                  <label className="cursor-pointer flex">
                    <input
                      type="checkbox"
                      value={publisherData[0]}
                    //   checked={selectedFilters.publisher.includes(
                    //     publisherData[0]
                    //   )}
                      onChange={() =>
                        handleFilterChange('publisher', publisherData[0])
                      }
                    />
                    <span className="ml-1">{publisherData[0]}</span>
                    <span className="ml-auto text-gray-300">{publisherData[1]}</span>
                  </label>
                </li>
              ))}
            </ul>
          </div>
        )}
        {/* Reset button to clear filters */}
        <button 
            className="mt-2 py-1 px-2 bg-red-500 text-white rounded-md"
            onClick={resetFilters}>Reset Filters</button>
      </div>
    
    );
}