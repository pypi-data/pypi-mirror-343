import win32api
import win32gui
import pyaudio
import wave
import numpy as np
import noisereduce as nr
import time

WM_APPCOMMAND = 0x319
APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000

SUCCESS_MIC_MUTE = "SUCCESS_MIC_MUTE"
SUCCESS_MIC_UNMUTE = "SUCCESS_MIC_UNMUTE"
ERR_MIC_MUTE = "ERR_MIC_MUTE"
ERR_MIC_UNMUTE = "ERR_MIC_UNMUTE"
SUCCESS_RECORDING = "SUCCESS_RECORDING"
ERR_RECORDING = "ERR_RECORDING"
ERR_NO_DEVICE = "ERR_NO_DEVICE"

def micmute():
    try:
        hwnd_active = win32gui.GetForegroundWindow()
        win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)
        return SUCCESS_MIC_MUTE
    except Exception:
        return ERR_MIC_MUTE

def micunmute():
    try:
        hwnd_active = win32gui.GetForegroundWindow()
        win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)
        return SUCCESS_MIC_UNMUTE
    except Exception:
        return ERR_MIC_UNMUTE

def list_audio_devices():
    p = pyaudio.PyAudio()
    print("Available audio devices:")
    for index in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(index)
        print(f"Index {index}: {device_info['name']} (inputs: {device_info['maxInputChannels']})")
    p.terminate()

def get_system_audio_device_index():
    p = pyaudio.PyAudio()
    
    potential_devices = []
    
    for index in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(index)
        if device_info['maxInputChannels'] > 0:
            name = device_info['name'].lower()
            
            if ('miks stereo' in name or 'stereo mix' in name or 
                'what u hear' in name or 'loopback' in name):
                potential_devices.append((index, 5))
            elif 'virtual' in name and 'cable' in name:
                potential_devices.append((index, 4))
            elif 'line' in name and device_info['maxInputChannels'] >= 2:
                potential_devices.append((index, 3))
            elif 'virtual' in name:
                potential_devices.append((index, 2))
            elif device_info['maxInputChannels'] >= 2:
                potential_devices.append((index, 1))
    
    potential_devices.sort(key=lambda x: x[1], reverse=True)
    
    if potential_devices:
        for device_index, priority in potential_devices:
            device_info = p.get_device_info_by_index(device_index)
            print(f"Trying system audio device: {device_info['name']} (Index: {device_index})")
            
            try:
                test_stream = p.open(
                    format=pyaudio.paInt16,
                    channels=2,
                    rate=44100,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=1024,
                    start=False
                )
                test_stream.close()
                print(f"Selected system audio device: {device_info['name']} (Index: {device_index})")
                p.terminate()
                return device_index
            except Exception as e:
                print(f"Cannot use device {device_index}: {e}")
    
    print("No working system audio device found")
    p.terminate()
    return None

def get_mic_input_device_index():
    p = pyaudio.PyAudio()
    
    potential_devices = []
    
    for index in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(index)
        if device_info['maxInputChannels'] > 0:
            name = device_info['name'].lower()
            
            if 'fifine' in name:
                potential_devices.append((index, 5))
            elif 'microphone' in name:
                potential_devices.append((index, 4))
            elif 'mic' in name:
                potential_devices.append((index, 3))
            elif 'input' in name:
                potential_devices.append((index, 2))
            else:
                potential_devices.append((index, 1))
    
    potential_devices.sort(key=lambda x: x[1], reverse=True)
    
    if potential_devices:
        for device_index, priority in potential_devices:
            device_info = p.get_device_info_by_index(device_index)
            print(f"Trying microphone device: {device_info['name']} (Index: {device_index})")
            
            try:
                test_stream = p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=1024,
                    start=False
                )
                test_stream.close()
                print(f"Selected microphone device: {device_info['name']} (Index: {device_index})")
                p.terminate()
                return device_index
            except Exception as e:
                print(f"Cannot use device {device_index}: {e}")

    print("No working microphone device found")
    p.terminate()
    return None

def record(time_ms, path, noise_removal=False, progress_callback=None):
    try:
        p = pyaudio.PyAudio()
        rate = 44100
        channels = 1
        format = pyaudio.paInt16
        frames_per_buffer = 1024

        input_device_index = get_mic_input_device_index()
        if input_device_index is None:
            return ERR_NO_DEVICE

        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        input_device_index=input_device_index,
                        frames_per_buffer=frames_per_buffer)

        frames = []
        time_seconds = time_ms / 1000
        total_frames = int(rate / frames_per_buffer * time_seconds)

        for i in range(total_frames):
            try:
                data = stream.read(frames_per_buffer)
                frames.append(data)
            except Exception as e:
                return f'WARN_DURING_RECORDING\n{e}'

            if progress_callback:
                progress = int((i / total_frames) * 100)
                progress_callback(progress)

        stream.stop_stream()
        stream.close()

        if not frames:
            return f'ERR_RECORDING\n{e}'

        audio_data = b''.join(frames)
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        
        if noise_removal and len(audio_np) > 0:
            try:
                # Zakładamy, że pierwsze 0.25 sekundy to sam szum
                noise_sample = audio_np[:int(0.25 * rate)]
                audio_np = nr.reduce_noise(y=audio_np, y_noise=noise_sample, sr=rate, prop_decrease=0.9999)

            except Exception as e:
                print(f"Noise reduction failed: {e}")
        
        if len(audio_np) > 0 and np.max(np.abs(audio_np)) > 0:
            audio_np = np.int16(audio_np / np.max(np.abs(audio_np)) * 32767)

        with wave.open(path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(audio_np.tobytes())

        p.terminate()
        return SUCCESS_RECORDING
    except Exception as e:
        print(f"Error during recording: {e}")
        return ERR_RECORDING