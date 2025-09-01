"""
Voice processing module for handling speech-to-text and text-to-speech
"""

import os
import tempfile
import asyncio
import logging
from typing import Optional
import speech_recognition as sr
import pyttsx3
from telegram import File
import wave
import pyaudio

from utils.logger import setup_logger

logger = setup_logger(__name__)

class VoiceProcessor:
    """Handle voice message processing and text-to-speech generation"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = None
        self._init_tts_engine()
    
    def _init_tts_engine(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to use a female voice for educational content
                for voice in voices:
                    if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate (slower for educational content)
            self.tts_engine.setProperty('rate', 150)  # Default is usually 200
            self.tts_engine.setProperty('volume', 0.8)
            
        except Exception as e:
            logger.warning(f"Could not initialize TTS engine: {e}")
            self.tts_engine = None
    
    async def process_voice_message(self, voice_file: File) -> Optional[str]:
        """Convert voice message to text"""
        try:
            # Create temporary file for voice data
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_ogg:
                await voice_file.download_to_drive(temp_ogg.name)
                
                # Convert OGG to WAV for speech recognition
                wav_file = await self._convert_ogg_to_wav(temp_ogg.name)
                
                if not wav_file:
                    logger.error("Failed to convert voice file")
                    return None
                
                # Enhance audio for better recognition
                from utils.audio_handler import AudioHandler
                audio_handler = AudioHandler()
                enhanced_file = await audio_handler.enhance_audio_for_speech(wav_file)
                
                # Perform speech recognition on enhanced audio
                text = await self._speech_to_text(enhanced_file or wav_file)
                
                # If speech recognition completely failed, try direct Gemini processing
                if not text and wav_file:
                    logger.info("All traditional STT methods failed, trying direct Gemini audio processing...")
                    text = await self._gemini_audio_transcription(wav_file)
                
                # Clean up temporary files
                try:
                    os.unlink(temp_ogg.name)
                    os.unlink(wav_file)
                except Exception as e:
                    logger.warning(f"Could not clean up temp files: {e}")
                
                return text
                
        except Exception as e:
            logger.error(f"Error processing voice message: {e}")
            return None
    
    async def _convert_ogg_to_wav(self, ogg_file: str) -> Optional[str]:
        """Convert OGG file to WAV format with better Telegram compatibility"""
        try:
            import subprocess
            
            wav_file = ogg_file.replace('.ogg', '.wav')
            
            # Use ffmpeg with optimized settings for speech recognition
            try:
                # Enhanced ffmpeg conversion for better speech recognition
                subprocess.run([
                    'ffmpeg', '-i', ogg_file, 
                    '-acodec', 'pcm_s16le',  # 16-bit PCM
                    '-ar', '16000',          # 16kHz sample rate
                    '-ac', '1',              # Mono channel
                    '-af', 'highpass=f=200,lowpass=f=3000',  # Filter for speech
                    '-y', wav_file
                ], check=True, capture_output=True)
                
                logger.info(f"Successfully converted {ogg_file} to {wav_file}")
                return wav_file
                
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                logger.warning(f"ffmpeg conversion failed: {e}")
                # Fallback: try using pydub if ffmpeg not available
                return await self._convert_with_pydub(ogg_file, wav_file)
                
        except Exception as e:
            logger.error(f"Error converting OGG to WAV: {e}")
            return None
    
    async def _convert_with_pydub(self, input_file: str, output_file: str) -> Optional[str]:
        """Fallback conversion using pydub with enhanced processing"""
        try:
            from pydub import AudioSegment
            from pydub.effects import normalize
            
            # Load the audio file (handle different Telegram formats)
            try:
                audio = AudioSegment.from_ogg(input_file)
            except:
                # Try as general audio file if OGG fails
                audio = AudioSegment.from_file(input_file)
            
            # Enhance audio for speech recognition
            # 1. Normalize volume
            audio = normalize(audio)
            
            # 2. Convert to optimal format for speech recognition
            audio = audio.set_channels(1)  # Mono
            audio = audio.set_frame_rate(16000)  # 16kHz
            audio = audio.set_sample_width(2)  # 16-bit
            
            # 3. Apply audio filters for better speech clarity
            # High-pass filter to remove low-frequency noise
            audio = audio.high_pass_filter(200)
            # Low-pass filter to remove high-frequency noise
            audio = audio.low_pass_filter(3000)
            
            # 4. Adjust volume if too quiet
            if audio.dBFS < -30:
                audio = audio + (20 - abs(audio.dBFS))
            
            # Export as WAV
            audio.export(output_file, format='wav')
            
            logger.info(f"Enhanced audio conversion complete: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error with pydub conversion: {e}")
            return None
    
    async def _speech_to_text(self, wav_file: str) -> Optional[str]:
        """Convert WAV audio file to text"""
        try:
            with sr.AudioFile(wav_file) as source:
                # Adjust for ambient noise with longer duration
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Adjust energy threshold for better detection
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
                
                # Record the audio
                audio_data = self.recognizer.record(source)
                
                # Try multiple recognition services
                text = None
                
                # Try Google Speech Recognition first
                try:
                    text = self.recognizer.recognize_google(
                        audio_data, 
                        language='en-US',
                        show_all=False
                    )
                    logger.info(f"Google STT successful: {text}")
                except sr.UnknownValueError:
                    logger.warning("Google STT could not understand audio")
                except sr.RequestError as e:
                    logger.warning(f"Google STT request failed: {e}")
                
                # Try with different language if English fails
                if not text:
                    try:
                        # Try with auto-detect language
                        text = self.recognizer.recognize_google(audio_data)
                        logger.info(f"Google STT with auto-detect successful: {text}")
                    except (sr.UnknownValueError, sr.RequestError):
                        logger.warning("Google STT auto-detect also failed")
                
                # Try Gemini AI audio processing as fallback
                if not text:
                    try:
                        logger.info("Attempting Gemini AI audio transcription as fallback...")
                        # Use Gemini AI for audio understanding
                        text = await self._gemini_audio_transcription(wav_file)
                        if text:
                            logger.info(f"✅ Gemini audio transcription successful: {text}")
                        else:
                            logger.warning("❌ Gemini audio transcription returned empty result")
                    except Exception as e:
                        logger.error(f"❌ Gemini audio transcription failed: {e}")
                
                return text
                
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            return None
    
    async def _gemini_audio_transcription(self, wav_file: str) -> Optional[str]:
        """Use Gemini AI for audio transcription as fallback"""
        try:
            from google import genai
            from google.genai import types
            import os
            
            # Initialize Gemini client
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.error("GEMINI_API_KEY not available for audio transcription")
                return None
            
            client = genai.Client(api_key=api_key)
            
            # Read audio file as bytes
            with open(wav_file, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            
            # Use Gemini for audio understanding
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[
                    types.Part.from_bytes(
                        data=audio_bytes,
                        mime_type="audio/wav"
                    ),
                    "Please transcribe this audio message. Focus on extracting the spoken text accurately. If it's a programming or coding question, preserve technical terms exactly."
                ]
            )
            
            if response and response.text:
                transcribed_text = response.text.strip()
                logger.info(f"Gemini transcription result: {transcribed_text}")
                return transcribed_text
            
            return None
            
        except Exception as e:
            logger.error(f"Error in Gemini audio transcription: {e}")
            return None
    
    async def text_to_speech(self, text: str) -> Optional[bytes]:
        """Convert text to speech audio"""
        if not self.tts_engine:
            logger.warning("TTS engine not available")
            return None
        
        try:
            # Create temporary file for audio output
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                temp_file = temp_audio.name
            
            # Configure TTS for educational tone
            educational_text = self._prepare_educational_text(text)
            
            # Generate speech
            self.tts_engine.save_to_file(educational_text, temp_file)
            self.tts_engine.runAndWait()
            
            # Read the generated audio file
            try:
                with open(temp_file, 'rb') as audio_file:
                    audio_data = audio_file.read()
                
                # Clean up
                os.unlink(temp_file)
                
                return audio_data
                
            except Exception as e:
                logger.error(f"Error reading TTS output: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            return None
    
    def _prepare_educational_text(self, text: str) -> str:
        """Prepare text for educational speech synthesis"""
        # Remove markdown formatting
        import re
        
        # Remove markdown bold/italic
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        
        # Remove code blocks
        text = re.sub(r'```.*?```', '[code example]', text, flags=re.DOTALL)
        text = re.sub(r'`(.*?)`', r'\1', text)
        
        # Replace emojis with words
        emoji_replacements = {
            '🎓': 'Education',
            '🚀': 'Important',
            '💡': 'Tip',
            '🔍': 'Note',
            '⚠️': 'Warning',
            '✅': 'Correct',
            '❌': 'Incorrect',
            '🐛': 'Bug'
        }
        
        for emoji, replacement in emoji_replacements.items():
            text = text.replace(emoji, replacement)
        
        # Add pauses for better clarity in speech
        text = text.replace('.', '. ')
        text = text.replace(',', ', ')
        text = text.replace(':', ': ')
        text = text.replace(';', '; ')
        
        # Limit length for voice messages
        if len(text) > 500:
            text = text[:500] + "... For the full explanation, please read the text response."
        
        return text
    
    async def _gemini_text_to_speech(self, text: str) -> Optional[bytes]:
        """Use Gemini AI for text-to-speech generation (placeholder for future implementation)"""
        # Note: This is a placeholder - Gemini TTS may not be available yet
        # For now, we'll rely on the traditional TTS engine
        logger.info("Gemini TTS not yet implemented")
        return None
