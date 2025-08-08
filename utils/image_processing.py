"""Image processing utilities for uploaded images."""
import os
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime
import logging

def process_uploaded_image(file_storage, max_size=(1200, 1200), thumbnail_size=(300, 300)):
    """
    Process uploaded image: create original, WebP, and thumbnail versions.
    
    Args:
        file_storage: Flask FileStorage object
        max_size: Maximum dimensions for the main image
        thumbnail_size: Dimensions for thumbnail
        
    Returns:
        Dictionary with filenames or None if processing failed
    """
    try:
        # Ensure upload directory exists
        upload_dir = 'static/images'
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_filename = secure_filename(file_storage.filename)
        name, ext = os.path.splitext(original_filename)
        
        # Clean the name
        name = name.lower().replace(' ', '-')
        
        # Create filenames
        base_name = f"{name}_{timestamp}"
        original_path = os.path.join(upload_dir, f"{base_name}{ext}")
        webp_path = os.path.join(upload_dir, f"{base_name}.webp")
        thumb_path = os.path.join(upload_dir, f"{base_name}_thumb.webp")
        
        # Open and process image
        img = Image.open(file_storage)
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create a white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Save original (with size limit)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(original_path, optimize=True, quality=85)
        
        # Create WebP version
        img.save(webp_path, 'WEBP', optimize=True, quality=80)
        
        # Create thumbnail
        thumb = img.copy()
        thumb.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        thumb.save(thumb_path, 'WEBP', optimize=True, quality=75)
        
        # Return relative paths for database storage
        return {
            'original': f"{base_name}{ext}",
            'webp': f"{base_name}.webp",
            'thumbnail': f"{base_name}_thumb.webp"
        }
        
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return None

def generate_webp_for_existing(image_path):
    """
    Generate WebP version for existing images.
    
    Args:
        image_path: Path to the existing image
        
    Returns:
        WebP filename or None if failed
    """
    try:
        if not os.path.exists(image_path):
            return None
        
        # Open image
        img = Image.open(image_path)
        
        # Convert if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Generate WebP path
        name, _ = os.path.splitext(image_path)
        webp_path = f"{name}.webp"
        
        # Save as WebP
        img.save(webp_path, 'WEBP', optimize=True, quality=80)
        
        return os.path.basename(webp_path)
        
    except Exception as e:
        logging.error(f"Error generating WebP: {e}")
        return None

def batch_generate_webp():
    """Generate WebP versions for all existing images."""
    image_dir = 'static/images'
    supported_formats = ('.jpg', '.jpeg', '.png')
    converted = []
    
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(supported_formats):
            filepath = os.path.join(image_dir, filename)
            webp_name = generate_webp_for_existing(filepath)
            if webp_name:
                converted.append((filename, webp_name))
                logging.info(f"Generated WebP for {filename}")
    
    return converted