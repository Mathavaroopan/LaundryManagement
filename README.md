A small-scale laundry service provider aims to develop a system for maintaining customer details. The laundry service system should facilitate the creation, viewing, and updating of customer information. When a customer deposits clothes for laundering, the system is expected to generate a unique transaction slip with details such as cloth types, laundry requirements, cost, and delivery date. A transaction is considered closed when a customer completes the payment.

The system is designed to have two login pages—one for the laundry service manager and another for the customer. The following functionalities are expected:

Customer Actions:

    Place an order specifying different types of clothes.
    Complete a transaction while placing the order for it to be accepted.
    View a list of their placed orders.


Laundry Manager Actions:

    View all orders.
    Search for orders using customer usernames.
    View orders within a specified date range, including last week and last month.
    Send messages to specific customers whose clothes have been laundered.
    Send a common message to all customers, e.g., informing them of the unavailability of laundry services today due to rain.
    After delivering an order, remove the order from the specific customer's order variable.


To implement these functionalities, standard design patterns such as singleton, observer, strategy, decorator, template, iterator, comprehension, and generator will be utilized. These patterns contribute to the system's modularity, extensibility, and maintainability, adhering to best practices in software design.
