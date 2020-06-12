# Waitlist

Final project for Coding Dojo Software Development Bootcamp. The assignment was to build a web application in a 2 week sprint.

# Goals

•	My goal is to create an open source tool for online sellers to add a waitlist feature to their website for customers to order from incoming shipments. This will allow customers to secure their order ahead of time and ensure access to high demand items.

•	Additionally, the tool will help sellers manage demand by giving them the option to place limits on how many items a customer can order.

•	The tool should easily integrate into a seller’s current business processes, allowing them to better serve their customers while increasing profits.

# Background and Strategic Fit

The current pandemic has greatly altered customers shopping habits both online and in store. The hoarding of essential products like toilet paper, food, medications, and cleaning supplies caused worry and panic amongst shoppers. More customers are choosing to shop online gather than risk contracting COVID-19 by shopping in store.

Most ecommerce websites do not have a waitlist option for customers. A waitlist would allow the customers in dire need of certain products to guarantee they would receive them at some point. It would also save customers time by avoiding having to constantly check back to see if a product is back in stock. Additionally, sellers should be able limit purchase quantities to prevent people from hoarding essential products. 

# Workflow

<p align="middle">
  <img src="/images/dashboard.png" width="600" />
</p>

The dashboard is the central hub of the application. It provides users with a snapshot view of their products, the amount in transit from incoming shipments, and the date those shipments arrive.

To add additional products, the user would select the Add Product button in the upper right-hand corner.

<p align="middle">
  <img src="/images/add_a_new_product.png" width="600" />
</p>

The user then fills out the new product form. In this form, the user can set a purchase limit that prevents customers from ordering more than the designated amount.

<img align="right" src="/images/customer_waitlist.png" width="250" />

Once the new product form is submitted, users will be rediretced back to the dashboard. Here they have the option to add additional shipments, edit the product information, and edit the shipment information if necessary.

Additionally, a customer-facing waitlist form for that product is automatically created. The form will show the arrival date of the next incoming shipment as the back in stock date. This will allow customers to make an educated decision regarding whether they are willing to wait for this product to become back in stock.

Customers will need to enter their name, email address, and quantity they wish to purchase to join the waitlist. The quantity dropdown will show a range from 1 to the purchase limit that was entered as by the user.

Additional restrictions are put in place to prevent customers from over-ordering. Once a customer joins a waitlist for a particular product, they will not be able to join again using the same email address.

Users are able to see a list of all of the customers that have joined the waitlist, their email addresses, and the amount the customer ordered by navigating to the Manage Waitlist page from the dashboard. Customer and order product totals are displayed at the top of the page for a quick snapshot view.

<p align="middle">
  <img src="/images/manage_waitlist.png" width="600" />
</p>

# Built With
Python, Flask, HTML, CSS, Materialize

# Installation
Activate your Flask virtual environment.

Navigate to the downloaded folder in your terminal. Run the following command.

‘’’ $ python3 app.py ‘’’

Go to localhost:5000/dashboard in your web browser.
