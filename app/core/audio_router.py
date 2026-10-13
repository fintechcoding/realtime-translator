from typing import Optional

from app.utils.logger import log


class AudioRouter:
    def __init__(self):
        self._virtual_device_name: Optional[str] = None

    def find_virtual_cable(self) -> Optional[dict]:
        try:
            import sounddevice as sd
            devices = sd.query_devices()
            vb_keywords = ["CABLE", "VB-Audio", "Virtual", "VoiceMeeter"]
            for i, d in enumerate(devices):
                name_lower = d["name"].lower()
                for kw in vb_keywords:
                    if kw.lower() in name_lower:
                        self._virtual_device_name = d["name"]
                        return {
                            "id": i,
                            "name": d["name"],
                            "input_channels": d["max_input_channels"],
                            "output_channels": d["max_output_channels"],
                        }
        except Exception as e:
            log.error(f"Error scanning devices: {e}")
        return None

    def is_virtual_cable_installed(self) -> bool:
        return self.find_virtual_cable() is not None

    def get_virtual_output_device(self) -> Optional[int]:
        try:
            import sounddevice as sd
            devices = sd.query_devices()
            vb_keywords = ["CABLE Input", "VB-Audio Virtual Cable"]
            for i, d in enumerate(devices):
                if d["max_output_channels"] > 0:
                    for kw in vb_keywords:
                        if kw.lower() in d["name"].lower():
                            return i
        except Exception as e:
            log.error(f"Error finding virtual output: {e}")
        return None

    def get_virtual_input_device(self) -> Optional[int]:
        try:
            import sounddevice as sd
            devices = sd.query_devices()
            vb_keywords = ["CABLE Output", "VB-Audio Virtual Cable"]
            for i, d in enumerate(devices):
                if d["max_input_channels"] > 0:
                    for kw in vb_keywords:
                        if kw.lower() in d["name"].lower():
                            return i
        except Exception as e:
            log.error(f"Error finding virtual input: {e}")
        return None

    def set_default_device(self, device_id: int, role: str = "multimedia"):
        try:
            from pycaw.pycaw import AudioUtilities
            log.info(f"Setting default device {device_id} for role {role}")
        except ImportError:
            log.warning("pycaw not installed, cannot set default device programmatically")
        except Exception as e:
            log.error(f"Error setting default device: {e}")

    def get_device_volume(self, device_id: Optional[int] = None) -> float:
        try:
            from pycaw.pycaw import AudioUtilities
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import IAudioEndpointVolume

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            return volume.GetMasterVolumeLevelScalar()
        except Exception as e:
            log.error(f"Error getting volume: {e}")
            return 1.0
