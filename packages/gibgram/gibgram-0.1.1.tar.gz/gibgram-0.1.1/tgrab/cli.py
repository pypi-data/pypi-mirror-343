"""
Command-line interface for TGrab.

This module provides a clean, minimal CLI for the TGrab tool.
"""

import os
import sys
import re
import asyncio
import argparse
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime

from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn
from rich.panel import Panel
from rich import box

from dotenv import load_dotenv

from .client import TGrabClient

# Configure logging - minimal output
logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize rich console
console = Console()

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="TGrab - Minimal Telegram Media Grabber",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-u", "--user",
        help="Username or user ID to download media from"
    )

    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=100,
        help="Maximum number of messages to check"
    )

    parser.add_argument(
        "-o", "--output",
        default="downloads",
        help="Output directory for downloaded media"
    )

    parser.add_argument(
        "--from-date",
        help="Start date for filtering messages (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--to-date",
        help="End date for filtering messages (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--session",
        default="gibgram",
        help="Session name for Telegram authentication"
    )

    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to .env file with API credentials"
    )

    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Run in background monitoring mode to catch self-destructing media"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Interval in seconds between checks when in monitoring mode"
    )

    parser.add_argument(
        "--media-types",
        default="photo",
        help="Comma-separated list of media types to download (photo, document, video)"
    )

    parser.add_argument(
        "--retry-pending",
        action="store_true",
        help="Retry downloading previously failed media files"
    )

    parser.add_argument(
        "--store-credentials",
        action="store_true",
        help="Store API credentials securely in the system keyring"
    )

    parser.add_argument(
        "--use-session-string",
        help="Use a session string instead of a session file"
    )

    parser.add_argument(
        "--export-session",
        action="store_true",
        help="Export the current session as a string"
    )

    # Media organization options
    organization_group = parser.add_argument_group("Media Organization")

    organization_group.add_argument(
        "--organize-by",
        choices=["date", "type", "chat", "none"],
        default="none",
        help="How to organize downloaded media in folders"
    )

    organization_group.add_argument(
        "--filename-template",
        default="{name}{prefix}_{id}.{ext}",
        help="Template for filenames. Available variables: {name}, {prefix}, {timestamp}, {id}, {ext}, {sender}, {chat}"
    )

    organization_group.add_argument(
        "--save-metadata",
        action="store_true",
        help="Save message metadata (caption, date, sender) alongside media files"
    )

    # Media filtering options
    filter_group = parser.add_argument_group("Media Filtering")

    filter_group.add_argument(
        "--min-size",
        help="Minimum file size (e.g., 100KB, 1MB, 2.5MB)"
    )

    filter_group.add_argument(
        "--max-size",
        help="Maximum file size (e.g., 10MB, 1GB)"
    )

    filter_group.add_argument(
        "--min-width",
        type=int,
        help="Minimum width for images/videos (in pixels)"
    )

    filter_group.add_argument(
        "--min-height",
        type=int,
        help="Minimum height for images/videos (in pixels)"
    )

    filter_group.add_argument(
        "--min-duration",
        help="Minimum duration for videos/audio (e.g., 10s, 1m, 1h)"
    )

    filter_group.add_argument(
        "--max-duration",
        help="Maximum duration for videos/audio (e.g., 30s, 5m, 1h)"
    )

    filter_group.add_argument(
        "--has-caption",
        action="store_true",
        help="Only download media with captions"
    )

    filter_group.add_argument(
        "--caption-contains",
        help="Only download media with captions containing this text"
    )

    filter_group.add_argument(
        "--date-after",
        help="Only download media sent after this date (YYYY-MM-DD)"
    )

    filter_group.add_argument(
        "--date-before",
        help="Only download media sent before this date (YYYY-MM-DD)"
    )

    # Performance options
    performance_group = parser.add_argument_group("Performance")

    performance_group.add_argument(
        "--parallel",
        type=int,
        default=1,
        help="Number of parallel downloads (default: 1)"
    )

    performance_group.add_argument(
        "--chunk-size",
        type=int,
        default=128,
        help="Download chunk size in KB (default: 128)"
    )

    # Deduplication options
    dedup_group = parser.add_argument_group("Deduplication")

    dedup_group.add_argument(
        "--dedup",
        action="store_true",
        help="Enable media deduplication to avoid downloading duplicate files"
    )

    dedup_group.add_argument(
        "--dedup-method",
        choices=["hash", "filename", "size", "all"],
        default="hash",
        help="Method to use for deduplication (default: hash)"
    )

    dedup_group.add_argument(
        "--dedup-across-users",
        action="store_true",
        help="Apply deduplication across all users, not just the current one"
    )

    # Interactive mode options
    interactive_group = parser.add_argument_group("Interactive Mode")

    interactive_group.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )

    interactive_group.add_argument(
        "--preview-count",
        type=int,
        default=5,
        help="Number of media items to preview in interactive mode (default: 5)"
    )

    # Scheduled downloads options
    schedule_group = parser.add_argument_group("Scheduled Downloads")

    schedule_group.add_argument(
        "--schedule",
        action="store_true",
        help="Run in scheduled mode"
    )

    schedule_group.add_argument(
        "--schedule-add",
        action="store_true",
        help="Add a new scheduled task"
    )

    schedule_group.add_argument(
        "--schedule-list",
        action="store_true",
        help="List all scheduled tasks"
    )

    schedule_group.add_argument(
        "--schedule-remove",
        type=int,
        help="Remove a scheduled task by ID"
    )

    schedule_group.add_argument(
        "--schedule-interval",
        type=str,
        help="Interval for scheduled downloads (e.g., '1h', '30m', '1d')"
    )

    schedule_group.add_argument(
        "--schedule-name",
        type=str,
        help="Name for the scheduled task"
    )

    return parser.parse_args()

