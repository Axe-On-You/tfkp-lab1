import time
import numpy as np
from util import make_gif, make_png


def mandelbrot_matrix(fractal_params, iterations, borders, density):
    z0 = fractal_params.get("z0")
    r = fractal_params.get("r")
    plane_start, plane_end = borders
    # Вектор действительных частей комплексной плоскости
    re_vec = np.linspace(plane_start.real, plane_end.real, density, dtype=np.float64)
    # Вектор мнимых частей комплексной плоскости
    im_vec = np.linspace(plane_start.imag, plane_end.imag, density, dtype=np.float64) * 1j
    # Формируем дискретную комплексную плоскость точек C с помощью декартового сложения двух векторов
    # В итоговой плоскости получаем density^2 точек
    plane = np.add.outer(im_vec, re_vec)

    # Результирующая матрица для вывода и окраски
    output = np.zeros(plane.shape, dtype='uint16')

    # Промежуточная матрица из комплексных чисел для формирования последовательности, заполненная z0
    # В ней будем хранить n-ые члены последовательности для всех подходящий точек c (plane)
    z = np.full(plane.shape, z0, np.complex128)

    for i in range(iterations):
        # Матрица из точек, в которых текущее z еще не "убежало"
        mask = np.less(np.abs(z), r)
        # Чем больше чисел попало в точку, тем большее число для данной точке будет в результирующей матрице
        output[mask] = i
        # Формируем следующий член последовательности для чисел, которые отвечают радиусу
        # z_{n+1} = z_n^2 + c
        z[mask] = z[mask] ** 2 + plane[mask]

    return output


if __name__ == "__main__":
    title = "Множество Мандельброта"

    places = [
        (100, 1/ 1.98, 0, "mandelbrot_main.png"),
        (500, 1/0.005904900000000002, -0.7451968299999999  + 0.10186988500000009j, "mandelbrot_seahorse.png"),
        (1500, 1/5.205901380161776E-11, -1.7397156556930304  + -9.157504622931403E-8j, "mandelbrot_wormhole.png"),
        (1500, 1/9.68059489050412E-9 , 0.35787121400640803   + -0.10813970113434704j, "mandelbrot_carousel.png"),
    ]

    for iters, scale, center, f_name in places:
        make_png(
            generator=mandelbrot_matrix,
            fractal_params={
                "z0": 0,
                "r": 2
            },
            iterations=iters,
            scale=scale,
            center=center,
            density=2000,
            dpi=200,
            colors="inferno",
            title=title,
            file_path=f"output/{f_name}"
        )

    gif_frames = 240
    make_gif(
        generator=mandelbrot_matrix,
        fractal_params={
            "z0": 0,
            "r": 2
        },
        iterations=100,
        scales=np.linspace(0.5, 400, gif_frames),
        centers=np.linspace(-1.4 + 0j, -1.45 + 0j, gif_frames),
        density=400,
        dpi=100,
        colors="inferno",
        title=title,
        file_path="output/mandelbrot_along_ox.gif",
        frames_count=gif_frames,
        fps=24,
        verbose=False
    )
    make_gif(
        generator=mandelbrot_matrix,
        fractal_params={
            "z0": 0,
            "r": 2
        },
        iterations_change=np.linspace(0, 100, gif_frames).astype(int),
        scales=np.linspace(1/ 1.98, 1/ 1.98, gif_frames),
        centers=np.linspace(0, 0, gif_frames),
        density=400,
        dpi=100,
        colors="inferno",
        title=title,
        file_path="output/mandelbrot_iters_change.gif",
        frames_count=gif_frames,
        fps=24,
        verbose=False
    )