import subprocess
import sys
import os
import pkg_resources
# from importlib.metadata import distributions, PackageNotFoundError # Alternative for >= 3.8
import json # Needed for loading target_file in replay

from .history import (
    add_install_entry,
    add_uninstall_entry,
    load_history,
    save_exported_sequence,
    get_history_path,
    get_export_path,
    EXPORT_FILE_NAME # Import constant to check filename
)

# --- get_package_version (Finds version of an installed package) ---
def get_package_version(package_name):
    """Gets the installed version of a package."""
    try:
        # Normalize name for lookup using pkg_resources standard
        normalized_name = pkg_resources.safe_name(package_name).lower()
        return pkg_resources.get_distribution(normalized_name).version
    except pkg_resources.DistributionNotFound:
        # print(f"Debug: Version not found for '{package_name}' (normalized: '{normalized_name}')") # Optional debug
        return None
    except Exception as e:
        print(f"Warning: Error getting version for '{package_name}': {e}")
        return None

# --- run_pip_install (Executes pip install) ---
def run_pip_install(packages_to_install, pip_args=None):
    """Runs the actual pip install command."""
    command = [sys.executable, "-m", "pip", "install"]
    if pip_args:
        command.extend(pip_args)
    command.extend(packages_to_install)

    print(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        if result.stderr:
            # Sometimes pip logs warnings or non-fatal messages to stderr
            print("--- pip stderr ---", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            print("--- end pip stderr ---", file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: pip install failed with exit code {e.returncode}", file=sys.stderr)
        print("--- pip stdout ---", file=sys.stderr)
        print(e.stdout, file=sys.stderr)
        print("--- pip stderr ---", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        print("--- end pip output ---", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: Failed to execute pip install command. Error: {e}", file=sys.stderr)
        return False

# --- record_install (Wrapper for pip install + recording) ---
def record_install(packages_to_install, pip_args=None, history_path=None):
    """Runs pip install and records the successfully installed packages."""
    # Combine packages and args for recording the original command
    original_command_args = packages_to_install + (pip_args if pip_args else [])

    # Identify explicitly requested package names (best effort)
    requested_base_names = set()
    for pkg_spec in packages_to_install:
        # Ignore arguments/options starting with '-' unless part of a valid spec (e.g., URL, path)
        if pkg_spec.startswith('-') and not any(c in pkg_spec for c in":/@"):
             # Likely an option like -r, -e, -c, --upgrade etc. skip parsing as package name
             continue
        try:
            # pkg_resources Requirement parsing is good for standard names/specs
            req = pkg_resources.Requirement.parse(pkg_spec)
            requested_base_names.add(req.project_name.lower())
        except ValueError:
             # Handle complex cases like URLs, file paths, git links etc.
             # We won't try complex parsing here, just record the command
             # The version lookup later will try based on assumption or fail gracefully
             print(f"Info: Could not parse '{pkg_spec}' as standard requirement. Will attempt version lookup if install succeeds.")
             # Basic fallback: try to guess name before first standard specifier/separator
             name_part = pkg_spec
             # Prioritize separators that strongly indicate end of name
             for char in ['==', '<=', '>=', '<', '>', '~=', '===', '!=', '[', '#', '@', ' ']:
                 if char in name_part:
                     name_part = name_part.split(char, 1)[0].strip()
                     break
             # Further cleanup for potential file paths or URLs
             if os.path.sep in name_part or ':' in name_part:
                 # Too complex, don't add a likely incorrect base name
                 pass
             elif name_part:
                requested_base_names.add(name_part.lower())


    if not run_pip_install(packages_to_install, pip_args):
        print("Installation failed. Nothing recorded.")
        return False

    installed_info = []
    print("Recording versions for explicitly requested/identified packages...")
    # Rescan installed packages *after* the install command finishes
    pkg_resources.working_set = pkg_resources.WorkingSet()

    # Filter out duplicates and attempt version lookup
    unique_requested_names = set()
    for name in requested_base_names:
        # Normalize name for consistent checking
        normalized_name = pkg_resources.safe_name(name).lower()
        if normalized_name: # Avoid empty strings if parsing failed badly
            unique_requested_names.add(normalized_name)


    for name in unique_requested_names:
        version = get_package_version(name) # Uses normalized name internally
        if version:
            # Store the original name/spec if possible, fallback to normalized?
            # Let's store normalized name for consistency in replay keys
            installed_info.append({"package": name, "version": version})
        else:
            print(f"Could not determine installed version for '{name}' after install. It will not be added to the sequence record with a version.")
            # Optionally record without version? For now, skip to ensure replay works cleanly.
            # installed_info.append({"package": name, "version": None})

    if installed_info:
         add_install_entry(original_command_args, installed_info, path=history_path)
         return True
    elif not requested_base_names:
         # Handle cases like `pip-sequencer install -r req.txt` successfully ran
         print("Install command executed successfully, but no direct package names were specified or resolved for recording versions.")
         # Record a generic entry indicating the command ran
         add_install_entry(original_command_args, [], path=history_path)
         return True
    else:
         print("Install command ran, but no explicitly requested packages seem to have been installed successfully or version lookup failed. Nothing specific recorded.")
         return False # Indicate nothing *useful* was recorded

# --- run_pip_uninstall (Executes pip uninstall) ---
def run_pip_uninstall(packages_to_uninstall, pip_args=None):
    """Runs the actual pip uninstall command, always adding '-y'."""
    command = [sys.executable, "-m", "pip", "uninstall", "-y"] # Add -y automatically
    if pip_args:
        # Filter out '-y' if user accidentally provided it
        filtered_args = [arg for arg in pip_args if arg.lower() != '-y' and arg.lower() != '--yes']
        command.extend(filtered_args)
    # Add packages *after* options
    command.extend(packages_to_uninstall)

    print(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        if result.stderr:
            print("--- pip stderr ---", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            print("--- end pip stderr ---", file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        # pip uninstall often returns non-zero if a package wasn't found, but might proceed with others.
        # Check stderr for common "not installed" messages vs real errors.
        stderr_lower = e.stderr.lower()
        if "not installed" in stderr_lower or "no files were found" in stderr_lower:
             print(f"Warning: pip uninstall reported some packages not installed (exit code {e.returncode}). Proceeding.")
             print("--- pip stdout ---", file=sys.stderr)
             print(e.stdout, file=sys.stderr)
             print("--- pip stderr ---", file=sys.stderr)
             print(e.stderr, file=sys.stderr)
             print("--- end pip output ---", file=sys.stderr)
             return True # Treat as success for recording purposes if some packages were requested but not found
        else:
            print(f"Error: pip uninstall failed with exit code {e.returncode}", file=sys.stderr)
            print("--- pip stdout ---", file=sys.stderr)
            print(e.stdout, file=sys.stderr)
            print("--- pip stderr ---", file=sys.stderr)
            print(e.stderr, file=sys.stderr)
            print("--- end pip output ---", file=sys.stderr)
            return False # Genuine error
    except Exception as e:
        print(f"Error: Failed to execute pip uninstall command. Error: {e}", file=sys.stderr)
        return False

# --- record_uninstall (Wrapper for pip uninstall + recording) ---
def record_uninstall(packages_to_uninstall, pip_args=None, history_path=None):
    """Runs pip uninstall and records the action."""
    # Record the originally requested package names (excluding options)
    requested_packages = [pkg for pkg in packages_to_uninstall if not pkg.startswith('-')]
    # Combine packages and args for recording the original command
    original_command_args = packages_to_uninstall + (pip_args if pip_args else [])

    if not run_pip_uninstall(packages_to_uninstall, pip_args):
        print("Uninstall command failed or encountered significant errors. Nothing recorded.")
        return False

    # Rescan available packages after uninstall might be useful for other logic, but not strictly needed for recording this action.
    # pkg_resources.working_set = pkg_resources.WorkingSet()

    # Add entry to history using the *requested* packages list
    add_uninstall_entry(original_command_args, requested_packages, path=history_path)
    return True


# --- replay_install (Replays installs from history or export file) ---
def replay_install(history_path=None, start_step=1, end_step=None, target_file=None):
    """Replays the installation sequence from a history or export file."""
    is_export_file = False
    history = []

    if target_file:
        # Check if the target filename matches the default export filename pattern
        # This isn't foolproof if user renames files, but helps identify intent
        is_export_file = os.path.basename(target_file) == EXPORT_FILE_NAME
        replay_file_path = target_file
        print(f"Attempting to replay from specified file: {replay_file_path}")
        try:
            with open(replay_file_path, 'r', encoding='utf-8') as f:
                 content = f.read()
                 if not content:
                      history = []
                 else:
                      history = json.loads(content)
        except (FileNotFoundError) as e:
             print(f"Error: Replay file not found: {replay_file_path}")
             return
        except (json.JSONDecodeError, IOError) as e:
             print(f"Error: Could not load or parse replay file {replay_file_path}. Error: {e}")
             return
    else:
        # Default to using the standard history file
        replay_file_path = get_history_path(history_path)
        print(f"Attempting to replay from history file: {replay_file_path}")
        history = load_history(path=history_path) # Load from standard history path potentially overridden by --file
        is_export_file = False # Explicitly mark as not export file if target_file wasn't provided

    if not history:
        print(f"Replay file '{replay_file_path}' is empty or could not be loaded. Nothing to replay.")
        return

    print(f"Starting replay from file: {replay_file_path}")

    max_step = 0
    if history:
       try:
            # Find max sequence number, handling potential gaps or missing keys
            max_step = max(entry.get('sequence', 0) for entry in history)
       except ValueError:
           max_step = 0 # Handle empty history after loading


    # Determine the effective range of steps to process
    effective_start_step = max(1, start_step)
    effective_end_step = end_step if end_step is not None else float('inf') # Use infinity if no end step specified

    steps_processed_count = 0
    last_step_processed = 0
    replay_failed = False

    for entry in history:
        seq = entry.get('sequence', 0)

        # Skip if outside the requested sequence range
        if not (effective_start_step <= seq <= effective_end_step):
            continue

        # If reading from history file, only process 'install' actions
        action = entry.get('action')
        if not is_export_file and action != "install":
            print(f"Skipping step {seq}: Action '{action}' not replayed from history file.")
            continue

        print(f"\n--- Replaying Step {seq} ---")

        # Determine where the package list is: 'installed' for history, 'packages' for export
        installed_list = entry.get("installed") if not is_export_file else entry.get("packages")

        if not isinstance(installed_list, list) or not installed_list:
            print(f"Skipping step {seq}: No valid package list found in entry.")
            continue

        # Construct package==version strings for pip
        packages_to_install_specs = []
        valid_step = True
        for item in installed_list:
            if not isinstance(item, dict):
                 print(f"Warning: Skipping invalid item in step {seq}: {item}")
                 valid_step = False
                 break
            pkg = item.get('package')
            ver = item.get('version')
            if pkg and ver:
                 packages_to_install_specs.append(f"{pkg}=={ver}")
            elif pkg: # Handle case where version might be missing (allow install without constraint)
                 print(f"Warning: Version missing for package '{pkg}' in step {seq}. Attempting to install without version constraint.")
                 packages_to_install_specs.append(pkg)
            else:
                 print(f"Warning: Skipping entry with missing package name in step {seq}: {item}")
                 valid_step = False
                 break # Skip the whole step if an entry is badly malformed

        if not valid_step:
            print(f"Skipping step {seq} due to invalid item format.")
            continue

        if not packages_to_install_specs:
             print(f"Skipping step {seq}: No packages could be formatted for installation.")
             continue

        # Install packages from this step one by one to preserve order strictly
        step_success = True
        for package_spec in packages_to_install_specs:
             print(f"Attempting to install: {package_spec}")
             if not run_pip_install([package_spec]):
                 print(f"Error: Failed to install '{package_spec}' from step {seq}. Stopping replay.")
                 step_success = False
                 replay_failed = True
                 break # Stop installing packages within this step

        if not step_success:
             break # Stop the entire replay process if a step fails

        steps_processed_count += 1
        last_step_processed = seq
        print(f"--- Step {seq} completed ---")
        # Check if this was the user-specified end step
        if end_step is not None and seq == end_step:
            print(f"Reached specified end step {end_step}. Stopping replay.")
            break


    # --- Final Replay Summary ---
    print("\n--- Replay Summary ---")
    if steps_processed_count > 0:
        range_desc = f"from sequence {effective_start_step}"
        if end_step is not None:
             range_desc += f" up to {min(last_step_processed, end_step)}"
        elif last_step_processed > 0:
             range_desc += f" up to {last_step_processed}"
        else: # Only start_step processed
             range_desc = f"for sequence step {effective_start_step}"

        status = "partially completed" if replay_failed else "completed"
        print(f"Replay {status}. Processed {steps_processed_count} step(s) {range_desc} from {replay_file_path}.")
        if replay_failed:
             print("Replay stopped due to an error during installation.")
    else:
         range_desc = f"in range {effective_start_step}"
         if end_step is not None:
              range_desc += f" to {end_step}"
         else:
              range_desc += " onwards"
         print(f"No eligible install steps found {range_desc} in {replay_file_path}.")

    print("----------------------")


# --- export_sequence (Generates filtered sequence file) ---
def export_sequence(history_path=None, export_file_path=None):
    """Exports the sequence of currently installed packages based on history."""
    history = load_history(path=history_path)
    if not history:
        print(f"History file '{get_history_path(history_path)}' is empty or not found. Cannot export.")
        return

    print("Getting list of currently installed packages...")
    # Use pkg_resources to get currently installed packages (more reliable generally)
    pkg_resources.working_set = pkg_resources.WorkingSet() # Ensure it's fresh
    installed_packages_map = {} # Store as {normalized_name: distribution}
    try:
        for dist in pkg_resources.working_set:
             installed_packages_map[dist.key] = dist # key is already normalized name
    except Exception as e:
        print(f"Error getting installed packages via pkg_resources: {e}. Cannot perform export accurately.")
        return

    # Alternative: Use pip freeze (might be slower, different output format)
    # try:
    #     process = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, check=True, encoding='utf-8')
    #     installed_packages_map = {}
    #     for line in process.stdout.strip().splitlines():
    #         if '==' in line:
    #             name, version = line.split('==', 1)
    #             normalized_name = pkg_resources.safe_name(name).lower()
    #             installed_packages_map[normalized_name] = version # Only store version here
    #         # Handle editable installs etc. if needed
    # except Exception as e:
    #     print(f"Error getting installed packages via pip freeze: {e}. Cannot perform export accurately.")
    #     return

    if not installed_packages_map:
        print("Warning: No installed packages found in the current environment.")
        # Proceed, maybe history contains items installed then uninstalled

    print(f"Found {len(installed_packages_map)} installed packages.")

    filtered_sequence = []
    original_sequences_included = set()
    packages_added_to_export = set() # Track normalized names added

    print("Filtering history based on currently installed packages...")
    for entry in history:
        # Only consider 'install' actions from the history
        if entry.get("action") != "install":
            continue

        seq = entry.get("sequence")
        installed_list = entry.get("installed", [])

        if not isinstance(installed_list, list) or not installed_list:
            # Skip install steps that didn't record any specific packages
            # print(f"Debug: Skipping step {seq}: No 'installed' list or empty.")
            continue

        # Check if *all* packages explicitly recorded in this step are still present
        # AND ensure we haven't already added these specific packages from a *later* install step
        all_present_and_new = True
        packages_in_this_step_to_add = [] # Store tuples of (normalized_name, original_dict)

        for item in installed_list:
            if not isinstance(item, dict): continue # Skip malformed
            pkg_name = item.get("package")
            if not pkg_name: continue # Skip malformed

            normalized_name = pkg_resources.safe_name(pkg_name).lower()

            # Check 1: Is the package currently installed?
            if normalized_name not in installed_packages_map:
                # print(f"Debug: Package '{pkg_name}' (normalized: {normalized_name}) from step {seq} not currently installed.")
                all_present_and_new = False
                break

            # Check 2: Has this package already been added to the export from a LATER step?
            # This handles cases where a package was installed, then upgraded/reinstalled later.
            # We want the LATEST install action for each package in the final export.
            # (This requires iterating history potentially twice or storing seen packages with sequence numbers)
            # Simpler approach for now: Just ensure it's present. Let replay handle overrides if needed.
            # Refined check: Only add if not already added *to the export sequence*
            if normalized_name in packages_added_to_export:
                # This package was likely installed again in a later step that we've already processed (if iterating backwards)
                # Or if iterating forwards, we skip adding it here if a previous step already added it.
                # Let's iterate forward and add the FIRST time we see an installed package.
                # print(f"Debug: Package '{normalized_name}' from step {seq} already added to export.")
                # We don't set all_present_and_new = False here, just skip adding this specific package again.
                 pass # Don't add this package again, but don't invalidate the step for others
            else:
                 # Get current version to potentially update the record? No, stick to recorded version.
                 current_dist = installed_packages_map.get(normalized_name)
                 recorded_version = item.get("version")
                 # Sanity check: does recorded version roughly match current? Optional.
                 # if current_dist and recorded_version and current_dist.version != recorded_version:
                 #     print(f"Warning: Recorded version '{recorded_version}' for '{normalized_name}' in step {seq} differs from currently installed '{current_dist.version}'. Using recorded version for export.")

                 packages_in_this_step_to_add.append((normalized_name, item))


        # If after checking all items, the step is still valid and has packages to add
        if all_present_and_new and packages_in_this_step_to_add:
            # Add the packages from this step to the export
            valid_packages_for_export_entry = []
            for norm_name, item_dict in packages_in_this_step_to_add:
                 if norm_name not in packages_added_to_export:
                     valid_packages_for_export_entry.append(item_dict)
                     packages_added_to_export.add(norm_name) # Mark as added

            if valid_packages_for_export_entry:
                export_entry = {
                    "sequence": seq,
                    # Keep the original structure {"package": name, "version": ver}
                    "packages": valid_packages_for_export_entry
                }
                filtered_sequence.append(export_entry)
                original_sequences_included.add(seq)
                # print(f"Debug: Including step {seq} for packages: {[p['package'] for p in valid_packages_for_export_entry]}")


    if not filtered_sequence:
        print("No install steps from the history correspond to currently installed packages, or packages were already covered by earlier steps.")
        # Still try to generate freeze file
    else:
        # Sort by original sequence number
        filtered_sequence.sort(key=lambda x: x.get('sequence', 0))
        print(f"Generated export sequence with {len(filtered_sequence)} steps including {len(packages_added_to_export)} unique packages (original sequence numbers: {sorted(list(original_sequences_included))}).")
        # Save the filtered sequence
        save_exported_sequence(filtered_sequence, path=export_file_path)


    # --- Generate standard requirements.txt as well ---
    freeze_path = "requirements_frozen.txt"
    print(f"\nGenerating standard freeze file (no sequence) to {freeze_path}...")
    try:
        with open(freeze_path, 'w', encoding='utf-8') as f:
            # Use pip freeze for standard output
            result = subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=f, stderr=subprocess.PIPE, check=True, text=True, encoding='utf-8')
            if result.stderr:
                 print("--- pip freeze stderr ---", file=sys.stderr)
                 print(result.stderr, file=sys.stderr)
                 print("--- end pip freeze stderr ---", file=sys.stderr)
        print(f"Standard frozen requirements saved to {freeze_path}")
    except FileNotFoundError:
         print(f"Error: Could not find '{sys.executable} -m pip'. Is pip installed correctly in the environment?")
    except subprocess.CalledProcessError as e:
        print(f"Error running pip freeze (exit code {e.returncode}):", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
    except Exception as e:
        print(f"Could not generate standard requirements.txt: {e}")