# ****************************************************************************
#
#    audio_manager.py
#
#    By: dhde-lim <dhde-lim@student.42.rio> and
#        ganselmo <ganselmo@student.42.rio>
#
#    Description: Background audio manager responsible for
#             controlling themed music playback in loop mode.
#    Created: 2026/05/19
#
# ****************************************************************************

import os


class AudioManager:
    """Background terminal audio manager."""
    def __init__(self) -> None:
        """Initialize audio manager."""
        self.current_music: str | None = None

    def stop(self) -> None:
        """Stop current music."""
        os.system("pkill mpg123 > /dev/null 2>&1")
        self.current_music = None

    def play(self, music_path: str) -> None:
        """
        Play music in loop mode.

        Stops the current track before starting
        the new background music.

        Args:
            music_path: Path to the audio file.
        """
        self.stop()
        self.current_music = music_path
        os.system(f"mpg123 --loop -1 {music_path} > /dev/null 2>&1 &")

    def is_playing(self) -> bool:
        """
        Check if music is currently playing.

        Returns:
            True if a track is active.
        """
        return self.current_music is not None

    def toggle(self, music_path: str) -> None:
        """
        Toggle music playback state.

        Args:
            music_path: Path to the audio file.
        """
        if self.is_playing():
            self.stop()
        else:
            self.play(music_path)
