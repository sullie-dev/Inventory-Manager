# Inventory manager

[View project here](https://inventory-manager.sullie.repl.co/)

---
This app allows a user to create products, locations and shipments, and assign products to the corrisponding lcoations. This is to help manage their product invetory and to get an overview on where the inventory is located vs what the have incoming

![Image of project](https://i.imgur.com/BYHBeQh.png)

## Deployment

Project is deployed using Repli.it

The products, locations and shipments are written to a PostgreSQL database which is hoasted on Heroku

---

## Features
The app has the followuing features

- Basic CRUD funnctions for the products, shipments, and locations
- The ability to assign an item to a warehouse location 
- The ability to create a basic shipment which **doesn't** affect stock levels, these need to be manually adjusted. 


---

## Bugs:

---

#### Solved bugs:
n/a
#### Unsolved bugs:
- Removing locations and not have the products updated. For this I removed the baility to delete locations
---

## Content

---

## Credits
n/a
## Media

No media is used in this project

---

## Technologies used

- HTML 5
- CSS 3
- Bootstrap
- GitHub
- Replit
- Flask