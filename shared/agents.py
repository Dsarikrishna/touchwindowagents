"""
TouchWindow AI Agents - Working Implementations
Uses free public APIs for demonstration purposes.
"""
import logging
import requests
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Free Public APIs (no API key required)
DUMMYJSON_BASE = "https://dummyjson.com"
FAKESTORE_BASE = "https://fakestoreapi.com"
JSONPLACEHOLDER_BASE = "https://jsonplaceholder.typicode.com"

# ----- Agent 1: Order Processing Agent -----
def run_order_processing_agent() -> Dict[str, Any]:
    """
    Order Processing Agent - Fetches and analyzes orders from DummyJSON.
    Validates pricing, calculates margins, identifies issues.
    """
    logger.info("[OrderProcessingAgent] Running at %s", datetime.utcnow())
    results = {
        "status": "success",
        "orders_processed": 0,
        "total_revenue": 0.0,
        "alerts": [],
        "order_details": []
    }
    
    try:
        # Fetch carts (simulated orders) from DummyJSON
        response = requests.get(f"{DUMMYJSON_BASE}/carts", timeout=10)
        response.raise_for_status()
        data = response.json()
        carts = data.get("carts", [])
        
        for cart in carts:
            order_total = cart.get("total", 0)
            discount = cart.get("discountedTotal", order_total)
            results["total_revenue"] += discount
            results["orders_processed"] += 1
            
            # Calculate margin (simulated)
            cost = order_total * 0.6  # Assume 60% cost
            margin = ((discount - cost) / discount * 100) if discount > 0 else 0
            
            results["order_details"].append({
                "order_id": cart.get("id"),
                "total": order_total,
                "discounted": discount,
                "margin_pct": round(margin, 2),
                "products": len(cart.get("products", []))
            })
            
            # Alert if margin below threshold
            if margin < 10 and margin > 0:
                results["alerts"].append({
                    "order_id": cart.get("id"),
                    "issue": "Margin below 10%",
                    "margin": f"{round(margin, 2)}%"
                })
        
        results["total_revenue"] = round(results["total_revenue"], 2)
        logger.info("[OrderProcessingAgent] Processed %d orders, Revenue: $%.2f",
                   results["orders_processed"], results["total_revenue"])
                   
    except Exception as e:
        logger.error("[OrderProcessingAgent] Error: %s", str(e))
        results["status"] = "error"
        results["error"] = str(e)
    
    return results


# ----- Agent 2: Product Agent -----
def run_product_agent() -> Dict[str, Any]:
    """
    Product Agent - Analyzes product catalog from FakeStoreAPI.
    Tracks categories, ratings, and price ranges.
    """
    logger.info("[ProductAgent] Running at %s", datetime.utcnow())
    results = {
        "status": "success",
        "total_products": 0,
        "categories": {},
        "avg_rating": 0.0,
        "price_range": {"min": 0, "max": 0},
        "top_rated": [],
        "alerts": []
    }
    
    try:
        response = requests.get(f"{FAKESTORE_BASE}/products", timeout=10)
        response.raise_for_status()
        products = response.json()
        
        results["total_products"] = len(products)
        ratings = []
        prices = []
        
        for product in products:
            # Track categories
            category = product.get("category", "Unknown")
            results["categories"][category] = results["categories"].get(category, 0) + 1
            
            # Track ratings
            rating = product.get("rating", {}).get("rate", 0)
            ratings.append(rating)
            
            # Track prices
            price = product.get("price", 0)
            prices.append(price)
            
            # Top rated products (rating >= 4.5)
            if rating >= 4.5:
                results["top_rated"].append({
                    "id": product.get("id"),
                    "title": product.get("title", "")[:50],
                    "rating": rating,
                    "price": price
                })
            
            # Alert for low-rated products
            if rating < 2.5 and rating > 0:
                results["alerts"].append({
                    "product_id": product.get("id"),
                    "issue": "Low rating product",
                    "rating": rating
                })
        
        if ratings:
            results["avg_rating"] = round(sum(ratings) / len(ratings), 2)
        if prices:
            results["price_range"] = {"min": min(prices), "max": max(prices)}
            
        logger.info("[ProductAgent] Analyzed %d products across %d categories",
                   results["total_products"], len(results["categories"]))
                   
    except Exception as e:
        logger.error("[ProductAgent] Error: %s", str(e))
        results["status"] = "error"
        results["error"] = str(e)
    
    return results


