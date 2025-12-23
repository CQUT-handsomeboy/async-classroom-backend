from manim import *
import numpy as np

class TrigonometricFunctionAnimation(Scene):
    def construct(self):
        # 标题
        title = Text("函数 f(x) = 5cos x - cos 5x", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建坐标轴
        axes = Axes(
            x_range=[0, PI/2, PI/8],
            y_range=[-2, 6, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": BLUE},
            x_axis_config={
                "numbers_to_include": [0, PI/8, PI/4, PI/2],
                "decimal_number_config": {"num_decimal_places": 3},
            },
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        # 将坐标轴移动到合适位置
        axes_group = VGroup(axes, axes_labels)
        axes_group.shift(DOWN * 0.5)

        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        # 定义函数
        def f(x):
            return 5 * np.cos(x) - np.cos(5 * x)

        # 绘制函数图像
        graph = axes.plot(f, x_range=[0, PI/2], color=YELLOW)
        graph_label = axes.get_graph_label(graph, label="f(x)=5\\cos x-\\cos 5x")

        self.play(Create(graph), Write(graph_label))
        self.wait(2)

        # 显示关键点：π/6
        pi_over_6 = PI/6
        f_pi_over_6 = f(pi_over_6)

        # 计算最大值点
        max_point = axes.c2p(pi_over_6, f_pi_over_6)
        max_dot = Dot(point=max_point, color=RED, radius=0.08)
        max_label = MathTex(f"x=\\frac{{\\pi}}{{6}}", font_size=32)
        max_label.next_to(max_dot, UP)

        # 显示导数为0的点
        derivative_text = MathTex("f'(x) = 5(\\sin 5x - \\sin x) = 0", font_size=36)
        derivative_text.next_to(title, DOWN)

        self.play(Write(derivative_text))
        self.wait(1)

        # 显示导数的三角变换
        derivative_transform = MathTex(
            "f'(x) = 10\\cos 3x \\cdot \\sin 2x",
            font_size=36
        )
        derivative_transform.next_to(derivative_text, DOWN)

        self.play(Transform(derivative_text, derivative_transform))
        self.wait(2)

        # 标记极值点
        self.play(FadeIn(max_dot), Write(max_label))

        # 显示最大值
        max_value_text = MathTex(
            f"f\\left(\\frac{{\\pi}}{{6}}\\right) = 3\\sqrt{{3}} \\approx {f_pi_over_6:.3f}",
            font_size=36
        )
        max_value_text.next_to(max_label, UP)

        self.play(Write(max_value_text))
        self.wait(2)

        # 清理屏幕，准备第二部分
        self.play(
            FadeOut(title),
            FadeOut(derivative_text),
            FadeOut(max_value_text),
            FadeOut(max_label),
            FadeOut(max_dot),
            FadeOut(graph_label),
            FadeOut(graph),
            FadeOut(axes_labels),
            FadeOut(axes)
        )

        # 第二部分：证明存在性
        self.show_part_two()

        # 第三部分：最小值问题
        self.show_part_three()

    def show_part_two(self):
        """展示第二部分：存在性证明"""
        # 标题
        title = Text("第二部分：存在性证明", font_size=48)
        title.to_edge(UP)

        # 问题陈述
        problem_line1 = MathTex("\\theta \\in (0, \\pi),", font_size=36)
        problem_line2 = MathTex("y \\in [a-\\theta, a+\\theta],", font_size=36)
        problem_line3 = MathTex("\\cos y \\leq \\cos \\theta", font_size=36)

        # 中文文本部分
        chinese_text1 = Text("给定", font_size=36).next_to(problem_line1, LEFT)
        chinese_text2 = Text("设 a 为实数，证明：存在", font_size=36).next_to(problem_line2, LEFT)
        chinese_text3 = Text("使得", font_size=36).next_to(problem_line3, LEFT)

        # 组合所有元素
        line1 = VGroup(chinese_text1, problem_line1)
        line2 = VGroup(chinese_text2, problem_line2)
        line3 = VGroup(chinese_text3, problem_line3)

        problem = VGroup(line1, line2, line3)
        problem.arrange(DOWN, aligned_edge=LEFT)
        problem.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.wait(1)
        self.play(
            Write(chinese_text1), Write(problem_line1),
            Write(chinese_text2), Write(problem_line2),
            Write(chinese_text3), Write(problem_line3)
        )
        self.wait(2)

        # 创建新的坐标轴来展示余弦函数
        axes2 = Axes(
            x_range=[-2*PI, 2*PI, PI/2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=12,
            y_length=6,
            axis_config={"color": BLUE},
            x_axis_config={
                "numbers_to_include": [-2*PI, -PI, 0, PI, 2*PI],
                "decimal_number_config": {"num_decimal_places": 3},
            },
        )
        axes2_labels = axes2.get_axis_labels(x_label="y", y_label="\\cos y")
        axes2_group = VGroup(axes2, axes2_labels)
        axes2_group.shift(DOWN * 0.5)

        self.play(Create(axes2), Write(axes2_labels))

        # 绘制余弦函数
        cos_graph = axes2.plot(lambda x: np.cos(x), x_range=[-2*PI, 2*PI], color=GREEN)
        cos_label = axes2.get_graph_label(cos_graph, label="\\cos y", x_val=-PI)

        self.play(Create(cos_graph), Write(cos_label))
        self.wait(1)

        # 选择一个a值（例如a=0）
        a = 0
        theta = PI/3  # 选择θ=π/3作为示例

        # 标记区间[a-θ, a+θ]
        interval_start = a - theta
        interval_end = a + theta

        # 创建区间标记
        interval_line = Line(
            axes2.c2p(interval_start, 0),
            axes2.c2p(interval_end, 0),
            color=RED,
            stroke_width=8
        )

        interval_label = MathTex(f"[{a}-\\theta, {a}+\\theta]", font_size=28)
        interval_label.next_to(interval_line, DOWN)

        # 标记cosθ的值
        cos_theta = np.cos(theta)
        cos_theta_line = DashedLine(
            axes2.c2p(-2*PI, cos_theta),
            axes2.c2p(2*PI, cos_theta),
            color=YELLOW,
            stroke_width=2
        )

        cos_theta_label = MathTex(f"\\cos\\theta = {cos_theta:.3f}", font_size=28)
        cos_theta_label.next_to(cos_theta_line, LEFT)

        self.play(
            Create(interval_line),
            Write(interval_label),
            Create(cos_theta_line),
            Write(cos_theta_label)
        )
        self.wait(2)

        # 显示证明思路
        proof_text = Text("证明思路：考虑区间端点的余弦值", font_size=32, color=YELLOW)
        proof_text.next_to(problem, DOWN, buff=0.5)

        self.play(Write(proof_text))
        self.wait(2)

        # 标记区间端点
        left_dot = Dot(axes2.c2p(interval_start, np.cos(interval_start)), color=PURPLE)
        right_dot = Dot(axes2.c2p(interval_end, np.cos(interval_end)), color=PURPLE)

        left_label = MathTex(f"\\cos({a}-\\theta)", font_size=24)
        right_label = MathTex(f"\\cos({a}+\\theta)", font_size=24)

        left_label.next_to(left_dot, DOWN)
        right_label.next_to(right_dot, DOWN)

        self.play(
            FadeIn(left_dot), Write(left_label),
            FadeIn(right_dot), Write(right_label)
        )
        self.wait(2)

        # 显示关键不等式
        key_inequality = MathTex(
            "\\cos(a-\\theta) + \\cos(a+\\theta) = 2\\cos a \\cos\\theta",
            font_size=36
        )
        key_inequality.next_to(proof_text, DOWN)

        self.play(Write(key_inequality))
        self.wait(2)

        conclusion_text = Text("因此，至少有一个端点满足", font_size=36, color=GREEN)
        conclusion_math = MathTex("\\cos y \\leq \\cos\\theta", font_size=36, color=GREEN)

        conclusion = VGroup(conclusion_text, conclusion_math)
        conclusion.arrange(RIGHT, aligned_edge=DOWN)
        conclusion.next_to(key_inequality, DOWN)

        self.play(Write(conclusion_text), Write(conclusion_math))
        self.wait(3)

        # 清理屏幕
        self.play(
            FadeOut(title),
            FadeOut(problem),
            FadeOut(proof_text),
            FadeOut(key_inequality),
            FadeOut(conclusion),
            FadeOut(axes2_group),
            FadeOut(cos_graph),
            FadeOut(cos_label),
            FadeOut(interval_line),
            FadeOut(interval_label),
            FadeOut(cos_theta_line),
            FadeOut(cos_theta_label),
            FadeOut(left_dot),
            FadeOut(left_label),
            FadeOut(right_dot),
            FadeOut(right_label)
        )

    def show_part_three(self):
        """展示第三部分：最小值问题"""
        # 标题
        title = Text("第三部分：最小值问题", font_size=48)
        title.to_edge(UP)

        # 问题陈述
        problem_line1_text = Text("若存在 t 使得对任意 x，都有", font_size=36)
        problem_line2_math = MathTex("5\\cos x - \\cos(5x + t) \\leq b", font_size=36)
        problem_line3_text = Text("求 b 的最小值", font_size=36)

        # 组合所有元素
        line1 = problem_line1_text
        line2 = problem_line2_math
        line3 = problem_line3_text

        problem = VGroup(line1, line2, line3)
        problem.arrange(DOWN, aligned_edge=LEFT)
        problem.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.wait(1)
        self.play(Write(problem_line1_text), Write(problem_line2_math), Write(problem_line3_text))
        self.wait(2)

        # 创建坐标轴
        axes3 = Axes(
            x_range=[0, 2*PI, PI/2],
            y_range=[-6, 6, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": BLUE},
            x_axis_config={
                "numbers_to_include": [0, PI/2, PI, 3*PI/2, 2*PI],
                "decimal_number_config": {"num_decimal_places": 3},
            },
        )
        axes3_labels = axes3.get_axis_labels(x_label="x", y_label="g(x)")
        axes3_group = VGroup(axes3, axes3_labels)
        axes3_group.shift(DOWN * 0.5)

        self.play(Create(axes3), Write(axes3_labels))

        # 显示函数族
        function_family_text = Text("函数族：g(x) = 5cos x - cos(5x + t)", font_size=32, color=YELLOW)
        function_family_text.next_to(problem, DOWN, buff=0.5)

        self.play(Write(function_family_text))
        self.wait(1)

        # 绘制几个不同t值的函数
        t_values = [0, PI/4, PI/2, PI]
        colors = [RED, GREEN, YELLOW, PURPLE]

        graphs = []
        labels = []

        for i, (t, color) in enumerate(zip(t_values, colors)):
            def g(x, t_val=t):
                return 5 * np.cos(x) - np.cos(5 * x + t_val)

            graph = axes3.plot(lambda x: g(x), x_range=[0, 2*PI], color=color)
            graphs.append(graph)

            label = MathTex(f"t={t:.2f}", font_size=24, color=color)
            label.next_to(graph.point_from_proportion(0.3), UP)
            labels.append(label)

            self.play(Create(graph), Write(label), run_time=1)

        self.wait(2)

        # 显示上确界
        supremum_text = Text("我们需要找到所有t对应的上确界的最小值", font_size=32, color=ORANGE)
        supremum_text.next_to(function_family_text, DOWN)

        self.play(Write(supremum_text))
        self.wait(2)

        # 数学推导
        derivation = MathTex(
            "\\max_x [5\\cos x - \\cos(5x + t)]",
            "= \\max_x [5\\cos x - (\\cos 5x \\cos t - \\sin 5x \\sin t)]",
            font_size=30
        )
        derivation.arrange(DOWN, aligned_edge=LEFT)
        derivation.next_to(supremum_text, DOWN)

        self.play(Write(derivation))
        self.wait(2)

        # 继续推导
        derivation2 = MathTex(
            "= \\max_x [(5 - \\cos t)\\cos x + \\sin t \\sin 5x]",
            "\\leq \\sqrt{(5 - \\cos t)^2 + (\\sin t)^2}",
            font_size=30
        )
        derivation2.arrange(DOWN, aligned_edge=LEFT)
        derivation2.next_to(derivation, DOWN)

        self.play(Write(derivation2))
        self.wait(2)

        # 最终结果
        final_result = MathTex(
            "b_{\\min} = \\min_t \\sqrt{26 - 10\\cos t} = 4",
            font_size=36,
            color=GREEN
        )
        final_result.next_to(derivation2, DOWN, buff=0.5)

        self.play(Write(final_result))
        self.wait(3)

        # 总结
        summary = Text("动画演示完成！", font_size=48, color=YELLOW)
        summary.move_to(ORIGIN)

        self.play(
            FadeOut(title),
            FadeOut(problem),
            FadeOut(function_family_text),
            FadeOut(supremum_text),
            FadeOut(derivation),
            FadeOut(derivation2),
            FadeOut(final_result),
            FadeOut(axes3_group),
            *[FadeOut(graph) for graph in graphs],
            *[FadeOut(label) for label in labels]
        )

        self.play(Write(summary))
        self.wait(2)

        # 结束
        self.play(FadeOut(summary))

# 运行动画的代码
if __name__ == "__main__":
    # 使用命令行运行：
    # manim -pql main.py TrigonometricFunctionAnimation
    pass