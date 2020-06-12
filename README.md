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

To add additional products, the user would select the Add Product button in the upper right corner.

<p align="middle">
  <img src="/images/add_a_new_product.png" width="600" />
</p>

The user then fills out the new product form. In this form, the user can set a purchase limit that prevents customers from ordering more than the designated amount.

<img align="right" src="/images/customer_waitlist.png" width="300" />

Once the product is submitted, users will be rediretced to the dashboard. Here they have the option to add additional shipments, edit the product information, and edit the shipment information if necessary.

Additionally, a customer-facing waitlist form is automatically created. The form will show the arrival date of the next incoming shipment as the back in stock date. This will allow customers to make an educated decision regarding whether they are willing to wait for this product to become back in stock.

Users would first register their email address and create a password that would be encrypted and stored in the database. This would allow for all of their events to be stored in one secure location.

After registering, users would login and be directed to the Create an event form. Following the Facebook model, users would enter all necessary details of their upcoming event including time, date, location and description.

After clicking submit, the user would be directed to the Dashboard. As the central home of the app, the Dashboard includes all of their events, evites, and quick snapshots of the RSVPs.

Clicking on Event details would show all of the details submitted in the event form and provide a list of all of the RSVPed guests, including their names and email addresses.

Clicking on My evite would open the event invitation with all of their specified details and RSVP form. To make it easy for attendees to find the event location, we added the Google Map API which shows a map of the physical location.

<br>

<p align="middle">
  <img src="/images/dashboard.png" width="600" />
  <img src="/images/event_details.png" width="600" />
  <img src="/images/RSVP.png" width="600" />
</p>

# Built With
Python, Django, HTML, Materialize

# Installation
Activate your Django virtual environment.

Navigate to the downloaded folder in your terminal. Run the following command.

‘’’ $ python manage.py runserver ‘’’

Go to localhost:8000 in your web browser.