# ----- Agent 3: Efficiency Agent -----
def run_efficiency_agent() -> Dict[str, Any]:
    """
    Efficiency Agent - Monitors API health and response times.
    Simulates system efficiency checks.
    """
    logger.info("[EfficiencyAgent] Running at %s", datetime.utcnow())
    results = {
        "status": "success",
        "checks_performed": 0,
        "avg_response_time_ms": 0,
        "endpoints_checked": [],
        "alerts": []
    }
    
    endpoints = [
        (DUMMYJSON_BASE + "/products?limit=1", "DummyJSON Products"),
        (FAKESTORE_BASE + "/products/1", "FakeStore Product"),
        (JSONPLACEHOLDER_BASE + "/posts/1", "JSONPlaceholder Post"),
    ]
    
    response_times = []
    
    for url, name in endpoints:
        try:
            start = datetime.now()
            response = requests.get(url, timeout=10)
            elapsed = (datetime.now() - start).total_seconds() * 1000
            
            results["endpoints_checked"].append({
                "name": name,
                "url": url,
                "status_code": response.status_code,
                "response_time_ms": round(elapsed, 2),
                "healthy": response.status_code == 200
            })
            
            if response.status_code == 200:
                response_times.append(elapsed)
            else:
                results["alerts"].append({
                    "endpoint": name,
                    "issue": f"Non-200 status: {response.status_code}"
                })
            
            if elapsed > 2000:
                results["alerts"].append({
                    "endpoint": name,
                    "issue": f"Slow response: {round(elapsed)}ms"
                })
                
            results["checks_performed"] += 1
            
        except Exception as e:
            results["endpoints_checked"].append({
                "name": name,
                "url": url,
                "status_code": 0,
                "response_time_ms": 0,
                "healthy": False,
                "error": str(e)
            })
            results["alerts"].append({
                "endpoint": name,
                "issue": f"Connection failed: {str(e)}"
            })
    
    if response_times:
        results["avg_response_time_ms"] = round(sum(response_times) / len(response_times), 2)
    
    logger.info("[EfficiencyAgent] Checked %d endpoints, Avg response: %.2fms",
               results["checks_performed"], results["avg_response_time_ms"])
    
    return results


# ----- Agent 4: Competition Minder Agent -----
def run_competition_minder_agent() -> Dict[str, Any]:
    """
    Competition Minder Agent - Compares prices across different sources.
    Simulates competitor price monitoring.
    """
    logger.info("[CompetitionMinderAgent] Running at %s", datetime.utcnow())
    results = {
        "status": "success",
        "products_compared": 0,
        "price_differences": [],
        "avg_price_diff_pct": 0.0,
        "alerts": []
    }
    
    try:
        # Get products from FakeStore (our prices)
        our_response = requests.get(f"{FAKESTORE_BASE}/products?limit=5", timeout=10)
        our_response.raise_for_status()
        our_products = our_response.json()
        
        # Get products from DummyJSON (competitor prices)
        comp_response = requests.get(f"{DUMMYJSON_BASE}/products?limit=5", timeout=10)
        comp_response.raise_for_status()
        comp_data = comp_response.json()
        comp_products = comp_data.get("products", [])
        
        # Compare similar product categories
        price_diffs = []
        for i, our_prod in enumerate(our_products[:5]):
            if i < len(comp_products):
                comp_prod = comp_products[i]
                our_price = our_prod.get("price", 0)
                comp_price = comp_prod.get("price", 0)
                
                if our_price > 0:
                    diff_pct = ((comp_price - our_price) / our_price) * 100
                    price_diffs.append(diff_pct)
                    
                    results["price_differences"].append({
                        "our_product": our_prod.get("title", "")[:30],
                        "our_price": our_price,
                        "competitor_price": comp_price,
                        "difference_pct": round(diff_pct, 2)
                    })
                    
                    # Alert if competitor is significantly cheaper
                    if diff_pct < -15:
                        results["alerts"].append({
                            "product": our_prod.get("title", "")[:30],
                            "issue": f"Competitor {abs(round(diff_pct))}% cheaper"
                        })
                    
                    results["products_compared"] += 1
        
        if price_diffs:
            results["avg_price_diff_pct"] = round(sum(price_diffs) / len(price_diffs), 2)
        
        logger.info("[CompetitionMinderAgent] Compared %d products", results["products_compared"])
        
    except Exception as e:
        logger.error("[CompetitionMinderAgent] Error: %s", str(e))
        results["status"] = "error"
        results["error"] = str(e)
    
    return results


