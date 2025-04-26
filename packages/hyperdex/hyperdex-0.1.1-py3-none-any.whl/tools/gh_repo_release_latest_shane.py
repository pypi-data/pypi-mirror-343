#!/usr/bin/env python3

import csv
import subprocess
import json
import sys
import os
import platform

# Attempt to import packaging, provide guidance if missing
try:
    from packaging import version
except ImportError:
    print("Error: 'packaging' library not found.")
    print("Please install it: pip install packaging")
    sys.exit(1)

# --- Color Codes ---
# Check if running on Windows, which might not support ANSI codes directly
# in all terminals without extra configuration (like colorama or WT).
# Basic check, might need refinement for specific Windows terminal emulators.
IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    # Simple output for Windows without ANSI codes
    COLOR_GREEN = ""
    COLOR_RED = ""
    COLOR_YELLOW = ""
    COLOR_BLUE = ""
    COLOR_RESET = ""
    INDICATOR_SUCCESS = "[x]"
    INDICATOR_FAIL = "[ ]"
    INDICATOR_WARN = "[-]"
    INDICATOR_INFO = "[i]"
else:
    # ANSI escape codes for other terminals (Linux, macOS, modern Windows Terminal)
    COLOR_GREEN = "\033[32m"
    COLOR_RED = "\033[31m"
    COLOR_YELLOW = "\033[33m"
    COLOR_BLUE = "\033[34m"  # Added for info
    COLOR_RESET = "\033[0m"
    INDICATOR_SUCCESS = f"{COLOR_GREEN}[x]{COLOR_RESET}"
    INDICATOR_FAIL = f"{COLOR_RED}[ ]{COLOR_RESET}"
    INDICATOR_WARN = f"{COLOR_YELLOW}[-]{COLOR_RESET}"
    INDICATOR_INFO = f"{COLOR_BLUE}[i]{COLOR_RESET}"


# Configuration
GITHUB_USERNAME = "shaneholloman"
CSV_FILE = "github-project-readmes-shane/repositories.csv"
REPO_COLUMN_NAME = "Repository"  # Header in the CSV for repository names


