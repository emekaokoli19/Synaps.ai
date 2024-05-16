import random
import json

class AmazonOrderDataGenerator:
    def __init__(self):
        self.product_names = [
            "Laptop", "Headphones", "Book", "Coffee Maker", "Phone Charger",
            "Table", "Chair", "Shoes", "Trousers", "Shirts", "Cupboard"
        ]
        self.order_statuses = ["Shipped", "Delivered", "Pending", "Canceled"]

    def generate_item_details(self):
        item_name = random.choice(self.product_names)
        quantity = random.randint(1, 5)
        price = f"${random.uniform(10, 200):.2f}"
        return {"name": item_name, "quantity": quantity, "price": price}

    def generate_order_data(self):
        order_id = f"D01-{random.randint(1000000, 9999999)}-{random.randint(1000000, 9999999)}"
        order_date = f"{random.randint(2020, 2024)}-{random.randint(1, 12)}-{random.randint(1, 28)}"
        order_total = f"${random.uniform(30, 500):.2f}"
        shipping_address = "123 Mavin St, Anytown, LAG, NG 12345"
        delivery_status = random.choice(self.order_statuses)
        items = [self.generate_item_details() for _ in range(random.randint(1, 5))]  # 1 to 5 items per order
        return {
            "order_id": order_id,
            "order_date": order_date,
            "order_total": order_total,
            "shipping_address": shipping_address,
            "delivery_status": delivery_status,
            "items": items
        }

    def generate_html_snippet(self, order_data, template_variation):
        if template_variation == 1:
            html = f"""<div id="orderDetails">
                        <span class="a-color-secondary" data-a-popover='{{"header": "Order ID"}}'>Order ID:</span> {order_data['order_id']}
                        <span class="a-color-secondary" data-a-popover='{{"header": "Order placed"}}'>Order placed:</span> {order_data['order_date']}
                        <span class="a-color-secondary" data-a-popover='{{"header": "Total"}}'>Total:</span> {order_data['order_total']}
                        <div id="shippingAddressWidget">
                            <span class="displayAddressFullName">John Doe</span>
                            <li class="displayAddressLI"><span>{order_data['shipping_address']}</span></li>
                        </div>
                        <div id="deliveryStatusBarWidget-container">
                            <div class="a-row">{order_data['delivery_status']}</div>
                        </div>
                        <div id="ordersInPackage-container">"""

            for item in order_data["items"]:
                html += f"""
                            <div class="a-fixed-left-grid-inner">
                                <a class="a-link-normal">{item["name"]}</a>
                                <span class="item-view-qty">Qty: {item["quantity"]}</span>
                                <span class="a-offscreen">{item["price"]}</span>
                            </div>"""
            html += """</div>  </div>"""
        elif template_variation == 2:
            # Template 2 (Different class names and structure)
            html = f"""<div class="order-details-section">
                        <h2>Order {order_data['order_id']}</h2>
                        <p>Placed on {order_data['order_date']}</p>
                        <p>Total: {order_data['order_total']}</p>
                        <h3>Shipping Address:</h3>
                        <p>{order_data['shipping_address']}</p>
                        <h3>Delivery Status:</h3>
                        <p>{order_data['delivery_status']}</p>
                        <h3>Items:</h3>
                        <ul>"""
            for item in order_data["items"]:
                html += f"""<li>{item['name']} (Qty: {item['quantity']}, Price: {item['price']})</li>"""
            html += "</ul></div>"
        elif template_variation == 3:
            # Template 3 (New variation with a table layout)
            html = f"""<div id="orderDetailsTable">
                        <table>
                            <tr><th>Order ID:</th><td>{order_data['order_id']}</td></tr>
                            <tr><th>Order Placed:</th><td>{order_data['order_date']}</td></tr>
                            <tr><th>Total:</th><td>{order_data['order_total']}</td></tr>
                            <tr><th>Shipping Address:</th><td>{order_data['shipping_address']}</td></tr>
                            <tr><th>Delivery Status:</th><td>{order_data['delivery_status']}</td></tr>
                            <tr><th colspan="2">Items:</th></tr>"""
            for item in order_data["items"]:
                html += f"""<tr><td>{item['name']}</td><td>Qty: {item['quantity']}, Price: {item['price']}</td></tr>"""
            html += """</table></div>"""
        else:
            raise ValueError("Invalid template variation")

        return html

    def generate_dataset(self, num_examples=1000):
        data = []
        for _ in range(num_examples):
            order_data = self.generate_order_data()
            template_variation = random.randint(1, 3) # Choose random template
            html_snippet = self.generate_html_snippet(order_data, template_variation)
            data.append({
                "html": html_snippet,
                "output": json.dumps(order_data, indent=4)
            })
        return data
