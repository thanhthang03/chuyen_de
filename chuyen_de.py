from PyQt6 import QtCore, QtGui, QtWidgets
import resAI
import pyodbc
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# (thang) library for record and save buttons
import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import os

#(duc) library for convertToText button
import speech_recognition as sr
import pydub  

class Ui_Dialog(object):    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Ghi âm ngôn ngữ tự nhiên")
        Dialog.resize(548, 654)
        self.record = QtWidgets.QPushButton(parent=Dialog)
        self.record.setGeometry(QtCore.QRect(90, 20, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.NoAntialias)
        self.record.setFont(font)
        self.record.setStyleSheet("QPushButton {\n"
"background-color:rgb(215, 211, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:rgb(74, 162, 255);\n"
"}")
        self.record.setObjectName("record")
        self.convertToText = QtWidgets.QPushButton(parent=Dialog)
        self.convertToText.setGeometry(QtCore.QRect(370, 20, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.convertToText.setFont(font)
        self.convertToText.setStyleSheet("QPushButton {\n"
"background-color:rgb(215, 211, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:rgb(74, 162, 255);\n"
"}")
        self.convertToText.setObjectName("convertToText")
        self.saveAudio = QtWidgets.QPushButton(parent=Dialog)
        self.saveAudio.setGeometry(QtCore.QRect(90, 80, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.saveAudio.setFont(font)
        self.saveAudio.setStyleSheet("QPushButton {\n"
"background-color:rgb(215, 211, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:rgb(74, 162, 255);\n"
"}")
        self.saveAudio.setObjectName("saveAudio")
        self.textEdit = QtWidgets.QTextEdit(parent=Dialog)
        self.textEdit.setGeometry(QtCore.QRect(30, 140, 491, 491))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        font.setUnderline(False)
        self.textEdit.setFont(font)
        self.textEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.textEdit.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setStyleSheet("background-color: rgb(239, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 551, 651))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/background/image/galaxyAI.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setGeometry(QtCore.QRect(100, 30, 20, 21))
        self.label_2.setAutoFillBackground(False)
        self.label_2.setLineWidth(-5)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/icons/image/record_button"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setGeometry(QtCore.QRect(100, 90, 21, 21))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/icons/image/save_button"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=Dialog)
        self.label_4.setGeometry(QtCore.QRect(370, 60, 121, 21))
        self.label_4.setAutoFillBackground(False)
        self.label_4.setLineWidth(-5)
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/icons/image/convert to text button.jpg"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.AISummarize = QtWidgets.QPushButton(parent=Dialog)
        self.AISummarize.setGeometry(QtCore.QRect(370, 80, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.AISummarize.setFont(font)
        self.AISummarize.setStyleSheet("QPushButton {\n"
"background-color:rgb(215, 211, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color:rgb(74, 162, 255);\n"
"}")
        self.AISummarize.setObjectName("AISummarize")
        self.label.raise_()
        self.textEdit.raise_()
        self.record.raise_()
        self.saveAudio.raise_()
        self.convertToText.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.AISummarize.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        # click button
        self.record.clicked.connect(self.toggle_recording)
        self.saveAudio.clicked.connect(self.save_audio)
        self.convertToText.clicked.connect(self.convert_to_text)
        self.saveAudio.setEnabled(False)   
        # (thang)click button AISummarize
        self.AISummarize.clicked.connect(self.summarize_text)
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.record.setText(_translate("Dialog", "   RECORD"))
        self.convertToText.setText(_translate("Dialog", "CONVERT TO TEXT"))
        self.saveAudio.setText(_translate("Dialog", "      SAVE AUDIO"))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:9pt; font-weight:400; font-style:italic;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; font-style:normal;\">dữ liệu văn bản được hiện ở đây</span></p></body></html>"))
        self.AISummarize.setText(_translate("Dialog", "AI SUMMARIZE"))
    # button record and save
    def toggle_recording(self):
        if not hasattr(self, 'recording'):
            self.recording = False
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        self.start_time = time.time()
        self.recording = True
        self.record.setText("STOP RECORDING")
        self.recorded_frames = []
        self.stream = sd.InputStream(callback=self.audio_callback, channels=2, samplerate=44100, dtype="int16")
        self.stream.start()
        self.start_timer()

    def stop_recording(self):
        self.recording = False
        self.record.setText("RECORD")
        self.stream.stop()
        self.stream.close()
        self.audio_data = np.concatenate(self.recorded_frames, axis=0)
        self.saveAudio.setEnabled(True)

    def audio_callback(self, indata, frames, time, status):
        self.recorded_frames.append(indata.copy())

    def start_timer(self):
        elapsed_time = time.time() - self.start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.record.setText(f"      Time: {time_str}")
        if self.recording:
            QtCore.QTimer.singleShot(1000, self.start_timer)

    def save_audio(self):
        if hasattr(self, 'audio_data') and self.audio_data is not None:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save Audio", "", "WAV files (*.wav)")
            if filename:
                sf.write(filename, self.audio_data, samplerate=44100)
  
    # button 
    def transcribe_mp3(self, filename, chunk_length_ms=30000):
        # Convert MP3 to WAV
        sound = pydub.AudioSegment.from_mp3(filename)
        
        # Determine the number of chunks
        num_chunks = len(sound) // chunk_length_ms + 1
        
        recognizer = sr.Recognizer()
        transcribed_text = []

        for i in range(num_chunks):
            start_ms = i * chunk_length_ms
            end_ms = min((i + 1) * chunk_length_ms, len(sound))
            chunk = sound[start_ms:end_ms]
            
            # Save chunk as temporary WAV file
            chunk_filename = f"temp_chunk_{i}.wav"
            chunk.export(chunk_filename, format="wav")

            try:
                with sr.AudioFile(chunk_filename) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="vi-VN")
                    transcribed_text.append(text)
            except sr.UnknownValueError:
                print("Audio could not be understood.")
                transcribed_text.append("[Unintelligible]")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                transcribed_text.append("[Request Error]")

            # Clean up the temporary file
            os.remove(chunk_filename)

        return " ".join(transcribed_text)

    def convert_to_text(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open Audio File", "", "Audio Files (*.mp3 *.wav)")
        if filename:
            text = self.transcribe_mp3(filename)
            if text:
                self.textEdit.setText(text)
            else:
                self.textEdit.setText("Transcription failed.")

    def summarize_text(self):
        # Lấy văn bản từ TextEdit
        text = self.textEdit.toPlainText()
        
        # Thêm tiền tố theo yêu cầu của mô hình Vit5
        formatted_text = "vietnews: " + text + " </s>"
        
        # Tạo tokenizer và model từ Hugging Face
        tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-large-vietnews-summarization")
        model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-large-vietnews-summarization")
        
        # Đưa model lên GPU nếu có
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

        # Tokenize văn bản
        encoding = tokenizer(formatted_text, return_tensors="pt", truncation=True)
        input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)
        
        # Tạo văn bản tóm tắt
        outputs = model.generate(
            input_ids=input_ids, attention_mask=attention_masks,
            max_length=256,  # Giới hạn độ dài tóm tắt
            early_stopping=True
        )
        
        # Giải mã văn bản tóm tắt
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
        
        # Định dạng kết quả tóm tắt để hiển thị trong textEdit
        formatted_summary_html = f"<h3><b>Tóm Tắt</b></h3><ul><li>{summary}</li></ul>"
        
        # Đặt văn bản tóm tắt đã định dạng vào textEdit
        self.textEdit.setHtml(formatted_summary_html)

        conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=LAPTOP-7NM21PDG\SQLEXPRESS;'
            r'DATABASE=PROJECT_RECORDER;'  # Kết nối tới cơ sở dữ liệu mới
            r'Trusted_Connection=yes;'
        )

        try:
            # Kết nối tới SQL Server
            db = pyodbc.connect(conn_str)
            cursor = db.cursor()
            
            # Insert toàn bộ văn bản tóm tắt vào bảng SUMMARIZED_CONTENT
            cursor.execute("INSERT INTO SUMMARIZED_CONTENT (NDUNGCHINH) VALUES (?)", summary)

            # Commit các thay đổi vào cơ sở dữ liệu
            db.commit()
            print("Summary saved to database successfully.")

        except pyodbc.Error as e:
            print(f"Error: {e}")

        finally:
            # Đóng kết nối đến cơ sở dữ liệu
            if 'db' in locals():
                db.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())