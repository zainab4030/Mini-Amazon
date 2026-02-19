# Mini-Amazon
console-based e-commerce application built using Python

Project Overview

Mini-Amazon allows users to:

Create an account

Log into the system

Browse available products

Search products (case-insensitive)

Add and remove items from a shopping cart

Checkout and generate an order receipt

View order history

All user data, product data, cart data, and orders are saved permanently using JSON files.

🚀 Features Implemented
👤 User System

User registration with unique username validation

Password minimum length validation

Login authentication

Persistent user storage (users.json)

🛍 Product Catalog

List all available products

Search products by keyword (case-insensitive)

View product price and stock

Stock validation during cart addition

Persistent product storage (products.json)

🛒 Cart System

Add items to cart

Remove items from cart

View cart with subtotal and total calculation

Cart linked to each logged-in user

Persistent cart storage (carts.json)

💳 Checkout System

Re-validates stock before purchase

Deducts stock from products after purchase

Generates unique Order ID

Stores order history with timestamp

Clears cart after successful checkout

Persistent order storage (orders.json)
