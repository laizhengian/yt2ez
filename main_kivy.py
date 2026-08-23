import os
import sys
import threading
from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.combobox import ComboBox
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.utils import platform

import yt_dlp


KV = '''
<RootWidget>:
    orientation: 'vertical'
    padding: dp(20)
    spacing: dp(15)

    Label:
        text: 'yt2ez'
        font_size: sp(28)
        bold: True
        size_hint_y: None
        height: dp(50)
        color: 0.2, 0.6, 1, 1

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        size_hint_y: None
        height: dp(120)

        Label:
            text: 'Video URL:'
            font_size: sp(16)
            size_hint_y: None
            height: dp(30)
            halign: 'left'
            text_size: self.width, None

        BoxLayout:
            spacing: dp(5)
            size_hint_y: None
            height: dp(50)

            TextInput:
                id: url_input
                hint_text: 'https://youtube.com/watch?v=...'
                font_size: sp(16)
                multiline: False
                on_text_validate: root.fetch_formats()

            Button:
                text: 'Fetch Qualities'
                size_hint_x: None
                width: dp(150)
                on_press: root.fetch_formats()

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        size_hint_y: None
        height: dp(100)

        Label:
            text: 'Save to:'
            font_size: sp(16)
            size_hint_y: None
            height: dp(30)
            halign: 'left'
            text_size: self.width, None

        BoxLayout:
            spacing: dp(5)
            size_hint_y: None
            height: dp(50)

            TextInput:
                id: path_input
                text: root.download_path
                font_size: sp(14)
                readonly: True
                background_color: 0.95, 0.95, 0.95, 1

            Button:
                text: 'Browse'
                size_hint_x: None
                width: dp(100)
                on_press: root.browse_path()

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        size_hint_y: None
        height: dp(100)

        Label:
            text: 'Format:'
            font_size: sp(16)
            size_hint_y: None
            height: dp(30)
            halign: 'left'
            text_size: self.width, None

        BoxLayout:
            spacing: dp(10)
            size_hint_y: None
            height: dp(50)

            ToggleButton:
                id: mp3_btn
                text: 'MP3 (Audio 192kbps)'
                group: 'format'
                state: 'down'
                on_state: root.on_format_change('mp3') if self.state == 'down' else None

            ToggleButton:
                id: mp4_btn
                text: 'MP4 (Video + Audio)'
                group: 'format'
                on_state: root.on_format_change('mp4') if self.state == 'down' else None

    BoxLayout:
        id: resolution_box
        orientation: 'vertical'
        spacing: dp(10)
        size_hint_y: None
        height: dp(80) if root.show_resolution else 0
        opacity: 1 if root.show_resolution else 0
        disabled: not root.show_resolution

        Label:
            text: 'Resolution:'
            font_size: sp(16)
            size_hint_y: None
            height: dp(30)
            halign: 'left'
            text_size: self.width, None

        Spinner:
            id: resolution_spinner
            text: 'best (auto)'
            values: root.resolution_options
            font_size: sp(16)
            size_hint_y: None
            height: dp(50)
            on_text: root.on_resolution_change(self.text)

    ProgressBar:
        id: progress_bar
        max: 100
        value: 0
        size_hint_y: None
        height: dp(10)

    Label:
        id: status_label
        text: 'Ready'
        font_size: sp(14)
        size_hint_y: None
        height: dp(30)
        color: 0.4, 0.4, 0.4, 1

    BoxLayout:
        spacing: dp(15)
        size_hint_y: None
        height: dp(60)

        Button:
            id: download_btn
            text: 'Download MP3'
            font_size: sp(18)
            bold: True
            background_color: 0.2, 0.6, 1, 1
            on_press: root.start_download()

        Button:
            text: 'Open Folder'
            font_size: sp(16)
            size_hint_x: None
            width: dp(150)
            on_press: root.open_folder()

<FileChooserPopup>:
    title: 'Select Download Folder'
    size_hint: 0.9, 0.9
    BoxLayout:
        orientation: 'vertical'
        FileChooserListView:
            id: filechooser
            path: root.download_path
            filters: []
            dirselect: True
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            Button:
                text: 'Cancel'
                on_press: root.dismiss()
            Button:
                text: 'Select'
                background_color: 0.2, 0.6, 1, 1
                on_press: root.select_path(filechooser.path)
'''

Builder.load_string(KV)


