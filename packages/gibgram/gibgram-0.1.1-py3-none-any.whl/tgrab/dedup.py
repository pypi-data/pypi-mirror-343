"""
Media deduplication module for TGrab.

This module provides functionality for detecting and handling duplicate media files.
"""

import os
import json
import hashlib
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

class DedupDatabase:
    """Database for tracking downloaded files to prevent duplicates."""

    def __init__(self, base_folder: str):
        """
        Initialize the deduplication database.

        Args:
            base_folder: Base folder for storing the database file
        """
        self.base_folder = base_folder
        self.db_folder = os.path.join(base_folder, ".tgrab")
        self.db_file = os.path.join(self.db_folder, "dedup_db.json")
        self.db = self._load_db()

    def _load_db(self) -> Dict[str, Any]:
        """
        Load the deduplication database from disk.

        Returns:
            Dict containing the database
        """
        # Create database directory if it doesn't exist
        os.makedirs(self.db_folder, exist_ok=True)

        # Load existing database if it exists
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    db = json.load(f)
                logger.info(f"Loaded deduplication database with {len(db.get('files', []))} entries")
                return db
            except Exception as e:
                logger.warning(f"Error loading deduplication database: {e}")
                # Return empty database if loading fails
                return {"files": [], "version": 1}
        else:
            # Create new database
            return {"files": [], "version": 1}

    def _save_db(self) -> bool:
        """
        Save the deduplication database to disk.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.db_file, 'w') as f:
                json.dump(self.db, f, indent=2)
            logger.info(f"Saved deduplication database with {len(self.db.get('files', []))} entries")
            return True
        except Exception as e:
            logger.error(f"Error saving deduplication database: {e}")
            return False

    def add_file(self, file_path: str, user_id: Optional[int] = None, message_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Add a file to the deduplication database.

        Args:
            file_path: Path to the file
            user_id: ID of the user who sent the file
            message_id: ID of the message containing the file

        Returns:
            Dict with file information
        """
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return {}

        # Get file information
        file_info = self._get_file_info(file_path, user_id, message_id)

        # Add to database
        self.db.setdefault("files", []).append(file_info)

        # Save database
        self._save_db()

        return file_info

    def _get_file_info(self, file_path: str, user_id: Optional[int] = None, message_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get information about a file for deduplication.

        Args:
            file_path: Path to the file
            user_id: ID of the user who sent the file
            message_id: ID of the message containing the file

        Returns:
            Dict with file information
        """
        # Get file stats
        file_stats = os.stat(file_path)
        file_size = file_stats.st_size

        # Calculate file hash
        file_hash = self._calculate_file_hash(file_path)

        # Get relative path
        rel_path = os.path.relpath(file_path, self.base_folder)

        # Create file info
        file_info = {
            "path": rel_path,
            "size": file_size,
            "hash": file_hash,
            "added": datetime.now().isoformat(),
        }

        # Add user and message info if available
        if user_id:
            file_info["user_id"] = user_id
        if message_id:
            file_info["message_id"] = message_id

        return file_info

    def _calculate_file_hash(self, file_path: str, chunk_size: int = 8192) -> str:
        """
        Calculate a hash for a file.

        Args:
            file_path: Path to the file
            chunk_size: Size of chunks to read

        Returns:
            Hash string
        """
        hasher = hashlib.md5()

        try:
            with open(file_path, 'rb') as f:
                # Read file in chunks to handle large files
                chunk = f.read(chunk_size)
                while chunk:
                    hasher.update(chunk)
                    chunk = f.read(chunk_size)

            return hasher.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""

    def is_duplicate(self, file_path: str, method: str = "hash", user_id: Optional[int] = None, across_users: bool = False) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Check if a file is a duplicate.

        Args:
            file_path: Path to the file
            method: Deduplication method (hash, filename, size, all)
            user_id: ID of the user who sent the file
            across_users: Whether to check across all users

        Returns:
            Tuple of (is_duplicate, duplicate_info)
        """
        # Extract message ID from filename if possible
        try:
            message_id = int(os.path.basename(file_path).split("_")[-1].split(".")[0])
        except (ValueError, IndexError):
            message_id = None

        # For files that don't exist yet (planned downloads), we need to check by name
        file_name = os.path.basename(file_path)

        # Get file size if the file exists
        file_size = None
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)

        # Only calculate hash if needed and file exists
        file_hash = None
        if method in ["hash", "all"] and os.path.exists(file_path):
            file_hash = self._calculate_file_hash(file_path)

        # Log what we're checking
        logger.debug(f"Checking for duplicates: path={file_path}, name={file_name}, size={file_size}, hash={file_hash}, message_id={message_id}")

        # Check for duplicates
        for entry in self.db.get("files", []):
            # Skip if this is the same message (not a duplicate)
            if message_id and entry.get("message_id") == message_id:
                continue

            # Skip if user_id doesn't match and not checking across users
            if not across_users and user_id and entry.get("user_id") != user_id:
                continue

            # Check based on method
            if method == "hash" and file_hash and entry.get("hash") == file_hash:
                logger.debug(f"Hash match: {file_hash} == {entry.get('hash')}")
                return True, entry
            elif method == "filename" and os.path.basename(entry.get("path", "")) == file_name:
                logger.debug(f"Filename match: {file_name} == {os.path.basename(entry.get('path', ''))}")
                return True, entry
            elif method == "size" and file_size and entry.get("size") == file_size:
                logger.debug(f"Size match: {file_size} == {entry.get('size')}")
                return True, entry
            elif method == "all":
                # Check all criteria
                size_match = file_size and entry.get("size") == file_size
                name_match = os.path.basename(entry.get("path", "")) == file_name
                hash_match = file_hash and entry.get("hash") == file_hash

                # Consider it a duplicate if size and (name or hash) match
                if size_match and (name_match or hash_match):
                    logger.debug(f"All match: size={size_match}, name={name_match}, hash={hash_match}")
                    return True, entry

        return False, None

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the deduplication database.

        Returns:
            Dict with statistics
        """
        files = self.db.get("files", [])
        total_size = sum(entry.get("size", 0) for entry in files)

        return {
            "total_files": len(files),
            "total_size": total_size,
            "users": len(set(entry.get("user_id") for entry in files if "user_id" in entry))
        }
