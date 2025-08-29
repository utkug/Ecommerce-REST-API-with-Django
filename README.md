# 🛒 E-Commerce REST API with Django  

A **fully featured e-commerce REST API** built with Django. 🚀  
It provides secure **authentication**, distinct **user roles** (customers, stores, and admins), and essential e-commerce features such as **product & category management**, **shopping cart**, **orders**, and **address management**. 🔐📦  

Designed to be **scalable, secure, and flexible**, this API is a solid foundation for modern e-commerce platforms. ⚡  

## ✨ Key Features  
- 👥 **Role-Based User Management** (Customers, Stores, Admins)  
- 🔑 **Authentication & Authorization** with `dj-rest-auth`  
- 🏪 **Store & Product CRUD Operations**  
- 📂 **Category Management** (Admin only)  
- 🛒 **Shopping Cart** with add, update, and remove items  
- 📦 **Order Processing** for customers & stores  
- 📬 **Address Management** for multiple shipping addresses  
- 🔍 **Filtering & Search Support** for products  

## Features

*   **User Roles:** Distinct roles for Customers and Stores, each with specific permissions.
*   **Authentication:** Secure registration and login for all user types using `dj-rest-auth`.
*   **Product Management:** Full CRUD (Create, Read, Update, Delete) functionality for products, restricted to store owners.
*   **Category Management:** Admins can manage product categories.
*   **Shopping Cart:** Customers can add, view, update, and remove items from their personal shopping cart.
*   **Order Processing:** Customers can place orders from their cart, and stores can view and manage orders for their products.
*   **Address Management:** Customers can save and manage multiple shipping addresses.
*   **Role-Based Permissions:** Granular access control ensures users can only perform actions they are authorized for (e.g., a store owner can only edit their own products).
*   **Filtering & Searching:** Endpoints support filtering (e.g., by price) and searching for products.


## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/utkug/ecommerce-rest-api-with-django.git
    cd ecommerce-rest-api-with-django
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.


## API Endpoints

The API provides the following endpoints. Authentication is required for most write operations.

### Authentication
*   `POST /dj-rest-auth/registration/`: Register a new user. Include `is_customer: true` or `is_store: true`.
*   `POST /dj-rest-auth/login/`: Log in to get an authentication token.
*   `POST /dj-rest-auth/logout/`: Log out and invalidate the token.

### Product Catalog
*   `GET /product/`: List all products. Supports searching (`?search=...`) and ordering.
*   `POST /product/`: Create a new product (Store users only).
*   `GET /product/<id>/`: Retrieve a specific product.
*   `PUT /product/<id>/`: Update a product (Store owner only).
*   `DELETE /product/<id>/`: Delete a product (Store owner only).

### Categories
*   `GET /category/`: List all categories. Supports filtering by product price (`?min_price=...`, `?max_price=...`).
*   `POST /category/`: Create a new category (Admin only).
*   `GET /category/<id>/`: Retrieve a specific category.
*   `PUT /category/<id>/`: Update a category (Admin only).
*   `DELETE /category/<id>/`: Delete a category (Admin only).

### Stores
*   `GET /store/`: List all stores.
*   `GET /store/<id>/`: Retrieve a specific store and its associated products.
*   `PUT /store/<id>/`: Update store information (Store owner only).

### Shopping Cart (Customer only)
*   `GET /cart/`: View all items in the authenticated customer's cart.
*   `POST /cart/`: Add a product to the cart. If the product is already in the cart, the quantity is increased. Requires `product` (ID) and `quantity`.
*   `DELETE /cart/delete-all`: Remove all items from the cart.
*   `DELETE /cart/<id>/delete-one`: Decrease the quantity of a product (with `id`) by one. If quantity becomes zero, the item is removed.

### Addresses (Customer only)
*   `GET /address/`: List all addresses for the authenticated customer.
*   `POST /address/`: Create a new address.
*   `GET /address/<id>/`: Retrieve a specific address.
*   `PUT /address/<id>/`: Update an address.
*   `DELETE /address/<id>/`: Delete an address.

### Orders
#### For Customers:
*   `GET /order/`: List all orders placed by the authenticated customer.
*   `POST /order/`: Create a new order from the items in the cart. Requires an `address` (ID) in the request body. The cart will be cleared upon successful order placement.
*   `GET /order/<id>/`: View the details of a specific order.

#### For Stores:
*   `GET /store-orders`: List all orders that contain products sold by the authenticated store. Supports searching by customer username.
*   `GET /store-orders/<id>/`: Get details for a specific order (`id`).
*   `PUT /store-orders/<order_id>/update`: Update the status of items in an order. Requires `status` (ID) in the request body.