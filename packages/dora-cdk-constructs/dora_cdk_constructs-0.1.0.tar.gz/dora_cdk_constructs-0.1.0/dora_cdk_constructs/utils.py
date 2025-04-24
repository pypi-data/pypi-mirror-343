"""Utility functions for the stack module."""
import shutil
import json
import os

from dora_core.conf import Profile
from dora_core.utils import logger

log = logger(__name__)

def update_profile(name: str = None):
    """
    Update the profile with the given name by loading its stack outputs and saving the updated profile.

    This function loads the profile specified by the name parameter, reads the stack outputs from the profile's stack file,
    constructs a dictionary with the target, updates the profile's jobs with this dictionary, and saves the updated profile.

    Args:
        name (str, optional): The name of the profile to update. If not provided, the default profile is loaded.
    """
    if name is None:
        profile = Profile.load()
    else:
        profile = Profile.load(name)  # Load the profile with the given name
    with open(profile.stack, mode='r', encoding='utf-8') as _f:
        outputs = json.load(_f)[profile.name]['Outputs']  # Load the stack outputs from the profile's stack file
        construcs = {profile.target: json.loads(outputs)}  # Parse the outputs and create a dictionary with the target
    profile.jobs = construcs  # Update the profile's jobs with the constructed dictionary
    log.info('Updated profile:%s', profile.name)
    profile.save(name)  # Save the updated profile

def rm_dir(directory_path):
    """
    Removes a directory and all its contents if it exists.

    This function checks if the specified directory exists and is a directory. If so, it removes the directory and all its contents.
    If the directory does not exist, it logs a debug message.

    Args:
        directory_path (str): The path to the directory to be removed.
    """
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
        log.debug("Directory '%s' has been removed.", directory_path)
    else:
        log.debug("Directory '%s' does not exist.", directory_path)
