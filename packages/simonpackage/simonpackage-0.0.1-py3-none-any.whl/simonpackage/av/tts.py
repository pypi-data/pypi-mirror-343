from pyttsx3 import Engine
import time


class TTSEngine(Engine):
    def __init__(self):
        super(TTSEngine, self).__init__()

    def speak(self, text, rate=150, voice_id=0):
        """
        :param text:
        :param rate:
        :param voice_id: 0为中英文女声，1为纯英文女声，2为纯英文男声
        :return:
        """
        voices = self.getProperty('voices')
        self.setProperty('voice', voices[voice_id])
        if text.isascii():
            self.setProperty('voice', voices[1])
        self.setProperty('rate', rate)
        self.say(text, 'fox')
        self.runAndWait()

    def save_file(self, text, file_name = ''):
        voices = self.getProperty('voices')
        self.setProperty('voice', voices[voice_id])
        if text.isascii():
            self.setProperty('voice', voices[1])
        if not file_name:
            file_name = f'{int(time.time())}.mp3'
        self.save_to_file(text, file_name)
        self.runAndWait()


if __name__ == '__main__':
    engine = TTSEngine()
    # engine.speak('中国是一个伟大的国家， 你好，刘宗昊')
    engine.speak('china is a great country',voice_id=1, rate=120)