# ----- Agent 5: Customer Minder Agent -----
def run_customer_minder_agent() -> Dict[str, Any]:
    """
    Customer Minder Agent - Analyzes customer data and order patterns.
    Identifies top customers and opportunities.
    """
    logger.info("[CustomerMinderAgent] Running at %s", datetime.utcnow())
    results = {
        "status": "success",
        "total_customers": 0,
        "customers_by_region": {},
        "top_customers": [],
        "alerts": []
    }
    
    try:
        # Get users from DummyJSON
        response = requests.get(f"{DUMMYJSON_BASE}/users?limit=20", timeout=10)
        response.raise_for_status()
        data = response.json()
        users = data.get("users", [])
        
        results["total_customers"] = len(users)
        
        # Get carts to calculate customer value
        carts_response = requests.get(f"{DUMMYJSON_BASE}/carts", timeout=10)
        carts_response.raise_for_status()
        carts_data = carts_response.json()
        carts = carts_data.get("carts", [])
        
        # Map user spending
        user_spending = {}
        for cart in carts:
            user_id = cart.get("userId")
            total = cart.get("discountedTotal", cart.get("total", 0))
            user_spending[user_id] = user_spending.get(user_id, 0) + total
        
        for user in users:
            # Track by region
            city = user.get("address", {}).get("city", "Unknown")
            state = user.get("address", {}).get("state", "Unknown")
            region = f"{city}, {state}"
            results["customers_by_region"][region] = results["customers_by_region"].get(region, 0) + 1
            
            user_id = user.get("id")
            spending = user_spending.get(user_id, 0)
            
            # Top customers
            if spending > 100:
                results["top_customers"].append({
                    "id": user_id,
                    "name": f"{user.get('firstName', '')} {user.get('lastName', '')}",
                    "email": user.get("email", ""),
                    "total_spent": round(spending, 2)
                })
        
        # Sort top customers
        results["top_customers"] = sorted(
            results["top_customers"],
            key=lambda x: x["total_spent"],
            reverse=True
        )[:10]
        
        logger.info("[CustomerMinderAgent] Analyzed %d customers", results["total_customers"])
        
    except Exception as e:
        logger.error("[CustomerMinderAgent] Error: %s", str(e))
        results["status"] = "error"
        results["error"] = str(e)
    
    return results


# ----- Agent 6: Supplier Minder Agent -----
def run_supplier_minder_agent() -> Dict[str, Any]:
    """
    Supplier Minder Agent - Monitors supplier activity and inventory.
    Tracks product availability and supplier performance.
    """
    logger.info("[SupplierMinderAgent] Running at %s", datetime.utcnow())
    results = {
        "status": "success",
        "suppliers_monitored": 0,
        "products_tracked": 0,
        "inventory_alerts": [],
        "supplier_status": []
    }
    
    try:
        # Use product categories as "suppliers"
        response = requests.get(f"{DUMMYJSON_BASE}/products?limit=30", timeout=10)
        response.raise_for_status()
        data = response.json()
        products = data.get("products", [])
        
        results["products_tracked"] = len(products)
        
        # Group by brand (simulated supplier)
        suppliers = {}
        for product in products:
            brand = product.get("brand", "Generic")
            if brand not in suppliers:
                suppliers[brand] = {
                    "name": brand,
                    "products": 0,
                    "avg_rating": [],
                    "avg_stock": [],
                    "total_value": 0
                }
            suppliers[brand]["products"] += 1
            suppliers[brand]["avg_rating"].append(product.get("rating", 0))
            suppliers[brand]["avg_stock"].append(product.get("stock", 0))
            suppliers[brand]["total_value"] += product.get("price", 0)
        
        for brand, info in suppliers.items():
            avg_rating = sum(info["avg_rating"]) / len(info["avg_rating"]) if info["avg_rating"] else 0
            avg_stock = sum(info["avg_stock"]) / len(info["avg_stock"]) if info["avg_stock"] else 0
            
            supplier_info = {
                "supplier": brand,
                "products": info["products"],
                "avg_rating": round(avg_rating, 2),
                "avg_stock": round(avg_stock),
                "total_value": round(info["total_value"], 2)
            }
            results["supplier_status"].append(supplier_info)
            
            # Low stock alert
            if avg_stock < 20:
                results["inventory_alerts"].append({
                    "supplier": brand,
                    "issue": f"Low average stock: {round(avg_stock)}",
                    "priority": "high" if avg_stock < 10 else "medium"
                })
            
            # Low rating alert
            if avg_rating < 3.5 and avg_rating > 0:
                results["inventory_alerts"].append({
                    "supplier": brand,
                    "issue": f"Low supplier rating: {round(avg_rating, 1)}",
                    "priority": "medium"
                })
        
        results["suppliers_monitored"] = len(suppliers)
        
        # Sort by total value
        results["supplier_status"] = sorted(
            results["supplier_status"],
            key=lambda x: x["total_value"],
            reverse=True
        )[:10]
        
        logger.info("[SupplierMinderAgent] Monitored %d suppliers, %d products",
                   results["suppliers_monitored"], results["products_tracked"])
        
    except Exception as e:
        logger.error("[SupplierMinderAgent] Error: %s", str(e))
        results["status"] = "error"
        results["error"] = str(e)
    
    return results


# Test all agents when run directly
if __name__ == "__main__":
    print("=" * 60)
    print("Testing TouchWindow AI Agents with Free Public APIs")
    print("=" * 60)
    
    import json
    
    agents = [
        ("Order Processing Agent", run_order_processing_agent),
        ("Product Agent", run_product_agent),
        ("Efficiency Agent", run_efficiency_agent),
        ("Competition Minder Agent", run_competition_minder_agent),
        ("Customer Minder Agent", run_customer_minder_agent),
        ("Supplier Minder Agent", run_supplier_minder_agent),
    ]
    
    for name, func in agents:
        print(f"\n{'='*60}")
        print(f"Testing: {name}")
        print("=" * 60)
        result = func()
        print(json.dumps(result, indent=2, default=str)[:1000])
        print("..." if len(json.dumps(result)) > 1000 else "")
