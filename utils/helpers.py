"""Helper functions for the application."""
import re
import os
from datetime import datetime
from typing import Tuple, Optional, Dict, Any

def clean_description_and_extract_allergens(description: str) -> Tuple[str, str]:
    """
    Separate allergen info from description.
    
    Args:
        description: Full description text that may contain allergen info
        
    Returns:
        Tuple of (clean_description, allergens)
    """
    if not description:
        return '', ''
    
    # Look for allergen patterns like "Allergener: 1,2,3"
    allergen_match = re.search(r'[.\s]*Allergener?:\s*([0-9,\s]+)', description, re.IGNORECASE)
    if allergen_match:
        allergens = allergen_match.group(1).strip()
        # Remove allergen info from description
        clean_desc = re.sub(r'[.\s]*Allergener?:\s*[0-9,\s]+', '', description, flags=re.IGNORECASE).strip().rstrip('.')
        return clean_desc, allergens
    
    return description, ''

def format_price(price: str) -> str:
    """
    Format price for display.
    
    Args:
        price: Price string
        
    Returns:
        Formatted price with kr suffix
    """
    if not price:
        return ''
    
    # Remove any existing 'kr' suffix
    price = re.sub(r'\s*kr\.?\s*$', '', price, flags=re.IGNORECASE)
    
    # Add space and kr
    return f"{price} kr"

def get_allergen_list() -> Dict[str, str]:
    """
    Get the standard allergen list for Norway.
    
    Returns:
        Dictionary mapping allergen numbers to descriptions
    """
    return {
        '1': 'Gluten',
        '2': 'Skalldyr',
        '3': 'Egg',
        '4': 'Fisk',
        '5': 'Peanøtter',
        '6': 'Soya',
        '7': 'Melk/Laktose',
        '8': 'Nøtter',
        '9': 'Selleri',
        '10': 'Sennep',
        '11': 'Sesamfrø',
        '12': 'Svoveldioksid/Sulfitt',
        '13': 'Lupin',
        '14': 'Bløtdyr'
    }

def parse_allergens(allergen_string: str) -> list:
    """
    Parse allergen string into list of allergen names.
    
    Args:
        allergen_string: Comma-separated allergen numbers
        
    Returns:
        List of allergen names
    """
    if not allergen_string:
        return []
    
    allergen_map = get_allergen_list()
    allergen_numbers = [num.strip() for num in allergen_string.split(',')]
    
    return [allergen_map.get(num, f"Allergen {num}") for num in allergen_numbers if num]

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove non-alphanumeric characters except dots and hyphens
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with hyphens
    filename = re.sub(r'\s+', '-', filename)
    # Remove multiple consecutive dots
    filename = re.sub(r'\.+', '.', filename)
    
    return filename.lower()

def generate_unique_filename(original_filename: str, prefix: str = '') -> str:
    """
    Generate a unique filename with timestamp.
    
    Args:
        original_filename: Original filename
        prefix: Optional prefix for the filename
        
    Returns:
        Unique filename
    """
    name, ext = os.path.splitext(original_filename)
    name = sanitize_filename(name)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if prefix:
        return f"{prefix}_{name}_{timestamp}{ext}"
    
    return f"{name}_{timestamp}{ext}"

def format_norwegian_date(date: datetime) -> str:
    """
    Format date in Norwegian style.
    
    Args:
        date: Datetime object
        
    Returns:
        Formatted date string
    """
    if not date:
        return ''
    
    months = {
        1: 'januar', 2: 'februar', 3: 'mars', 4: 'april',
        5: 'mai', 6: 'juni', 7: 'juli', 8: 'august',
        9: 'september', 10: 'oktober', 11: 'november', 12: 'desember'
    }
    
    return f"{date.day}. {months[date.month]} {date.year}"

def truncate_text(text: str, length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= length:
        return text
    
    # Try to break at a word boundary
    truncated = text[:length].rsplit(' ', 1)[0]
    
    # If we couldn't find a space, just truncate at the length
    if not truncated:
        truncated = text[:length]
    
    return truncated + suffix

def is_valid_norwegian_phone(phone: str) -> bool:
    """
    Validate Norwegian phone number.
    
    Args:
        phone: Phone number string
        
    Returns:
        True if valid Norwegian phone number
    """
    # Remove spaces and dashes
    phone = re.sub(r'[\s-]', '', phone)
    
    # Check for Norwegian phone patterns
    # +47 followed by 8 digits or just 8 digits
    patterns = [
        r'^\+47\d{8}$',
        r'^47\d{8}$',
        r'^\d{8}$'
    ]
    
    return any(re.match(pattern, phone) for pattern in patterns)

def format_norwegian_phone(phone: str) -> str:
    """
    Format Norwegian phone number for display.
    
    Args:
        phone: Phone number string
        
    Returns:
        Formatted phone number
    """
    # Remove all non-digit characters except +
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Add +47 if not present
    if not phone.startswith('+47') and not phone.startswith('47'):
        if len(phone) == 8:
            phone = '+47 ' + phone
    elif phone.startswith('47'):
        phone = '+' + phone
    
    # Format with spaces
    if phone.startswith('+47'):
        digits = phone[3:]
        if len(digits) == 8:
            return f"+47 {digits[:2]} {digits[2:4]} {digits[4:6]} {digits[6:]}"
    
    return phone