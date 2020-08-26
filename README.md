# Code Institute Full Stack Frameworks with Django

# Cloudberry Grocer E-Commerce Website

## Project Objectives
This website is created to serve users who are customers of online grocery purchases. With the advancement in technology, users these 
days are spoilt for choice when purchasing groceries online. There are many e-commerce services that provide the users with a huge variety 
of choice when it comes to food products.Other than grocery purchase, this site also offers a small service to the registered shoppers. 
A side app allows user to manage their purchased product inventory and offers to track their product expiry date for them on the 
app's dashboard.

## Deployed Link
The deployed website can be found [here](https://oraclebun-project4.herokuapp.com/)

## UX/UI
### Overview and Colour
The colour on this website is chosen to be bright and cheery to give customers a bright and cheerful experience when they shop. The 
bright background also serves to highlight the products available. The site name is chosen because just like the berry which is a rarity
in other parts of the world, I hope the site is also rare and the experience of using it gives the users a good and special feeling 
that they are well served.

## User Stories
### Basic User Stories
1. As a customer of the online grocery store, a user would like to be able to browse through the products on offer immediately when he/she 
goes to the website.
2. As a user of the website, he/she should be able to search for the products available, either by sorted categories or by a search
bar.
3. Users should be able to view products in detail when they click into the product cards. Users should also be able to see the
prices of the product on display clearly.
4. Users should be able to easily add a product to the shopping cart and immediately checkout the product they want to purchase.
5. Likewise, a user should also be able to easily remove items from the shopping cart.
6. Users could see immediately in the shopping cart page when they add the items or remove items, how much the total cost would be.
### Additional User Stories
1. Users should be able to register their household profile in the website.
2. Users should be able to edit their household profile and delete their household profile if they no longer want to use the site.
3. Users should be able to add, edit and delete named storages in the website.
4. Users should be able to add, edit and delete food items in the storage in that site.
5. On the dashboard, users will be notified immediately if a food item is nearing expiry or is expired depending on the threshold set 
by the user.
6. Users will be able to purchase new food (add to cart) the food that is expired direct from their storage view.

## Wireframes

## E-grocery Shop Features
### Index/Home page
a. Feature that attracts draws user attention
* The homepage has a jumbotron that welcomes the user to the e-grocer. It has the name of the e-grocer as well as the Call-to-Action
text and an action that links user to the product directory.
* Below the jumbotron, there's a row of image that links users to products, sorted by categories.
* Below the row of categories images, there is a row of cards showing filtered products that are on discount.

b. Features that allow users to navigate to other pages
* At the top of the homepage, there is a navbar to allow users to navigate to Directory, Product Category and SignUp or Login/Logout
pages and also the shopping cart page.

c. Features that allow users to view shopping cart.
* On the right of the navbar, there is a shopping cart icon to link the users to view the shopping cart contents.

### Directory page
a. Search Feature
* On the Directory page, there are 3 search inputs: 1 text input and 2 number inputs. The text input allows user to search for
queries in the product name. The number inputs act as a search range to allow user to search for a range in product price. Users 
have to key in the minimum range limit in the minimum number input and the maximum range limit in the max number input. 
* Below the search inputs, users will be able to see a text that will show the query term.
* Also, as the prices are searched in the root price field, the search result will return results of products in their root 
price.

b. Cards Display
* Below the Search Feature, there are cards display to display all products in the store if no search is performed.
* If a search is requested, the cards display will show the products which are result of the search query.

c. Hidden Feature
* If the logged in user is a superuser/staff or has permissions to perform CRUD functions, the user would be able to see
the add product/ edit product and delete product button.

### Product Category Pages
a. Sorting Feature
*  The navbar has a dropdown to link users to each page that show products sorted to the relevant categories. The links are also
presented in the category images on the index page.

### Staff Access Page
a. CRUD functions
* The admin/staff should be able to access the Staff Access link on the navbar. The Staff Access is a dropdown menu that link 
authorised users to view/create/update/delete product related attributes : Brand, Subcategory and Usage.

### Login/Logout/SignUp/Accounts Management Page
* The account management pages are managed by Django-AllAuth

### Shopping Cart Page
a. Cart Feature
* The users will see an empty shopping cart if no products are added to the shopping cart.
* If there are items added to cart, the users will be able to see items in the shopping cart page.
* There are also buttons that allow user to increase or decrease the quantity of the item to purchase.
* There is a bin icon at the top right corner of the cart to allow user to delete the item immediately if he/she changes his/her 
mind.
* On the right of the products, there is a side card shows the users the subtotal and the grand total of the products.
* Below that, there is a CheckOut button that users can click to checkout and pay for the items purchased.

## My Kitchen App
### MyKitchen Index Page
a. Mini Infoboard Feature
* When the user enters MyKitchen App from the navbar link (after they are authenticated), they are able to see a mini infoboard that
tells the user to register and setup a household name and link other e-commerce registered site users as member of the household.
* When users create storage, add food items with expiry date into it and set the relevant threshold, they should see a persistent
alert message on the infoboard that the food item has hit the expiry threshold and will expire in the time duration set by the user.
(If the item has hit the expiry threshold). Otherwise, users will not see any alert message on the infoboard.

### MyKitchen Household Profile View and Registration Pages
b. Household Profile Registration and CRUD Features
* Users are able to register their household name and select other e-commerce registered site users by username as member of the 
household.
* When a user registers a household, that user will be assigned as the owner of the household and will have the priviledge to edit,
and delete the household profile, perform CRUD on the storage and food items in the website.
* The other users being selected as his/her household member will be assigned as the member of the household and will have the 
priviledge to perform CRUD on the storage and food items in the website.

### CRUD Storage and Food Item Pages
c. View Storage and View Food Items Pages
* Users are able to view their household storage by name and add/create new storage location similar to what they have in their kitchen.
* Users are able to edit and delete their household storage.
* Users are able to "go into the storage" and view/add/update/delete food items information in their storage.

### NavBar Links
d. NavBar Links
* On the navbar, when relevant links are clicked, users are redirected to the relevant sites.

## Technologies Used
The technologies used for this project are:
1. [Django(Release 2.2.14)](https://www.djangoproject.com/start/overview/). Django is a Python Web Framework that encourages rapid
development and clean design. It is the main requirement of this project.
2. [Python(Release 3.8.3)](https://www.python.org/downloads/release/python-383/). Python is the programming language that Django 
is built on.
3. [HTML5](https://html.spec.whatwg.org/). HTML is the markup language that structures the webpage documents.
4. [CSS3](https://www.w3.org/TR/2001/WD-css3-roadmap-20010523/). Cascading style sheet is the language that presents and styles 
the HTML documents.
5. [Javascript and JQuery](https://developer.oracle.com/sg/javascript/). Javascript and Jquery is used primarily to do DOM 
manipulation and it is the main engine to serve interactivity and event handling to the webpages.
6. [Bootstrap (Release 4.5)](https://getbootstrap.com/docs/4.5/getting-started/introduction/). Bootstrap is the layout framework
used to organize the website's display.
7. [Gitpod](https://www.gitpod.io/)  
Gitpod is an online IDE that can be launched in Github. It is used to develop and write the code for this project.
8. [Git and Github](https://github.com/)  
Github is an online hosting service for software development that utilizes Git for version control.
9. [Stripe](https://stripe.com/en-sg). Stripe is a financial software service provider that provides the API for software developers
to integrate payment into their websites and mobile apps.
10. [Google Fonts](https://fonts.google.com/). Google Fonts Poppins (sans-serif) is used for headings. Google Fonts Bitter (serif)
is used for body and in paragraph tags. Google Font Delius Swash Caps is used in the navbar brand/logo name.
11. [Font Awesome](https://fontawesome.com/) Font Awesome Icons are used in this project to give illustrations to some edit and 
delete buttons.

Django Libraries
1. [Django-AllAuth](https://django-allauth.readthedocs.io/en/latest/overview.html) is a Django Library that manages authentication, 
registration, account management as well as 3rd party (social) account authentication 
2. [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/) is Django package that provides DRY Django Forms.

### Database
The database used in the project is PostgreSQL. PostgreSQL is an open source Relational Database Management System that is similar
to MySQL but it has an object oriented database model which are directly supported in database schemas and query language.

### Database Structure
A UML diagram to illustrate the relationship between models is drawn and shown [here](https://github.com/Oraclebun/ci-fullstack-project4/blob/master/documents/UML.pdf)

## Testing
Due to the shortage in time, testing is for this project is done manually:
As the testing write-up is quite long, the details of testing is documented in [Testing.md]()



