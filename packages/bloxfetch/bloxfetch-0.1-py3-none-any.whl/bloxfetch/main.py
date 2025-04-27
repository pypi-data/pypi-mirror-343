import requests

__all__ = ["fetch_user"]

class User:
    def __init__(self, user_id, size="large"):
        """
        Initialize the User object, fetching user details along with avatar and headshot URLs.

        Args:
            user_id (int): The Roblox user ID.
            size (str): The size of the images ("small", "medium", "large", "xlarge").
        """
        self.user_id = user_id
        self.size_mapping = {
            "small": "50x50",
            "medium": "100x100",
            "large": "420x420",
            "xlarge": "840x840",
        }

        if size not in self.size_mapping:
            raise ValueError(f"Invalid size '{size}'. Valid options are: {', '.join(self.size_mapping.keys())}")

        self.size = size
        self.name = None
        self.display_name = None
        self.avatar_url = None
        self.headshot_url = None
        self.description = None
        self._fetch_user_data()

    def _fetch_user_data(self):
        """
        Fetches user data, avatar URL, and headshot URL from Roblox API.
        """
        try:
            # Fetch user details
            user_url = f"https://users.roblox.com/v1/users/{self.user_id}"
            user_response = requests.get(user_url)
            user_response.raise_for_status()
            user_data = user_response.json()

            self.name = user_data.get("name", "Name not found")
            self.display_name = user_data.get("displayName", "Display name not found")
            self.description = user_data.get("description", "Description not found")

            # Fetch avatar URL
            avatar_url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={self.user_id}&size={self.size_mapping[self.size]}&format=png&isCircular=false"
            avatar_response = requests.get(avatar_url)
            avatar_response.raise_for_status()
            avatar_data = avatar_response.json()

            if 'data' in avatar_data and len(avatar_data['data']) > 0:
                self.avatar_url = avatar_data['data'][0].get('imageUrl', "Avatar URL not found")
            else:
                self.avatar_url = "Avatar URL not found"

            # Fetch headshot URL
            headshot_url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={self.user_id}&size={self.size_mapping[self.size]}&format=png&isCircular=false"
            headshot_response = requests.get(headshot_url)
            headshot_response.raise_for_status()
            headshot_data = headshot_response.json()

            if 'data' in headshot_data and len(headshot_data['data']) > 0:
                self.headshot_url = headshot_data['data'][0].get('imageUrl', "Headshot URL not found")
            else:
                self.headshot_url = "Headshot URL not found"

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to fetch user data: {e}")


def fetch_user(user_id, size="large"):
    """
    Fetches a User object for the given Roblox user ID.

    Args:
        user_id (int): The Roblox user ID.
        size (str): The size of the images ("small", "medium", "large", "xlarge").

    Returns:
        User: The User object containing user details, avatar, and headshot URLs.
    """
    return User(user_id, size)