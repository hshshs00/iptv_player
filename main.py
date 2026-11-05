from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import requests
import re

Window.clearcolor = (0.1, 0.1, 0.15, 1)

class IPTVPlayer(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.channels = []
        
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        main_layout.add_widget(Label(
            text='IPTV Player', 
            font_size='24sp', 
            size_hint_y=0.1,
            color=(0.3, 0.7, 1, 1)
        ))
        
        # URL input
        url_box = BoxLayout(size_hint_y=0.15, spacing=5)
        url_box.add_widget(Label(text='M3U URL:', size_hint_x=0.25))
        self.url_input = TextInput(
            hint_text='http://example.com/list.m3u',
            multiline=False
        )
        url_box.add_widget(self.url_input)
        load_btn = Button(text='Load', size_hint_x=0.2)
        load_btn.bind(on_press=self.load_playlist)
        url_box.add_widget(load_btn)
        main_layout.add_widget(url_box)
        
        # Search
        search_box = BoxLayout(size_hint_y=0.1, spacing=5)
        search_box.add_widget(Label(text='Search:', size_hint_x=0.2))
        self.search_input = TextInput(
            hint_text='Search channels...',
            multiline=False
        )
        self.search_input.bind(text=self.filter_channels)
        search_box.add_widget(self.search_input)
        main_layout.add_widget(search_box)
        
        # Channel list
        scroll = ScrollView(size_hint_y=0.75)
        self.channel_grid = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None,
            padding=5
        )
        self.channel_grid.bind(minimum_height=self.channel_grid.setter('height'))
        scroll.add_widget(self.channel_grid)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def load_playlist(self, instance):
        url = self.url_input.text.strip()
        if not url:
            return
        try:
            response = requests.get(url, timeout=10)
            self.channels = self.parse_m3u(response.text)
            self.display_channels(self.channels)
        except Exception as e:
            print(f"Error: {e}")
    
    def parse_m3u(self, content):
        channels = []
        lines = content.split('\n')
        current = {}
        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF:'):
                match = re.search(r',(.*?)$', line)
                if match:
                    current = {'name': match.group(1).strip()}
            elif line and not line.startswith('#'):
                if current:
                    current['url'] = line
                    channels.append(current)
                    current = {}
        return channels
    
    def display_channels(self, channels):
        self.channel_grid.clear_widgets()
        for ch in channels:
            btn = Button(
                text=ch['name'],
                size_hint_y=None,
                height=50
            )
            btn.bind(on_press=lambda x, c=ch: self.play_channel(c))
self.channel_grid.add_widget(btn)
    
    def filter_channels(self, instance, value):
        if not self.channels:
            return
        term = value.lower().strip()
        filtered = self.channels if not term else [
            c for c in self.channels if term in c['name'].lower()
        ]
        self.display_channels(filtered)
    
    def play_channel(self, channel):
        print(f"Playing: {channel['name']}")
        print(f"URL: {channel['url']}")

if __name__ == '__main__':
    IPTVPlayer().run()
