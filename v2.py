from manim import *
import numpy as np
from manim_voiceover import VoiceoverScene
from speech_machine import CustomService

class TrigonometricFunctionAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(CustomService())
        pp = []
        # 显示题目

        # 第一行：设函数和导数公式
        line1 = VGroup(
            Text("设函数", font_size=28),
            MathTex("f(x) = 5\\cos x - \\cos 5x", font_size=28)
        ).arrange(RIGHT, buff=0.3).to_corner(UL)
        pp.append(line1)

        # 第一问
        q1 = VGroup(
            Text("(1) 求", font_size=24),
            MathTex("f(x)", font_size=24),
            Text("在", font_size=24),
            MathTex("(0, \\frac{\\pi}{4})", font_size=24),
            Text("的最大值", font_size=24)
        ).arrange(RIGHT, buff=0.2).next_to(line1, DOWN, aligned_edge=LEFT)
        pp.append(q1)

        # 第二问
        q2 = VGroup(
            Text("(2) 给定", font_size=24),
            MathTex("\\theta \\in (0, \\pi)", font_size=24),
            Text("，设", font_size=24),
            MathTex("a", font_size=24),
            Text("为实数，证明：", font_size=24),
            Text("存在", font_size=24),
            MathTex("y \\in [a-\\theta, a+\\theta]", font_size=24),
            Text("，使得", font_size=24),
            MathTex("\\cos y \\leq \\cos \\theta", font_size=24)
        ).arrange(RIGHT, buff=0.2).next_to(q1, DOWN, aligned_edge=LEFT)
        pp.append(q2)


        # 第三问
        q3 = VGroup(
            Text("(3) 若存在", font_size=24),
            MathTex("t", font_size=24),
            Text("使得对任意", font_size=24),
            MathTex("x", font_size=24),
            Text("，都有", font_size=24),
             MathTex("5\\cos x - \\cos(5x + t) \\leq b", font_size=24),
            Text("，求", font_size=24),
            MathTex("b", font_size=24),
            Text("的最小值", font_size=24)
        ).arrange(RIGHT, buff=0.2).next_to(q2, DOWN, aligned_edge=LEFT)
        pp.append(q3)
        
        self.play([Write(x) for x in pp])
        with self.voiceover(text="首先看一下第一小问，求零到四分之派的最大值") as tracker:
            self.play(FadeOut(q2),FadeOut(q3))
        
        with self.voiceover(text="最快的方法是和差化积") as tracker:
            self.wait(1)
        
        with self.voiceover(text="首先直接对它求导会发现应该是五倍的sin5X减去sin x，这个部分可以进行和差化积") as tracker:
            a1 = VGroup(
                tex:=MathTex("f'(x) = -5\\sin x + 5\\sin 5x",
                        "=",
                        "5(\\sin 5x - \\sin x)",
                        "=",
                        "10 \\cos 3x \\cdot ","\\sin 2x", font_size=24),
            ).arrange(RIGHT, buff=0.2).next_to(q1, DOWN, aligned_edge=LEFT)
            self.play(Write(a1))
            self.play(Indicate(tex[2]))
            self.wait(1)
        
        with self.voiceover(text="得到结果10 cos 3x乘sin 2x") as tracker:
            self.play(Indicate(tex[4:]))
            
        with self.voiceover(text="因为sin2x是零到四分之派") as tracker:
            self.play(Indicate(q1[3]))

        with self.voiceover(text="所以sin2x大于0，因此cos 3x的零点决定整个式子的零点") as tracker:
            self.play(Indicate(tex[5]))
        
        with self.voiceover(text="可知fx在0到六分之派中单调递增，在六分之派单调递减") as tracker:
            a2 = VGroup(
                MathTex("f(x)",font_size=24),
                Text("在",font_size=24),
                MathTex("(0, \\frac{\\pi}{6}) \\nearrow",font_size=24),
                Text("在",font_size=24),
                MathTex("(\\frac{\\pi}{6}, \\frac{\\pi}{4}) \\searrow",font_size=24),
            ).arrange(RIGHT, buff=0.2).next_to(a1, DOWN, aligned_edge=LEFT)
            self.play(Write(a2))
        
        with self.voiceover(text="因此最大值是3倍根号3") as tracker:
            a3 = VGroup(
                MathTex("f(x)_{\\max} = f\\left(\\frac{\\pi}{6}\\right) = \\frac{5\\sqrt{3}}{2} + \\frac{\\sqrt{3}}{2} = 3\\sqrt{3}",font_size=24),
            ).arrange(RIGHT, buff=0.2).next_to(a2, DOWN, aligned_edge=LEFT)
            self.play(Write(a3))
            
        
# manim -pql .\v2.py TrigonometricFunctionAnimation --disable_caching