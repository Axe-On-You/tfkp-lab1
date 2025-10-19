import matplotlib.pyplot as plt
import numpy as np
import io
import imageio.v3 as imageio
import concurrent.futures
from util import make_gif, make_png


def julia_matrix(fractal_params, iterations, borders, density):
    c = fractal_params.get("c")
    r = fractal_params.get("r")
    plane_start, plane_end = borders

    # Выбор оптимального r
    # Имеем: r^2 - r >= |c|
    # r >= (1 +- sqrt(1 + 4|c|))/2 + eps
    # Если передано значение r меньшее, чем оптимальное - оставляем как есть для исследования области с меньшим r
    # Иначе рассчитываем оптимальное значение, так как исследование области с большим r не имеет смысла
    r = min(r, (1 + np.sqrt(1+4*np.abs(c)))/2 + 0.01)

    # Вектор действительных частей комплексной плоскости
    re_vec = np.linspace(plane_start.real, plane_end.real, density, dtype=np.float64)
    # Вектор мнимых частей комплексной плоскости
    im_vec = np.linspace(plane_start.imag, plane_end.imag, density, dtype=np.float64) * 1j
    # Формируем дискретную комплексную плоскость с помощью декартового сложения двух векторов
    # В итоговой плоскости получаем density^2 точек
    z = np.add.outer(im_vec, re_vec)

    # Результирующая матрица для вывода и окраски
    output = np.zeros(z.shape, dtype='uint16')

    for i in range(iterations):
        # Матрица из точек, в которых текущее z еще не "убежало"
        mask = np.less(np.abs(z), r)
        # Чем больше чисел попало в точку, тем большее число для данной точке будет в результирующей матрице
        output[mask] = i
        # Формируем следующий член последовательности для чисел, которые отвечают радиусу
        # z_{n+1} = z_n ^ 2 + c (const)
        # Аналогично первому фракталу, но используем c как const и применяем функцию к каждой точке z
        z[mask] = z[mask] ** 2 + c
    return output



if __name__ == "__main__":
    title = "Множество Жюлиа"

    places = [
        (100, -0.5251993 + 0.5251993j , 0.5, 0, "julia_classic.png"),
        (500, 0.355 + 0.355j, 0.75, 0, "julia_spirals.png"),
        (350, 0.355 + 0.355j, 100, -0.021 + 0.496j, "julia_spirals_zoomed.png"),
        (150, 0.34 - 0.05j, 0.8, 0, "julia_squid.png")
    ]
    for iters, c, scale, center, f_name in places:
        make_png(
            generator=julia_matrix,
            fractal_params={
                "c": c,
                "r": 2
            },
            iterations=iters,
            scale=scale,
            center=center,
            density=2000,
            dpi=200,
            title=f"{title}\nc={c}",
            colors="viridis",
            file_path=f"output/{f_name}"
        )

    gif_frames = 240
    c_gif = -0.5251993 + 0.5251993j
    make_gif(
        generator=julia_matrix,
        fractal_params={
            "c": c_gif,
            "r": 2
        },
        iterations=100,
        scales=np.linspace(1, 50, gif_frames),
        centers=np.linspace(0, 0.275 + 0.26j, gif_frames),
        density=400,
        dpi=100,
        title=f"{title}\nc={c_gif}",
        colors="viridis",
        file_path="output/julia.gif",
        frames_count=gif_frames,
        fps=24,
        verbose=False
    )