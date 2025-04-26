import sys

# Only for windows!
use_audio = sys.platform == "win32"

if use_audio:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    def mute():
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)
            return "SUCCESS_MUTE"
        except Exception as e:
            return f"ERR_MUTE: {str(e)}"

    def unmute():
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(0, None)
            return "SUCCESS_UNMUTE"
        except Exception as e:
            return f"ERR_UNMUTE: {str(e)}"

else:
    print("Audio control features are disabled on this platform.")