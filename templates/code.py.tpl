from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene

from pathlib import Path
import sys
sys.path.append("{{ module_path }}")
from speech_machine import CustomService

class MainAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(CustomService())
        pp = []
        {% for line in lines %}
        {{ line }}
        {% endfor %}