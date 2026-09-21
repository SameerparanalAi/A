import os
import json
import urllib.request
import urllib.error

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (0.03, 0.05, 0.09, 1)

KEY_FILE = "groq_api_key.txt"

def get_key():
    if os.path.exists(KEY_FILE):
        try:
            with open(KEY_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
        except:
            pass
    return ""

def save_key(key):
    with open(KEY_FILE, "w", encoding="utf-8") as f:
        f.write(key.strip())

class SameerAI(App):

    def build(self):
        root = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=8
        )

        title = Label(
            text="SAMEER AI\nYour Personal AI Assistant",
            font_size=24,
            bold=True,
            size_hint_y=None,
            height=80
        )
        root.add_widget(title)

        self.chat = Label(
            text="AI: Hello Sameer!\n\n",
            font_size=18,
            halign="left",
            valign="top"
        )
        root.add_widget(self.chat)

        self.input_box = TextInput(
            hint_text="Apna sawal likho...",
            multiline=False,
            font_size=18,
            size_hint_y=None,
            height=55
        )
        root.add_widget(self.input_box)

        row = BoxLayout(
            size_hint_y=None,
            height=60,
            spacing=6
        )

        send = Button(text="SEND", font_size=18)
        send.bind(on_press=self.ask)
        row.add_widget(send)

        api = Button(text="API KEY", font_size=18)
        api.bind(on_press=self.api_key)
        row.add_widget(api)

        root.add_widget(row)

        return root

    def add_chat(self, text):
        self.chat.text += text + "\n\n"

    def api_key(self, instance):
        key = self.input_box.text.strip()

        if not key:
            self.add_chat("AI: Pehle API key box me likho.")
            return

        save_key(key)
        self.input_box.text = ""
        self.add_chat("AI: ✓ Groq API key save ho gayi.")

    def ask(self, instance):
        question = self.input_box.text.strip()

        if not question:
            return

        self.input_box.text = ""
        self.add_chat("You: " + question)

        key = get_key()

        if not key:
            self.add_chat(
                "AI: Pehle API KEY button se apni Groq API key save karo."
            )
            return

        try:
            url = "https://api.groq.com/openai/v1/chat/completions"

            data = {
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {
                        "role": "system",
                        "content":
                        "You are SAMEER AI. "
                        "Answer the user clearly in Hindi or Hinglish."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }

            request = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + key
                },
                method="POST"
            )

            with urllib.request.urlopen(
                request, timeout=60
            ) as response:

                result = json.loads(
                    response.read().decode("utf-8")
                )

            answer = result["choices"][0]["message"]["content"]

            self.add_chat("AI: " + answer)

        except urllib.error.HTTPError as e:
            try:
                error = e.read().decode("utf-8")
            except:
                error = str(e)

            self.add_chat(
                "AI: Groq error " +
                str(e.code) + "\n" + error
            )

        except Exception as e:
            self.add_chat(
                "AI: Connection/error:\n" + str(e)
            )


SameerAI().run()
