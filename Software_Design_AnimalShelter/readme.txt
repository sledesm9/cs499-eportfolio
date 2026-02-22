Rescue Dashboard 



Overview

--------



I created this interactive dashboard application for the Grazioso Salvare animal rescue shelter. This application bridges a MongoDB datastore with a Python CRUD Module, and Dash front-end interface. The dashboard allows for easy browsing/shelter data to find dogs fitting the various rescue tiers.



Filter records, view charts and data on a map all from one dashboard



Architecture

------------



The dashboard components were designed with a loose/simple modular architecture where each element has a well defined role:



Data Layer: Animal records are persisted in MongoDB



Model Layer: AnimalShelter CRUD class performs DB operations



Model Layer: The AnimalShelter CRUD class handles all the database work. 





Controller Layer: The Dash will react to what the user does in the dashboard as well as view updates.



View Layer: Dash components (table/charts/map)



By loosely defining these roles each layer becomes more readable, maintainable and extensible.



Key Enhancements



Improved code readability/commenting



Enhanced error handling/validation within CRUD module



Retained modular nature of CRUD module to enable re-use in future projects



Added comments describing data flow between dashboard/views and datastore



Technologies Used

-----------------



Python 3



MongoDB



Dash / Plotly



Pandas



JupyterDash



Getting Started

---------------



Define your MongoDB username/password (env vars or directly in the Config section).



Ensure mongod service is running.



Open notebook, Run Dash dashboard within Jupyter/Codio