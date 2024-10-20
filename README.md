# Introduction

This module Integrates Drillbit with Frappe/Education, so that Teachers can check pliagrism status of a submitted assignment.

This is the general flow:

## Non Administrative

- Student submits the assignment to any Teacher/Mentor of their choice.

![Submit Assignment](https://i.imgur.com/KHdX9He.png)

- Head of Department can see all the assignments and process if needed.

![Assignments list](https://i.imgur.com/LPvZ1Fc.png)

- Teacher/Hod can select the particular drillbit folder to upload the assignments in.

![Process Assignment](https://i.imgur.com/54f2x6e.png)

![Report](https://i.imgur.com/epEn5cC.png)



## Administrative

- Website admin can set the credentials of drillbit and edit/create folders.

![Drillbit Module](https://i.imgur.com/nprV5vT.png)


- This is the interface an admin sees after installing the app:

![Drillbit Interface](https://i.imgur.com/okwWy3q.png)

- The api credentials can be set here:

![API creds](https://i.imgur.com/QGjC9X9.png)

- An admin can create the drillbit folders here.

![Drillbit Folders](https://i.imgur.com/kQeQ4LV.png)

![Create Folder](https://i.imgur.com/xXfRoyO.png)



# Installation
## Requiements 

- frappe/Erpnext
- frappe/Education

## Installation

To install the Drillbit module, follow these steps:

- In your bench enviornment type: bench get-app https://github.com/GreatDevelopers/drillbit.git
- bench install-app drillbit

