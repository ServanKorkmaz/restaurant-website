"""Database backup utilities."""
import os
import shutil
from datetime import datetime
import logging

def create_backup(db_path='instance/restaurant.db', backup_dir='backups'):
    """
    Create a timestamped backup of the database.
    
    Args:
        db_path: Path to the database file
        backup_dir: Directory to store backups
        
    Returns:
        Backup filename if successful
    """
    try:
        # Ensure backup directory exists
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy database file
        if os.path.exists(db_path):
            shutil.copy2(db_path, backup_path)
            logging.info(f"Backup created: {backup_filename}")
            
            # Clean old backups (keep last 30)
            clean_old_backups(backup_dir, keep_count=30)
            
            return backup_filename
        else:
            logging.error(f"Database file not found: {db_path}")
            return None
            
    except Exception as e:
        logging.error(f"Backup failed: {e}")
        raise

def restore_backup(backup_filename, backup_dir='backups', db_path='instance/restaurant.db'):
    """
    Restore database from a backup file.
    
    Args:
        backup_filename: Name of the backup file
        backup_dir: Directory containing backups
        db_path: Target database path
        
    Returns:
        True if successful
    """
    try:
        backup_path = os.path.join(backup_dir, backup_filename)
        
        if not os.path.exists(backup_path):
            logging.error(f"Backup file not found: {backup_path}")
            return False
        
        # Create a backup of current database before restoring
        if os.path.exists(db_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pre_restore_backup = os.path.join(backup_dir, f"pre_restore_{timestamp}.db")
            shutil.copy2(db_path, pre_restore_backup)
        
        # Restore the backup
        shutil.copy2(backup_path, db_path)
        logging.info(f"Database restored from: {backup_filename}")
        
        return True
        
    except Exception as e:
        logging.error(f"Restore failed: {e}")
        return False

def clean_old_backups(backup_dir='backups', keep_count=30):
    """
    Remove old backup files, keeping only the most recent ones.
    
    Args:
        backup_dir: Directory containing backups
        keep_count: Number of backups to keep
    """
    try:
        # Get all backup files
        backup_files = [
            f for f in os.listdir(backup_dir)
            if f.startswith('backup_') and f.endswith('.db')
        ]
        
        # Sort by modification time
        backup_files.sort(
            key=lambda f: os.path.getmtime(os.path.join(backup_dir, f)),
            reverse=True
        )
        
        # Remove old backups
        for old_backup in backup_files[keep_count:]:
            os.remove(os.path.join(backup_dir, old_backup))
            logging.info(f"Removed old backup: {old_backup}")
            
    except Exception as e:
        logging.error(f"Error cleaning old backups: {e}")

def get_backup_list(backup_dir='backups'):
    """
    Get list of available backups with metadata.
    
    Args:
        backup_dir: Directory containing backups
        
    Returns:
        List of backup info dictionaries
    """
    backups = []
    
    try:
        if not os.path.exists(backup_dir):
            return backups
        
        for filename in os.listdir(backup_dir):
            if filename.startswith('backup_') and filename.endswith('.db'):
                filepath = os.path.join(backup_dir, filename)
                stat = os.stat(filepath)
                
                backups.append({
                    'filename': filename,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_mtime),
                    'size_mb': round(stat.st_size / (1024 * 1024), 2)
                })
        
        # Sort by creation date (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        
    except Exception as e:
        logging.error(f"Error listing backups: {e}")
    
    return backups