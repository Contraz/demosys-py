from demosys.window import Window


def main():
    window = Window(320, 256, None)
    while not window.should_close():
        window.poll_events()
        window.swap_buffers()


if __name__ == "__main__":
    main()
