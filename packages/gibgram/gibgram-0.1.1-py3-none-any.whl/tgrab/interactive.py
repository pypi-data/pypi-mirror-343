"""
Interactive mode for TGrab.

This module provides an interactive interface for browsing and downloading media from Telegram.
"""

import os
import logging
from typing import List
from datetime import datetime

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich import box

from telethon.tl.types import Message, User, Chat, Channel

from .client import TGrabClient
from .dedup import DedupDatabase

# Configure logging
logger = logging.getLogger(__name__)

# Create console for interactive mode
console = Console()

class InteractiveMode:
    """Interactive mode for TGrab."""

    def __init__(self, client: TGrabClient, preview_count: int = 5):
        """
        Initialize interactive mode.

        Args:
            client: TGrab client
            preview_count: Number of media items to preview
        """
        self.client = client
        self.preview_count = preview_count
        self._cached_dialogs = None  # Cache for dialogs to avoid refetching

    async def start(self):
        """Start interactive mode."""
        console.print(Panel.fit(
            "[bold blue]TGrab Interactive Mode[/bold blue]\n"
            "Browse and download media from Telegram",
            box=box.ROUNDED,
            border_style="blue"
        ))

        # Connect to Telegram
        console.print("[cyan]Connecting to Telegram...[/cyan]")

        # Define code callback for interactive mode
        def code_callback():
            code = Prompt.ask("Enter the verification code")
            return code

        # Connect with retry
        connected = await self.client.connect(code_callback=code_callback)

        if not connected:
            console.print("[red]Failed to connect to Telegram. Please try again.[/red]")
            return

        console.print("[green]Connected to Telegram successfully![/green]")

        # Main menu loop
        while True:
            choice = await self.show_main_menu()

            if choice == "1":
                # Browse chats
                await self.browse_chats()
            elif choice == "2":
                # Search for media
                await self.search_media()
            elif choice == "3":
                # Configure settings
                await self.configure_settings()
            elif choice == "4":
                # Exit
                console.print("[yellow]Exiting interactive mode...[/yellow]")
                # Disconnect from Telegram
                await self.client.disconnect()
                break
            else:
                console.print("[red]Invalid choice. Please try again.[/red]")

    async def show_main_menu(self) -> str:
        """
        Show the main menu.

        Returns:
            User's choice
        """
        console.print("\n[bold cyan]Main Menu[/bold cyan]")
        console.print("1. Browse chats")
        console.print("2. Search for media")
        console.print("3. Configure settings")
        console.print("4. Exit")

        return Prompt.ask("\nEnter your choice", choices=["1", "2", "3", "4"])

    # This will be moved to __init__

    async def browse_chats(self):
        """Browse and select chats."""
        console.print("\n[bold cyan]Loading chats...[/bold cyan]")

        # Use cached dialogs if available, otherwise fetch them
        if not self._cached_dialogs:
            try:
                # Ensure connection
                if not await self.client.ensure_connected():
                    console.print("[red]Not connected to Telegram. Please try again.[/red]")
                    return

                # Get dialogs (chats)
                console.print("[cyan]Fetching chats...[/cyan]")
                self._cached_dialogs = await self.client.get_dialogs()
                console.print(f"[green]Found {len(self._cached_dialogs) if self._cached_dialogs else 0} chats[/green]")

                if not self._cached_dialogs:
                    console.print("[yellow]No chats found.[/yellow]")
                    return
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                import traceback
                console.print(f"[dim]{traceback.format_exc()}[/dim]")
                return

        # Use the cached dialogs
        dialogs = self._cached_dialogs

        # Set up pagination
        page_size = 10
        current_page = 0
        total_pages = (len(dialogs) + page_size - 1) // page_size  # Ceiling division

        while True:
            # Calculate start and end indices for current page
            start_idx = current_page * page_size
            end_idx = min(start_idx + page_size, len(dialogs))

            # Create a table to display chats
            table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
            table.add_column("#", style="dim", width=4)
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Messages", style="blue")

            # Add chats to table for current page
            try:
                for i, dialog in enumerate(dialogs[start_idx:end_idx], start_idx + 1):
                    try:
                        entity = dialog.entity

                        # Handle name safely
                        title = getattr(entity, 'title', None)
                        first_name = getattr(entity, 'first_name', None) or ''
                        last_name = getattr(entity, 'last_name', None) or ''

                        if title:
                            name = title
                        else:
                            name = (first_name + (' ' + last_name if last_name else '')).strip()

                        if not name:
                            name = f"Chat {i}"

                        # Determine chat type
                        if isinstance(entity, User):
                            chat_type = "User"
                        elif isinstance(entity, Chat):
                            chat_type = "Group"
                        elif isinstance(entity, Channel):
                            chat_type = "Channel"
                        else:
                            chat_type = "Unknown"

                        # Add row to table
                        table.add_row(
                            str(i),
                            name.strip(),
                            chat_type,
                            str(dialog.unread_count)
                        )
                    except Exception as e:
                        console.print(f"[yellow]Warning: Could not process chat {i}: {e}[/yellow]")
            except Exception as e:
                console.print(f"[red]Error processing chats: {e}[/red]")

            # Display table
            console.print(table)

            # Show pagination info
            console.print(f"\n[dim]Page {current_page + 1} of {total_pages}[/dim]")

            # Create choices for pagination
            choices = []

            # Add chat numbers for current page
            for i in range(start_idx + 1, end_idx + 1):
                choices.append(str(i))

            # Add navigation options
            if current_page > 0:
                choices.append("p")  # Previous page
            if current_page < total_pages - 1:
                choices.append("n")  # Next page
            choices.append("r")  # Refresh chats
            choices.append("b")  # Back to main menu

            # Create prompt message
            prompt_message = "\nSelect a chat"
            if current_page > 0:
                prompt_message += ", 'p' for previous page"
            if current_page < total_pages - 1:
                prompt_message += ", 'n' for next page"
            prompt_message += ", 'r' to refresh chats, or 'b' to go back"

            # Ask user to select a chat or navigate
            choice = Prompt.ask(prompt_message, choices=choices)

            if choice == "b":
                return
            elif choice == "p" and current_page > 0:
                current_page -= 1
                continue
            elif choice == "n" and current_page < total_pages - 1:
                current_page += 1
                continue
            elif choice == "r":
                # Refresh the chat list
                console.print("[cyan]Refreshing chats...[/cyan]")
                try:
                    # Clear the cache and fetch again
                    self._cached_dialogs = None

                    # Ensure connection
                    if not await self.client.ensure_connected():
                        console.print("[red]Not connected to Telegram. Please try again.[/red]")
                        return

                    # Get dialogs (chats)
                    self._cached_dialogs = await self.client.get_dialogs()
                    console.print(f"[green]Found {len(self._cached_dialogs) if self._cached_dialogs else 0} chats[/green]")

                    if not self._cached_dialogs:
                        console.print("[yellow]No chats found.[/yellow]")
                        return

                    # Update dialogs and pagination
                    dialogs = self._cached_dialogs
                    total_pages = (len(dialogs) + page_size - 1) // page_size
                    current_page = 0  # Reset to first page
                except Exception as e:
                    console.print(f"[red]Error refreshing chats: {e}[/red]")
                continue
            else:
                # User selected a chat
                selected_chat = dialogs[int(choice) - 1]

                # Browse media in selected chat
                await self.browse_media(selected_chat.entity)
                return

    async def browse_media(self, entity):
        """
        Browse media in a chat.

        Args:
            entity: Chat entity
        """
        # Handle name safely
        title = getattr(entity, 'title', None)
        first_name = getattr(entity, 'first_name', None) or ''
        last_name = getattr(entity, 'last_name', None) or ''

        if title:
            name = title
        else:
            name = (first_name + (' ' + last_name if last_name else '')).strip()

        if not name:
            name = "Chat"

        console.print(f"\n[bold cyan]Browsing media in {name}[/bold cyan]")

        # Ask for media types
        media_types = await self._ask_media_types()

        # Ask for limit
        limit = int(Prompt.ask("\nEnter maximum number of media items to fetch", default="50"))

        # Get media messages
        console.print("\n[bold cyan]Fetching media...[/bold cyan]")
        messages = await self.client.get_media_messages(
            entity,
            limit=limit,
            media_types=media_types
        )

        if not messages:
            console.print("[yellow]No media found.[/yellow]")
            return

        console.print(f"[green]Found {len(messages)} media items.[/green]")

        # Show media preview
        await self._show_media_preview(messages)

        # Ask what to do with the media
        choice = Prompt.ask(
            "\nWhat would you like to do?",
            choices=["1", "2", "3", "b"],
            default="1"
        )

        if choice == "b":
            return
        elif choice == "1":
            # Download all media
            await self._download_media(messages)
        elif choice == "2":
            # Select media to download
            await self._select_media(messages)
        elif choice == "3":
            # Filter media
            await self._filter_media(messages, entity)

    async def search_media(self):
        """Search for media across all chats."""
        console.print("\n[bold cyan]Search for Media[/bold cyan]")

        try:
            # Ensure connection
            if not await self.client.ensure_connected():
                console.print("[red]Not connected to Telegram. Please try again.[/red]")
                return

            # Ask for search query
            query = Prompt.ask("\nEnter search query (leave empty to skip)")

            # Ask for media types
            media_types = await self._ask_media_types()

            # Ask for limit
            limit = int(Prompt.ask("\nEnter maximum number of media items to fetch", default="50"))

            # Get media messages
            console.print("\n[bold cyan]Searching for media...[/bold cyan]")

            if query:
                # Search with query
                messages = await self.client.search_media(
                    query=query,
                    limit=limit,
                    media_types=media_types
                )
            else:
                # Get global media without query
                messages = await self.client.get_global_media(
                    limit=limit,
                    media_types=media_types
                )

            if not messages:
                console.print("[yellow]No media found.[/yellow]")
                return
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return

        console.print(f"[green]Found {len(messages)} media items.[/green]")

        # Show media preview
        await self._show_media_preview(messages)

        # Ask what to do with the media
        choice = Prompt.ask(
            "\nWhat would you like to do?",
            choices=["1", "2", "b"],
            default="1"
        )

        if choice == "b":
            return
        elif choice == "1":
            # Download all media
            await self._download_media(messages)
        elif choice == "2":
            # Select media to download
            await self._select_media(messages)

    async def configure_settings(self):
        """Configure TGrab settings."""
        console.print("\n[bold cyan]Configure Settings[/bold cyan]")

        # Show current settings
        console.print("\n[bold]Current Settings:[/bold]")

        # Organization options
        console.print(f"Organization method: {self.client.organization_options.get('organize_by', 'none')}")
        console.print(f"Filename template: {self.client.organization_options.get('filename_template', '{name}{prefix}_{id}.{ext}')}")
        console.print(f"Save metadata: {self.client.organization_options.get('save_metadata', False)}")

        # Filter options
        console.print(f"\nMin size: {self.client.filter_options.get('min_size')}")
        console.print(f"Max size: {self.client.filter_options.get('max_size')}")
        console.print(f"Min width: {self.client.filter_options.get('min_width')}")
        console.print(f"Min height: {self.client.filter_options.get('min_height')}")
        console.print(f"Min duration: {self.client.filter_options.get('min_duration')}")
        console.print(f"Max duration: {self.client.filter_options.get('max_duration')}")

        # Performance options
        console.print(f"\nParallel downloads: {self.client.performance_options.get('parallel', 1)}")

        # Deduplication options
        console.print(f"\nDeduplication enabled: {self.client.dedup_options.get('enabled', False)}")
        console.print(f"Deduplication method: {self.client.dedup_options.get('method', 'hash')}")
        console.print(f"Deduplication across users: {self.client.dedup_options.get('across_users', False)}")

        # Ask which setting to change
        console.print("\n[bold]Change Settings:[/bold]")
        console.print("1. Organization options")
        console.print("2. Filter options")
        console.print("3. Performance options")
        console.print("4. Deduplication options")
        console.print("5. Scheduled downloads")
        console.print("6. Back to main menu")

        choice = Prompt.ask("\nEnter your choice", choices=["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            await self._configure_organization()
        elif choice == "2":
            await self._configure_filters()
        elif choice == "3":
            await self._configure_performance()
        elif choice == "4":
            await self._configure_deduplication()
        elif choice == "5":
            await self._configure_scheduled_downloads()
        elif choice == "6":
            return

    async def _configure_organization(self):
        """Configure organization options."""
        console.print("\n[bold cyan]Configure Organization Options[/bold cyan]")

        # Ask for organization method
        organize_by = Prompt.ask(
            "Organization method",
            choices=["none", "date", "chat", "type"],
            default=self.client.organization_options.get("organize_by", "none")
        )

        # Ask for filename template
        filename_template = Prompt.ask(
            "Filename template",
            default=self.client.organization_options.get("filename_template", "{name}{prefix}_{id}.{ext}")
        )

        # Ask for save metadata
        save_metadata = Confirm.ask(
            "Save metadata?",
            default=self.client.organization_options.get("save_metadata", False)
        )

        # Update organization options
        self.client.organization_options.update({
            "organize_by": organize_by,
            "filename_template": filename_template,
            "save_metadata": save_metadata
        })

        console.print("[green]Organization options updated.[/green]")

    async def _configure_filters(self):
        """Configure filter options."""
        console.print("\n[bold cyan]Configure Filter Options[/bold cyan]")

        # Ask for min size
        min_size = Prompt.ask(
            "Minimum size (e.g., 10KB, 1MB)",
            default=str(self.client.filter_options.get("min_size", ""))
        )

        # Ask for max size
        max_size = Prompt.ask(
            "Maximum size (e.g., 10MB, 1GB)",
            default=str(self.client.filter_options.get("max_size", ""))
        )

        # Ask for min width
        min_width_str = Prompt.ask(
            "Minimum width in pixels",
            default=str(self.client.filter_options.get("min_width", ""))
        )
        min_width = int(min_width_str) if min_width_str.isdigit() else None

        # Ask for min height
        min_height_str = Prompt.ask(
            "Minimum height in pixels",
            default=str(self.client.filter_options.get("min_height", ""))
        )
        min_height = int(min_height_str) if min_height_str.isdigit() else None

        # Ask for min duration
        min_duration = Prompt.ask(
            "Minimum duration (e.g., 10s, 1m)",
            default=str(self.client.filter_options.get("min_duration", ""))
        )

        # Ask for max duration
        max_duration = Prompt.ask(
            "Maximum duration (e.g., 30s, 5m)",
            default=str(self.client.filter_options.get("max_duration", ""))
        )

        # Ask for caption filter
        has_caption = Confirm.ask(
            "Only media with captions?",
            default=self.client.filter_options.get("has_caption", False)
        )

        # Ask for caption contains
        caption_contains = Prompt.ask(
            "Caption contains text",
            default=str(self.client.filter_options.get("caption_contains", ""))
        )

        # Update filter options
        self.client.filter_options.update({
            "min_size": min_size if min_size else None,
            "max_size": max_size if max_size else None,
            "min_width": min_width,
            "min_height": min_height,
            "min_duration": min_duration if min_duration else None,
            "max_duration": max_duration if max_duration else None,
            "has_caption": has_caption,
            "caption_contains": caption_contains if caption_contains else None
        })

        console.print("[green]Filter options updated.[/green]")

    async def _configure_performance(self):
        """Configure performance options."""
        console.print("\n[bold cyan]Configure Performance Options[/bold cyan]")

        # Ask for parallel downloads
        parallel_str = Prompt.ask(
            "Number of parallel downloads",
            default=str(self.client.performance_options.get("parallel", 1))
        )
        parallel = int(parallel_str) if parallel_str.isdigit() else 1

        # Ask for chunk size
        chunk_size_str = Prompt.ask(
            "Download chunk size in KB",
            default=str(self.client.performance_options.get("chunk_size", 128 * 1024) // 1024)
        )
        chunk_size = int(chunk_size_str) * 1024 if chunk_size_str.isdigit() else 128 * 1024

        # Update performance options
        self.client.performance_options.update({
            "parallel": parallel,
            "chunk_size": chunk_size
        })

        console.print("[green]Performance options updated.[/green]")

    async def _configure_deduplication(self):
        """Configure deduplication options."""
        console.print("\n[bold cyan]Configure Deduplication Options[/bold cyan]")

        # Ask for deduplication enabled
        enabled = Confirm.ask(
            "Enable deduplication?",
            default=self.client.dedup_options.get("enabled", False)
        )

        # Ask for deduplication method
        method = Prompt.ask(
            "Deduplication method",
            choices=["hash", "filename", "size", "all"],
            default=self.client.dedup_options.get("method", "hash")
        )

        # Ask for deduplication across users
        across_users = Confirm.ask(
            "Apply deduplication across all users?",
            default=self.client.dedup_options.get("across_users", False)
        )

        # Update deduplication options
        self.client.dedup_options.update({
            "enabled": enabled,
            "method": method,
            "across_users": across_users
        })

        # Initialize deduplication database if enabled
        if enabled and not self.client.dedup_db:
            self.client.dedup_db = DedupDatabase(self.client.download_folder)

        console.print("[green]Deduplication options updated.[/green]")

    async def _configure_scheduled_downloads(self):
        """Configure scheduled downloads."""
        console.print("\n[bold cyan]Configure Scheduled Downloads[/bold cyan]")

        # Import scheduler
        from .scheduler import Scheduler

        # Create scheduler
        scheduler = Scheduler()

        # Show current scheduled tasks
        tasks = scheduler.list_tasks()

        if tasks:
            # Create a table to display tasks
            table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
            table.add_column("ID", style="dim")
            table.add_column("Name", style="cyan")
            table.add_column("Interval", style="green")
            table.add_column("Next Run", style="blue")

            for task in tasks:
                next_run = task.next_run.strftime("%Y-%m-%d %H:%M:%S") if task.next_run else "N/A"

                table.add_row(
                    str(task.task_id),
                    task.name,
                    task.interval,
                    next_run
                )

            console.print("\n[bold]Current Scheduled Tasks:[/bold]")
            console.print(table)
        else:
            console.print("\n[yellow]No scheduled tasks found.[/yellow]")

        # Show options
        console.print("\n[bold]Options:[/bold]")
        console.print("1. Add new scheduled task")
        console.print("2. Remove scheduled task")
        console.print("3. Back to settings")

        choice = Prompt.ask("\nEnter your choice", choices=["1", "2", "3"])

        if choice == "1":
            # Add new scheduled task
            await self._add_scheduled_task(scheduler)
        elif choice == "2":
            # Remove scheduled task
            await self._remove_scheduled_task(scheduler)
        elif choice == "3":
            return

    async def _add_scheduled_task(self, scheduler):
        """
        Add a new scheduled task.

        Args:
            scheduler: Scheduler instance
        """
        console.print("\n[bold cyan]Add New Scheduled Task[/bold cyan]")

        # Ask for task name
        name = Prompt.ask("Task name", default=f"TGrab Task {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Ask for interval
        interval = Prompt.ask("Interval (e.g., 1h, 30m, 1d)", default="1h")

        # Ask for user
        user = Prompt.ask("Username or user ID to download from (leave empty to skip)", default="")

        # Ask for media types
        media_types = await self._ask_media_types()
        media_types_str = ",".join(media_types)

        # Ask for limit
        limit = Prompt.ask("Maximum number of messages to check", default="100")

        # Build command
        import sys

        command = [sys.executable, "-m", "tgrab"]

        # Add arguments
        if user:
            command.extend(["--user", user])

        command.extend(["--limit", limit])
        command.extend(["--media-types", media_types_str])

        # Add current client options
        if self.client.organization_options.get("organize_by") != "none":
            command.extend(["--organize-by", self.client.organization_options.get("organize_by")])

        if self.client.organization_options.get("save_metadata"):
            command.append("--save-metadata")

        if self.client.filter_options.get("min_size"):
            command.extend(["--min-size", str(self.client.filter_options.get("min_size"))])

        if self.client.filter_options.get("max_size"):
            command.extend(["--max-size", str(self.client.filter_options.get("max_size"))])

        if self.client.filter_options.get("min_width"):
            command.extend(["--min-width", str(self.client.filter_options.get("min_width"))])

        if self.client.filter_options.get("min_height"):
            command.extend(["--min-height", str(self.client.filter_options.get("min_height"))])

        if self.client.filter_options.get("min_duration"):
            command.extend(["--min-duration", str(self.client.filter_options.get("min_duration"))])

        if self.client.filter_options.get("max_duration"):
            command.extend(["--max-duration", str(self.client.filter_options.get("max_duration"))])

        if self.client.filter_options.get("has_caption"):
            command.append("--has-caption")

        if self.client.filter_options.get("caption_contains"):
            command.extend(["--caption-contains", self.client.filter_options.get("caption_contains")])

        if self.client.performance_options.get("parallel") > 1:
            command.extend(["--parallel", str(self.client.performance_options.get("parallel"))])

        if self.client.dedup_options.get("enabled"):
            command.append("--dedup")
            command.extend(["--dedup-method", self.client.dedup_options.get("method", "hash")])

            if self.client.dedup_options.get("across_users"):
                command.append("--dedup-across-users")

        # Add the task
        task_id = scheduler.add_task(name, interval, command)

        console.print(f"\n[green]Task {task_id} added successfully.[/green]")
        console.print(f"[green]Name: {name}[/green]")
        console.print(f"[green]Interval: {interval}[/green]")
        console.print(f"[green]Command: {' '.join(command)}[/green]")

    async def _remove_scheduled_task(self, scheduler):
        """
        Remove a scheduled task.

        Args:
            scheduler: Scheduler instance
        """
        console.print("\n[bold cyan]Remove Scheduled Task[/bold cyan]")

        # Get tasks
        tasks = scheduler.list_tasks()

        if not tasks:
            console.print("[yellow]No scheduled tasks found.[/yellow]")
            return

        # Ask for task ID
        task_ids = [str(task.task_id) for task in tasks]
        task_id_str = Prompt.ask("Enter task ID to remove", choices=task_ids)
        task_id = int(task_id_str)

        # Confirm removal
        confirm = Confirm.ask(f"Are you sure you want to remove task {task_id}?")

        if not confirm:
            console.print("[yellow]Task removal cancelled.[/yellow]")
            return

        # Remove task
        if scheduler.remove_task(task_id):
            console.print(f"[green]Task {task_id} removed successfully.[/green]")
        else:
            console.print(f"[red]Failed to remove task {task_id}.[/red]")

    async def _ask_media_types(self) -> List[str]:
        """
        Ask user for media types to fetch.

        Returns:
            List of media types
        """
        console.print("\n[bold]Select media types:[/bold]")
        console.print("1. Photos")
        console.print("2. Videos")
        console.print("3. Documents")
        console.print("4. Audio")
        console.print("5. All media types")

        choice = Prompt.ask("\nEnter your choice", choices=["1", "2", "3", "4", "5"])

        if choice == "1":
            return ["photo"]
        elif choice == "2":
            return ["video"]
        elif choice == "3":
            return ["document"]
        elif choice == "4":
            return ["audio"]
        else:
            return ["photo", "video", "document", "audio"]

    async def _show_media_preview(self, messages: List[Message]):
        """
        Show a preview of media messages.

        Args:
            messages: List of media messages
        """
        console.print("\n[bold cyan]Media Preview[/bold cyan]")

        # Create a table to display media
        table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
        table.add_column("#", style="dim", width=4)
        table.add_column("Type", style="green")
        table.add_column("Date", style="blue")
        table.add_column("Size", style="cyan")
        table.add_column("Caption", style="yellow")

        # Add media to table
        for i, msg in enumerate(messages[:self.preview_count], 1):
            # Get media type
            media_type, _ = self.client.get_media_type_and_extension(msg)

            # Get date
            date = msg.date.strftime("%Y-%m-%d %H:%M")

            # Get size
            size = "Unknown"
            if hasattr(msg.media, 'document') and hasattr(msg.media.document, 'size'):
                size_bytes = msg.media.document.size
                if size_bytes < 1024:
                    size = f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    size = f"{size_bytes / 1024:.1f} KB"
                else:
                    size = f"{size_bytes / (1024 * 1024):.1f} MB"

            # Get caption
            caption = getattr(msg, 'message', '')
            if caption and len(caption) > 30:
                caption = caption[:27] + "..."

            # Add row to table
            table.add_row(
                str(i),
                media_type,
                date,
                size,
                caption
            )

        # Display table
        console.print(table)

        # Show total count
        if len(messages) > self.preview_count:
            console.print(f"[dim]Showing {self.preview_count} of {len(messages)} items[/dim]")

        # Show options
        console.print("\n[bold]Options:[/bold]")
        console.print("1. Download all media")
        console.print("2. Select media to download")
        console.print("3. Filter media")
        console.print("b. Back")

    async def _download_media(self, messages: List[Message]):
        """
        Download media messages.

        Args:
            messages: List of media messages
        """
        console.print("\n[bold cyan]Downloading Media[/bold cyan]")

        try:
            # Ensure connection
            if not await self.client.ensure_connected():
                console.print("[red]Not connected to Telegram. Please try again.[/red]")
                return

            # Create progress callback
            with console.status("[bold green]Downloading media...") as status:
                def progress_callback(current, total):
                    status.update(f"[bold green]Downloading media... {current}/{total}")

                # Download media
                stats = await self.client.download_media(
                    messages,
                    progress_callback=progress_callback
                )
        except Exception as e:
            console.print(f"[red]Error downloading media: {e}[/red]")
            return

        # Show download summary
        if stats["success"] > 0:
            console.print(f"[green]✓ {stats['success']} files downloaded to {os.path.abspath(self.client.download_folder)}[/green]")
        else:
            console.print("[yellow]No files downloaded[/yellow]")

        # Show duplicate files
        if stats.get("duplicates", 0) > 0:
            console.print(f"[blue]ℹ {stats['duplicates']} duplicate files skipped[/blue]")

        # Show pending downloads
        if stats.get("pending", 0) > 0:
            console.print(f"[yellow]⚠ {stats['pending']} downloads pending (will be retried next time)[/yellow]")

        # Show failed downloads
        if stats["failed"] > 0:
            console.print(f"[red]✗ {stats['failed']} downloads failed[/red]")

    async def _select_media(self, messages: List[Message]):
        """
        Select and download specific media messages.

        Args:
            messages: List of media messages
        """
        console.print("\n[bold cyan]Select Media to Download[/bold cyan]")

        # Create a table to display all media
        table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
        table.add_column("#", style="dim", width=4)
        table.add_column("Type", style="green")
        table.add_column("Date", style="blue")
        table.add_column("Size", style="cyan")
        table.add_column("Caption", style="yellow")

        # Add media to table
        for i, msg in enumerate(messages, 1):
            # Get media type
            media_type, _ = self.client.get_media_type_and_extension(msg)

            # Get date
            date = msg.date.strftime("%Y-%m-%d %H:%M")

            # Get size
            size = "Unknown"
            if hasattr(msg.media, 'document') and hasattr(msg.media.document, 'size'):
                size_bytes = msg.media.document.size
                if size_bytes < 1024:
                    size = f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    size = f"{size_bytes / 1024:.1f} KB"
                else:
                    size = f"{size_bytes / (1024 * 1024):.1f} MB"

            # Get caption
            caption = getattr(msg, 'message', '')
            if caption and len(caption) > 30:
                caption = caption[:27] + "..."

            # Add row to table
            table.add_row(
                str(i),
                media_type,
                date,
                size,
                caption
            )

        # Display table
        console.print(table)

        # Ask for selection
        selection = Prompt.ask(
            "\nEnter numbers to download (comma-separated, e.g., 1,3,5-7)",
            default="all"
        )

        # Parse selection
        selected_indices = []

        if selection.lower() == "all":
            selected_indices = list(range(len(messages)))
        else:
            parts = selection.split(",")
            for part in parts:
                part = part.strip()
                if "-" in part:
                    # Range
                    start, end = part.split("-")
                    if start.isdigit() and end.isdigit():
                        start_idx = int(start) - 1
                        end_idx = int(end)
                        if 0 <= start_idx < len(messages) and 0 < end_idx <= len(messages):
                            selected_indices.extend(range(start_idx, end_idx))
                elif part.isdigit():
                    # Single number
                    idx = int(part) - 1
                    if 0 <= idx < len(messages):
                        selected_indices.append(idx)

        # Get selected messages
        selected_messages = [messages[i] for i in selected_indices]

        if not selected_messages:
            console.print("[yellow]No media selected.[/yellow]")
            return

        # Download selected media
        await self._download_media(selected_messages)

    async def _filter_media(self, messages: List[Message], _=None):
        """
        Filter and download media messages.

        Args:
            messages: List of media messages
            _: Unused parameter (for compatibility)
        """
        console.print("\n[bold cyan]Filter Media[/bold cyan]")

        # Ask for date range
        console.print("\n[bold]Date range:[/bold]")
        date_from = Prompt.ask("From date (YYYY-MM-DD)", default="")
        date_to = Prompt.ask("To date (YYYY-MM-DD)", default="")

        # Ask for size range
        console.print("\n[bold]Size range:[/bold]")
        min_size = Prompt.ask("Minimum size (e.g., 10KB, 1MB)", default="")
        max_size = Prompt.ask("Maximum size (e.g., 10MB, 1GB)", default="")

        # Ask for dimensions
        console.print("\n[bold]Dimensions:[/bold]")
        min_width_str = Prompt.ask("Minimum width in pixels", default="")
        min_width = int(min_width_str) if min_width_str.isdigit() else None

        min_height_str = Prompt.ask("Minimum height in pixels", default="")
        min_height = int(min_height_str) if min_height_str.isdigit() else None

        # Ask for duration
        console.print("\n[bold]Duration (for videos/audio):[/bold]")
        min_duration = Prompt.ask("Minimum duration (e.g., 10s, 1m)", default="")
        max_duration = Prompt.ask("Maximum duration (e.g., 30s, 5m)", default="")

        # Ask for caption filter
        console.print("\n[bold]Caption:[/bold]")
        has_caption = Confirm.ask("Only media with captions?", default=False)
        caption_contains = Prompt.ask("Caption contains text", default="")

        # Parse dates
        from .cli import parse_date, parse_size, parse_duration

        date_from_obj = parse_date(date_from)
        date_to_obj = parse_date(date_to)

        # Filter messages
        filtered_messages = []

        for msg in messages:
            # Check date range
            if date_from_obj and msg.date < date_from_obj:
                continue
            if date_to_obj and msg.date > date_to_obj:
                continue

            # Check caption
            if has_caption and not getattr(msg, 'message', ''):
                continue

            if caption_contains and caption_contains.lower() not in getattr(msg, 'message', '').lower():
                continue

            # Check size
            if min_size or max_size:
                size_bytes = None
                if hasattr(msg.media, 'document') and hasattr(msg.media.document, 'size'):
                    size_bytes = msg.media.document.size

                if size_bytes:
                    if min_size:
                        min_size_bytes = parse_size(min_size)
                        if min_size_bytes and size_bytes < min_size_bytes:
                            continue

                    if max_size:
                        max_size_bytes = parse_size(max_size)
                        if max_size_bytes and size_bytes > max_size_bytes:
                            continue

            # Check dimensions
            if min_width or min_height:
                width = height = None

                if hasattr(msg.media, 'document') and hasattr(msg.media.document, 'attributes'):
                    for attr in msg.media.document.attributes:
                        if hasattr(attr, 'w') and hasattr(attr, 'h'):
                            width = attr.w
                            height = attr.h
                            break

                if width and height:
                    if min_width and width < min_width:
                        continue
                    if min_height and height < min_height:
                        continue

            # Check duration
            if min_duration or max_duration:
                duration = None

                if hasattr(msg.media, 'document') and hasattr(msg.media.document, 'attributes'):
                    for attr in msg.media.document.attributes:
                        if hasattr(attr, 'duration'):
                            duration = attr.duration
                            break

                if duration:
                    if min_duration:
                        min_duration_seconds = parse_duration(min_duration)
                        if min_duration_seconds and duration < min_duration_seconds:
                            continue

                    if max_duration:
                        max_duration_seconds = parse_duration(max_duration)
                        if max_duration_seconds and duration > max_duration_seconds:
                            continue

            # If we get here, the message passed all filters
            filtered_messages.append(msg)

        if not filtered_messages:
            console.print("[yellow]No media matches the filters.[/yellow]")
            return

        console.print(f"[green]Found {len(filtered_messages)} media items matching the filters.[/green]")

        # Show media preview
        await self._show_media_preview(filtered_messages)

        # Ask what to do with the filtered media
        choice = Prompt.ask(
            "\nWhat would you like to do?",
            choices=["1", "2", "b"],
            default="1"
        )

        if choice == "b":
            return
        elif choice == "1":
            # Download all filtered media
            await self._download_media(filtered_messages)
        elif choice == "2":
            # Select media to download
            await self._select_media(filtered_messages)
