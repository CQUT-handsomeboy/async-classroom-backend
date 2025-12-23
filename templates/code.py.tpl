from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene
from speech_machine import CustomService

class MainAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(CustomService())
        pp = []
        {% for line in lines %}
        {{ line }}
        {% endfor %}