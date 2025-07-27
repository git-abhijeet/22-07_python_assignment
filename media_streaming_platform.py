from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random


class MediaContent(ABC):
    def __init__(self, title, content_id, is_premium=False):
        self.title = title
        self.content_id = content_id
        self.is_premium = is_premium
        self.ratings = []
    
    @abstractmethod
    def play(self):
        pass
    
    @abstractmethod
    def get_duration(self):
        pass
    
    @abstractmethod
    def get_file_size(self):
        pass
    
    @abstractmethod
    def calculate_streaming_cost(self):
        pass
    
    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.ratings.append(rating)
            return True
        return False
    
    def get_average_rating(self):
        if not self.ratings:
            return 0
        return sum(self.ratings) / len(self.ratings)
    
    def is_premium_content(self):
        return self.is_premium


class StreamingDevice(ABC):
    def __init__(self, device_id, device_name):
        self.device_id = device_id
        self.device_name = device_name
        self.is_connected = False
    
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def stream_content(self, content):
        pass
    
    @abstractmethod
    def adjust_quality(self, quality):
        pass
    
    def get_device_info(self):
        return f"{self.device_name} (ID: {self.device_id})"
    
    def check_compatibility(self, content):
        return True


class Movie(MediaContent):
    def __init__(self, title, content_id, duration_minutes, resolution, genre, director, is_premium=False):
        super().__init__(title, content_id, is_premium)
        self.duration_minutes = duration_minutes
        self.resolution = resolution
        self.genre = genre
        self.director = director
    
    def play(self):
        return f"Playing movie: {self.title} directed by {self.director}"
    
    def get_duration(self):
        return self.duration_minutes
    
    def get_file_size(self):
        base_size = self.duration_minutes * 10
        if self.resolution == "4K":
            return base_size * 4
        elif self.resolution == "1080p":
            return base_size * 2
        return base_size
    
    def calculate_streaming_cost(self):
        base_cost = 0.05 * self.duration_minutes
        return base_cost * 2 if self.is_premium else base_cost


class TVShow(MediaContent):
    def __init__(self, title, content_id, episodes, seasons, current_episode=1, is_premium=False):
        super().__init__(title, content_id, is_premium)
        self.episodes = episodes
        self.seasons = seasons
        self.current_episode = current_episode
    
    def play(self):
        return f"Playing TV Show: {self.title} - Episode {self.current_episode}"
    
    def get_duration(self):
        return self.episodes * 45
    
    def get_file_size(self):
        return self.episodes * 45 * 8
    
    def calculate_streaming_cost(self):
        base_cost = 0.03 * self.episodes * 45
        return base_cost * 1.5 if self.is_premium else base_cost


class Podcast(MediaContent):
    def __init__(self, title, content_id, episode_number, duration_minutes, transcript_available=False):
        super().__init__(title, content_id, False)
        self.episode_number = episode_number
        self.duration_minutes = duration_minutes
        self.transcript_available = transcript_available
    
    def play(self):
        return f"Playing Podcast: {self.title} - Episode {self.episode_number}"
    
    def get_duration(self):
        return self.duration_minutes
    
    def get_file_size(self):
        return self.duration_minutes * 1
    
    def calculate_streaming_cost(self):
        return 0.01 * self.duration_minutes


class Music(MediaContent):
    def __init__(self, title, content_id, artist, album, duration_minutes, lyrics_available=False, is_premium=False):
        super().__init__(title, content_id, is_premium)
        self.artist = artist
        self.album = album
        self.duration_minutes = duration_minutes
        self.lyrics_available = lyrics_available
    
    def play(self):
        return f"Playing Music: {self.title} by {self.artist}"
    
    def get_duration(self):
        return self.duration_minutes
    
    def get_file_size(self):
        return self.duration_minutes * 0.5
    
    def calculate_streaming_cost(self):
        base_cost = 0.02 * self.duration_minutes
        return base_cost * 1.5 if self.is_premium else base_cost


class SmartTV(StreamingDevice):
    def __init__(self, device_id):
        super().__init__(device_id, "Smart TV")
        self.supports_4k = True
        self.surround_sound = True
    
    def connect(self):
        self.is_connected = True
        return "Smart TV connected via WiFi"
    
    def stream_content(self, content):
        if not self.is_connected:
            return "Device not connected"
        return f"Streaming {content.title} on large screen with 4K support"
    
    def adjust_quality(self, quality):
        return f"Quality adjusted to {quality} on Smart TV"


class Laptop(StreamingDevice):
    def __init__(self, device_id):
        super().__init__(device_id, "Laptop")
        self.headphone_support = True
    
    def connect(self):
        self.is_connected = True
        return "Laptop connected"
    
    def stream_content(self, content):
        if not self.is_connected:
            return "Device not connected"
        return f"Streaming {content.title} on laptop with headphone support"
    
    def adjust_quality(self, quality):
        return f"Quality adjusted to {quality} on Laptop"


class Mobile(StreamingDevice):
    def __init__(self, device_id):
        super().__init__(device_id, "Mobile")
        self.battery_optimization = True
    
    def connect(self):
        self.is_connected = True
        return "Mobile connected"
    
    def stream_content(self, content):
        if not self.is_connected:
            return "Device not connected"
        return f"Streaming {content.title} on mobile with battery optimization"
    
    def adjust_quality(self, quality):
        return f"Quality adjusted to {quality} for battery optimization"


