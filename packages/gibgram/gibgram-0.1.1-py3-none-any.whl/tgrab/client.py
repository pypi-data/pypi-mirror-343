"""
Telegram client module for TGrab.

This module handles the connection to Telegram and provides
methods for downloading media.
"""

import os
import asyncio
import logging
import json
from typing import Optional, List, Dict, Any, Callable, Union
from datetime import datetime

from telethon import TelegramClient

from .dedup import DedupDatabase
from telethon.tl.types import (
    Message,
    MessageMediaPhoto,
    MessageMediaDocument,
    DocumentAttributeFilename,
    DocumentAttributeVideo,
    DocumentAttributeAudio,
    MessageService,
    MessageActionScreenshotTaken
)

# Configure logging - minimal output
logger = logging.getLogger(__name__)
# Disable Telethon's logs
logging.getLogger('telethon').setLevel(logging.WARNING)

class TGrabClient:
    """Client for connecting to Telegram and downloading media."""

    # Media type mapping
    MEDIA_TYPES = {
        "photo": MessageMediaPhoto,
        "document": MessageMediaDocument,
        # Videos are actually documents with video attributes in Telethon
        "video": MessageMediaDocument
    }

    # Common file extensions
    COMMON_EXTENSIONS = {
        # Images
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/webp": "webp",
        "image/bmp": "bmp",
        "image/tiff": "tiff",
        # Videos
        "video/mp4": "mp4",
        "video/quicktime": "mov",
        "video/x-msvideo": "avi",
        "video/x-matroska": "mkv",
        "video/webm": "webm",
        # Audio
        "audio/mpeg": "mp3",
        "audio/ogg": "ogg",
        "audio/wav": "wav",
        "audio/flac": "flac",
        # Documents
        "application/pdf": "pdf",
        "application/zip": "zip",
        "application/x-rar-compressed": "rar",
        "application/x-tar": "tar",
        "application/x-7z-compressed": "7z",
        "application/msword": "doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        "application/vnd.ms-excel": "xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        "application/vnd.ms-powerpoint": "ppt",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
        "text/plain": "txt"
    }

    def __init__(
        self,
        api_id: int,
        api_hash: str,
        phone: str,
        session_name: str = "tgrab",
        download_folder: str = "downloads",
        session_string: Optional[str] = None,
        organization_options: Optional[Dict[str, Any]] = None,
        filter_options: Optional[Dict[str, Any]] = None,
        performance_options: Optional[Dict[str, Any]] = None,
        dedup_options: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the TGrab client.

        Args:
            api_id: Telegram API ID
            api_hash: Telegram API hash
            phone: Phone number with country code
            session_name: Name for the Telethon session file
            download_folder: Folder to save downloaded media
            session_string: Optional session string to use instead of session file
            organization_options: Options for organizing downloaded media
            filter_options: Options for filtering media
            performance_options: Options for performance tuning
            dedup_options: Options for media deduplication
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.session_name = session_name
        self.download_folder = download_folder
        self.session_string = session_string
        self.client = None

        # Set default organization options
        self.organization_options = {
            "organize_by": "none",
            "filename_template": "{name}{prefix}_{id}.{ext}",
            "save_metadata": False
        }

        # Update with provided options
        if organization_options:
            self.organization_options.update(organization_options)

        # Set default filter options
        self.filter_options = {
            "min_size": None,
            "max_size": None,
            "min_width": None,
            "min_height": None,
            "min_duration": None,
            "max_duration": None,
            "has_caption": False,
            "caption_contains": None
        }

        # Update with provided options
        if filter_options:
            self.filter_options.update(filter_options)

        # Set default performance options
        self.performance_options = {
            "parallel": 1,
            "chunk_size": 128 * 1024  # 128 KB in bytes
        }

        # Update with provided options
        if performance_options:
            self.performance_options.update(performance_options)

        # Set default deduplication options
        self.dedup_options = {
            "enabled": False,
            "method": "hash",
            "across_users": False
        }

        # Update with provided options
        if dedup_options:
            self.dedup_options.update(dedup_options)

        # Create download directory
        os.makedirs(download_folder, exist_ok=True)

        # Semaphore for limiting concurrent downloads
        self.download_semaphore = None

        # Initialize deduplication database if enabled
        self.dedup_db = None
        if self.dedup_options.get("enabled", False):
            self.dedup_db = DedupDatabase(download_folder)

    async def download_single_message(
        self,
        message: Message,
        is_self_destructing: bool = False,
        is_likely_self_destructing: bool = False,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Download media from a single message.

        Args:
            message: Message containing media
            is_self_destructing: Whether the message is self-destructing
            is_likely_self_destructing: Whether the message is likely self-destructing
            max_retries: Maximum number of retry attempts

        Returns:
            Dict with download result
        """
        # Set retry count based on message type
        retry_count = max_retries if is_self_destructing or is_likely_self_destructing else 1

        # Determine media type and extension
        media_type, extension = self.get_media_type_and_extension(message)

        # Generate organized file path
        filename = self.generate_organized_path(message, media_type, extension)

        # Check if file already exists (to avoid re-downloading)
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            logger.info(f"File already exists: {filename}")

            # Save metadata if enabled
            metadata_path = None
            if self.organization_options.get("save_metadata", False):
                metadata_path = self.save_message_metadata(message, filename)

            # Add to deduplication database if enabled
            if self.dedup_options.get("enabled", False) and self.dedup_db:
                user_id = None
                if hasattr(message, 'sender') and message.sender:
                    user_id = getattr(message.sender, 'id', None)
                self.dedup_db.add_file(filename, user_id=user_id, message_id=message.id)

            return {
                "success": True,
                "path": filename,
                "is_self_destructing": is_self_destructing,
                "is_likely_self_destructing": is_likely_self_destructing,
                "metadata_path": metadata_path,
                "already_exists": True
            }

        # Check for duplicates if deduplication is enabled
        if self.dedup_options.get("enabled", False) and self.dedup_db:
            # Get user ID if available
            user_id = None
            if hasattr(message, 'sender') and message.sender:
                user_id = getattr(message.sender, 'id', None)

            # Create a temporary file to check for duplicates
            # This is needed because the file doesn't exist yet
            temp_file = os.path.join(self.download_folder, ".temp_dedup")

            # Copy media content to temp file if needed for hash-based deduplication
            if self.dedup_options.get("method", "hash") in ["hash", "all"]:
                try:
                    # Download to temp file first
                    temp_path = await self.client.download_media(message.media, temp_file)

                    # Check if this is a duplicate using the temp file
                    is_dup, dup_info = self.dedup_db.is_duplicate(
                        temp_path,
                        method=self.dedup_options.get("method", "hash"),
                        user_id=user_id,
                        across_users=self.dedup_options.get("across_users", False)
                    )

                    # Remove temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except Exception as e:
                    logger.warning(f"Error checking for duplicates: {e}")
                    is_dup, dup_info = False, None
            else:
                # For non-hash methods, we can check without downloading
                is_dup, dup_info = self.dedup_db.is_duplicate(
                    filename,
                    method=self.dedup_options.get("method", "hash"),
                    user_id=user_id,
                    across_users=self.dedup_options.get("across_users", False)
                )

            if is_dup and dup_info:
                duplicate_path = os.path.join(self.download_folder, dup_info.get("path", ""))
                logger.info(f"Duplicate detected: {filename} matches {duplicate_path}")

                # Save metadata if enabled
                metadata_path = None
                if self.organization_options.get("save_metadata", False):
                    metadata_path = self.save_message_metadata(message, duplicate_path)

                return {
                    "success": True,
                    "path": duplicate_path,
                    "is_self_destructing": is_self_destructing,
                    "is_likely_self_destructing": is_likely_self_destructing,
                    "is_duplicate": True,
                    "duplicate_path": duplicate_path,
                    "metadata_path": metadata_path,
                    "message_id": message.id
                }

        # Try to download with retries
        download_error = None
        path = None

        for attempt in range(retry_count):
            try:
                # Download the media with progress callback
                path = await self.client.download_media(
                    message.media,
                    filename,
                    progress_callback=None  # No progress callback for parallel downloads
                )

                if path:
                    # Log success
                    if is_self_destructing or is_likely_self_destructing:
                        logger.warning(f"Successfully downloaded self-destructing media to {path}")
                    else:
                        logger.info(f"Downloaded media to {path}")

                    # Save metadata if enabled
                    metadata_path = None
                    if self.organization_options.get("save_metadata", False):
                        metadata_path = self.save_message_metadata(message, path)

                    # Add to deduplication database if enabled
                    if self.dedup_options.get("enabled", False) and self.dedup_db:
                        user_id = None
                        if hasattr(message, 'sender') and message.sender:
                            user_id = getattr(message.sender, 'id', None)
                        self.dedup_db.add_file(path, user_id=user_id, message_id=message.id)

                    return {
                        "success": True,
                        "path": path,
                        "is_self_destructing": is_self_destructing,
                        "is_likely_self_destructing": is_likely_self_destructing,
                        "metadata_path": metadata_path,
                        "already_exists": False,
                        "is_duplicate": False
                    }
                else:
                    # If last attempt
                    if attempt == retry_count - 1:
                        download_error = "Download returned empty path"
                    else:
                        # Wait before retrying (exponential backoff)
                        await asyncio.sleep(2 ** attempt)
                        logger.info(f"Retrying download for message {message.id}, attempt {attempt + 2}/{retry_count}")

            except Exception as e:
                # If last attempt
                if attempt == retry_count - 1:
                    download_error = f"Error: {e}"
                else:
                    # Wait before retrying (exponential backoff)
                    await asyncio.sleep(2 ** attempt)
                    logger.info(f"Retrying download for message {message.id}, attempt {attempt + 2}/{retry_count}")

        # If we get here, all attempts failed
        logger.error(f"Failed to download media from message {message.id}: {download_error}")

        return {
            "success": False,
            "error": download_error,
            "is_self_destructing": is_self_destructing,
            "is_likely_self_destructing": is_likely_self_destructing
        }

    async def connect(self, code_callback: Optional[Callable] = None, max_retries: int = 3) -> bool:
        """
        Connect to Telegram with automatic retry.

        Args:
            code_callback: Optional callback function for handling verification codes
            max_retries: Maximum number of connection attempts

        Returns:
            bool: True if connection was successful
        """
        for attempt in range(max_retries):
            try:
                # Create client if it doesn't exist
                if not self.client:
                    if self.session_string:
                        # Use session string
                        try:
                            from telethon.sessions import StringSession
                            self.client = TelegramClient(
                                StringSession(self.session_string),
                                self.api_id,
                                self.api_hash
                            )
                            logger.info("Using session string for authentication")
                        except Exception as e:
                            logger.error(f"Error using session string: {e}")
                            # Fall back to session file
                            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
                    else:
                        # Use session file
                        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

                # Check if already connected
                if self.client.is_connected():
                    logger.info("Already connected to Telegram")
                    return True

                # Use custom code callback if provided
                if code_callback:
                    # Wrap the code callback to ensure it returns a string
                    def wrapped_code_callback():
                        code = code_callback()
                        if code is None:
                            return ""
                        return str(code)

                    await self.client.start(phone=self.phone, code_callback=wrapped_code_callback)
                else:
                    await self.client.start(phone=self.phone)

                logger.info("Connected to Telegram successfully")
                return True

            except ConnectionError as e:
                logger.warning(f"Connection error (attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error("Maximum connection attempts reached")
                    return False

            except Exception as e:
                logger.error(f"Failed to connect to Telegram: {e}")
                return False

        return False

    async def ensure_connected(self, code_callback: Optional[Callable] = None) -> bool:
        """
        Ensure the client is connected, reconnecting if necessary.

        Args:
            code_callback: Optional callback function for handling verification codes

        Returns:
            bool: True if connection is active
        """
        if not self.client:
            return await self.connect(code_callback)

        try:
            if not self.client.is_connected():
                logger.info("Connection lost, reconnecting...")
                try:
                    await self.client.connect()
                except Exception as e:
                    logger.warning(f"Error during reconnection: {e}")
                    return await self.connect(code_callback)

                # Check if reconnection was successful
                if not self.client.is_connected():
                    logger.warning("Reconnection failed, attempting full restart")
                    return await self.connect(code_callback)

            return True

        except Exception as e:
            logger.error(f"Error checking connection: {e}")
            return await self.connect(code_callback)

    async def disconnect(self):
        """Disconnect from Telegram."""
        if self.client:
            await self.client.disconnect()
            logger.info("Disconnected from Telegram")

    async def get_session_string(self) -> Optional[str]:
        """
        Get the current session as a string.

        Returns:
            Optional[str]: Session string or None if not available
        """
        if not self.client:
            logger.error("Client not connected")
            return None

        try:
            from telethon.sessions import StringSession
            return StringSession.save(self.client.session)
        except Exception as e:
            logger.error(f"Error getting session string: {e}")
            return None

    def save_message_metadata(self, message: Message, media_path: str) -> Optional[str]:
        """
        Save message metadata to a JSON file.

        Args:
            message: Telegram message with media
            media_path: Path to the downloaded media file

        Returns:
            Optional[str]: Path to the metadata file or None if failed
        """
        if not self.organization_options.get("save_metadata", False):
            return None

        try:
            # Create metadata file path (same as media file but with .json extension)
            metadata_path = os.path.splitext(media_path)[0] + ".json"

            # Extract metadata
            metadata = {
                "message_id": message.id,
                "date": message.date.isoformat(),
                "media_type": self.get_media_type_and_extension(message)[0],
                "is_self_destructing": getattr(message, 'is_self_destructing', False),
                "is_likely_self_destructing": getattr(message, 'is_likely_self_destructing', False),
            }

            # Add caption if available
            if hasattr(message, 'message') and message.message:
                metadata["caption"] = message.message

            # Add sender info if available
            if hasattr(message, 'sender') and message.sender:
                sender = {}
                for attr in ['id', 'username', 'first_name', 'last_name', 'phone']:
                    if hasattr(message.sender, attr):
                        value = getattr(message.sender, attr)
                        if value:
                            sender[attr] = value
                if sender:
                    metadata["sender"] = sender

            # Add chat info if available
            if hasattr(message, 'chat') and message.chat:
                chat = {}
                for attr in ['id', 'username', 'title', 'type']:
                    if hasattr(message.chat, attr):
                        value = getattr(message.chat, attr)
                        if value:
                            chat[attr] = value
                if chat:
                    metadata["chat"] = chat

            # Save metadata to file
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)

            logger.info(f"Saved metadata to {metadata_path}")
            return metadata_path

        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
            return None

    def generate_organized_path(self, message: Message, media_type: str, extension: str) -> str:
        """
        Generate an organized file path based on organization options.

        Args:
            message: Telegram message with media
            media_type: Type of media (photo, video, etc.)
            extension: File extension

        Returns:
            Organized file path relative to download folder
        """
        # Get organization options
        organize_by = self.organization_options.get("organize_by", "none")
        filename_template = self.organization_options.get("filename_template", "{prefix}_{timestamp}_{id}.{ext}")

        # Base directory is the download folder
        base_dir = self.download_folder

        # Create subdirectory based on organization option
        if organize_by == "date":
            # Organize by date (YYYY-MM-DD)
            date_str = message.date.strftime("%Y-%m-%d")
            base_dir = os.path.join(base_dir, date_str)
        elif organize_by == "type":
            # Organize by media type
            base_dir = os.path.join(base_dir, media_type)
        elif organize_by == "chat":
            # Organize by chat/sender
            if hasattr(message, 'chat') and message.chat:
                chat_name = getattr(message.chat, 'username', None) or getattr(message.chat, 'title', None)
                if chat_name:
                    # Sanitize chat name for filesystem
                    chat_name = "".join(c for c in chat_name if c.isalnum() or c in " _-").strip()
                    base_dir = os.path.join(base_dir, chat_name)
            elif hasattr(message, 'sender') and message.sender:
                sender_name = getattr(message.sender, 'username', None) or getattr(message.sender, 'first_name', None)
                if sender_name:
                    # Sanitize sender name for filesystem
                    sender_name = "".join(c for c in sender_name if c.isalnum() or c in " _-").strip()
                    base_dir = os.path.join(base_dir, sender_name)

        # Create directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)

        # Check if message is self-destructing
        is_self_destructing = getattr(message, 'is_self_destructing', False)
        is_likely_self_destructing = getattr(message, 'is_likely_self_destructing', False)

        # Determine prefix (shorter and more concise)
        if is_self_destructing:
            prefix = f"sd_{media_type}"  # sd = self-destructing
        elif is_likely_self_destructing:
            prefix = f"lsd_{media_type}"  # lsd = likely self-destructing
        else:
            prefix = media_type

        # Get timestamp
        timestamp = message.date.strftime("%Y%m%d_%H%M%S")

        # Get sender info
        sender = ""
        if hasattr(message, 'sender') and message.sender:
            sender = getattr(message.sender, 'username', None) or getattr(message.sender, 'first_name', None) or ""
            # Sanitize sender name
            sender = "".join(c for c in sender if c.isalnum() or c in "_-").strip()

        # Get chat info
        chat = ""
        if hasattr(message, 'chat') and message.chat:
            chat = getattr(message.chat, 'username', None) or getattr(message.chat, 'title', None) or ""
            # Sanitize chat name
            chat = "".join(c for c in chat if c.isalnum() or c in "_-").strip()

        # Get sender name for filename prefix
        name_prefix = ""
        if hasattr(message, 'sender') and message.sender:
            # Try to get first_name or username
            name_prefix = getattr(message.sender, 'first_name', None) or getattr(message.sender, 'username', None) or ""
            # Sanitize name prefix
            name_prefix = "".join(c for c in name_prefix if c.isalnum() or c in "_-").strip()
            # Limit length to avoid very long filenames
            if name_prefix:
                name_prefix = name_prefix[:15] + "_"

        # Format filename using template with name prefix
        filename = filename_template.format(
            prefix=prefix,
            timestamp=timestamp,
            id=message.id,
            ext=extension,
            sender=sender,
            chat=chat,
            name=name_prefix
        )

        # Combine directory and filename
        return os.path.join(base_dir, filename)

    def passes_filter(self, message: Message) -> bool:
        """
        Check if a message passes the filter criteria.

        Args:
            message: Telegram message with media

        Returns:
            bool: True if the message passes all filters, False otherwise
        """
        # Skip if no media
        if not message.media:
            return False

        # Check caption filters
        if self.filter_options.get("has_caption", False):
            if not hasattr(message, 'message') or not message.message:
                return False

        if self.filter_options.get("caption_contains"):
            caption_text = getattr(message, 'message', '')
            if not caption_text or self.filter_options["caption_contains"].lower() not in caption_text.lower():
                return False

        # Get media type and extension
        media_type, _ = self.get_media_type_and_extension(message)

        # Check size filters
        min_size = self.filter_options.get("min_size")
        max_size = self.filter_options.get("max_size")

        if min_size or max_size:
            # Get file size
            if hasattr(message.media, 'document') and hasattr(message.media.document, 'size'):
                file_size = message.media.document.size
            elif hasattr(message.media, 'photo') and hasattr(message.media.photo, 'sizes'):
                # Get the largest photo size
                sizes = message.media.photo.sizes
                file_size = max((getattr(s, 'size', 0) for s in sizes), default=0)
            else:
                # Can't determine size, assume it passes
                file_size = 0

            # Check min size
            if min_size and file_size < min_size:
                return False

            # Check max size
            if max_size and file_size > max_size:
                return False

        # Check dimension filters for photos and videos
        min_width = self.filter_options.get("min_width")
        min_height = self.filter_options.get("min_height")

        if (min_width or min_height) and media_type in ["photo", "image", "video"]:
            width = 0
            height = 0

            # Get dimensions
            if hasattr(message.media, 'document') and hasattr(message.media.document, 'attributes'):
                # Look for video attributes
                for attr in message.media.document.attributes:
                    if hasattr(attr, 'w') and hasattr(attr, 'h'):
                        width = attr.w
                        height = attr.h
                        break
            elif hasattr(message.media, 'photo') and hasattr(message.media.photo, 'sizes'):
                # Get the largest photo size
                sizes = message.media.photo.sizes
                for size in sizes:
                    if hasattr(size, 'w') and hasattr(size, 'h'):
                        if size.w > width or size.h > height:
                            width = size.w
                            height = size.h

            # Check min width
            if min_width and width < min_width:
                return False

            # Check min height
            if min_height and height < min_height:
                return False

        # Check duration filters for videos and audio
        min_duration = self.filter_options.get("min_duration")
        max_duration = self.filter_options.get("max_duration")

        if (min_duration or max_duration) and media_type in ["video", "audio"]:
            duration = 0

            # Get duration
            if hasattr(message.media, 'document') and hasattr(message.media.document, 'attributes'):
                # Look for duration attribute
                for attr in message.media.document.attributes:
                    if hasattr(attr, 'duration'):
                        duration = attr.duration
                        break

            # Check min duration
            if min_duration and duration < min_duration:
                return False

            # Check max duration
            if max_duration and duration > max_duration:
                return False

        # All filters passed
        return True

    def get_media_type_and_extension(self, message: Message) -> tuple:
        """
        Determine the media type and appropriate file extension for a message.

        Args:
            message: Telegram message with media

        Returns:
            Tuple of (media_type, file_extension)
        """
        if not message.media:
            return "unknown", "bin"

        # Check for photos
        if isinstance(message.media, MessageMediaPhoto):
            return "photo", "jpg"

        # Check for documents and videos
        if isinstance(message.media, MessageMediaDocument):
            document = message.media.document

            # Get mime type
            mime_type = document.mime_type

            # Check for known mime types
            if mime_type in self.COMMON_EXTENSIONS:
                # Determine media type category
                if mime_type.startswith("image/"):
                    return "image", self.COMMON_EXTENSIONS[mime_type]
                elif mime_type.startswith("video/"):
                    return "video", self.COMMON_EXTENSIONS[mime_type]
                elif mime_type.startswith("audio/"):
                    return "audio", self.COMMON_EXTENSIONS[mime_type]
                else:
                    return "document", self.COMMON_EXTENSIONS[mime_type]

            # Check document attributes for more info
            for attr in document.attributes:
                # Video attribute
                if isinstance(attr, DocumentAttributeVideo):
                    return "video", "mp4"

                # Audio attribute
                elif isinstance(attr, DocumentAttributeAudio):
                    return "audio", "mp3"

                # Note: DocumentAttributeImage doesn't exist in current Telethon
                # We'll rely on mime type and filename for images

                # Filename attribute
                elif isinstance(attr, DocumentAttributeFilename):
                    # Extract extension from filename
                    filename = attr.file_name
                    ext = os.path.splitext(filename)[1].lower().lstrip(".")
                    if ext:
                        # Determine media type from extension
                        if ext in ["jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff"]:
                            return "image", ext
                        elif ext in ["mp4", "mov", "avi", "mkv", "webm"]:
                            return "video", ext
                        elif ext in ["mp3", "ogg", "wav", "flac"]:
                            return "audio", ext
                        else:
                            return "document", ext

            # Fallback based on mime type prefix
            if mime_type.startswith("image/"):
                return "image", "jpg"
            elif mime_type.startswith("video/"):
                return "video", "mp4"
            elif mime_type.startswith("audio/"):
                return "audio", "mp3"

        # Default fallback
        return "document", "bin"

    async def get_user(self, user_identifier: Union[int, str], code_callback: Optional[Callable] = None) -> Optional[Any]:
        """
        Get a user entity by ID or username.

        Args:
            user_identifier: User ID (int) or username (str)
            code_callback: Optional callback for verification codes if reconnection is needed

        Returns:
            User entity or None if not found
        """
        # Ensure connection
        if not await self.ensure_connected(code_callback):
            logger.error("Failed to ensure connection")
            return None

        # Maximum retry attempts for API errors
        max_retries = 3

        for attempt in range(max_retries):
            try:
                entity = await self.client.get_entity(user_identifier)
                logger.info(f"Found user: {entity.first_name} {getattr(entity, 'last_name', '')}")
                return entity

            except ConnectionError as e:
                logger.warning(f"Connection error while getting user (attempt {attempt+1}/{max_retries}): {e}")

                # Try to reconnect
                if not await self.ensure_connected(code_callback):
                    logger.error("Failed to reconnect")
                    return None

                # Last attempt failed
                if attempt == max_retries - 1:
                    logger.error(f"Failed to find user after {max_retries} attempts")
                    return None

                # Wait before retrying
                await asyncio.sleep(2 ** attempt)

            except Exception as e:
                logger.error(f"Failed to find user {user_identifier}: {e}")
                return None

        return None

    async def get_media_messages(
        self,
        user: Any,
        limit: int = 100,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        media_types: List[str] = None,
        min_id: int = 0,
        code_callback: Optional[Callable] = None
    ) -> List[Message]:
        """
        Get messages containing media from a specific user.

        Args:
            user: User entity
            limit: Maximum number of messages to fetch
            date_from: Start date for filtering messages
            date_to: End date for filtering messages
            media_types: List of media types to include (photo, document, etc.)
            min_id: Only get messages with ID greater than this
            code_callback: Optional callback for verification codes if reconnection is needed

        Returns:
            List of messages containing media, with self-destructing messages prioritized
        """
        # Ensure connection
        if not await self.ensure_connected(code_callback):
            logger.error("Failed to ensure connection")
            return []

        if media_types is None:
            media_types = ["photo"]

        # Maximum retry attempts for API errors
        max_retries = 3

        for attempt in range(max_retries):
            try:
                # Get messages from the user
                messages = await self.client.get_messages(user, limit=limit, min_id=min_id)
                logger.info(f"Retrieved {len(messages)} messages")

                # Filter messages with media
                regular_media_messages = []
                self_destructing_messages = []

                for msg in messages:
                    # Skip messages without media
                    if not msg.media:
                        continue

                    # Skip messages outside date range
                    if date_from and msg.date < date_from:
                        continue
                    if date_to and msg.date > date_to:
                        continue

                    # Check if media type matches requested types
                    media_type_matches = False

                    # Check each requested media type
                    for media_type in media_types:
                        if media_type in self.MEDIA_TYPES:
                            if isinstance(msg.media, self.MEDIA_TYPES[media_type]):
                                media_type_matches = True
                                break

                    # Skip if not matching any requested media type
                    if not media_type_matches:
                        continue

                    # Apply additional filters
                    if not self.passes_filter(msg):
                        logger.debug(f"Message {msg.id} filtered out by media filters")
                        continue

                    # Check if message is self-destructing (has TTL)
                    is_self_destructing = False

                    # Check for TTL in message
                    if hasattr(msg, 'ttl_period') and msg.ttl_period:
                        is_self_destructing = True
                        logger.warning(f"Found self-destructing message with ID {msg.id}, TTL: {msg.ttl_period}s")

                    # Check for screenshot notifications (often indicates self-destructing content)
                    elif isinstance(msg, MessageService) and isinstance(msg.action, MessageActionScreenshotTaken):
                        try:
                            # Look for media messages right before the screenshot notification
                            context = await self.client.get_messages(user, limit=5, max_id=msg.id)
                            for ctx_msg in context:
                                if ctx_msg.media:
                                    ctx_msg.is_likely_self_destructing = True
                                    self_destructing_messages.append(ctx_msg)
                        except Exception as e:
                            logger.warning(f"Error checking context messages: {e}")

                    # Add to appropriate list
                    if is_self_destructing:
                        # Add custom attribute to mark as self-destructing
                        msg.is_self_destructing = True
                        self_destructing_messages.append(msg)
                    else:
                        regular_media_messages.append(msg)

                # Combine lists with self-destructing messages first
                media_messages = self_destructing_messages + regular_media_messages

                # Log findings
                if self_destructing_messages:
                    logger.warning(f"Found {len(self_destructing_messages)} self-destructing media messages!")

                logger.info(f"Found {len(media_messages)} total media messages")
                return media_messages

            except ConnectionError as e:
                logger.warning(f"Connection error while getting messages (attempt {attempt+1}/{max_retries}): {e}")

                # Try to reconnect
                if not await self.ensure_connected(code_callback):
                    logger.error("Failed to reconnect")
                    return []

                # Last attempt failed
                if attempt == max_retries - 1:
                    logger.error(f"Failed to get messages after {max_retries} attempts")
                    return []

                # Wait before retrying
                await asyncio.sleep(2 ** attempt)

            except Exception as e:
                logger.error(f"Failed to get media messages: {e}")

                # For non-connection errors, we'll retry once
                if attempt < 1:
                    logger.info("Retrying after error...")
                    await asyncio.sleep(1)
                else:
                    return []

        return []

    async def download_media(
        self,
        messages: List[Message],
        progress_callback: Optional[Callable[[int, int], None]] = None,
        max_retries: int = 3,
        code_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Download media from messages with priority for self-destructing content.

        Args:
            messages: List of messages containing media
            progress_callback: Optional callback for progress updates
            max_retries: Maximum number of retry attempts for failed downloads
            code_callback: Optional callback for verification codes if reconnection is needed

        Returns:
            Dict with download statistics
        """
        # Ensure connection
        if not await self.ensure_connected(code_callback):
            logger.error("Failed to ensure connection")
            return {"success": 0, "failed": 0, "self_destructing": 0, "files": [], "pending": 0}

        stats = {
            "success": 0,
            "failed": 0,
            "self_destructing": 0,
            "files": [],
            "metadata_files": [],
            "pending": [],  # Track failed downloads for future retry
            "duplicates": 0  # Track duplicate files
        }

        total = len(messages)

        # Sort messages to prioritize self-destructing ones
        # This is a backup in case they weren't already prioritized
        prioritized_messages = sorted(
            messages,
            key=lambda msg: getattr(msg, 'is_self_destructing', False) or getattr(msg, 'is_likely_self_destructing', False),
            reverse=True
        )

        # Create download directory if it doesn't exist
        os.makedirs(self.download_folder, exist_ok=True)

        # Create a persistent download queue file
        queue_file = os.path.join(self.download_folder, ".download_queue.json")

        # Load existing queue if it exists
        pending_downloads = []
        if os.path.exists(queue_file):
            try:
                with open(queue_file, 'r') as f:
                    pending_data = json.load(f)
                    # We can only use the message IDs from the queue
                    # as Message objects can't be serialized
                    pending_ids = set(item.get('message_id') for item in pending_data)
                    logger.info(f"Loaded {len(pending_ids)} pending downloads from queue")
            except Exception as e:
                logger.warning(f"Error loading download queue: {e}")
                pending_ids = set()
        else:
            pending_ids = set()

        # Initialize semaphore for parallel downloads
        parallel = self.performance_options.get("parallel", 1)
        self.download_semaphore = asyncio.Semaphore(parallel)

        # Log parallel download info
        if parallel > 1:
            logger.info(f"Using {parallel} parallel downloads")

        # Create tasks for all downloads
        download_tasks = []
        for msg in prioritized_messages:
            # Check if message is self-destructing
            is_self_destructing = getattr(msg, 'is_self_destructing', False)
            is_likely_self_destructing = getattr(msg, 'is_likely_self_destructing', False)

            # Create task for this message
            task = self._download_message_with_semaphore(
                msg,
                is_self_destructing,
                is_likely_self_destructing,
                max_retries
            )
            download_tasks.append(task)

        # Process downloads with progress reporting
        completed = 0
        for task in asyncio.as_completed(download_tasks):
            # Wait for the task to complete
            result = await task

            # Update progress
            completed += 1
            if progress_callback:
                progress_callback(completed, total)

            # Update stats based on result
            if result["success"]:
                stats["success"] += 1
                stats["files"].append(result["path"])

                # Count self-destructing media
                if result["is_self_destructing"] or result["is_likely_self_destructing"]:
                    stats["self_destructing"] += 1

                # Add metadata file if present
                if result.get("metadata_path"):
                    stats["metadata_files"].append(result["metadata_path"])

                # Count duplicates
                if result.get("is_duplicate", False):
                    stats["duplicates"] += 1
                    logger.info(f"Skipped duplicate file: {result.get('path')}")

                # Remove from pending if it was there
                if result["message_id"] in pending_ids:
                    pending_ids.remove(result["message_id"])
            else:
                stats["failed"] += 1

                # Add to pending downloads for future retry
                message_id = result.get("message_id")
                if message_id and (result["is_self_destructing"] or result["is_likely_self_destructing"] or max_retries > 1):
                    pending_downloads.append({
                        "message_id": message_id,
                        "error": result.get("error", "Unknown error"),
                        "is_self_destructing": result["is_self_destructing"],
                        "is_likely_self_destructing": result["is_likely_self_destructing"]
                    })

        # Save pending downloads to queue file
        if pending_downloads:
            try:
                # Combine with existing pending downloads
                for msg_id in pending_ids:
                    # Only add if not already in the new pending list
                    if not any(item.get('message_id') == msg_id for item in pending_downloads):
                        pending_downloads.append({"message_id": msg_id})

                with open(queue_file, 'w') as f:
                    json.dump(pending_downloads, f)
                logger.info(f"Saved {len(pending_downloads)} pending downloads to queue")
            except Exception as e:
                logger.warning(f"Error saving download queue: {e}")
        elif os.path.exists(queue_file):
            # Remove queue file if no pending downloads
            try:
                os.remove(queue_file)
            except Exception as e:
                logger.warning(f"Error removing download queue file: {e}")

        # Log summary of self-destructing content
        if stats["self_destructing"] > 0:
            logger.warning(f"Downloaded {stats['self_destructing']} self-destructing media files!")

        # Add pending count to stats
        stats["pending"] = len(pending_downloads)

        return stats

    async def _download_message_with_semaphore(
        self,
        message: Message,
        is_self_destructing: bool,
        is_likely_self_destructing: bool,
        max_retries: int
    ) -> Dict[str, Any]:
        """
        Download a message with semaphore to limit concurrent downloads.

        Args:
            message: Message to download
            is_self_destructing: Whether the message is self-destructing
            is_likely_self_destructing: Whether the message is likely self-destructing
            max_retries: Maximum number of retry attempts

        Returns:
            Dict with download result
        """
        async with self.download_semaphore:
            result = await self.download_single_message(
                message,
                is_self_destructing,
                is_likely_self_destructing,
                max_retries
            )

            # Add message ID to result
            result["message_id"] = message.id

            return result

    async def retry_pending_downloads(
        self,
        user: Any,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        code_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Retry downloading previously failed media files.

        Args:
            user: User entity to get messages from
            progress_callback: Optional callback for progress updates
            code_callback: Optional callback for verification codes if reconnection is needed

        Returns:
            Dict with download statistics
        """
        # Ensure connection
        if not await self.ensure_connected(code_callback):
            logger.error("Failed to ensure connection")
            return {"success": 0, "failed": 0, "self_destructing": 0, "files": [], "pending": 0}

        # Create download directory if it doesn't exist
        os.makedirs(self.download_folder, exist_ok=True)

        # Check for queue file
        queue_file = os.path.join(self.download_folder, ".download_queue.json")
        if not os.path.exists(queue_file):
            logger.info("No pending downloads found")
            return {"success": 0, "failed": 0, "self_destructing": 0, "files": [], "pending": 0}

        # Load pending downloads
        try:
            with open(queue_file, 'r') as f:
                pending_data = json.load(f)

            if not pending_data:
                logger.info("No pending downloads found")
                return {"success": 0, "failed": 0, "self_destructing": 0, "files": [], "pending": 0}

            logger.info(f"Found {len(pending_data)} pending downloads")

            # Group by message ID to avoid duplicates
            message_ids = set()
            for item in pending_data:
                if 'message_id' in item:
                    message_ids.add(item['message_id'])

            if not message_ids:
                logger.info("No valid message IDs found in pending downloads")
                return {"success": 0, "failed": 0, "self_destructing": 0, "files": [], "pending": 0}

            # Fetch messages by ID
            messages = []
            for msg_id in message_ids:
                try:
                    msg = await self.client.get_messages(user, ids=msg_id)
                    if msg and msg.media:
                        messages.append(msg)
                except Exception as e:
                    logger.warning(f"Error fetching message {msg_id}: {e}")

            if not messages:
                logger.warning("Could not retrieve any pending messages")
                return {"success": 0, "failed": 0, "self_destructing": 0, "files": [], "pending": len(pending_data)}

            logger.info(f"Retrieved {len(messages)} messages for retry")

            # Download the messages
            stats = await self.download_media(
                messages=messages,
                progress_callback=progress_callback,
                max_retries=5,  # Use more retries for pending downloads
                code_callback=code_callback
            )

            return stats

        except Exception as e:
            logger.error(f"Error retrying pending downloads: {e}")
            return {"success": 0, "failed": 0, "self_destructing": 0, "files": [], "pending": 0}

    async def get_dialogs(self, limit: int = 100) -> List[Any]:
        """
        Get dialogs (chats) from Telegram.

        Args:
            limit: Maximum number of dialogs to fetch

        Returns:
            List of dialogs
        """
        if not self.client:
            logger.error("Client not connected")
            return []

        try:
            return await self.client.get_dialogs(limit=limit)
        except Exception as e:
            logger.error(f"Error getting dialogs: {e}")
            return []

    async def search_media(self, query: str, limit: int = 100, media_types: List[str] = None) -> List[Message]:
        """
        Search for media across all chats.

        Args:
            query: Search query
            limit: Maximum number of messages to fetch
            media_types: List of media types to fetch

        Returns:
            List of messages containing media
        """
        if not self.client:
            logger.error("Client not connected")
            return []

        if not media_types:
            media_types = ["photo"]

        # Convert media types to Telethon types
        telethon_types = []
        for media_type in media_types:
            if media_type in self.MEDIA_TYPES:
                telethon_types.append(self.MEDIA_TYPES[media_type])

        if not telethon_types:
            logger.warning("No valid media types specified")
            return []

        try:
            # Search for media
            messages = []
            async for msg in self.client.iter_messages(
                None,  # Search across all chats
                search=query,
                limit=limit,
                filter=telethon_types
            ):
                if msg.media:
                    messages.append(msg)

            return messages
        except Exception as e:
            logger.error(f"Error searching for media: {e}")
            return []

    async def get_global_media(self, limit: int = 100, media_types: List[str] = None) -> List[Message]:
        """
        Get media from all chats.

        Args:
            limit: Maximum number of messages to fetch
            media_types: List of media types to fetch

        Returns:
            List of messages containing media
        """
        if not self.client:
            logger.error("Client not connected")
            return []

        if not media_types:
            media_types = ["photo"]

        # Get dialogs
        dialogs = await self.get_dialogs(limit=50)  # Get top 50 chats

        # Collect media from each chat
        all_media = []
        remaining = limit

        for dialog in dialogs:
            if remaining <= 0:
                break

            # Get media from this chat
            chat_media = await self.get_media_messages(
                dialog.entity,
                limit=min(remaining, 20),  # Get up to 20 media items per chat
                media_types=media_types
            )

            if chat_media:
                all_media.extend(chat_media)
                remaining -= len(chat_media)

        return all_media
