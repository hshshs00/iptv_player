#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPTV Player - مشغل القنوات التلفزيونية
يدعم: M3U playlists, HTTP/HTTPS streams
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.core.window import Window
import requests
import re
import json
import os

Window.clearcolor = (0.1, 0.1, 0.15, 1)


class IPTVPlayer(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.channels = []
        self.current_channel = None
        self.video_player = None
        self.config_file = 'iptv_config.json'
        
    def build(self):
        self.title = "IPTV Player"
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint_y=0.1, spacing=5)
        header.add_widget(Label(
            text='[b]IPTV Player[/b]', 
            markup=True,
            font_size='20sp',
            color=(0.3, 0.7, 1, 1)
        ))
        main_layout.add_widget(header)
        
        # URL input section
        url_section = BoxLayout(size_hint_y=0.12, spacing=5)
        url_section.add_widget(Label(
            text='رابط M3U:', 
            size_hint_x=0.2,
            color=(1, 1, 1, 1)
        ))
        self.url_input = TextInput(
            multiline=False,
            hint_text='https://example.com/playlist.m3u',
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1)
        )
        url_section.add_widget(self.url_input)
        
        load_btn = Button(
            text='تحميل', 
            size_hint_x=0.2,
            background_color=(0.2, 0.6, 0.3, 1),
            on_press=self.load_playlist
        )
        url_section.add_widget(load_btn)
        main_layout.add_widget(url_section)
        
        # Search section
        search_section = BoxLayout(size_hint_y=0.1, spacing=5)
        search_section.add_widget(Label(
            text='بحث:', 
            size_hint_x=0.15,
            color=(1, 1, 1, 1)
        ))
        self.search_input = TextInput(
            multiline=False,
            hint_text='ابحث عن قناة...',
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.search_input.bind(text=self.filter_channels)
        search_section.add_widget(self.search_input)
        main_layout.add_widget(search_section)
        
        # Channel list
        self.channel_scroll = ScrollView(size_hint_y=0.45)
        self.channel_grid = GridLayout(
            cols=1, 
            spacing=5, 
            size_hint_y=None,
            padding=5
        )
        self.channel_grid.bind(minimum_height=self.channel_grid.setter('height'))
        self.channel_scroll.add_widget(self.channel_grid)
        main_layout.add_widget(self.channel_scroll)
        
        # Video player placeholder
        self.video_container = BoxLayout(size_hint_y=0.33)
        self.video_label = Label(
            text='اختر قناة لبدء المشاهدة',
            color=(0.7, 0.7, 0.7, 1)
        )
        self.video_container.add_widget(self.video_label)
        main_layout.add_widget(self.video_container)
        
        # Load saved config
        self.load_config()
        
        return main_layout
    
    def load_config(self):
        """تحميل الإعدادات المحفوظة"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.url_input.text = config.get('last_url', '')
            except:
                pass
    
    def save_config(self):
        """حفظ الإعدادات"""
        try:
            config = {'last_url': self.url_input.text}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False)
        except:
            pass
    
    def load_playlist(self, instance):
        """تحميل قائمة M3U"""
        url = self.url_input.text.strip()
        if not url:
            self.show_popup('خطأ', 'الرجاء إدخال رابط M3U')
            return
        
        self.show_popup('جاري التحميل...', 'يرجى الانتظار', auto_dismiss=True)
        
        try:
            # Download M3U content
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            content = response.text
            
            # Parse M3U
            self.channels = self.parse_m3u(content)
            
            if not self.channels:
                self.show_popup('خطأ', 'لم يتم العثور على قنوات في الملف')
                return
            
            # Save config
            self.save_config()
            
            # Display channels
            self.display_channels(self.channels)
            self.show_popup('نجح', f'تم تحميل {len(self.channels)} قناة')
            
        except requests.RequestException as e:
            self.show_popup('خطأ في الاتصال', str(e))
        except Exception as e:
            self.show_popup('خطأ', f'حدث خطأ: {str(e)}')
    
    def parse_m3u(self, content):
        """تحليل محتوى M3U"""
        channels = []
        lines = content.split('\n')
        
        current_channel = {}
        for line in lines:
            line = line.strip()
            
            # Parse channel info
            if line.startswith('#EXTINF:'):
                # Extract channel name
                match = re.search(r',(.*?)$', line)
                if match:
                    name = match.group(1).strip()
                    current_channel = {'name': name}
                    
                    # Extract logo if present
                    logo_match = re.search(r'tvg-logo="([^"]+)"', line)
                    if logo_match:
                        current_channel['logo'] = logo_match.group(1)
            
            # Parse stream URL
            elif line and not line.startswith('#'):
                if current_channel:
                    current_channel['url'] = line
                    channels.append(current_channel)
                    current_channel = {}
        
        return channels
    
    def display_channels(self, channels):
        """عرض قائمة القنوات"""
        self.channel_grid.clear_widgets()
        
        for channel in channels:
            btn = Button(
                text=channel['name'],
                size_hint_y=None,
                height=50,
                background_color=(0.2, 0.3, 0.4, 1),
                background_normal='',
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=lambda x, ch=channel: self.play_channel(ch))
            self.channel_grid.add_widget(btn)
    
    def filter_channels(self, instance, value):
        """تصفية القنوات حسب البحث"""
        if not self.channels:
            return
        
        search_term = value.lower().strip()
        if not search_term:
            filtered = self.channels
        else:
            filtered = [
                ch for ch in self.channels 
                if search_term in ch['name'].lower()
            ]
        
        self.display_channels(filtered)
    
    def play_channel(self, channel):
        """تشغيل قناة"""
        self.current_channel = channel
        
        # Clear video container
        self.video_container.clear_widgets()
        
        # Create video player
        self.video_player = Video(
            source=channel['url'],
            state='play',
            options={'eos': 'loop'}
        )
        self.video_container.add_widget(self.video_player)
        
        # Show notification
        self.show_popup('جاري التشغيل', f"القناة: {channel['name']}", auto_dismiss=True, timeout=2)
    
    def show_popup(self, title, message, auto_dismiss=False, timeout=3):
        """عرض رسالة منبثقة"""
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message, color=(1, 1, 1, 1)))
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.3),
            auto_dismiss=auto_dismiss
        )
        
        if not auto_dismiss:
            close_btn = Button(
                text='إغلاق',
                size_hint_y=0.3,
                background_color=(0.3, 0.3, 0.8, 1)
            )
            close_btn.bind(on_press=popup.dismiss)
            content.add_widget(close_btn)
        else:
            Clock.schedule_once(lambda dt: popup.dismiss(), timeout)
        
        popup.open()
    
    def on_stop(self):
        """عند إغلاق التطبيق"""
        if self.video_player:
            self.video_player.state = 'stop'


if __name__ == '__main__':
    IPTVPlayer().run()
