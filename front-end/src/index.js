import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';

import App from './App';
import { ResultContextProvider } from './contexts/ResultContextProvider';
import './global.css';

// ReactDom.render(
//   <StateContextProvider>
//     <Router>
//       <App />
//     </Router>
//   </StateContextProvider>,
//   document.getElementById('root'),
// );

const domNode = document.getElementById('root');
const root = createRoot(domNode);

root.render(
    <ResultContextProvider>
        <Router>
            <App />
        </Router>
    </ResultContextProvider>);
