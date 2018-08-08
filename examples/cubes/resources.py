from demosys.resources.meta import TextureDescription, ProgramDescription


def local(path):
    # Figure out the package name prepending it path
    return path


resources = [
    ProgramDescription(path="cubes/cube_plain.glsl", label="plain"),
    ProgramDescription(path="cubes/cube_light.glsl", label="light"),
    ProgramDescription(path="cubes/cube_textured.glsl", label="textured"),
    TextureDescription(path="cubes/crate.jpg", label="crate"),
]

# Some function to support local path?

# def local_path(func):
#     """
#     Decorator modifying the `path` parameter depending
#     on the `local` parameter.
#     If `local` is `True` we prepend the current effect name to the path.
#     """
#     @wraps(func)
#     def local_wrapper(*args, **kwargs):
#         use_local = kwargs.get('local')

#         # If use_local is True prepend the package name to the path
#         if use_local is True:
#             path = args[1]
#             path = os.path.join(args[0].effect_name, path)

#             # Replace path and rebuild tuple
#             args = list(args)
#             args[1] = path
#             args = tuple(args)

#         return func(*args, **kwargs)
#     return local_wrapper
