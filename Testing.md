### Testing without Authentication (Anonymous User)
1. Index Page.
    i. As an Anonymous User, the index page shows the below image:
    ![Anon User Screenshot](https://github.com/Oraclebun/ci-fullstack-project4/blob/master/documents/readme_images/Test_Home_AnonUser.jpg)
    ii. The navbar has the following links : Home, Directory, Product Category, Sign Up, Login and Shopping Cart Icon.
    iii. The index page shows all the features mentioned in the Features Section.
    iv. On clicking the Call To Action Button, the page is directed to the Current Offers Section.

2. Directory Page.
a. Search bar functionality
    i. Click on Search Button without any search input will show all products cards displayed.
    ii. Key in search term "cereal" without min and max price range, returns 2 products with the name "Great Grains Cereal - "
    iii. With no input in the search input and with min price set to 4 and max price range set to 5, the product "Organic Black
        Beans" is returned.
    iv. With input "baking" and with min price set to 1 and max price set to 2, the product "Pure Baking Soda" is returned.

3. Category Page 
a. Index Image Link
i. Click on Breakfast image, will direct the user to the view Product by Breakfast Page. (/products/breakfast).
ii. Click on Biscuits and Cookies image, will direct the user to the view Product by Biscuits and Cookies Page. (
    /products/biscuits-and-cookies).
iii. Click on Grains and Dried Beans image, will direct the user to the view Product by Grains and Dried Beans Page. (
    /products/grains-and-dried-beans).
iv. Click on Nuts image, will direct the user to the view Product by Nuts Page. (
    /products/nuts)
v. Click on Baking Ingredients image, will direct the user to the view Product by Baking Ingredients Page. (
    /products/baking-ingredients)
vi. Click on Fresh Produce image, will direct the user to the view Product by Fresh Produce Page. (
    /products/fresh-produce)
b. Navbar Link for Product categories
i. All the above test stated above works exactly the same way for the navbar dropdown links in Product Category.

4. Other NavBar Links
i. Click on the SignUp link will redirect the User to the Sign Up page.
ii. Click on the Login link will redirect the User to the Login page.
iii. Click on the Shopping Cart Icon will redirect the User to the Shopping Cart Page. 

5. Shopping Cart Page
a. If shopping cart is empty, user will
see an image of an empty shopping cart.
iv.  If items have already been added to cart, user will see the list of added items on the left and the billing summary on the
right.

### Testing with Permission Access.
1. Index Page.
* As User with Permission Access, the index page shows the below image:
![Staff User Screenshot]()
* The navbar has the following links : Home, Directory, Product Category, Sign Up, Login, StaffAccess and Shopping Cart Icon.
* The index page shows all the features mentioned in the Features Section.
* On clicking the Call To Action Button, the page is directed to the Current Offers Section.

2. Directory Page
3. Category Page
4. Other NavBar Links
* All item 2,3,4 above have the same test result as Testing with Anonymous User Access.

5. CRUD functionality
In the Navbar, there is a StaffAccess Dropdown in the menu. This Dropdown menu item is only visible for admin and users with 
CRUD permissions.
a. View Brand
* When clicked, the staff/admin user will be directed to a page that list all brands of products. On the top of the list there
is a floating button that allows staff/admin users to add brand names.
* When add brand button is clicked, admin/staff user is directed to an "Input Brand Name" form.
* If form input is empty on submit a popover will appear with message "Please fill out this field".
* If form is filled with valid text input, flash message with "Brand xxx was succesfully created" will appear on the home page,
after user is redirected.

b. Edit Brand
* The edit brand button is next to each brand name on the list in blue.
* When clicked, user will be directed to an edit brand form.
* If form input is empty on submit, a popover will appear with message "Please fill out this field".
* If form is filled with valid text input, a flash message with "Brand xxx was updated succesfully will appear on the home page
after user is redirected.

c. Delete Brand
* The delete brand button is next to the edit button on the list of the brands. The button is red to highlight the danger of deleting.
* When clicked, a modal will appear with the message to confirm the brand deletion. 
* When user confirms deletion, the brand will be deleted with a success message "Brand xxx was deleted successfully" on the homepage
after user is redirected.

d. For all the CRUD functions above, the same test process are used for Subcategory and Usage.
* When form is empty on submit, form will fail validation with the message "Please fill out this field".
* When form is filled with a valid text input, form is succesfully submitted and the flash message to inform user that the 
create,update or delete has been successful will show up after redirecting to the home page.

e. Shopping Cart Page
* The admin/staff user are also able to make purchase on this website and add items to the shopping cart.
* The functionality section with the shopping cart page is the same as for Anonymous User.