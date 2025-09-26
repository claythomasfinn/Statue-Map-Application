# Statue Map Application  
This application maps statues of athletes nationwide and allows searching, viewing additional information including images and histories, filtering by date, and more. It is based on statue data produced by Ashley Loup, PhD, a professor at the University of Iowa. It has been deployed using Heroku. 
## Features  
Features are integrated into Dash using the native callbacks for hover data, modal windows, and dropdown inputs.
 - Interactive map with zoom and pan
 - Hover tooltips for picture and title
 - Modal windows for additional information
 - Searchable athlete list
 - Filter by year statue was erected
## Programming  
 - Frontend: Plotly Dash
 - Backend: Python, Plotly Dash
 - Deployment: Heroku
 - Data: Pandas, CSV
## Deployment  
The project is already adapted for deployment to Heroku with the necessary requirements and Procfile. It has been deployed to the following site: [Clayton Finn - Statue Map Application](https://www.claytonfinn.com/statuemap)  
## Installation  
The project can easily be cloned and run locally and/or adapted to a new data set. Contributions and ideas are welcome!  
  
`git clone https://github.com/claythomasfinn/Statue-Map-Application/`  
## Bugs
There is currently an issue with the dropdown search menu blocking clicking on the first available athlete option. This appears to be an issue with how Dash renders and layers the dropdown menu in conjunction with the search results. The first option can easily be selected by hitting enter. I believe this can be alleviated by switching the Dash feature to an input menu instead of a dropdown, but I prefer having the dropdown to show available choices.  
