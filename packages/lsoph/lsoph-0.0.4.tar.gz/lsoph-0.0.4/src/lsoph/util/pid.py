#!/usr/bin/env python3
# Filename: src/lsoph/util/pid.py

import argparse
import logging
import os
import sys

import psutil

log = logging.getLogger(__name__)


def get_descendants(parent_pid: int) -> list[int]:
    """
    Retrieves a list of all descendant process IDs (PIDs) for a given parent PID.
    """
    descendant_pids: list[int] = []
    try:
        parent = psutil.Process(parent_pid)
        descendant_procs = parent.children(recursive=True)
        descendant_pids = [proc.pid for proc in descendant_procs]
        log.debug(f"Found descendants for PID {parent_pid}: {descendant_pids}")
    except psutil.NoSuchProcess:
        log.warning(f"Process with PID {parent_pid} not found.")
    except psutil.AccessDenied:
        log.warning(f"Access denied getting descendants of PID {parent_pid}.")
    except Exception as e:
        log.error(f"Unexpected error getting descendants for PID {parent_pid}: {e}")
    return descendant_pids


def get_cwd(pid: int) -> bytes | None:
    """
    Retrieves the Current Working Directory (CWD) for a given PID as bytes.

    Uses psutil for cross-platform compatibility where possible, encodes the
    result using os.fsencode(). Falls back to /proc/<pid>/cwd on Linux if needed,
    which returns bytes directly.

    Args:
        pid: The Process ID.

    Returns:
        The absolute path bytes of the CWD, or None if the process doesn't exist,
        access is denied, or the CWD cannot be determined.
    """
    try:
        proc = psutil.Process(pid)
        cwd_str = proc.cwd()  # psutil returns str
        # --- ENCODE TO BYTES ---
        cwd_bytes = os.fsencode(cwd_str)
        # -----------------------
        log.debug(f"Retrieved CWD for PID {pid}: {cwd_str!r} -> {cwd_bytes!r}")
        return cwd_bytes
    except psutil.NoSuchProcess:
        log.warning(f"Process with PID {pid} not found when getting CWD.")
        return None
    except psutil.AccessDenied:
        log.warning(f"Access denied getting CWD for PID {pid} via psutil.")
        # Attempt Linux /proc fallback (might also fail with AccessDenied)
        try:
            # --- USE BYTES PATH ---
            proc_path = os.path.join(b"/proc", str(pid).encode("ascii"), b"cwd")
            # --------------------
            # Use os.stat on bytes path to check existence/permissions before readlink
            try:
                os.stat(proc_path)
            except FileNotFoundError:
                log.warning(f"/proc path {os.fsdecode(proc_path)!r} not found.")
                return None
            except PermissionError:
                log.warning(
                    f"Permission denied accessing /proc path {os.fsdecode(proc_path)!r}."
                )
                return None
            except OSError as stat_err:
                log.warning(
                    f"Error stating /proc path {os.fsdecode(proc_path)!r}: {stat_err}"
                )
                return None

            # If stat succeeded, try readlink
            cwd_bytes = os.readlink(proc_path)  # readlink on bytes path returns bytes
            log.debug(f"Retrieved CWD via /proc for PID {pid}: {cwd_bytes!r}")
            return cwd_bytes
        except (OSError, PermissionError) as e:
            log.warning(f"Failed /proc fallback for CWD of PID {pid}: {e}")
            return None
        except Exception as e:  # Catch other potential errors
            log.error(
                f"Unexpected error during /proc fallback for CWD of PID {pid}: {e}"
            )
            return None
    except Exception as e:
        # Catch other potential psutil errors (e.g., ZombieProcess on some platforms)
        log.error(f"An unexpected error occurred getting CWD for PID {pid}: {e}")
        return None


# --- Main Execution Function (for testing) ---
def main(argv: list[str] | None = None) -> int:
    """
    Command-line entry point for testing pid functions.
    """
    # --- Setup logging here ONLY for standalone script execution ---
    # This allows running `python -m lsoph.util.pid ...` with logging
    # It won't interfere when imported as a module by cli.py
    parser = argparse.ArgumentParser(
        description="Test PID utilities: List descendants or get CWD.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("pid", type=int, help="The PID of the target process.")
    parser.add_argument(
        "--log",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: WARNING)",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--descendants", action="store_true", help="List descendant PIDs (default)."
    )
    mode_group.add_argument("--cwd", action="store_true", help="Get the process CWD.")

    args = parser.parse_args(argv)

    # Configure logging based on args ONLY if run as main
    logging.basicConfig(
        level=args.log.upper(), format="%(levelname)s:%(name)s:%(message)s"
    )
    # -----------------------------------------------------------------

    try:
        if args.cwd:
            cwd_bytes = get_cwd(args.pid)
            if cwd_bytes:
                # Print bytes directly to stdout, let terminal handle display
                sys.stdout.buffer.write(cwd_bytes + b"\n")
                sys.stdout.buffer.flush()
            else:
                print(f"Could not retrieve CWD for PID {args.pid}.", file=sys.stderr)
                return 1
        else:  # Default to descendants
            descendant_pids = get_descendants(args.pid)
            if not descendant_pids:
                # Check if process exists at all
                if not psutil.pid_exists(args.pid):
                    print(f"Process {args.pid} not found.", file=sys.stderr)
                    return 1
                else:
                    # Process exists but no descendants found (or access denied)
                    print(
                        f"No descendants found for PID {args.pid} (or access denied)."
                    )
            else:
                for d_pid in descendant_pids:
                    print(d_pid)
        return 0  # Success
    except Exception as e:
        log.critical(f"An unexpected error occurred in main: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
