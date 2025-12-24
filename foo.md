<question>
设函数 $f(x) = 5\cos x - \cos 5x$。

（1）求 $f(x)$ 在 $ <quote3>(0, \frac{\pi}{4})</quote3>$ 的最大值；

（2）给定 $\theta \in (0, \pi)$，设 $a$ 为实数，证明：存在 $y \in [a-\theta, a+\theta]$，使得 $\cos y \leq \cos \theta$；

（3）若存在 $t$ 使得对任意 $x$，都有 $5\cos x - \cos(5x + t) \leq b$，求 $b$ 的最小值。
</question>

<narrator>
首先来看一下第一小问，求0到pi/4的最大值，最快的方法是和差化积。
</narrator>

<sametime>
<answer>
$ f'(x) = -5\sin x + 5\sin 5x = <quote1>5(\sin 5x - \sin x) </quote1> = <quote2>10\cos 3x \cdot \sin 2x</quote2> $
</answer>

<narrator>
首先直接对它求导会发现，<quote1/> 此部分可进行和差化积，得到结果<quote2/>
而由于条件 <quote3/> 所以 sin 2x 大于零，因此 cos 3x决定零点。
</narrator>

</sametime>

<sametime>
<answer>

$f(x)$在 $(0,\frac{\pi}{6}) \nearrow$ 在$(\frac{\pi}{6},\frac{\pi}{4}) \searrow$

</answer>

<narrator>
因此可知 f(x)在0到六分之派单调递增，在六分之派到四分之派单调递减。
</narrator>
</sametime>