import numpy as np
from util import make_gif, make_png

def burning_ship_julia_matrix(fractal_params, iterations, borders, density):
    c = fractal_params.get("c")
    r = fractal_params.get("r")
    plane_start, plane_end = borders
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
        # Аналогично первому фракталу, но используем c как const и применяем функцию к каждой точке z
        z[mask] = (np.abs(np.real(z[mask])) + 1j * np.abs(np.imag(z[mask])) ) ** 2 + c
    return output


if __name__ == "__main__":
    title = "Множество \"Горящий корабль\" (версия Жюлиа)"
    places = [
        (100, -1.762 - 0.028j , 0.5, 0, "ship_j_large.png"),
        (100, -1.762 - 0.028j , 4, 0, "ship_j_x4.png"),
        (250, -1.762 - 0.028j , 100000, -0.1 + 0.05j, "ship_j_x100000.png"),
    ]
    for iters, c, scale, center, f_name in places:
        make_png(
                generator=burning_ship_julia_matrix,
                fractal_params={
                    "c": c,
                    "r": 2
                },
                iterations=iters,
                scale=scale,
                center=center,
                density=2000,
                dpi=200,
                colors="seismic",
                title=title,
                file_path=f"output/{f_name}",
            )

    gif_frames = 240
    make_gif(
        generator=burning_ship_julia_matrix,
        fractal_params={
            "c": -1.762 - 0.028j,
            "r": 2
        },
        iterations=250,
        scales=np.linspace(0.5, 40, gif_frames),
        centers=np.linspace(0, 0, gif_frames),
        density=400,
        dpi=200,
        colors="seismic",
        title=title,
        file_path="output/ship_julia.gif",
        frames_count=gif_frames,
        fps=24,
        verbose=False
    )