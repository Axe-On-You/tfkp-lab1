import matplotlib.pyplot as plt
import io
import imageio.v3 as imageio
import matplotlib
import concurrent.futures

def generate_frame(**kwargs):
    matplotlib.use('agg')
    matrix_generator = kwargs.get('generator')
    iterations = kwargs.get('iterations')
    plane_title = kwargs.get('plane_title')
    cmap = kwargs.get('cmap')
    borders = kwargs.get("borders")
    extent = kwargs.get('extent')
    dpi = kwargs.get('dpi')
    fractal_params = kwargs.get("fractal_params")
    density = kwargs.get("density")
    scale = kwargs.get("scale")
    fig, ax = plt.subplots(dpi=dpi)
    matrix = matrix_generator(fractal_params, iterations, borders, density)
    plane_title = f"{plane_title}\niters={int(iterations)} scale={round(scale, 5)}"
    ax.imshow(matrix,
              cmap=cmap,
              vmin=0,
              vmax=iterations,
              extent=extent,
              origin='upper')
    ax.set_title(plane_title, fontsize=11)
    ax.set_ylabel('Im(z)')
    ax.set_xlabel('Re(z)')
    frame = None
    with io.BytesIO() as buffer:
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        frame = imageio.imread(buffer)
    plt.close(fig)
    return frame


def get_dims(scale, center):
    plane_start = (-(1 / scale) - (1 / scale) * 1j) + center
    plane_end = ((1 / scale) + (1 / scale) * 1j) + center
    return plane_start, plane_end

def make_png(**kwargs):
    generator = kwargs.get("generator")
    iterations = kwargs.get("iterations", 100)
    scale = kwargs.get("scale", 1)
    center = kwargs.get("center", 0 + 0j)
    title = kwargs.get("title", "")
    file_path = kwargs.get("file_path")
    colors = kwargs.get("colors", "inferno")
    dpi = kwargs.get("dpi", 100)
    fractal_params = kwargs.get("fractal_params")
    density = kwargs.get("density", 800)

    plane_start, plane_end = get_dims(scale, center)
    borders = (plane_start, plane_end)
    extent = (plane_start.real, plane_end.real, plane_start.imag, plane_end.imag)
    print(f"Generating image...")
    frame = generate_frame(
        generator=generator,
        fractal_params=fractal_params,
        scale=scale,
        density=density,
        iterations=iterations,
        borders=borders,
        extent=extent,
        cmap=colors,
        dpi=dpi,
        plane_title=title)
    imageio.imwrite(file_path, frame)
    print(f"Image saved to {file_path}")


def __executor_generate_frame(args):
    scale, center, iterations, iteration_num, caller_kwargs = args
    kwargs = caller_kwargs
    generator = kwargs.get("generator")
    title = kwargs.get("title", "")
    colors = kwargs.get("colors", "inferno")
    dpi = kwargs.get("dpi", 100)
    fractal_params = kwargs.get("fractal_params")
    density = kwargs.get("density", 800)
    verbose = caller_kwargs.get("verbose", False)

    plane_start, plane_end = get_dims(scale, center)
    borders = (plane_start, plane_end)
    extent = (plane_start.real, plane_end.real, plane_start.imag, plane_end.imag)
    frame = generate_frame(
        generator=generator,
        fractal_params=fractal_params,
        density=density,
        scale=scale,
        iterations=iterations,
        borders=borders,
        extent=extent,
        cmap=colors,
        dpi=dpi,
        plane_title=title)

    if verbose:
        print(f"Generated frame #{iteration_num}")
    return frame
def make_gif(**kwargs):
    frames_count = kwargs.get("frames_count")
    scales = kwargs.get("scales")
    centers = kwargs.get("centers")
    iterations = kwargs.get("iterations", 100)
    iterations_change = kwargs.get("iterations_change", [iterations] * frames_count)


    fps = kwargs.get("fps")
    file_path = kwargs.get("file_path")
    print(f"Generating GIF...")
    executor_args = [(scales[i], centers[i], iterations_change[i], i + 1, kwargs) for i in range(0, frames_count)]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        frames = list(executor.map(__executor_generate_frame, executor_args))
    imageio.imwrite(file_path, frames, fps=fps)
    print(f"GIF saved to {file_path}")