class SmartSpeaker(StreamingDevice):
    def __init__(self, device_id):
        super().__init__(device_id, "Smart Speaker")
        self.voice_control = True
        self.audio_only = True
    
    def connect(self):
        self.is_connected = True
        return "Smart Speaker connected"
    
    def stream_content(self, content):
        if not self.is_connected:
            return "Device not connected"
        if isinstance(content, (Movie, TVShow)):
            return "Smart Speaker supports audio-only content"
        return f"Playing audio: {content.title} on Smart Speaker"
    
    def adjust_quality(self, quality):
        return f"Audio quality adjusted to {quality}"


class User:
    def __init__(self, user_id, name, subscription_tier="Free"):
        self.user_id = user_id
        self.name = name
        self.subscription_tier = subscription_tier
        self.watch_history = []
        self.preferences = []
    
    def add_to_history(self, content):
        self.watch_history.append({
            "content": content,
            "timestamp": datetime.now()
        })
    
    def set_preferences(self, preferences):
        self.preferences = preferences
    
    def can_access_premium(self):
        return self.subscription_tier in ["Premium", "Family"]


class StreamingPlatform:
    def __init__(self, platform_name):
        self.platform_name = platform_name
        self.content_library = []
        self.users = {}
        self.devices = {}
    
    def add_content(self, content):
        self.content_library.append(content)
    
    def register_user(self, user):
        self.users[user.user_id] = user
    
    def register_device(self, device):
        self.devices[device.device_id] = device
    
    def stream_content(self, user_id, content_id, device_id):
        user = self.users.get(user_id)
        content = next((c for c in self.content_library if c.content_id == content_id), None)
        device = self.devices.get(device_id)
        
        if not all([user, content, device]):
            return "Invalid user, content, or device"
        
        if content.is_premium_content() and not user.can_access_premium():
            return "Premium subscription required"
        
        device.connect()
        result = device.stream_content(content)
        user.add_to_history(content)
        return result
    
    def recommend_content(self, user_id):
        user = self.users.get(user_id)
        if not user:
            return []
        
        recommendations = []
        for content in self.content_library:
            if content.get_average_rating() > 3.5:
                recommendations.append(content)
        
        return recommendations[:5]
    
    def get_analytics(self, user_id):
        user = self.users.get(user_id)
        if not user:
            return {}
        
        total_watch_time = sum(item["content"].get_duration() for item in user.watch_history)
        content_types = {}
        
        for item in user.watch_history:
            content_type = type(item["content"]).__name__
            content_types[content_type] = content_types.get(content_type, 0) + 1
        
        return {
            "total_watch_time": total_watch_time,
            "content_breakdown": content_types,
            "total_items_watched": len(user.watch_history)
        }


if __name__ == "__main__":
    # Create streaming platform
    platform = StreamingPlatform("StreamFlix")
    
    # Create content
    movie = Movie("Inception", "M001", 148, "4K", "Sci-Fi", "Christopher Nolan", True)
    tv_show = TVShow("Breaking Bad", "TV001", 62, 5, 1, True)
    podcast = Podcast("Tech Talk", "P001", 15, 45, True)
    music = Music("Bohemian Rhapsody", "MU001", "Queen", "A Night at the Opera", 6, True, False)
    
    # Add content to platform
    platform.add_content(movie)
    platform.add_content(tv_show)
    platform.add_content(podcast)
    platform.add_content(music)
    
    # Create devices
    smart_tv = SmartTV("D001")
    laptop = Laptop("D002")
    mobile = Mobile("D003")
    speaker = SmartSpeaker("D004")
    
    # Register devices
    platform.register_device(smart_tv)
    platform.register_device(laptop)
    platform.register_device(mobile)
    platform.register_device(speaker)
    
    # Create users
    premium_user = User("U001", "John Doe", "Premium")
    free_user = User("U002", "Jane Smith", "Free")
    
    # Register users
    platform.register_user(premium_user)
    platform.register_user(free_user)
    
    # Test polymorphism
    print("=== Testing Polymorphism ===")
    contents = [movie, tv_show, podcast, music]
    for content in contents:
        print(f"{content.play()}")
        print(f"Duration: {content.get_duration()} minutes")
        print(f"File size: {content.get_file_size()} MB")
        print(f"Streaming cost: ${content.calculate_streaming_cost():.2f}")
        print()
    
    # Test device streaming
    print("=== Testing Device Streaming ===")
    devices = [smart_tv, laptop, mobile, speaker]
    for device in devices:
        print(f"{device.connect()}")
        print(f"{device.stream_content(movie)}")
        print(f"{device.adjust_quality('HD')}")
        print()
    
    # Test platform functionality
    print("=== Testing Platform Functionality ===")
    
    # Premium user streaming premium content
    result1 = platform.stream_content("U001", "M001", "D001")
    print(f"Premium user streaming: {result1}")
    
    # Free user trying premium content
    result2 = platform.stream_content("U002", "M001", "D002")
    print(f"Free user streaming premium: {result2}")
    
    # Free user streaming free content
    result3 = platform.stream_content("U002", "P001", "D003")
    print(f"Free user streaming free content: {result3}")
    
    # Add ratings
    movie.add_rating(5)
    movie.add_rating(4)
    tv_show.add_rating(5)
    podcast.add_rating(4)
    music.add_rating(3)
    
    # Get recommendations
    recommendations = platform.recommend_content("U001")
    print(f"\nRecommendations: {[content.title for content in recommendations]}")
    
    # Get analytics
    analytics = platform.get_analytics("U001")
    print(f"Analytics: {analytics}")
    
    print("\nMedia Streaming Platform successfully implemented with abstraction and polymorphism!")
