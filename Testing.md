## Testing

Manual Test.
### Testing without Authentication (Anonymous User)
1. Index Page.  
    i. As an Anonymous User, the index page shows the below image:  
    ![Anon User Screenshot](https://github.com/Oraclebun/ci-fullstack-project4/blob/master/documents/readme_images/Test_Home_AnonUser.jpg)  
    ii. The navbar has the following links : Home, Directory, Product Category, Sign Up, Login and Shopping Cart Icon.  
    iii. The index page shows all the features mentioned in the Features Section.  
    iv. On clicking the Call To Action Button, the page is directed to the Current Offers Section.
    v. On the index page, there are product shown in cards in the Current Offers Section. In every card, there is a shopping-cart
       icon, that can be clicked. Upon clicking, Users can see the cart number being updated on the top right corner of the navbar.
       The cart number shows the number of items in the shopping cart.  
    vi. A success message will appear to say that the `<product_name>` has been successfully added to cart.

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
    ii. Click on Biscuits and Cookies image, will direct the user to the view Product by Biscuits and Cookies Page.  
        (/products/biscuits-and-cookies).  
    iii. Click on Grains and Dried Beans image, will direct the user to the view Product by Grains and Dried Beans Page.  
        (/products/grains-and-dried-beans).  
    iv. Click on Nuts image, will direct the user to the view Product by Nuts Page.  
        (/products/nuts)
    v. Click on Baking Ingredients image, will direct the user to the view Product by Baking Ingredients Page.  
        (/products/baking-ingredients)  
    vi. Click on Fresh Produce image, will direct the user to the view Product by Fresh Produce Page.  
        (/products/fresh-produce)
b. Navbar Link for Product categories  
    i. All the above test stated above works exactly the same way for the navbar dropdown links in Product Category.

4. Other NavBar Links  
    i. Click on the SignUp link will redirect the User to the Sign Up page.  
    ii. Click on the Login link will redirect the User to the Login page.  
    iii. Click on the Shopping Cart Icon will redirect the User to the Shopping Cart Page. 

5. Shopping Cart Page  
    i. If shopping cart is empty, user will see an image of an empty shopping cart.  
    ii. If items have already been added to cart, user will see the list of added items on the left and the billing summary on the
        right.  
    iii. On the right of every item in the shopping cart, there are 3 boxes and 1 bin icon.
    iv. The bin icon, when clicked will remove the item immediately from the shopping cart.
    v. The 3 boxes in a row is actually a "-" input, a number and a "+" input.
    vi. When the "-" is clicked, the number shown in the input after it will decrease.
    vii. When the "+" is clicked, the number shown in the input before it will increase.
    viii. When either of the "-" or "+" is clicked, the billing summary will update accordingly to the number of items in the  
          shopping list.
    ix. Users will be able to see a blue Checkout Button, when clicked, will link to Stripe Payment Page.

6. Stripe Payment Page
    i. There will be an input to fill in the e-mail, the card information, the name on the card and the country or region the
        user is in. The test credit card number used is Default U.S. card—4242 4242 4242 4242. Test payment is done with any
        three-digit CVC code and an expiration date in the future.  
    ii. On payment success, user will be directed to the [checkout success page](https://oraclebun-project4.herokuapp.com/checkout/success)  
    iii. On the checkout success page, there will be a blue button "Continue Shopping".
    iv. When this button is clicked, User will be directed to the Home Page again.


### Testing with Permission Access User (Grocery Staff).
1. Index Page.  
i. As User with Permission Access, the index page shows the below image:
![Staff User Screenshot](https://github.com/Oraclebun/ci-fullstack-project4/blob/master/documents/readme_images/Test_Home_Staff.jpg)  
ii. The navbar has the following links : Home, Directory, Product Category, Sign Up, Login, StaffAccess and Shopping Cart Icon.  
iii. The index page shows all the features mentioned in the Features Section.  
iv. On clicking the Call To Action Button, the page is directed to the Current Offers Section.

2. Directory Page
3. Category Page
4. Other NavBar Links
* All item 2,3,4 above have the same test result as Testing with Anonymous User Access.

5. CRUD functionality
In the Navbar, there is a StaffAccess Dropdown in the menu. This Dropdown menu item is only visible for admin and users with 
CRUD permissions.  
a. View Brand  
    i. When clicked, the staff/admin user will be directed to a page that list all brands of products. On the top of the list there
        is a floating button that allows staff/admin users to add brand names.  
    ii. When add brand button is clicked, admin/staff user is directed to an "Input Brand Name" form.  
    iii. If form input is empty on submit a popover will appear with message "Please fill out this field".  
    iv. If form is filled with valid text input, flash message with "Brand xxx was succesfully created" will appear on the home page,
        after user is redirected.  
b. Edit Brand  
    i. The edit brand button is next to each brand name on the list in blue.  
    ii. When clicked, user will be directed to an edit brand form.  
    iii. If form input is empty on submit, a popover will appear with message "Please fill out this field".  
    iv. If form is filled with valid text input, a flash message with "Brand xxx was updated succesfully will appear on the home page
        after user is redirected.  
c. Delete Brand
    i. The delete brand button is next to the edit button on the list of the brands. The button is red to highlight the danger of deleting.  
    ii. When clicked, a modal will appear with the message to confirm the brand deletion.  
    iii. When user confirms deletion, the brand will be deleted with a success message "Brand xxx was deleted successfully" on the homepage
        after user is redirected.  
d. For all the CRUD functions above, the same test process are used for Subcategory and Usage.  
    i. When form is empty on submit, form will fail validation with the message "Please fill out this field".  
    ii. When form is filled with a valid text input, form is succesfully submitted and the flash message to inform user that the 
    create,update or delete has been successful will show up after redirecting to the home page.  
e. Shopping Cart Page  
    i. The admin/staff user are also able to make purchase on this website and add items to the shopping cart.  
    ii. The functionality section with the shopping cart page is the same as for Anonymous User.

### Testing for MyKitchen App.
#### Anonymous User  
    i. Anonymous Users will not see the link to MyKitchen in the navbar. If the user tries to type in the url, he/she will be 
    directed to the login page. 

#### Authenticated Users
    1. Dashboard/ Infoboard.  
    i. When an authenticated user is logged in, he/she will be able to see MyKitchen link in the navbar menu.  
    ii. On entering the homepage, the user will see a message on the dashboard to register the household and link other  
    grocery shop customers/users who are household members.  
    iii. In the navbar, the user will see the menu item : Back to Shop, MyKitchen Home, Register Home Profile, and Logout links.    
    iv. The user will also see a shopping cart in the navbar.  

    2. Home Profile Functionality  
    i. Registering Home Profile  
    * With an empty household name input, if submit button is clicked, form will not submit and user will see an error message to
        request user to fill up the form.
    * With a valid household name and no household members, form will be validated and submitted. This is because it is possible
        to have a single member household (which is just the household owner).  
    * The drop down list to select household members will show a list of users who are not members of any current household.   
    * Users will not be able to add existing e-grocery shoppers who are members of other household to their own household.  
    * However, users will be able to add any "free" unlinked e-grocery shoppers as their household member.

    ii. Viewing Home Profile.  
    * Upon registration, user will be able to see a link View Home Profile in the navbar instead of Register Home Profile.  
    * On clicking this link, users will be taken to a page that shows the household name and the current listed members.

    iii. Editing Home Profile  
    * The household profile edit button in blue, is below the home profile details on the view home profile page.
    * On clicking the edit button, users will be directed to a page with a form to update the household profile information.  
    * Again the same logic applies as the home registration page. Users will not be able to add members of other household 
        to their household membership. However, they are free to add unlinked users to their household membership. This is
        possible as the form select list is filtered against members and owners of existing household.  
    * User(Household owners) will need to check the delete button if they wish to exclude certain users from their household 
        membership.  
    * On form validated and successful submission, User will be directed to the MyKitchen Dashboard/Infoboard. They will see  
        a update success message. Your household profile `<household name>` has been edited on `<date>`.

    iv. Deleting Home Profile  
    * On the view home profile page, household owner will be able to see a delete button in red, just below the household profile
    information, next to the edit button.
    * On clicking this button, a modal will popup asking user to confirm household profile deletion.
    * When confirm button is clicked, users will be redirected to the MyKitchen Dashboard with the household deletion success
    message.
    * User will be deregistered of all household and will again see the message to tell him/her to register and link household
    members again on the MyKitchen Dashboard.

    3. Storage CRUD Functionality
    i. View Storage
    * Any household member or owner can add storage to their MyKitchen app.
    * Storage View is access via the navbar menu item "Storage"
    * On clicking the link, household members will be able to see the list of storage they have added for their household.
    * Above the list, there is a floating button to add/create storage. 
    * Beside each storage information, there is 1 edit button in blue and delete button in red.

    ii. Add Storage
    * On clicking the add storage button, User will be redirected to Input Storage Form.
    * If any fields are blank, form will not validate and submit. Error message is encountered.
