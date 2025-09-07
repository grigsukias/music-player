import sys
import os
import vlc
import eyed3

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox
from PyQt6.QtCore import QByteArray, QBuffer, Qt
from PyQt6.QtGui import QPixmap

os.add_dll_directory(os.path.dirname(os.path.abspath(__name__)))


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basic Music Player")
        self.resize(800, 600)
        
        self.label = QLabel("Select a song")
        self.dropdown = QComboBox()
        self.load_songs()
        
        self.backgroundPicture = QLabel()
        self.backgroundPicture.pixmap()
        
        self.button = QPushButton("Play")
        

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.dropdown)
        layout.addWidget(self.backgroundPicture)
        self.setLayout(layout)

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.button.clicked.connect(self.play_music)
        
    def load_songs(self):
        songs_Path = os.path.dirname(os.path.abspath(__file__))
        loadFolder = os.path.join(songs_Path, "testFiles")
        
        for file in  os.listdir(loadFolder):
            if file.endswith((".mp3", ".wav", ".ogg")):
                self.dropdown.addItem(os.path.join(loadFolder,file))

    def play_music(self):
        selected_item = self.dropdown.currentText()
        
        # set metadata
        
        audioFile = eyed3.load(selected_item)
        
        if audioFile.tag is not None:
            artist = audioFile.tag.artist
            album = audioFile.tag.album,
            title = audioFile.tag.title
            image = None
            
            if audioFile.tag is not None and audioFile.tag.images:
                image = audioFile.tag.images[0].image_data  # <-- here’s your variable
                pixmap = QPixmap()
                byte_array = QByteArray(image)
                buffer = QBuffer(byte_array)
                buffer.open(QBuffer.OpenModeFlag.ReadOnly)
                pixmap.loadFromData(buffer.data())
                
                pixmap = pixmap.scaled(
                      self.backgroundPicture.width(),
                      self.backgroundPicture.height(),
                      Qt.AspectRatioMode.KeepAspectRatio,
                      Qt.TransformationMode.SmoothTransformation
                    )

    
                self.backgroundPicture.setPixmap(pixmap)
            else:
                image = None
                self.backgroundPicture.clear()
            
            self.label.setText(title)
        else:
            print("This song has no metadata attached to it.")
            self.label.setText(selected_item)

        
        media = self.instance.media_new(selected_item)
        self.player.set_media(media)
        self.player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())