# Allow returning CalledProcessError when check=False
def run_gh_command(
    command: list, check: bool = True, capture_output: bool = True
) -> subprocess.CompletedProcess | subprocess.CalledProcessError:
    """Helper function to run GitHub CLI commands."""
    try:
        # Using shell=False is generally safer, command should be a list
        process = subprocess.run(
            command,
            text=True,
            check=check,
            capture_output=capture_output,
            encoding="utf-8",  # Explicitly set encoding
        )
        # Log stderr even on success for potential warnings
        if process.stderr:
            print(f"Stderr from {' '.join(command)}:\n{process.stderr.strip()}", file=sys.stderr)
        return process
    except FileNotFoundError:
        print(
            f"Error: '{command[0]}' command not found. Make sure GitHub CLI (gh) is installed and in your PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        # Log more details on error
        print(f"Error running command: {' '.join(command)}", file=sys.stderr)
        print(f"Return Code: {e.returncode}", file=sys.stderr)
        if e.stdout:
            print(f"Stdout: {e.stdout.strip()}", file=sys.stderr)
        if e.stderr:
            print(f"Stderr: {e.stderr.strip()}", file=sys.stderr)
        # If check=False was intended, return the error object instead of raising
        if not check:
            return e
        # Re-raise the error if check=True (default)
        raise
    except Exception as e:
        print(f"An unexpected error occurred running {' '.join(command)}: {e}", file=sys.stderr)
        sys.exit(1)


def get_tags(repo_name: str) -> list:
    """Fetch tags for a repository."""
    print(f"--- Fetching tags for {repo_name} ---")
    command = ["gh", "api", f"repos/{GITHUB_USERNAME}/{repo_name}/tags"]
    # Don't exit if tags fetch fails (e.g., repo deleted or no tags)
    result = run_gh_command(command, check=False)
    # Check if the result object is an error or a success
    if isinstance(result, subprocess.CalledProcessError) or result.returncode != 0:
        print(f"{INDICATOR_WARN} Could not fetch tags for {repo_name} (Maybe no tags or repo deleted?). Skipping.")
        return []
    try:
        tags_data = json.loads(result.stdout)
        # Ensure tags_data is a list before proceeding
        if isinstance(tags_data, list):
            return [tag.get("name") for tag in tags_data if tag.get("name")]
        else:
            print(
                f"{INDICATOR_WARN} Unexpected format for tags data for {repo_name}. Expected a list, got {type(tags_data)}. Skipping."
            )
            return []
    except json.JSONDecodeError:
        print(f"{INDICATOR_FAIL} Error parsing tags JSON for {repo_name}. Skipping.")
        return []


def find_latest_semver_tag(tags: list) -> str | None:
    """Find the latest semantic version tag from a list, preferring non-prereleases."""
    latest_stable_v = None
    latest_stable_tag_str = None
    latest_prerelease_v = None
    latest_prerelease_tag_str = None

    # print(f"Analyzing tags: {tags}") # Keep this less verbose unless debugging

    for tag_str in tags:
        try:
            # Allow optional 'v' prefix
            current_v_str = tag_str.lstrip("v")
            # Check if string is empty after stripping 'v'
            if not current_v_str:
                print(f"Skipping empty tag string derived from '{tag_str}'")
                continue
            current_v = version.parse(current_v_str)

            # Ensure it's a valid Version object (handles legacy versions too)
            if not isinstance(current_v, version.Version):
                print(f"Skipping tag '{tag_str}' - parsed as non-standard version type: {type(current_v)}")
                continue

            if current_v.is_prerelease:
                if latest_prerelease_v is None or current_v > latest_prerelease_v:
                    latest_prerelease_v = current_v
                    latest_prerelease_tag_str = tag_str
            else:  # Stable release
                if latest_stable_v is None or current_v > latest_stable_v:
                    latest_stable_v = current_v
                    latest_stable_tag_str = tag_str

        except version.InvalidVersion:
            # Ignore tags that are not valid versions
            # print(f"Ignoring invalid version tag: {tag_str}") # Less verbose
            continue
        except Exception as e:
            print(f"{INDICATOR_WARN} Unexpected error parsing tag '{tag_str}': {e}")
            continue

    # Prefer the latest stable tag if found
    if latest_stable_tag_str:
        print(f"{INDICATOR_INFO} Latest SemVer tag found: {COLOR_YELLOW}{latest_stable_tag_str}{COLOR_RESET} (stable)")
        return latest_stable_tag_str
    elif latest_prerelease_tag_str:
        print(
            f"{INDICATOR_INFO} Latest SemVer tag found: {COLOR_YELLOW}{latest_prerelease_tag_str}{COLOR_RESET} (pre-release)"
        )
        return latest_prerelease_tag_str
    else:
        print(f"{INDICATOR_WARN} No valid SemVer tags found.")
        return None


def check_release_exists(repo_name: str, tag: str) -> bool:
    """Check if a release exists for a given tag."""
    print(f"Checking for existing release for tag {tag}...")
    # Use full repo path
    full_repo = f"{GITHUB_USERNAME}/{repo_name}"
    command = ["gh", "release", "view", tag, "-R", full_repo]
    # Run with check=False as non-existence is expected
    result = run_gh_command(command, check=False, capture_output=True)

    # `gh release view` exits with 0 if found, non-zero (usually 1) if not found
    # Check if the result object is an error or a success
    is_error = isinstance(result, subprocess.CalledProcessError)
    return_code = result.returncode if not is_error else -1  # Use -1 or similar if it's an error obj

    exists = return_code == 0
    if exists:
        print(f"{INDICATOR_WARN} Release already exists for tag {COLOR_YELLOW}{tag}{COLOR_RESET}.")
    else:
        # Check stderr specifically for "release not found" to be sure
        stderr_lower = result.stderr.lower() if hasattr(result, "stderr") and result.stderr else ""
        if "release not found" in stderr_lower or "could not find release" in stderr_lower:
            print(f"{INDICATOR_INFO} Release does not exist for tag {COLOR_YELLOW}{tag}{COLOR_RESET}.")
        else:
            # Log unexpected error but treat as "not found" to potentially retry later
            print(
                f"{INDICATOR_WARN} Could not confirm release status for tag {COLOR_YELLOW}{tag}{COLOR_RESET}. `gh release view` failed with unexpected error. Assuming not found.",
                file=sys.stderr,
            )
            if hasattr(result, "stderr") and result.stderr:
                print(f"Stderr: {result.stderr.strip()}", file=sys.stderr)
            # Return False, allowing the script to attempt creation.
            # If creation fails due to existence, gh release create will handle it.
            return False
    return exists


def create_release(repo_name: str, tag: str):
    """Create a release for the given tag with auto-generated notes."""
    print(f"Attempting to create release for tag {tag}...")
    # Use full repo path
    full_repo = f"{GITHUB_USERNAME}/{repo_name}"
    command = ["gh", "release", "create", tag, "--generate-notes", "-R", full_repo]
    # Run with check=True, will raise CalledProcessError if creation fails
    try:
        result = run_gh_command(command, check=True, capture_output=True)
        print(f"{INDICATOR_SUCCESS} Successfully created release: {result.stdout.strip()}")
        return True  # Indicate success
    except subprocess.CalledProcessError as e:
        # Check if the error is because the release already exists (race condition?)
        stderr_lower = e.stderr.lower() if e.stderr else ""
        if "release already exists" in stderr_lower:
            print(
                f"{INDICATOR_WARN} Release for tag {COLOR_YELLOW}{tag}{COLOR_RESET} already exists (detected during creation attempt)."
            )
            return False  # Indicate skipped/already exists
        else:
            # Log other creation errors
            print(
                f"{INDICATOR_FAIL} Failed to create release for tag {COLOR_YELLOW}{tag}{COLOR_RESET}.", file=sys.stderr
            )
            # Stderr was logged by run_gh_command
            return False  # Indicate failure (explicit return for mypy)


def main():
    """Main script logic."""
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file not found at {CSV_FILE}", file=sys.stderr)
        sys.exit(1)

    repos_to_process = []
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            # Check if the crucial column exists
            if REPO_COLUMN_NAME not in reader.fieldnames:
                print(f"Error: Column '{REPO_COLUMN_NAME}' not found in header of {CSV_FILE}", file=sys.stderr)
                print(f"Available columns: {reader.fieldnames}", file=sys.stderr)
                sys.exit(1)
            # Read repository names
            for row_number, row in enumerate(reader, start=2):  # start=2 for header row
                repo_name = row.get(REPO_COLUMN_NAME)
                if repo_name and repo_name.strip():
                    repos_to_process.append(repo_name.strip())
                else:
                    print(
                        f"{INDICATOR_WARN} Empty repository name found in row {row_number} of {CSV_FILE}",
                        file=sys.stderr,
                    )

    except Exception as e:
        print(f"{INDICATOR_FAIL} Error reading CSV file {CSV_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    if not repos_to_process:
        print(f"{INDICATOR_WARN} No valid repository names found in CSV file.")
        return

    print(f"{INDICATOR_INFO} Found {len(repos_to_process)} repositories in {CSV_FILE}. Starting process...")
    print("-" * 30)

    created_count = 0
    skipped_exist_count = 0
    skipped_no_tag_count = 0
    error_count = 0

    for repo_name in repos_to_process:
        print(f"Processing repository: {COLOR_BLUE}{repo_name}{COLOR_RESET}")
        try:
            tags = get_tags(repo_name)
            if not tags:
                # Already logged in get_tags if fetch failed
                skipped_no_tag_count += 1
                print("-" * 30)  # Separator
                continue

            latest_tag = find_latest_semver_tag(tags)
            if not latest_tag:
                # Already logged in find_latest_semver_tag
                skipped_no_tag_count += 1
                print("-" * 30)  # Separator
                continue

            if not check_release_exists(repo_name, latest_tag):
                if create_release(repo_name, latest_tag):
                    created_count += 1
                else:
                    # If create_release returned False, it might be due to race condition or other error
                    # Check again if it exists now, maybe it was created between check and create
                    if check_release_exists(repo_name, latest_tag):
                        # Message already printed by check_release_exists if it exists now
                        skipped_exist_count += 1
                    else:
                        # Message already printed by create_release if it failed
                        error_count += 1
            else:
                # Release already existed based on initial check (message printed by check_release_exists)
                skipped_exist_count += 1

        except Exception as e:
            # Catch unexpected errors during the loop for a specific repo
            print(f"{INDICATOR_FAIL} An critical error occurred processing {repo_name}: {e}", file=sys.stderr)
            error_count += 1
        finally:
            # Ensure separator prints even if an error occurs mid-processing
            print("-" * 30)

    print("\n--- Processing Complete ---")
    print(f"Repositories Processed: {len(repos_to_process)}")
    print(f"{INDICATOR_SUCCESS} Releases Successfully Created: {created_count}")
    print(f"{INDICATOR_WARN} Releases Skipped (already existed): {skipped_exist_count}")
    print(f"{INDICATOR_WARN} Releases Skipped (no valid tag found): {skipped_no_tag_count}")
    print(f"{INDICATOR_FAIL} Errors during processing: {error_count}")


if __name__ == "__main__":
    main()
