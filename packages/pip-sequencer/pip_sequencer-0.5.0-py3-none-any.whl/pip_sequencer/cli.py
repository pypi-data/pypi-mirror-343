import argparse
import sys
import os # Needed for basename in replay argument processing
from .recorder import (
    record_install,
    record_uninstall,
    replay_install,
    export_sequence
)
from .history import get_history_path, get_export_path, EXPORT_FILE_NAME # Import constants

def main():
    parser = argparse.ArgumentParser(
        description="Record, replay, and export pip installation sequences.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter # Show defaults in help
    )
    parser.add_argument(
        "--file", "-f",
        metavar="HISTORY_FILE",
        help=f"Path to the sequence history file used for recording and potentially replaying/exporting.",
        default=get_history_path() # Use function to get default path dynamically
    )

    subparsers = parser.add_subparsers(dest="command", required=True, metavar='COMMAND')

    # --- Install Subparser ---
    parser_install = subparsers.add_parser(
        "install",
        help="Run 'pip install' and record the sequence. Pass pip arguments after '--'.",
        description="Wraps 'pip install'. Records explicitly specified packages and their installed versions to the history file. Use '--' to separate packages/options for this command from options intended for pip itself."
    )
    parser_install.add_argument(
        "packages",
        nargs='+',
        help="Package(s) or requirements file(s) to install (e.g., requests flask==2.0 -r reqs.txt)"
    )
    parser_install.add_argument(
        'pip_args',
        nargs=argparse.REMAINDER,
        help="Arguments to pass directly to pip install (prefix with '--', e.g., -- --no-cache-dir)"
    )

    # --- Uninstall Subparser ---
    parser_uninstall = subparsers.add_parser(
        "uninstall",
        help="Run 'pip uninstall -y' and record the action. Pass other pip args after '--'.",
        description="Wraps 'pip uninstall'. Automatically adds '-y' to confirm. Records the packages requested for removal to the history file. Use '--' to separate packages for this command from options intended for pip itself."
    )
    parser_uninstall.add_argument(
        "packages",
        nargs='+',
        help="Package(s) to uninstall (e.g., requests flask)"
    )
    parser_uninstall.add_argument(
        'pip_args',
        nargs=argparse.REMAINDER,
        help="Arguments to pass directly to pip uninstall (prefix with '--', e.g., -- --no-save)"
    )

    # --- Replay Subparser ---
    parser_replay = subparsers.add_parser(
        "replay",
        help="Re-install packages sequentially from history or an export file.",
        description=f"Reads install sequences from either the full history file ('{get_history_path()}') or a filtered export file ('{EXPORT_FILE_NAME}' by default, created by 'export'). Replays only install actions. Use '--from-export' to specify the export file."
    )
    parser_replay.add_argument(
        "--from-export",
        metavar="EXPORT_FILE",
        nargs='?', # Optional argument for the path
        const=get_export_path(), # Default value if flag is present *without* a value
        default=None, # Default if flag is *absent*
        help=f"Replay from a filtered export file instead of the full history file specified by --file. If path is omitted after flag, defaults to '{get_export_path()}'.",
    )
    parser_replay.add_argument(
        "--start", type=int, default=1, metavar="N",
        help="Sequence number (from the file being replayed) to start replay from."
    )
    parser_replay.add_argument(
        "--end", type=int, default=None, metavar="N",
        help="Sequence number (from the file being replayed) to end replay at (inclusive). Default: replay to the end of the file."
    )

    # --- Export Subparser ---
    parser_export = subparsers.add_parser(
        "export",
        help=f"Generate a sequenced file of currently installed packages based on install history.",
        description=f"Reads the history file (specified by --file), checks currently installed packages, and writes a new sequence file (default: '{EXPORT_FILE_NAME}') containing only the relevant install steps. Also creates 'requirements_frozen.txt'."
    )
    parser_export.add_argument(
        "--output", "-o",
        metavar="EXPORT_FILE",
        help=f"Path to save the exported sequence file.",
        default=get_export_path() # Use function to get default path dynamically
    )

    args = parser.parse_args()

    # Determine the history file path to use (relevant for all commands reading/writing history)
    # The --file argument on the main parser overrides the default.
    history_file_to_use = args.file

    exit_code = 0 # Default to success

    try:
        if args.command == "install":
            pip_options = args.pip_args
            # Correctly handle case where REMIANDER might capture '--'
            if pip_options and pip_options[0] == '--':
                pip_options = pip_options[1:]
            if not record_install(args.packages, pip_args=pip_options, history_path=history_file_to_use):
                 exit_code = 1 # Indicate failure if recording function returns False

        elif args.command == "uninstall":
            pip_options = args.pip_args
            if pip_options and pip_options[0] == '--':
                pip_options = pip_options[1:]
            if not record_uninstall(args.packages, pip_args=pip_options, history_path=history_file_to_use):
                 exit_code = 1

        elif args.command == "replay":
            # Determine the file to replay from
            # If --from-export is given (even without a value), args.from_export will not be None.
            # If --from-export is *not* given, args.from_export will be None.
            replay_target = args.from_export # This is either None or the path (default or specified)

            # We pass the history_path from --file as the fallback if replay_target is None
            replay_install(
                history_path=history_file_to_use if replay_target is None else None, # Pass history path only if not using export
                start_step=args.start,
                end_step=args.end,
                target_file=replay_target # Pass the specific export file path if provided
            )
            # Replay function prints errors, we don't strictly need to set exit code here unless it returns status

        elif args.command == "export":
            # Export reads from history_file_to_use and writes to args.output
            export_sequence(
                history_path=history_file_to_use,
                export_file_path=args.output
            )
            # Export function prints errors

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        # import traceback
        # traceback.print_exc() # Uncomment for detailed debugging
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()