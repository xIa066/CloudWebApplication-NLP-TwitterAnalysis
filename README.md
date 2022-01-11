# Cluster and Cloud Computing - Assignment 2 (Team 71)
This repository contains the source code for assignment 2 of the COMP90024 Cluster and Cloud Computing course at the University of Melbourne.

The system can be accessed via the following URL: 

### Overview
This project deploys a web application that harvests live tweets and generates interpretable visualizations from the live tweets data. This web application is deployed in a private cloud service (Melbourne Research Cloud). We use the Ansible playbook to automate the setup process. At the same time, we use Docker containers technology on top of the cloud virtualization.


**Web App:** 

[Analysis of Political Tweets in Australia](http://172.26.134.11/) (requires active connection Unimelb VPN)




### Submission Details

**Team members:**

- Aanchal Bhambhani (Student ID: 1235772)

- Zixi Chen (Student ID: 831860)

- Zexi Liu (Student ID: 813212)

- Naresh Olladapu (Student ID: 1233759)

- James Sun (Student ID: 140075)



## Project structure

* `API/` -- Source code for flask API which process the data requests from UI by connecting to CouchDB
* `mrc/` -- Ansible scripts for orchestration of cloud infrastructure and deployment of all necessary components 
* `Twitter-Harvester/` -- Source code for twitter harvester scripts
* `FrontEnd/` -- Source code for web-based visualization frontend


For further information, please refer to the project report attached to this submission.

## Software Stack
![Screen Shot 2022-01-11 at 12 58 48 pm](https://user-images.githubusercontent.com/37262666/148870186-eac02730-0bea-45c1-a927-8843b900a50f.png)

## Table of Cont
![Screen Shot 2022-01-11 at 1 26 56 pm](https://user-images.githubusercontent.com/37262666/148870680-e673df5e-2cb4-45a6-ae50-f84010ca83b8.png)

![Screen Shot 2022-01-11 at 1 27 18 pm](https://user-images.githubusercontent.com/37262666/148870714-dd98fd0d-b870-4849-ba58-1b4796b6b0b3.png)


