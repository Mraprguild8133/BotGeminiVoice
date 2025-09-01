"""
Audio handling utilities for voice processing
"""

import os
import tempfile
import logging
import wave
import subprocess
from typing import Optional, Tuple, Dict, List
import pyaudio

from .logger import setup_logger

logger = setup_logger(__name__)

class AudioHandler:
    """Handle audio processing operations"""
    
    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000  # 16kHz for speech recognition
        self.audio = None
        
        try:
            self.audio = pyaudio.PyAudio()
        except Exception as e:
            logger.warning(f"Could not initialize PyAudio: {e}")
    
    def __del__(self):
        """Clean up audio resources"""
        if self.audio:
            self.audio.terminate()
    
    async def convert_to_wav(self, input_file: str, output_file: str = None) -> Optional[str]:
        """Convert audio file to WAV format suitable for speech recognition"""
        if not output_file:
            output_file = input_file.replace('.ogg', '.wav').replace('.mp3', '.wav')
        
        try:
            # Try using ffmpeg first
            import subprocess
            
            subprocess.run([
                'ffmpeg', '-i', input_file,
                '-acodec', 'pcm_s16le',
                '-ar', str(self.rate),
                '-ac', str(self.channels),
                output_file, '-y'
            ], check=True, capture_output=True)
            
            return output_file
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to pydub
            return await self._convert_with_pydub(input_file, output_file)
    
    async def _convert_with_pydub(self, input_file: str, output_file: str) -> Optional[str]:
        """Convert audio using pydub as fallback"""
        try:
            from pydub import AudioSegment
            
            # Detect file type and load accordingly
            if input_file.endswith('.ogg'):
                audio = AudioSegment.from_ogg(input_file)
            elif input_file.endswith('.mp3'):
                audio = AudioSegment.from_mp3(input_file)
            else:
                audio = AudioSegment.from_file(input_file)
            
            # Convert to the format needed for speech recognition
            audio = audio.set_channels(self.channels)
            audio = audio.set_frame_rate(self.rate)
            audio = audio.set_sample_width(2)  # 16-bit
            
            # Export as WAV
            audio.export(output_file, format='wav')
            
            return output_file
            
        except Exception as e:
            logger.error(f"Error converting audio with pydub: {e}")
            return None
    
    def get_audio_info(self, wav_file: str) -> Optional[Dict]:
        """Get information about WAV audio file"""
        try:
            with wave.open(wav_file, 'rb') as wav:
                info = {
                    'channels': wav.getnchannels(),
                    'sample_width': wav.getsampwidth(),
                    'frame_rate': wav.getframerate(),
                    'frames': wav.getnframes(),
                    'duration': wav.getnframes() / wav.getframerate()
                }
                return info
        except Exception as e:
            logger.error(f"Error getting audio info: {e}")
            return None
    
    def validate_audio_format(self, wav_file: str) -> bool:
        """Validate if audio format is suitable for speech recognition"""
        info = self.get_audio_info(wav_file)
        if not info:
            return False
        
        # Check if format is suitable for speech recognition
        suitable_formats = {
            'channels': 1,  # Mono
            'sample_width': 2,  # 16-bit
            'frame_rate': [8000, 16000, 22050, 44100]  # Common sample rates
        }
        
        return (
            info['channels'] == suitable_formats['channels'] and
            info['sample_width'] == suitable_formats['sample_width'] and
            info['frame_rate'] in suitable_formats['frame_rate']
        )
    
    async def enhance_audio_for_speech(self, wav_file: str) -> Optional[str]:
        """Enhance audio quality for better speech recognition"""
        try:
            from pydub import AudioSegment
            from pydub.effects import normalize, compress_dynamic_range
            
            # Load audio
            audio = AudioSegment.from_wav(wav_file)
            
            # Apply enhancements
            # 1. Normalize volume
            audio = normalize(audio)
            
            # 2. Apply light compression to even out volume levels
            audio = compress_dynamic_range(audio)
            
            # 3. High-pass filter to remove low-frequency noise
            # (Approximated by reducing bass)
            audio = audio.low_pass_filter(3000)  # Remove high frequency noise
            audio = audio.high_pass_filter(300)   # Remove low frequency noise
            
            # 4. Ensure optimal format for speech recognition
            audio = audio.set_channels(1)  # Mono
            audio = audio.set_frame_rate(16000)  # 16kHz
            
            # Save enhanced version
            enhanced_file = wav_file.replace('.wav', '_enhanced.wav')
            audio.export(enhanced_file, format='wav')
            
            return enhanced_file
            
        except Exception as e:
            logger.warning(f"Could not enhance audio, using original: {e}")
            return wav_file
    
    async def split_audio_by_silence(self, wav_file: str, silence_threshold: int = -40) -> List[str]:
        """Split audio by silence to handle multiple sentences"""
        try:
            from pydub import AudioSegment
            from pydub.silence import split_on_silence
            
            audio = AudioSegment.from_wav(wav_file)
            
            # Split audio on silence
            chunks = split_on_silence(
                audio,
                min_silence_len=500,  # Minimum silence length in ms
                silence_thresh=silence_threshold,  # Silence threshold
                keep_silence=100  # Keep some silence at edges
            )
            
            # Save chunks as separate files
            chunk_files = []
            base_name = wav_file.replace('.wav', '')
            
            for i, chunk in enumerate(chunks):
                if len(chunk) > 1000:  # Only save chunks longer than 1 second
                    chunk_file = f"{base_name}_chunk_{i}.wav"
                    chunk.export(chunk_file, format='wav')
                    chunk_files.append(chunk_file)
            
            return chunk_files if chunk_files else [wav_file]
            
        except Exception as e:
            logger.warning(f"Could not split audio: {e}")
            return [wav_file]
    
    def create_silence(self, duration_ms: int, sample_rate: int = None) -> bytes:
        """Create silence audio data"""
        if not sample_rate:
            sample_rate = self.rate
        
        # Calculate number of samples needed
        samples = int(duration_ms * sample_rate / 1000)
        
        # Create silence (zeros)
        silence = b'\x00' * (samples * 2)  # 2 bytes per sample for 16-bit audio
        
        return silence
    
    async def record_audio(self, duration: int, output_file: str) -> Optional[str]:
        """Record audio from microphone (for testing purposes)"""
        if not self.audio:
            logger.error("PyAudio not available for recording")
            return None
        
        try:
            logger.info(f"Recording audio for {duration} seconds...")
            
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            frames = []
            for i in range(0, int(self.rate / self.chunk * duration)):
                data = stream.read(self.chunk)
                frames.append(data)
            
            stream.stop_stream()
            stream.close()
            
            # Save as WAV file
            with wave.open(output_file, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(frames))
            
            logger.info(f"Audio saved to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error recording audio: {e}")
            return None
