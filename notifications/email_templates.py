def build_order_created_email(payload):
    items_text = "\n".join(
        f"- {item['name']} × {item['qty']} (₹{item['price']})"
        for item in payload["items"]
    )

    body = f"""
Your order has been placed successfully!

Order ID: {payload['order_id']}
Total Amount: ₹{payload['total_amount']}

Delivery Address:
{payload['address']}

Items:
{items_text}
"""

    return {
        "subject": f"Order Confirmed – #{payload['order_id']}",
        "body": body,
    }


def build_payment_success_email(payload):
    body = f"""
Payment Successful!

Order ID: {payload['order_id']}
Amount Paid: ₹{payload['amount']}
Payment Time: {payload['paid_at']}
"""

    return {
        "subject": f"Payment Successful – Order #{payload['order_id']}",
        "body": body,
    }


def build_email(event, payload):
    if event == "order_created":
        return build_order_created_email(payload)

    if event == "payment_success":
        return build_payment_success_email(payload)

    raise ValueError("Unknown notification event")
