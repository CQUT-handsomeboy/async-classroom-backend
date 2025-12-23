from manim import *
import numpy as np

class TrigonometricFunctionAnimation(Scene):
    def construct(self):
        # 第一问
        # 首先看一下第一小问，求零到四分之派的最大值
        # 最快的方法是和差化积
        # 直接对它求导
        # 你会发现应该是五倍的sin5X减去sin x
        # 那这个东西啊可以进行一个和差化积
        # 可以不用这个
        # 但用这个应该是最快的
        # 用这个的话
        # 他应该就等于十倍的cos sin x乘以sin2X
        # 而X是0~4分之派
        # 所以sin2X是不是大于零啊
        # 因此就看cos3X了
        # 那它只有一个零点嘛
        # 在0~4分之派里就是一个六分之派
        # 所以FX在0~6分之派上递增
        # 六分之派到四分之派上是递减的
        # 因此FX max也就是F6分之派等于三根号三
        # 所以这个函数啊是在0~4分之派上
        # 先递增后递减
        # 然后这边有个最大值是三根号三
        pp = []
        # 显示题目

        # 第一行：设函数和导数公式
        line1 = VGroup(
            Text("设函数", font_size=28),
            MathTex("f(x) = 5\\cos x - \\cos 5x", font_size=28)
        ).arrange(RIGHT, buff=0.3).to_corner(UL)
        pp.append(line1)

        # 第一问
        q1_parts = VGroup(
            Text("(1) 求", font_size=24),
            MathTex("f(x)", font_size=24),
            Text("在", font_size=24),
            MathTex("(0, \\frac{\\pi}{4})", font_size=24),
            Text("的最大值", font_size=24)
        ).arrange(RIGHT, buff=0.2).next_to(line1, DOWN, aligned_edge=LEFT)
        pp.append(q1_parts)

        # 第二问
        q2_line1 = VGroup(
            Text("(2) 给定", font_size=24),
            MathTex("\\theta \\in (0, \\pi)", font_size=24),
            Text("，设", font_size=24),
            MathTex("a", font_size=24),
            Text("为实数，证明：", font_size=24),
            Text("存在", font_size=24),
            MathTex("y \\in [a-\\theta, a+\\theta]", font_size=24),
            Text("，使得", font_size=24),
            MathTex("\\cos y \\leq \\cos \\theta", font_size=24)
        ).arrange(RIGHT, buff=0.2).next_to(q1_parts, DOWN, aligned_edge=LEFT)
        pp.append(q2_line1)


        # 第三问
        q3_line1 = VGroup(
            Text("(3) 若存在", font_size=24),
            MathTex("t", font_size=24),
            Text("使得对任意", font_size=24),
            MathTex("x", font_size=24),
            Text("，都有", font_size=24),
             MathTex("5\\cos x - \\cos(5x + t) \\leq b", font_size=24),
            Text("，求", font_size=24),
            MathTex("b", font_size=24),
            Text("的最小值", font_size=24)
        ).arrange(RIGHT, buff=0.2).next_to(q2_line1, DOWN, aligned_edge=LEFT)
        pp.append(q3_line1)

        self.play([Write(x) for x in pp])
        self.wait(2)
# 运行动画的代码
if __name__ == "__main__":
    # 使用命令行运行：
    # manim -pql main.py TrigonometricFunctionAnimation
    pass