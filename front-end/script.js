// Function to switch between tabs
// nyu gwu lenr
function openTab(evt, tabName) {
    var viewcontent, tablinks;
    viewcontent = document.getElementsByClassName("view");
    for (i = 0; i < viewcontent.length; i++) {
        viewcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks active");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    if (tabName == 'neural'){

    }

    if (tabName == 'solr'){

    }

    if (tabName == 'keywords'){
        displayKeywords()
    }
}

// Function to perform search and display results
function search() {

    const parentView = document.getElementById('neural');
    while (parentView.firstChild) {
        parentView.removeChild(parentView.firstChild);
    }
    var query = document.getElementById("searchInput").value;
    var num_results = 20;
  
    var eventSource = new EventSource(`http://127.0.0.1:5000/search?query=${query}&num_results=${num_results}`, {
        withCredentials: true
      });
  
    eventSource.addEventListener('message', function(event) {
      var result = JSON.parse(event.data);
      displayNeuralSearchEngine(result);
    });
  
    eventSource.addEventListener('error', function(error) {
      console.error('Error:', error);
      eventSource.close();
    });
  
    eventSource.addEventListener('end', function() {
      eventSource.close();
    });
}

function displayNeuralSearchEngine(result){
    // Display article results
    var articlesTab = document.getElementById("neural");

    var articleElement = createArticleElement(result);
    console.log(result.answer);
    articlesTab.appendChild(articleElement);

    // Activate the articles tab by default
    document.getElementsByClassName("tablinks")[0].click();
}

function createArticleElement(article) {
    var articleDiv = document.createElement("div");
    articleDiv.classList.add("article");
  
    var titleElement = document.createElement("h1");
    titleElement.textContent = article.title;
  
    var authorElement = document.createElement("h2");
    authorElement.classList.add("author");
    authorElement.textContent = article.author;

    var citeElement = document.createElement("h3");
    citeElement.classList.add("publish-info");
    citeElement.textContent = article.publisher + ", Vol. " +  article.volume + ", " + article.year;
  
    // Abstract title
    var abstractTitleElement = document.createElement("h4");
    abstractTitleElement.classList.add("abstractTitle")
    abstractTitleElement.textContent = "Abstract";

    var abstractElement = document.createElement("p");
    abstractElement.classList.add("abstract");
    abstractElement.textContent = article.abstract;

    // Extracted Text Title
    var textTitleElement = document.createElement("h4");
    textTitleElement.classList.add("textTitle")
    textTitleElement.textContent = "Extracted Text";
  
    // Highlighted Text
    var textElement = document.createElement("p");
    textElement.classList.add("text");
    var beginendTokens = article.text.split(article.answer);
    var formattedText = ''
    if (beginendTokens.length == 2){
        formattedText = beginendTokens[0] + '<span class= "red">' + article.answer +  '</span>' + beginendTokens[1]
    }else{
        formattedText = beginendTokens[0] + '<span class= "red">' + article.answer + '</span>'
    }
    textElement.innerHTML = formattedText;

    var linkElement = document.createElement("a");
    linkElement.classList.add("link");
    linkElement.href = article.link;
    linkElement.textContent = "Open PDf";
  
    articleDiv.appendChild(titleElement);
    articleDiv.appendChild(authorElement);
    articleDiv.appendChild(citeElement);
    articleDiv.appendChild(abstractTitleElement);
    articleDiv.appendChild(abstractElement);
    articleDiv.appendChild(textTitleElement);
    articleDiv.appendChild(textElement);
    articleDiv.appendChild(linkElement);
  
    return articleDiv;
}

