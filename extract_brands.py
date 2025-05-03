# Define a list of common brands
common_brands = [
    "breville", "dewalt", "samsung", "gmktec", "xtool", "pipishell", "evenflo",
    "dji", "philips", "dyson", "panasonic", "jbl", "de'longhi", "ninja", "asus",
    "good start", "amazon", "garmin", "hp", "bissell", "grace & stella", "coway",
    "lg", "acer", "ecobee", "napoleon", "epson", "sharkninja", "wd", "boost", "galaxy"
]

# Define brand mapping
brand_mapping = {"galaxy": "Samsung"}

def extract_brand(title):
    title_lower = title.lower()
    # Manual check
    for brand in common_brands:
        if brand in title_lower:
            for word in title.split():
                if brand in word.lower():
                    return brand_mapping.get(brand, word)
    
    # If not matched in the brand pool, extract the first word in the title as the brand
    first_word = title.split()[0] if title and title.split() else "Unknown"
    return f"{first_word}_unchecked"