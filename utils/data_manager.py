"""
Data management utilities for the Book API.
Provides functions for managing data files, backups, and resets.
"""

import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any
from config import Config

class DataManager:
    """Utility class for managing data operations"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
    
    def backup_data(self, backup_name: str = None) -> Dict[str, Any]:
        """Create a backup of current data files"""
        if backup_name is None:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_dir = f"backups/{backup_name}"
        
        try:
            # Create backup directory
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup books file
            if os.path.exists(self.config.BOOKS_FILE):
                shutil.copy2(self.config.BOOKS_FILE, f"{backup_dir}/books.json")
            
            # Backup authors file
            if os.path.exists(self.config.AUTHORS_FILE):
                shutil.copy2(self.config.AUTHORS_FILE, f"{backup_dir}/authors.json")
            
            return {
                "success": True,
                "message": f"Backup created successfully: {backup_dir}",
                "backup_path": backup_dir,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create backup: {str(e)}"
            }
    
    def reset_to_defaults(self) -> Dict[str, Any]:
        """Reset data files to default values"""
        try:
            # Backup current data first
            backup_result = self.backup_data("before_reset")
            
            # Reset books
            if os.path.exists(self.config.DEFAULT_BOOKS_FILE):
                shutil.copy2(self.config.DEFAULT_BOOKS_FILE, self.config.BOOKS_FILE)
            
            # Reset authors
            if os.path.exists(self.config.DEFAULT_AUTHORS_FILE):
                shutil.copy2(self.config.DEFAULT_AUTHORS_FILE, self.config.AUTHORS_FILE)
            
            return {
                "success": True,
                "message": "Data reset to defaults successfully",
                "backup_created": backup_result["success"],
                "backup_path": backup_result.get("backup_path"),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to reset data: {str(e)}"
            }
    
    def get_data_stats(self) -> Dict[str, Any]:
        """Get statistics about current data"""
        try:
            stats = {
                "books_count": 0,
                "authors_count": 0,
                "books_file_size": 0,
                "authors_file_size": 0,
                "last_modified": {}
            }
            
            # Books stats
            if os.path.exists(self.config.BOOKS_FILE):
                with open(self.config.BOOKS_FILE, 'r', encoding='utf-8') as f:
                    books = json.load(f)
                    stats["books_count"] = len(books)
                stats["books_file_size"] = os.path.getsize(self.config.BOOKS_FILE)
                stats["last_modified"]["books"] = datetime.fromtimestamp(
                    os.path.getmtime(self.config.BOOKS_FILE)
                ).isoformat()
            
            # Authors stats
            if os.path.exists(self.config.AUTHORS_FILE):
                with open(self.config.AUTHORS_FILE, 'r', encoding='utf-8') as f:
                    authors = json.load(f)
                    stats["authors_count"] = len(authors)
                stats["authors_file_size"] = os.path.getsize(self.config.AUTHORS_FILE)
                stats["last_modified"]["authors"] = datetime.fromtimestamp(
                    os.path.getmtime(self.config.AUTHORS_FILE)
                ).isoformat()
            
            return {
                "success": True,
                "data": stats,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get data stats: {str(e)}"
            }
    
    def export_data(self, format: str = "json") -> Dict[str, Any]:
        """Export current data in specified format"""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "books": [],
                "authors": []
            }
            
            # Export books
            if os.path.exists(self.config.BOOKS_FILE):
                with open(self.config.BOOKS_FILE, 'r', encoding='utf-8') as f:
                    export_data["books"] = json.load(f)
            
            # Export authors
            if os.path.exists(self.config.AUTHORS_FILE):
                with open(self.config.AUTHORS_FILE, 'r', encoding='utf-8') as f:
                    export_data["authors"] = json.load(f)
            
            # Save export file
            export_filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(export_filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return {
                "success": True,
                "message": f"Data exported successfully: {export_filename}",
                "export_file": export_filename,
                "books_count": len(export_data["books"]),
                "authors_count": len(export_data["authors"])
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to export data: {str(e)}"
            }
    
    def import_data(self, import_file: str) -> Dict[str, Any]:
        """Import data from a backup or export file"""
        try:
            if not os.path.exists(import_file):
                return {
                    "success": False,
                    "error": f"Import file not found: {import_file}"
                }
            
            # Backup current data first
            backup_result = self.backup_data("before_import")
            
            with open(import_file, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Import books
            if "books" in import_data and isinstance(import_data["books"], list):
                with open(self.config.BOOKS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(import_data["books"], f, indent=2, ensure_ascii=False)
            
            # Import authors
            if "authors" in import_data and isinstance(import_data["authors"], list):
                with open(self.config.AUTHORS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(import_data["authors"], f, indent=2, ensure_ascii=False)
            
            return {
                "success": True,
                "message": f"Data imported successfully from: {import_file}",
                "backup_created": backup_result["success"],
                "backup_path": backup_result.get("backup_path"),
                "imported_books": len(import_data.get("books", [])),
                "imported_authors": len(import_data.get("authors", []))
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to import data: {str(e)}"
            } 