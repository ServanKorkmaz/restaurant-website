"""Generate WebP versions for existing images."""
from utils.image_processing import batch_generate_webp

if __name__ == "__main__":
    print("Generating WebP versions for existing images...")
    converted = batch_generate_webp()
    print(f"Successfully converted {len(converted)} images to WebP format")
    for original, webp in converted:
        print(f"  - {original} -> {webp}")