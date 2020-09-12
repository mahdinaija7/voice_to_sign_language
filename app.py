import tkinter as tk
import speech_recognition as sr
import pyglet
from concurrent import futures

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)
pyglet.font.add_file('Fingerspelling.ttf')


class Translator:

    def __init__(self, window):

        self.is_recording=False

        window.title("Translator")
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
        window.geometry(f'{width // 2}x{height // 2}')
        window.configure(bg='#E6A627')
        self.text_frame = tk.Frame(window, height=5)
        self.text_frame.pack_propagate(False)

        self.text = tk.Text(window, height=1, width=1, font=('Fingerspelling', 100), borderwidth=2)
        self.scroll = tk.Scrollbar(window, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        # read only
        self.text.config(state="disabled")
        self.text.pack(fill="x")
        self.text_frame.pack(side="top", fill="both")
        photo = tk.PhotoImage(file='microphone.png').subsample(3, 3)
        self.button = tk.Button(window, image=photo, command=self.on_button, borderwidth=2)

        self.button.image = photo
        self.button.pack(pady=50)
        self.background_label = tk.Label(window,text="Recording..")
        self.background_label.config(fg="red")
        self.background_label.pack_forget()
    def voice_to_text(self):
        print("start recording")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = r.listen(source, timeout=5)
                message = str(r.recognize_google(audio))
                print(message)
                self.text.config(state="normal")
                self.text.delete(1.0, "end")
                self.text.insert(1.0, message)
                self.text.config(state="disabled")
            except sr.UnknownValueError:
                print('Speech Recognition could not Understand audio')
                self.voice_to_text()
            except sr.RequestError as e:
                print('Could not request result from Google Speech Recogniser Service')
                self.voice_to_text()
            else:
                pass
        print("finished")
        self.is_recording=False
        self.background_label.pack_forget()


    def on_button(self):
        if not self.is_recording:
            self.background_label.pack(side="bottom",fill="x")
            thread_pool_executor.submit(self.voice_to_text)
            self.is_recording=True
        else:
            print("Recording")


if __name__ == '__main__':
    window = tk.Tk()
    window_edit = Translator(window)
    window.mainloop()