function displayKeywords() {

    var topics = [
        "Energy Experiments",
        "Atomic Structure and Energy Levels",
        "Cell heating and power transfer",
        "Palladium surface loading and deuterium-to-hydrogen ratio on cathode film",
        "Discharge and Cathode Ray",
        "tritium sample in titanium experiment cell",
        "Tritium experiments in heat-producing cells",
        "Power loading in PD cell",
        "Gas absorption on a surface layer",
        "Hydrogen wire experiment temperature",
        "Condensed Matter Physics",
        "Article on Neutron Detection in PD",
        "Hydrogen cracking process in palladium material during storm",
        "Cell Palladium Electrode Experiment",
        "Condensed Matter Experiment and Electron State",
        "Particle Detector",
        "Excess heat in the Fleischmann-Pons cell",
        "Ion Beam Screening and Target Yield",
        "policy and technology's impact on online public availability",
        "Heat experiment with tritium",
        "NASA research on aircraft and power at the university",
        "cell experiment",
        "energy"
      ];

    d3.csv('cluster_score_random_2_0.csv').then(function(data) {

        data.forEach(function(d) {
            d.x = +d['Dimension 1'];
            d.y = +d['Dimension 2'];
            d.label = +d['label'];
        });

        d3.csv('literature-records_with_pdf1.csv').then(function(articleData) {
            // Create a lookup table for article information
            var articleLookup = {};
            articleData.forEach(function(article) {
              var index = article.index;
              articleLookup[index] = {
                title: article.title,
                author: article.all_authors,
                abstract: article.abstract,
              };
            });

            var container = document.getElementById('keywords');
            var containerWidth = container.clientWidth;
            var containerHeight = container.clientHeight-10;
            var containerLeft = container.clientLeft;
            var containerTop = container.clientTop;
        
            var svg = d3.select('#keywords')
            .append('svg')
            .attr('width', containerWidth)
            .attr('height', containerHeight);

            // Set the dimensions and margins
            var margin = { top: 20, right: 20, bottom: 20, left: 20 };
            var width = +svg.attr('width') - margin.left - margin.right;
            var height = +svg.attr('height') - margin.top - margin.bottom;

            // Create scales for x and y axes
            var xScale = d3.scaleLinear()
                .domain(d3.extent(data, function(d) { return d.x; }))
                .range([margin.left, width - margin.right]);

            var yScale = d3.scaleLinear()
                .domain(d3.extent(data, function(d) { return d.y; }))
                .range([height - margin.bottom, margin.top]);

            var colors = d3.schemeCategory10.slice(0, topics.length);
            var colorScale = d3.scaleOrdinal()
            .domain(topics)
            .range(colors);

            var tooltip = d3.select('#keywords')
            .append('div')
            .style('opacity', 0)
            .style("position", "absolute")
            .attr('class', 'tooltip')
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "5px");

            // Create the scatter plot
            svg.selectAll('.dot')
                .data(data)
                .enter().append('circle')
                .attr('class', 'dot')
                .attr('cx', function(d) { return xScale(d.x); })
                .attr('cy', function(d) { return yScale(d.y); })
                .attr('r', 5)
                .style('fill', function(d) { return colorScale(topics[d.label]); })
                .on('mouseover', function(d) {
                    tooltip
                    .style("opacity", 1)
                    d3.select(this)
                    .style("stroke", "black")
                    .style("opacity", 1)
                })
                .on('mousemove', function(d){
                    var articleInfo = articleLookup[d.index];
                    tooltip
                    .style('left', (d.x-containerTop) + 'px')
                    .style('top', (d.y-containerLeft) + 'px')
                    .html('Title: ' + articleInfo.title + '<br>'
                      + 'Author: ' + articleInfo.author + '<br>'
                      + 'Abstract: ' + articleInfo.abstract)
                })
                .on('mouseout', function(d) {
                    tooltip
                    .style("opacity", 0)
                  d3.select(this)
                    .style("stroke", "none")
                    .style("opacity", 0.8)
                });


            // Add color legend
            var legend = svg.selectAll('.legend')
                .data(topics)
                .enter().append('g')
                .attr('class', 'legend')
                .attr('transform', function(d, i) {
                    var legendX = width - margin.right;
                    var legendY = margin.top + i * 20;
                return 'translate(' + legendX + ',' + legendY + ')';
            });

            legend.append('circle')
                .attr('r', 5)
                .style('fill', function(d, i) { return colors[i]; });

            legend.append('text')
                .attr('x', 12)
                .attr('y', 5)
                .text(function(d) { return d; });
        });
    });

}
  
  
