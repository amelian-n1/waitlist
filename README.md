# Waitlist

# Goals

•	My goal is to create an open source tool for online sellers to add a waitlist feature to their website for customers to order from incoming shipments. This will allow customers to secure their order ahead of time and ensure access to high demand items.

•	Additionally, the tool will help sellers manage demand by giving them the option to place limits on how many items a customer can order.

•	The tool should easily integrate into a seller’s current business processes, allowing them to better serve their customers while increasing profits.

# Background and Strategic Fit

The current pandemic has greatly altered customers shopping habits both online and in store. The hoarding of essential products like toilet paper, food, medications, and cleaning supplies caused worry and panic amongst shoppers. More customers are choosing to shop online gather than risk contracting COVID-19 by shopping in store.

Most ecommerce websites do not have a waitlist option for customers. A waitlist would allow the customers in dire need of certain products to guarantee they would receive them at some point. It would also save customers time by avoiding having to constantly check back to see if a product is back in stock. Additionally, sellers should be able limit purchase quantities to prevent people from hoarding essential products. 

# Workflow



<img align="right" src="/images/event_form.png" width="350" />

We set out to build an easy to use RSVP form creator for users to invite friends to their events and keep track of RSVPs. Rather than sending an invitation to a hand picked list of Facebook friends, users would distribute the evites themselves over email or text - whatever way they could most easily reach their desired guests.

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
