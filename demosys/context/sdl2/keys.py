# flake8: noqa
# https://github.com/marcusva/py-sdl2/blob/fa91007e6eebcbf5838f08cfe8d0b9d5cdf3ab83/sdl2/keycode.py
from demosys.context.base import BaseKeys

import sdl2


class Keys(BaseKeys):
    """Namespace defining sdl2 specific keys constants"""
    ACTION_PRESS = sdl2.SDL_KEYDOWN
    ACTION_RELEASE = sdl2.SDL_KEYUP

    ESCAPE = sdl2.SDLK_ESCAPE
    SPACE = sdl2.SDLK_SPACE
    ENTER = sdl2.SDLK_RETURN
    PAGE_UP = sdl2.SDLK_PAGEUP
    PAGE_DOWN = sdl2.SDLK_PAGEDOWN
    LEFT = sdl2.SDLK_LEFT
    RIGHT = sdl2.SDLK_RIGHT
    UP = sdl2.SDLK_UP
    DOWN = sdl2.SDLK_DOWN

    A = sdl2.SDLK_a
    B = sdl2.SDLK_b
    C = sdl2.SDLK_c
    D = sdl2.SDLK_d
    E = sdl2.SDLK_e
    F = sdl2.SDLK_f
    G = sdl2.SDLK_g
    H = sdl2.SDLK_h
    I = sdl2.SDLK_i
    J = sdl2.SDLK_j
    K = sdl2.SDLK_k
    L = sdl2.SDLK_l
    M = sdl2.SDLK_m
    N = sdl2.SDLK_n
    O = sdl2.SDLK_o
    P = sdl2.SDLK_p
    Q = sdl2.SDLK_q
    R = sdl2.SDLK_r
    S = sdl2.SDLK_s
    T = sdl2.SDLK_t
    U = sdl2.SDLK_u
    V = sdl2.SDLK_v
    W = sdl2.SDLK_w
    X = sdl2.SDLK_x
    Y = sdl2.SDLK_y
    Z = sdl2.SDLK_z
