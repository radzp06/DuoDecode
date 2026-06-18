# AICreator Flow - Centralized Affiliate Link Routing Configuration

AFFILIATE_ROUTING_ENGINE = {
    "default": {
        "amazon": "https://www.amazon.in/s?k=fashion+accessories",
        "zepto": "https://www.zeptonow.com"
    },
    "categories": {
        "beach": {
            "keywords": ["beach", "goa", "mumbai", "sea", "pool", "vacation"],
            "amazon": "https://www.amazon.in/s?k=polarized+sunglasses+for+men+women",
            "zepto": "https://www.zeptonow.com/search?q=sunscreen"
        },
        "formal": {
            "keywords": ["interview", "formal", "corporate", "office", "presentation", "meeting"],
            "amazon": "https://www.amazon.in/s?k=leather+belt+and+wallet+combo",
            "zepto": "https://www.zeptonow.com/search?q=perfume"
        },
        "party": {
            "keywords": ["party", "fest", "club", "gala", "concert", "evening"],
            "amazon": "https://www.amazon.in/s?k=unisex+silver+aesthetic+chain",
            "zepto": "https://www.zeptonow.com/search?q=hair+wax"
        }
    }
}

def get_smart_links(user_occasion_input):
    """Analyzes user text input and returns targeted rapid-delivery links"""
    query = user_occasion_input.lower()
    
    for key, category in AFFILIATE_ROUTING_ENGINE["categories"].items():
        if any(keyword in query for keyword in category["keywords"]):
            print(f"[AICreator Flow] Matching destination profile routing activated: {key}")
            return {"amazon": category["amazon"], "zepto": category["zepto"]}
            
    return AFFILIATE_ROUTING_ENGINE["default"]