def load_env(env_file: str) -> Dict[str, Any]:
    """
    Load environment variables from .env file or secure storage.

    Args:
        env_file: Path to .env file

    Returns:
        Dict with API credentials
    """
    # Try to get credentials from keyring first
    try:
        import keyring
        api_id = keyring.get_password("gibgram", "api_id")
        api_hash = keyring.get_password("gibgram", "api_hash")
        phone = keyring.get_password("gibgram", "phone")

        # If all credentials are found in keyring, use them
        if all([api_id, api_hash, phone]):
            logger.info("Using credentials from secure keyring")
            return {
                "api_id": int(api_id),
                "api_hash": api_hash,
                "phone": phone
            }
        else:
            logger.info("Some credentials not found in keyring, falling back to .env file")
    except ImportError:
        logger.info("Keyring not available, falling back to .env file")
    except Exception as e:
        logger.warning(f"Error accessing keyring: {e}, falling back to .env file")

    # Fall back to .env file
    if os.path.exists(env_file):
        load_dotenv(env_file)

    # Get credentials from environment
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    phone = os.getenv("TELEGRAM_PHONE")

    # Validate credentials
    if not all([api_id, api_hash, phone]):
        console.print(Panel(
            "[bold red]Missing Telegram API credentials[/bold red]\n\n"
            "Please create a .env file with the following variables:\n"
            "- TELEGRAM_API_ID\n"
            "- TELEGRAM_API_HASH\n"
            "- TELEGRAM_PHONE\n\n"
            "You can get these from https://my.telegram.org/auth\n\n"
            "Alternatively, you can store them securely using the --store-credentials option.",
            title="Error",
            border_style="red",
            box=box.ROUNDED
        ))
        sys.exit(1)

    return {
        "api_id": int(api_id),
        "api_hash": api_hash,
        "phone": phone
    }

