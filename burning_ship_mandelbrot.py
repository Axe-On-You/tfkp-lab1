import numpy as np
from util import make_png, make_gif


def burning_ship_matrix(fractal_params, iterations, borders, density):
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
        # z_{n+1} = (|Re(z)| + i|Im(z)|)^2 + c
        z[mask] = (np.abs(z[mask].real) + 1j * np.abs(z[mask].imag)) ** 2 + plane[mask]

    return output


if __name__ == "__main__":
    title = "Множество \"Горящий корабль\""

    places = [
        (100, 0.5, 0, "ship_m_large.png"),
        (100, 20, -1.762 - 0.028j, "ship_m_ship.png"),
        (250, 250000, -1.764 - 0.028j, "ship_m_zoomed.png"),
    ]
    for iters, scale, center, f_name in places:
        make_png(
            generator=burning_ship_matrix,
            fractal_params={
                "z0": 0,
                "r": 2
            },
            iterations=iters,
            scale=scale,
            center=center,
            density=2000,
            dpi=200,
            colors="hot",
            title=title ,
            file_path=f"output/{f_name}"
        )

    gif_frames = 240
    make_gif(
        generator=burning_ship_matrix,
        fractal_params={
            "z0": 0,
            "r": 2
        },
        iterations=100,
        scales=np.linspace(300, 15, gif_frames),
        centers=np.linspace(-1.762 - 0.028j, -1.762 - 0.028j, gif_frames),
        density=400,
        dpi=100,
        colors="hot",
        title=title,
        file_path="output/ship_mandelbrot.gif",
        frames_count=gif_frames,
        fps=24,
        verbose=False

    )