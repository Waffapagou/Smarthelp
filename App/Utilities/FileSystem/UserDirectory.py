"""
All the path for uploads and more
"""
import os

#app.py path
base_dir = os.getcwd()
# relative dir
relative_dir = "uploads"
# Uploads dir path
uploads_dir = base_dir+"/static/uploads"

def get_user_dir (user_token) :
    """
    Return user dir path using user_token
    """
    return uploads_dir+"/"+str (user_token)

def get_user_files_dir (user_token) :
    """
    Return user file dir path using user_token
    """
    return uploads_dir+"/"+str (user_token)+"/files"

def create_user_directory(user_token:str) -> bool:
    """
    Create the necessary directories for a user.

    Args:
        user_token (str): The token associated with the user.

    Returns:
        None

    Raises:
        OSError: If there is an error creating the directory.

    """
    try:
        # Create /uploads/<user_token>
        os.mkdir(get_user_dir(user_token))
        # Create /uploads/<user_token>/files
        os.mkdir(get_user_files_dir(user_token))
        return True
    except OSError as e:
        raise OSError("Error creating user directory") from e 

def delete_user_directory(user_token:str) -> bool:
    """
    Delete the directories associated with a user.

    Args:
        user_token (str): The token associated with the user.

    Returns:
        None

    Raises:
        OSError: If there is an error deleting the directory.

    """
    try:
        # Delete /uploads/<user_token>/files
        os.rmdir(get_user_files_dir(user_token))
        # Delete /uploads/<user_token>
        os.rmdir(get_user_dir(user_token))
        return True
    except OSError as e:
        raise OSError("Error deleting user directory") from e