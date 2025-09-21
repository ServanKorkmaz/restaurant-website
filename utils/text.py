"""Text processing utilities for the restaurant website."""

import re


def clean_description_and_extract_allergens(description):
    """
    Separate allergen information from description.
    
    Args:
        description (str): Original description that may contain allergen info
        
    Returns:
        tuple: (cleaned_description, allergen_info)
    """
    if not description:
        return "", ""
    
    # Look for allergen patterns like "Allergener: 1,2,3"
    allergen_pattern = r"Allergener:\s*([\d,\s]+)"
    allergen_match = re.search(allergen_pattern, description, re.IGNORECASE)
    
    if allergen_match:
        allergen_info = allergen_match.group(1).strip()
        # Remove allergen info from description
        cleaned_desc = re.sub(allergen_pattern, "", description, flags=re.IGNORECASE)
        cleaned_desc = cleaned_desc.strip()
        # Clean up any trailing punctuation or whitespace
        cleaned_desc = re.sub(r'\s*[.,;]\s*$', '', cleaned_desc)
        return cleaned_desc, allergen_info
    
    return description, ""