def get_ffmpeg_path():
    """Get path to bundled ffmpeg"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    ffmpeg = os.path.join(base_path, "ffmpeg")
    if platform == 'android':
        return ffmpeg
    return ffmpeg + ('.exe' if platform == 'win32' else '')


def get_download_dir():
    if platform == 'android':
        from android.storage import primary_external_storage_path
        return os.path.join(primary_external_storage_path(), 'Music', 'yt2ez')
    return os.path.expanduser('~/Music/yt2ez')


class FileChooserPopup(Popup):
    download_path = StringProperty('')

    def select_path(self, path):
        App.get_running_app().root.download_path = path
        App.get_running_app().root.ids.path_input.text = path
        self.dismiss()


class RootWidget(BoxLayout):
    download_path = StringProperty('')
    resolution_options = ListProperty(['best (auto)'])
    show_resolution = BooleanProperty(False)
    selected_resolution = StringProperty('best (auto)')
    download_format = StringProperty('mp3')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_path = get_download_dir()
        os.makedirs(self.download_path, exist_ok=True)
        self.ffmpeg_path = get_ffmpeg_path()
        self._fetch_thread = None

    def on_format_change(self, fmt):
        self.download_format = fmt
        self.show_resolution = (fmt == 'mp4')
        self.ids.download_btn.text = f'Download {fmt.upper()}'
        if fmt == 'mp4':
            self.fetch_formats()

    def on_resolution_change(self, res):
        self.selected_resolution = res

    def browse_path(self):
        popup = FileChooserPopup(download_path=self.download_path)
        popup.open()

    def fetch_formats(self):
        url = self.ids.url_input.text.strip()
        if not url or self.download_format != 'mp4':
            return

        self.ids.status_label.text = 'Fetching qualities...'
        self.ids.status_label.color = (0.2, 0.6, 1, 1)

        def fetch():
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'skip_download': True,
                    'ffmpeg_location': self.ffmpeg_path,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = info.get('formats', [])

                video_formats = {}
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('height'):
                        height = f['height']
                        fs = f.get('filesize') or f.get('filesize_approx') or 0
                        existing_fs = video_formats[height].get('filesize') or video_formats[height].get('filesize_approx') or 0 if height in video_formats else 0
                        if height not in video_formats or fs > existing_fs:
                            video_formats[height] = f

                resolutions = sorted(video_formats.keys(), reverse=True)
                resolution_options = ['best (auto)'] + [f'{h}p' for h in resolutions]

                Clock.schedule_once(lambda dt: self.update_resolution_combo(resolution_options))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_resolution_combo(['best (auto)']))

        self._fetch_thread = threading.Thread(target=fetch, daemon=True)
        self._fetch_thread.start()

    def update_resolution_combo(self, options):
        self.resolution_options = options
        if self.selected_resolution not in options:
            self.selected_resolution = options[0]
        self.ids.resolution_spinner.values = options
        self.ids.status_label.text = 'Ready'
        self.ids.status_label.color = (0.4, 0.4, 0.4, 1)

    def start_download(self):
        url = self.ids.url_input.text.strip()
        if not url:
            self.show_error('Please enter a YouTube URL')
            return

        self.ids.download_btn.disabled = True
        self.ids.progress_bar.value = 0
        self.ids.status_label.text = 'Downloading...'
        self.ids.status_label.color = (0.2, 0.6, 1, 1)
        self.ids.url_input.text = ''

        if self.download_format == 'mp3':
            thread = threading.Thread(target=self.download_mp3_worker, args=(url,), daemon=True)
        else:
            thread = threading.Thread(target=self.download_mp4_worker, args=(url,), daemon=True)
        thread.start()

    def download_mp3_worker(self, url):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 30,
                'retries': 3,
                'ffmpeg_location': self.ffmpeg_path,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            Clock.schedule_once(lambda dt: self.on_success())
        except Exception as e:
            Clock.schedule_once(lambda dt: self.on_error(f'MP3 download failed:\n{e}'))

    def download_mp4_worker(self, url):
        try:
            res = self.selected_resolution
            if res == 'best (auto)':
                format_spec = 'bestvideo+bestaudio/best'
            else:
                height = res.replace('p', '')
                format_spec = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'

            print(f'MP4 format_spec: {format_spec}')

            ydl_opts = {
                'format': format_spec,
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 30,
                'retries': 3,
                'ffmpeg_location': self.ffmpeg_path,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            Clock.schedule_once(lambda dt: self.on_success())
        except Exception as e:
            print(f'MP4 error: {e}')
            Clock.schedule_once(lambda dt: self.on_error(f'MP4 download failed:\n{e}'))

    def on_success(self):
        self.ids.progress_bar.value = 100
        self.ids.download_btn.disabled = False
        self.ids.status_label.text = f'Done! Saved to {self.download_path}'
        self.ids.status_label.color = (0.2, 0.8, 0.2, 1)
        self.show_popup('Success', f'{self.download_format.upper()} downloaded successfully!')

    def on_error(self, error):
        self.ids.download_btn.disabled = False
        self.ids.status_label.text = 'Error occurred'
        self.ids.status_label.color = (1, 0.2, 0.2, 1)
        self.show_error(error)

    def show_error(self, msg):
        popup = Popup(
            title='Error',
            content=Label(text=msg, text_size=(dp(300), None), halign='center'),
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def show_popup(self, title, msg):
        popup = Popup(
            title=title,
            content=Label(text=msg, text_size=(dp(300), None), halign='center'),
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def open_folder(self):
        if platform == 'android':
            from android import activity
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')
            
            folder = File(self.download_path)
            uri = Uri.fromFile(folder)
            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(uri, 'resource/folder')
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            activity.startActivity(intent)
        else:
            import subprocess
            if platform == 'win32':
                os.startfile(self.download_path)
            elif platform == 'macosx':
                subprocess.run(['open', self.download_path])
            else:
                subprocess.run(['xdg-open', self.download_path])


class YT2EZApp(App):
    def build(self):
        self.title = 'yt2ez'
        return RootWidget()

    def on_pause(self):
        return True


if __name__ == '__main__':
    YT2EZApp().run()