def store_credentials_in_keyring(api_id: str, api_hash: str, phone: str) -> bool:
    """
    Store API credentials in the system's secure keyring.

    Args:
        api_id: Telegram API ID
        api_hash: Telegram API hash
        phone: Phone number

    Returns:
        bool: True if credentials were stored successfully
    """
    try:
        import keyring
        keyring.set_password("gibgram", "api_id", api_id)
        keyring.set_password("gibgram", "api_hash", api_hash)
        keyring.set_password("gibgram", "phone", phone)
        return True
    except ImportError:
        console.print("[yellow]Keyring module not available. Cannot store credentials securely.[/yellow]")
        return False
    except Exception as e:
        console.print(f"[red]Error storing credentials in keyring: {e}[/red]")
        return False

def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse date string in YYYY-MM-DD format."""
    if not date_str:
        return None

    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        console.print(f"[yellow]Warning: Invalid date format: {date_str}. Using None.[/yellow]")
        return None

def parse_size(size_str: Optional[str]) -> Optional[int]:
    """
    Parse a size string like '10MB' or '1.5GB' into bytes.

    Args:
        size_str: Size string or None

    Returns:
        Size in bytes or None
    """
    if not size_str:
        return None

    # Remove any spaces
    size_str = size_str.replace(" ", "")

    # Define size multipliers
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 * 1024,
        'GB': 1024 * 1024 * 1024,
        'TB': 1024 * 1024 * 1024 * 1024
    }

    # Match pattern like '10MB', '1.5GB', etc.
    pattern = r'^(\d+(\.\d+)?)([KMGT]?B)$'
    match = re.match(pattern, size_str, re.IGNORECASE)

    if not match:
        console.print(f"[yellow]Warning: Invalid size format: {size_str}. Use formats like 100KB, 10MB, 1.5GB. Using None.[/yellow]")
        return None

    value = float(match.group(1))
    unit = match.group(3).upper()

    if unit not in multipliers:
        console.print(f"[yellow]Warning: Invalid size unit: {unit}. Use B, KB, MB, GB, or TB. Using None.[/yellow]")
        return None

    return int(value * multipliers[unit])

def parse_duration(duration_str: Optional[str]) -> Optional[int]:
    """
    Parse a duration string like '10s', '5m', '1h' into seconds.

    Args:
        duration_str: Duration string or None

    Returns:
        Duration in seconds or None
    """
    if not duration_str:
        return None

    # Remove any spaces
    duration_str = duration_str.replace(" ", "")

    # Define duration multipliers
    multipliers = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400
    }

    # Match pattern like '10s', '5m', '1.5h', etc.
    pattern = r'^(\d+(\.\d+)?)([smhd])$'
    match = re.match(pattern, duration_str, re.IGNORECASE)

    if not match:
        console.print(f"[yellow]Warning: Invalid duration format: {duration_str}. Use formats like 30s, 5m, 1.5h, 2d. Using None.[/yellow]")
        return None

    value = float(match.group(1))
    unit = match.group(3).lower()

    if unit not in multipliers:
        console.print(f"[yellow]Warning: Invalid duration unit: {unit}. Use s, m, h, or d. Using None.[/yellow]")
        return None

    return int(value * multipliers[unit])

async def monitor_messages(client, user, interval=30, limit=20, media_types=None, code_callback=None):
    """
    Monitor for new messages continuously, focusing on self-destructing media.

    Args:
        client: TGrabClient instance
        user: User entity
        interval: Seconds between checks
        limit: Maximum number of messages to check each time
        media_types: List of media types to download
        code_callback: Optional callback for verification codes if reconnection is needed
    """
    if media_types is None:
        media_types = ["photo"]
    last_message_id = 0
    total_downloaded = 0
    total_self_destructing = 0

    console.print("[bold cyan]Monitoring mode activated[/bold cyan]")
    console.print(f"[dim]Checking for new messages every {interval} seconds...[/dim]")
    console.print("[dim]Press Ctrl+C to stop monitoring[/dim]")

    try:
        while True:
            # Get new messages
            with console.status(f"[cyan]Checking for new messages...[/cyan]"):
                messages = await client.get_media_messages(
                    user=user,
                    limit=limit,
                    min_id=last_message_id,
                    media_types=media_types,
                    code_callback=code_callback
                )

            if messages:
                # Update last message ID
                last_message_id = max(msg.id for msg in messages)

                # Count self-destructing messages
                self_destructing_count = sum(
                    1 for msg in messages
                    if getattr(msg, 'is_self_destructing', False) or getattr(msg, 'is_likely_self_destructing', False)
                )

                if self_destructing_count > 0:
                    console.print(f"[bold red]! Found {self_destructing_count} self-destructing images![/bold red]")

                # Get media type description
                media_types_str = "media files" if len(media_types) > 1 else f"{media_types[0]}s"
                console.print(f"[cyan]Found {len(messages)} new {media_types_str}[/cyan]")

                # Download media
                with Progress(
                    TextColumn("[cyan]{task.description}"),
                    BarColumn(bar_width=40),
                    TextColumn("[cyan]{task.completed}/{task.total}"),
                    console=console
                ) as progress:
                    task = progress.add_task("Downloading", total=len(messages))

                    # Progress callback
                    def update_progress(current, _):
                        progress.update(task, completed=current)

                    # Download media
                    stats = await client.download_media(
                        messages,
                        progress_callback=update_progress,
                        code_callback=code_callback
                    )

                # Update totals
                total_downloaded += stats["success"]
                total_self_destructing += stats.get("self_destructing", 0)

                # Show results
                console.print(f"[green]✓ {stats['success']} files downloaded[/green]")

                if stats.get('self_destructing', 0) > 0:
                    console.print(f"[bold red]! {stats['self_destructing']} self-destructing media files saved[/bold red]")

                # Show metadata info if any were saved
                if stats.get('metadata_files', []):
                    console.print(f"[cyan]ℹ {len(stats['metadata_files'])} metadata files saved[/cyan]")

                if stats.get('failed', 0) > 0:
                    console.print(f"[yellow]✗ {stats['failed']} files failed[/yellow]")

                # Show pending downloads
                if stats.get('pending', 0) > 0:
                    console.print(f"[blue]ℹ {stats['pending']} files queued for future retry[/blue]")

                # Show running totals
                console.print(f"[dim]Total downloaded: {total_downloaded} ({total_self_destructing} self-destructing)[/dim]")

            # Wait for next check
            await asyncio.sleep(interval)

    except asyncio.CancelledError:
        console.print("\n[yellow]Monitoring stopped[/yellow]")
        console.print(f"[green]Total downloaded: {total_downloaded} files ({total_self_destructing} self-destructing)[/green]")

async def main_async():
    """Async entry point for the CLI."""
    # Parse arguments
    args = parse_args()

    # Load credentials
    creds = load_env(args.env_file)

    # Handle store-credentials option
    if args.store_credentials:
        console.print("[cyan]Storing credentials in secure keyring...[/cyan]")
        if store_credentials_in_keyring(
            str(creds["api_id"]),
            creds["api_hash"],
            creds["phone"]
        ):
            console.print("[green]✓ Credentials stored successfully[/green]")
        else:
            console.print("[yellow]Failed to store credentials securely[/yellow]")

    # Parse dates
    date_from = parse_date(args.from_date)
    date_to = parse_date(args.to_date)

    # Parse additional date filters
    date_after = parse_date(args.date_after)
    date_before = parse_date(args.date_before)

    # Use the most restrictive date range
    if date_after and (not date_from or date_after > date_from):
        date_from = date_after
    if date_before and (not date_to or date_before < date_to):
        date_to = date_before

    # Parse media types
    media_types = [media_type.strip() for media_type in args.media_types.split(",") if media_type.strip()]
    if not media_types:
        media_types = ["photo"]  # Default to photos if no valid types provided

    # Parse size filters
    min_size = parse_size(args.min_size)
    max_size = parse_size(args.max_size)

    # Parse duration filters
    min_duration = parse_duration(args.min_duration)
    max_duration = parse_duration(args.max_duration)

    # Create filter options
    filter_options = {
        "min_size": min_size,
        "max_size": max_size,
        "min_width": args.min_width,
        "min_height": args.min_height,
        "min_duration": min_duration,
        "max_duration": max_duration,
        "has_caption": args.has_caption,
        "caption_contains": args.caption_contains
    }

    # Show minimal banner
    console.print("[bold cyan]TGrab[/bold cyan] [dim]v0.1.0[/dim]")

    # Create organization options
    organization_options = {
        "organize_by": args.organize_by,
        "filename_template": args.filename_template,
        "save_metadata": args.save_metadata
    }

    # Create performance options
    performance_options = {
        "parallel": args.parallel,
        "chunk_size": args.chunk_size * 1024  # Convert KB to bytes
    }

    # Create deduplication options
    dedup_options = {
        "enabled": args.dedup,
        "method": args.dedup_method,
        "across_users": args.dedup_across_users
    }

    # Initialize client
    client = TGrabClient(
        api_id=creds["api_id"],
        api_hash=creds["api_hash"],
        phone=creds["phone"],
        session_name=args.session,
        download_folder=args.output,
        session_string=args.use_session_string,
        organization_options=organization_options,
        filter_options=filter_options,
        performance_options=performance_options,
        dedup_options=dedup_options
    )

    # Check if interactive mode is enabled
    if args.interactive:
        from .interactive import InteractiveMode
        interactive = InteractiveMode(client, preview_count=args.preview_count)
        try:
            await interactive.start()
        except Exception as e:
            console.print(f"[bold red]Error in interactive mode: {e}[/bold red]")
        finally:
            # Ensure client is disconnected
            await client.disconnect()
        return

    # Check if scheduled mode is enabled
    if args.schedule or args.schedule_add or args.schedule_list or args.schedule_remove:
        from .scheduler import Scheduler

        # Create scheduler
        scheduler = Scheduler()

        # Handle schedule commands
        if args.schedule_list:
            # List scheduled tasks
            tasks = scheduler.list_tasks()

            if not tasks:
                console.print("[yellow]No scheduled tasks found.[/yellow]")
                return

            # Create a table to display tasks
            from rich.table import Table

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="dim")
            table.add_column("Name", style="cyan")
            table.add_column("Interval", style="green")
            table.add_column("Next Run", style="blue")
            table.add_column("Command", style="yellow")

            for task in tasks:
                next_run = task.next_run.strftime("%Y-%m-%d %H:%M:%S") if task.next_run else "N/A"
                command = " ".join(task.command)

                table.add_row(
                    str(task.task_id),
                    task.name,
                    task.interval,
                    next_run,
                    command
                )

            console.print(table)
            return

        elif args.schedule_remove is not None:
            # Remove a scheduled task
            task_id = args.schedule_remove

            if scheduler.remove_task(task_id):
                console.print(f"[green]Task {task_id} removed successfully.[/green]")
            else:
                console.print(f"[red]Task {task_id} not found.[/red]")

            return

        elif args.schedule_add:
            # Add a new scheduled task
            if not args.schedule_interval:
                console.print("[red]Error: --schedule-interval is required for adding a task.[/red]")
                return

            # Get task name
            name = args.schedule_name or f"GibGram Task {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Build command
            import sys

            command = [sys.executable, "-m", "gibgram"]

            # Add all arguments except scheduling ones
            for arg_name, arg_value in vars(args).items():
                if arg_name.startswith("schedule_") or arg_name == "schedule":
                    continue

                if arg_value is True:
                    command.append(f"--{arg_name.replace('_', '-')}")
                elif arg_value not in [False, None]:
                    command.append(f"--{arg_name.replace('_', '-')}")
                    command.append(str(arg_value))

            # Add the task
            task_id = scheduler.add_task(name, args.schedule_interval, command)

            console.print(f"[green]Task {task_id} added successfully.[/green]")
            console.print(f"[green]Name: {name}[/green]")
            console.print(f"[green]Interval: {args.schedule_interval}[/green]")
            console.print(f"[green]Command: {' '.join(command)}[/green]")

            return

        elif args.schedule:
            # Run the scheduler
            console.print("[cyan]Starting scheduler...[/cyan]")

            try:
                scheduler.start()

                # Keep the main thread alive
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                console.print("\n[yellow]Stopping scheduler...[/yellow]")
                scheduler.stop()

            return

    try:
        # Connect to Telegram
        console.print("[cyan]Connecting...[/cyan]")

        # Custom code callback
        async def code_callback():
            console.print("\n[yellow]Verification required[/yellow]")
            return console.input("[bold]Enter code from Telegram: [/bold]")

        connected = await client.connect(code_callback=code_callback)
        if not connected:
            console.print("[red]Connection failed[/red]")
            return

        # Handle export-session option
        if args.export_session:
            session_string = await client.get_session_string()
            if session_string:
                console.print(Panel(
                    f"[bold green]Session String:[/bold green]\n\n{session_string}",
                    title="Session Export",
                    border_style="green",
                    box=box.ROUNDED
                ))
                console.print("[yellow]Keep this string secure! It can be used to access your Telegram account.[/yellow]")
                console.print("[cyan]Use it with the --use-session-string option to avoid entering verification codes.[/cyan]")
                return
            else:
                console.print("[red]Failed to export session string[/red]")
                return

        # Skip user lookup for store-credentials option
        if args.store_credentials:
            return

        # Check if user argument is provided for operations that require it
        if not args.user:
            if args.monitor or args.retry_pending or not args.export_session:
                console.print("[red]Error: --user argument is required for this operation[/red]")
                return

        # Get user if needed
        user = None
        if args.user:
            user = await client.get_user(args.user, code_callback=code_callback)
            if not user:
                console.print(f"[red]User not found: {args.user}[/red]")
                return

        # Check if retry-pending mode is enabled
        if args.retry_pending:
            console.print("[cyan]Retrying pending downloads...[/cyan]")

            # Minimal progress bar
            with Progress(
                TextColumn("[cyan]{task.description}"),
                BarColumn(bar_width=40),
                TextColumn("[cyan]{task.completed}/{task.total}"),
                console=console
            ) as progress:
                # We don't know the total yet, so start with 0
                task = progress.add_task("Retrying", total=0)

                # Progress callback
                def update_progress(current, total):
                    # Update total if it changed
                    if progress.tasks[task].total != total:
                        progress.update(task, total=total)
                    progress.update(task, completed=current)

                # Retry pending downloads
                stats = await client.retry_pending_downloads(
                    user=user,
                    progress_callback=update_progress,
                    code_callback=code_callback
                )

            # Show results
            if stats["success"] > 0:
                console.print(f"[green]✓ {stats['success']} files recovered[/green]")

                # Show self-destructing media info if any were found
                if stats.get('self_destructing', 0) > 0:
                    console.print(f"[bold red]! {stats['self_destructing']} self-destructing images saved[/bold red]")
            else:
                console.print("[yellow]No files were recovered[/yellow]")

            if stats["failed"] > 0:
                console.print(f"[yellow]✗ {stats['failed']} files failed again[/yellow]")

            # Show remaining pending downloads
            if stats.get('pending', 0) > 0:
                console.print(f"[blue]ℹ {stats['pending']} files still pending[/blue]")

            return

        # Check if monitoring mode is enabled
        if args.monitor:
            await monitor_messages(
                client=client,
                user=user,
                interval=args.interval,
                limit=args.limit,
                media_types=media_types,
                code_callback=code_callback
            )
            return

        # Regular mode - get media messages
        with console.status("[cyan]Fetching messages...[/cyan]"):
            messages = await client.get_media_messages(
                user=user,
                limit=args.limit,
                date_from=date_from,
                date_to=date_to,
                media_types=media_types,
                code_callback=code_callback
            )

        if not messages:
            console.print("[yellow]No media found[/yellow]")
            return

        # Count self-destructing messages
        self_destructing_count = sum(
            1 for msg in messages
            if getattr(msg, 'is_self_destructing', False) or getattr(msg, 'is_likely_self_destructing', False)
        )

        if self_destructing_count > 0:
            console.print(f"[bold red]! Found {self_destructing_count} self-destructing images![/bold red]")

        # Get media type description
        media_types_str = "media files" if len(media_types) > 1 else f"{media_types[0]}s"
        console.print(f"[cyan]Found {len(messages)} {media_types_str}[/cyan]")

        # Minimal progress bar
        with Progress(
            TextColumn("[cyan]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[cyan]{task.completed}/{task.total}"),
            console=console
        ) as progress:
            task = progress.add_task("Downloading", total=len(messages))

            # Progress callback
            def update_progress(current, _):
                progress.update(task, completed=current)

            # Download media
            stats = await client.download_media(
                messages,
                progress_callback=update_progress,
                code_callback=code_callback
            )

        # Show minimal results with self-destructing info
        console.print(f"[green]✓ {stats['success']} files downloaded to {os.path.abspath(args.output)}[/green]")

        # Show self-destructing media info if any were found
        if stats.get('self_destructing', 0) > 0:
            console.print(f"[bold red]! {stats['self_destructing']} self-destructing media files saved[/bold red]")

        # Show metadata info if any were saved
        if stats.get('metadata_files', []):
            console.print(f"[cyan]ℹ {len(stats['metadata_files'])} metadata files saved[/cyan]")

        if stats['failed'] > 0:
            console.print(f"[yellow]✗ {stats['failed']} files failed[/yellow]")

        # Show pending downloads
        if stats.get('pending', 0) > 0:
            console.print(f"[blue]ℹ {stats['pending']} files queued for future retry[/blue]")

        # Show organization info
        if args.organize_by != "none":
            console.print(f"[dim]Files organized by: {args.organize_by}[/dim]")

        # Show active filters
        active_filters = []
        if args.min_size:
            active_filters.append(f"min size: {args.min_size}")
        if args.max_size:
            active_filters.append(f"max size: {args.max_size}")
        if args.min_width:
            active_filters.append(f"min width: {args.min_width}px")
        if args.min_height:
            active_filters.append(f"min height: {args.min_height}px")
        if args.min_duration:
            active_filters.append(f"min duration: {args.min_duration}")
        if args.max_duration:
            active_filters.append(f"max duration: {args.max_duration}")
        if args.has_caption:
            active_filters.append("has caption")
        if args.caption_contains:
            active_filters.append(f"caption contains: '{args.caption_contains}'")
        if args.date_after:
            active_filters.append(f"after: {args.date_after}")
        if args.date_before:
            active_filters.append(f"before: {args.date_before}")

        if active_filters:
            console.print(f"[dim]Filters applied: {', '.join(active_filters)}[/dim]")

        # Show performance info
        if args.parallel > 1:
            console.print(f"[dim]Using {args.parallel} parallel downloads with {args.chunk_size}KB chunks[/dim]")

        # Show deduplication info
        if args.dedup:
            dedup_info = f"Deduplication enabled (method: {args.dedup_method}"
            if args.dedup_across_users:
                dedup_info += ", across all users"
            dedup_info += ")"
            console.print(f"[dim]{dedup_info}[/dim]")

        # Show duplicate stats if available
        if stats and isinstance(stats, dict) and stats.get('duplicates', 0) > 0:
            console.print(f"[blue]ℹ {stats['duplicates']} duplicate files skipped[/blue]")

    finally:
        # Disconnect
        await client.disconnect()

def main():
    """Entry point for the CLI."""
    try:
        # Create event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Create main task
        main_task = loop.create_task(main_async())

        try:
            # Run until complete
            loop.run_until_complete(main_task)
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print("\n[yellow]Operation cancelled by user[/yellow]")

            # Cancel the main task
            main_task.cancel()

            # Allow task to handle cancellation
            try:
                loop.run_until_complete(main_task)
            except asyncio.CancelledError:
                pass
        finally:
            # Clean up pending tasks
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()

            # Run until all tasks are cancelled
            if pending:
                try:
                    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                except asyncio.CancelledError:
                    pass

            # Close the loop
            loop.close()
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
