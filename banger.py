import openai
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QLabel
from PyQt5.QtGui import QFont, QPalette, QPainterPath, QColor, QIcon
from PyQt5.QtCore import Qt, QRectF

# Set your OpenAI GPT-3 API key here
api_key = 'API-KEY'
openai.api_key = api_key

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 20, 400, 500)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        title = QLabel('Tweet Banger')
        title.setFont(QFont('Roboto', 24, QFont.Bold))
        title.setStyleSheet('color: black background-color: black')
        layout.addWidget(title)

        self.text_area = QTextEdit()
        self.text_area.setFont(QFont('Roboto', 14))
        self.text_area.setStyleSheet('color: black; background-color: black')
        layout.addWidget(self.text_area)

        self.text_input = QLineEdit()
        self.text_input.setFont(QFont('Roboto', 14))
        self.text_input.setStyleSheet('color: white; background-color: black')
        self.text_input.returnPressed.connect(self.handle_enter_pressed)
        layout.addWidget(self.text_input)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)


    def handle_enter_pressed(self):
        user_input = self.text_input.text()
        self.text_input.clear()

        self.text_area.append(f'Tweet: {user_input}')
        tweet_text = user_input
        
        prompt = f"Turn this tweet into a solid banger, where a banger is a tweet of higher quality compared to most others, usually in comedic value and wording: '{tweet_text}'"
        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=prompt,
            max_tokens=100,
            temperature=0.7,
        )

        banger_tweet = response.choices[0].text.strip()
        self.text_area.append(f'Banger: {banger_tweet}')


def run_app():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    run_app()
