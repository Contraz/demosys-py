
Audio
=====

We currently use pygame's mixer module for music playback.
More work needs to be done to find a better alternative
as depending on such a huge package should not be needed.

You will have to manually add pygame to your requirements
and pip install the package.

In oder to get pygame to work you probably need sdl, sdl_mixer
and libvorbis. These are binary dependencies and not python
packages.

We need to figure out what requiremnets are actually needed.

As mentioned in readme, the state of audio is not in good shape.

The sound player an be a bit wonky at times on startup refusing to play
on some platforms. We have tried a few libraries and ended up using
pygame's mixer module. (Optional setup for this)

Audio Requirements:

- As the current position in the music is what all
  draw timers are based on, we need a library that can deliver very accurate value for this.
- Efficient and accurate seeking + pause support
- Some way to extract simple data from the music for visualisation
