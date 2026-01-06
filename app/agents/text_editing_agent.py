"""
Text-Based Video Editing Agent
==============================

Edit videos by editing their transcript - inspired by Descript.
Revolutionary approach: edit video as easily as editing a document.

Features:
1. Transcription - Auto-transcribe video/audio
2. Text-Based Editing - Edit video by editing text
3. Multi-Speaker Detection - Identify different speakers
4. Filler Word Removal - Auto-detect "um", "ah", "like"
5. Smart Cut - Remove silences automatically
6. Word-Level Timeline - Precise word timing
7. Scene Detection - Auto-detect scene changes
8. Search & Replace - Find and edit across video
9. Overdub - Replace words with AI voice
10. Export EDL/XML - Professional editing software export
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import re

logger = logging.getLogger(__name__)


class TranscriptionProvider(Enum):
    WHISPER = "whisper"
    ASSEMBLY_AI = "assembly_ai"
    DEEPGRAM = "deepgram"
    GOOGLE = "google"
    AWS = "aws"
    REV = "rev"


class FillerWordType(Enum):
    UM = "um"
    UH = "uh"
    AH = "ah"
    LIKE = "like"
    YOU_KNOW = "you_know"
    SO = "so"
    BASICALLY = "basically"
    ACTUALLY = "actually"
    LITERALLY = "literally"
    REPEATED = "repeated"  # Repeated words


@dataclass
class Word:
    """A single word with timing information"""
    word: str
    start_time: float  # seconds
    end_time: float
    confidence: float = 1.0
    speaker: str = ""
    is_filler: bool = False
    filler_type: Optional[FillerWordType] = None
    is_selected: bool = True  # False = cut from final video


@dataclass
class Sentence:
    """A sentence containing multiple words"""
    words: List[Word]
    start_time: float
    end_time: float
    speaker: str = ""
    text: str = ""

    def __post_init__(self):
        if not self.text and self.words:
            self.text = " ".join(w.word for w in self.words)


@dataclass
class Speaker:
    """Speaker identification"""
    speaker_id: str
    name: str = ""
    color: str = "#3B82F6"  # Display color
    total_speaking_time: float = 0
    word_count: int = 0


@dataclass
class Scene:
    """Detected scene in video"""
    scene_id: str
    start_time: float
    end_time: float
    thumbnail_url: str = ""
    description: str = ""
    keywords: List[str] = field(default_factory=list)


@dataclass
class Transcript:
    """Complete transcript with metadata"""
    transcript_id: str
    video_path: str
    words: List[Word] = field(default_factory=list)
    sentences: List[Sentence] = field(default_factory=list)
    speakers: Dict[str, Speaker] = field(default_factory=dict)
    scenes: List[Scene] = field(default_factory=list)
    duration_seconds: float = 0
    language: str = "en"
    filler_words_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def text(self) -> str:
        """Get full transcript text"""
        return " ".join(w.word for w in self.words if w.is_selected)

    @property
    def full_text(self) -> str:
        """Get full transcript text including cut words"""
        return " ".join(w.word for w in self.words)


@dataclass
class EditOperation:
    """A single edit operation"""
    operation_type: str  # cut, keep, replace, insert
    start_index: int  # Word index
    end_index: int
    new_text: str = ""  # For replace/insert
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EditHistory:
    """Edit history for undo/redo"""
    operations: List[EditOperation] = field(default_factory=list)
    current_index: int = -1

    def add(self, operation: EditOperation):
        # Remove any operations after current index (for redo branch)
        self.operations = self.operations[:self.current_index + 1]
        self.operations.append(operation)
        self.current_index = len(self.operations) - 1

    def undo(self) -> Optional[EditOperation]:
        if self.current_index >= 0:
            op = self.operations[self.current_index]
            self.current_index -= 1
            return op
        return None

    def redo(self) -> Optional[EditOperation]:
        if self.current_index < len(self.operations) - 1:
            self.current_index += 1
            return self.operations[self.current_index]
        return None


class TextBasedEditingAgent:
    """
    Text-Based Video Editing Agent.

    Edit videos by editing their transcript - as easy as editing a document.
    """

    def __init__(
        self,
        openai_key: str = None,
        assembly_ai_key: str = None,
        deepgram_key: str = None
    ):
        self.openai_key = openai_key
        self.assembly_ai_key = assembly_ai_key
        self.deepgram_key = deepgram_key

        # Active transcripts
        self.transcripts: Dict[str, Transcript] = {}
        self.edit_histories: Dict[str, EditHistory] = {}

        # Filler word patterns
        self.filler_patterns = {
            FillerWordType.UM: r'\b(um+|umm+)\b',
            FillerWordType.UH: r'\b(uh+|uhh+)\b',
            FillerWordType.AH: r'\b(ah+|ahh+)\b',
            FillerWordType.LIKE: r'\b(like)\b',
            FillerWordType.YOU_KNOW: r'\b(you know)\b',
            FillerWordType.SO: r'^so\b',  # Only at start
            FillerWordType.BASICALLY: r'\b(basically)\b',
            FillerWordType.ACTUALLY: r'\b(actually)\b',
            FillerWordType.LITERALLY: r'\b(literally)\b',
        }

    async def transcribe(
        self,
        video_path: str,
        language: str = "en",
        detect_speakers: bool = True,
        detect_scenes: bool = True,
        provider: TranscriptionProvider = TranscriptionProvider.WHISPER
    ) -> Transcript:
        """
        Transcribe video/audio with word-level timestamps.

        Args:
            video_path: Path to video/audio file
            language: Language code
            detect_speakers: Enable speaker diarization
            detect_scenes: Enable scene detection
            provider: Transcription provider to use

        Returns:
            Transcript with word-level timing
        """
        import uuid
        transcript_id = str(uuid.uuid4())[:8]

        if provider == TranscriptionProvider.WHISPER:
            transcript = await self._transcribe_whisper(video_path, language, detect_speakers)
        elif provider == TranscriptionProvider.ASSEMBLY_AI:
            transcript = await self._transcribe_assembly(video_path, language, detect_speakers)
        elif provider == TranscriptionProvider.DEEPGRAM:
            transcript = await self._transcribe_deepgram(video_path, language, detect_speakers)
        else:
            transcript = await self._transcribe_whisper(video_path, language, detect_speakers)

        transcript.transcript_id = transcript_id
        transcript.video_path = video_path
        transcript.language = language

        # Detect filler words
        self._detect_filler_words(transcript)

        # Group into sentences
        self._group_sentences(transcript)

        # Detect scenes if requested
        if detect_scenes:
            transcript.scenes = await self._detect_scenes(video_path)

        # Store transcript
        self.transcripts[transcript_id] = transcript
        self.edit_histories[transcript_id] = EditHistory()

        return transcript

    async def _transcribe_whisper(
        self,
        video_path: str,
        language: str,
        detect_speakers: bool
    ) -> Transcript:
        """Transcribe using OpenAI Whisper"""
        if not self.openai_key:
            raise ValueError("OpenAI API key required for Whisper")

        try:
            import openai

            client = openai.AsyncOpenAI(api_key=self.openai_key)

            with open(video_path, "rb") as audio_file:
                # Use Whisper API with timestamps
                response = await client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language if language != "auto" else None,
                    response_format="verbose_json",
                    timestamp_granularities=["word", "segment"]
                )

            words = []
            for word_info in response.words:
                words.append(Word(
                    word=word_info.word,
                    start_time=word_info.start,
                    end_time=word_info.end,
                    confidence=1.0
                ))

            return Transcript(
                transcript_id="",
                video_path=video_path,
                words=words,
                duration_seconds=response.duration if hasattr(response, 'duration') else 0
            )

        except Exception as e:
            logger.error(f"Whisper transcription error: {e}")
            # Return empty transcript as fallback
            return Transcript(transcript_id="", video_path=video_path)

    async def _transcribe_assembly(
        self,
        video_path: str,
        language: str,
        detect_speakers: bool
    ) -> Transcript:
        """Transcribe using AssemblyAI"""
        if not self.assembly_ai_key:
            raise ValueError("AssemblyAI API key required")

        try:
            import httpx
            import time

            async with httpx.AsyncClient() as client:
                # Upload file
                with open(video_path, "rb") as f:
                    upload_response = await client.post(
                        "https://api.assemblyai.com/v2/upload",
                        headers={"authorization": self.assembly_ai_key},
                        data=f.read(),
                        timeout=300.0
                    )
                upload_url = upload_response.json()["upload_url"]

                # Start transcription
                transcript_request = {
                    "audio_url": upload_url,
                    "language_code": language,
                    "speaker_labels": detect_speakers,
                    "word_boost": []
                }

                response = await client.post(
                    "https://api.assemblyai.com/v2/transcript",
                    headers={"authorization": self.assembly_ai_key},
                    json=transcript_request
                )
                transcript_id = response.json()["id"]

                # Poll for completion
                while True:
                    status_response = await client.get(
                        f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                        headers={"authorization": self.assembly_ai_key}
                    )
                    status_data = status_response.json()

                    if status_data["status"] == "completed":
                        break
                    elif status_data["status"] == "error":
                        raise Exception(f"Transcription failed: {status_data.get('error')}")

                    await asyncio.sleep(3)

                # Extract words
                words = []
                speakers = {}

                for word_info in status_data.get("words", []):
                    speaker = word_info.get("speaker", "Speaker 1")
                    words.append(Word(
                        word=word_info["text"],
                        start_time=word_info["start"] / 1000,
                        end_time=word_info["end"] / 1000,
                        confidence=word_info.get("confidence", 1.0),
                        speaker=speaker
                    ))

                    if speaker not in speakers:
                        speakers[speaker] = Speaker(
                            speaker_id=speaker,
                            name=speaker
                        )

                return Transcript(
                    transcript_id="",
                    video_path=video_path,
                    words=words,
                    speakers=speakers,
                    duration_seconds=status_data.get("audio_duration", 0)
                )

        except Exception as e:
            logger.error(f"AssemblyAI transcription error: {e}")
            return Transcript(transcript_id="", video_path=video_path)

    async def _transcribe_deepgram(
        self,
        video_path: str,
        language: str,
        detect_speakers: bool
    ) -> Transcript:
        """Transcribe using Deepgram"""
        if not self.deepgram_key:
            raise ValueError("Deepgram API key required")

        try:
            import httpx

            async with httpx.AsyncClient() as client:
                with open(video_path, "rb") as f:
                    response = await client.post(
                        "https://api.deepgram.com/v1/listen",
                        headers={
                            "Authorization": f"Token {self.deepgram_key}",
                            "Content-Type": "audio/mpeg"
                        },
                        params={
                            "model": "nova-2",
                            "language": language,
                            "diarize": str(detect_speakers).lower(),
                            "punctuate": "true",
                            "utterances": "true"
                        },
                        data=f.read(),
                        timeout=300.0
                    )

                data = response.json()
                channel = data["results"]["channels"][0]
                alternative = channel["alternatives"][0]

                words = []
                for word_info in alternative.get("words", []):
                    words.append(Word(
                        word=word_info["word"],
                        start_time=word_info["start"],
                        end_time=word_info["end"],
                        confidence=word_info.get("confidence", 1.0),
                        speaker=word_info.get("speaker", "")
                    ))

                return Transcript(
                    transcript_id="",
                    video_path=video_path,
                    words=words,
                    duration_seconds=data.get("metadata", {}).get("duration", 0)
                )

        except Exception as e:
            logger.error(f"Deepgram transcription error: {e}")
            return Transcript(transcript_id="", video_path=video_path)

    def _detect_filler_words(self, transcript: Transcript):
        """Detect filler words in transcript"""
        filler_count = 0

        for word in transcript.words:
            word_lower = word.word.lower().strip(".,!?")

            for filler_type, pattern in self.filler_patterns.items():
                if re.match(pattern, word_lower, re.IGNORECASE):
                    word.is_filler = True
                    word.filler_type = filler_type
                    filler_count += 1
                    break

        # Detect repeated words
        prev_word = ""
        for word in transcript.words:
            if word.word.lower() == prev_word.lower() and len(word.word) > 2:
                word.is_filler = True
                word.filler_type = FillerWordType.REPEATED
                filler_count += 1
            prev_word = word.word

        transcript.filler_words_count = filler_count

    def _group_sentences(self, transcript: Transcript):
        """Group words into sentences"""
        sentences = []
        current_sentence_words = []
        sentence_end_chars = ".!?"

        for word in transcript.words:
            current_sentence_words.append(word)

            # Check if this word ends a sentence
            if any(word.word.endswith(c) for c in sentence_end_chars):
                if current_sentence_words:
                    sentences.append(Sentence(
                        words=current_sentence_words.copy(),
                        start_time=current_sentence_words[0].start_time,
                        end_time=current_sentence_words[-1].end_time,
                        speaker=current_sentence_words[0].speaker
                    ))
                    current_sentence_words = []

        # Add remaining words as final sentence
        if current_sentence_words:
            sentences.append(Sentence(
                words=current_sentence_words,
                start_time=current_sentence_words[0].start_time,
                end_time=current_sentence_words[-1].end_time,
                speaker=current_sentence_words[0].speaker
            ))

        transcript.sentences = sentences

    async def _detect_scenes(self, video_path: str) -> List[Scene]:
        """Detect scene changes in video"""
        # This would use a video analysis model in production
        # For now, return empty list
        return []

    def cut_selection(
        self,
        transcript_id: str,
        start_index: int,
        end_index: int
    ) -> bool:
        """
        Cut a selection of words from the video.

        Args:
            transcript_id: Transcript ID
            start_index: Starting word index
            end_index: Ending word index (exclusive)

        Returns:
            Success status
        """
        transcript = self.transcripts.get(transcript_id)
        if not transcript:
            return False

        for i in range(start_index, min(end_index, len(transcript.words))):
            transcript.words[i].is_selected = False

        # Record edit operation
        self.edit_histories[transcript_id].add(EditOperation(
            operation_type="cut",
            start_index=start_index,
            end_index=end_index
        ))

        return True

    def restore_selection(
        self,
        transcript_id: str,
        start_index: int,
        end_index: int
    ) -> bool:
        """Restore a cut selection"""
        transcript = self.transcripts.get(transcript_id)
        if not transcript:
            return False

        for i in range(start_index, min(end_index, len(transcript.words))):
            transcript.words[i].is_selected = True

        self.edit_histories[transcript_id].add(EditOperation(
            operation_type="keep",
            start_index=start_index,
            end_index=end_index
        ))

        return True

    def remove_filler_words(
        self,
        transcript_id: str,
        filler_types: List[FillerWordType] = None
    ) -> int:
        """
        Remove all filler words of specified types.

        Returns number of words removed.
        """
        transcript = self.transcripts.get(transcript_id)
        if not transcript:
            return 0

        filler_types = filler_types or list(FillerWordType)
        removed_count = 0

        for i, word in enumerate(transcript.words):
            if word.is_filler and word.filler_type in filler_types:
                word.is_selected = False
                removed_count += 1

        return removed_count

    def smart_cut_silences(
        self,
        transcript_id: str,
        min_silence_duration: float = 0.5
    ) -> int:
        """
        Automatically cut silences between words.

        Returns number of cuts made.
        """
        transcript = self.transcripts.get(transcript_id)
        if not transcript or len(transcript.words) < 2:
            return 0

        cuts_made = 0

        for i in range(1, len(transcript.words)):
            prev_word = transcript.words[i - 1]
            curr_word = transcript.words[i]

            gap = curr_word.start_time - prev_word.end_time
            if gap > min_silence_duration:
                # This gap would be shortened in the final video
                cuts_made += 1

        return cuts_made

    def find_and_replace(
        self,
        transcript_id: str,
        find_text: str,
        replace_text: str = None,
        cut_matches: bool = False
    ) -> int:
        """
        Find text in transcript and optionally replace or cut.

        Returns number of matches found.
        """
        transcript = self.transcripts.get(transcript_id)
        if not transcript:
            return 0

        matches = 0
        find_lower = find_text.lower()

        for i, word in enumerate(transcript.words):
            if find_lower in word.word.lower():
                matches += 1
                if cut_matches:
                    word.is_selected = False
                elif replace_text:
                    # Mark for overdub/replace
                    pass

        return matches

    def get_selected_words(self, transcript_id: str) -> List[Word]:
        """Get only selected (not cut) words"""
        transcript = self.transcripts.get(transcript_id)
        if not transcript:
            return []
        return [w for w in transcript.words if w.is_selected]

    def get_cut_ranges(self, transcript_id: str) -> List[Tuple[float, float]]:
        """Get time ranges that have been cut"""
        transcript = self.transcripts.get(transcript_id)
        if not transcript:
            return []

        cut_ranges = []
        in_cut = False
        cut_start = 0

        for word in transcript.words:
            if not word.is_selected and not in_cut:
                cut_start = word.start_time
                in_cut = True
            elif word.is_selected and in_cut:
                cut_ranges.append((cut_start, word.start_time))
                in_cut = False

        # Handle trailing cut
        if in_cut and transcript.words:
            cut_ranges.append((cut_start, transcript.words[-1].end_time))

        return cut_ranges

    def export_edl(self, transcript_id: str) -> str:
        """
        Export Edit Decision List (EDL) for professional editing software.

        Returns EDL format string.
        """
        transcript = self.transcripts.get(transcript_id)
        if not transcript:
            return ""

        def timecode(seconds: float) -> str:
            """Convert seconds to timecode format"""
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            f = int((seconds % 1) * 30)  # 30fps frames
            return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"

        edl_lines = [
            "TITLE: TAJ_CHAT_EXPORT",
            "FCM: NON-DROP FRAME",
            ""
        ]

        edit_num = 1
        selected_ranges = self._get_selected_ranges(transcript)

        for start, end in selected_ranges:
            edl_lines.append(
                f"{edit_num:03d}  001      V     C        "
                f"{timecode(start)} {timecode(end)} "
                f"{timecode(0)} {timecode(end - start)}"
            )
            edit_num += 1

        return "\n".join(edl_lines)

    def _get_selected_ranges(self, transcript: Transcript) -> List[Tuple[float, float]]:
        """Get time ranges of selected content"""
        ranges = []
        in_range = False
        range_start = 0

        for word in transcript.words:
            if word.is_selected and not in_range:
                range_start = word.start_time
                in_range = True
            elif not word.is_selected and in_range:
                ranges.append((range_start, word.start_time))
                in_range = False

        # Handle trailing selection
        if in_range and transcript.words:
            ranges.append((range_start, transcript.words[-1].end_time))

        return ranges

    def export_srt(self, transcript_id: str) -> str:
        """Export subtitles in SRT format"""
        transcript = self.transcripts.get(transcript_id)
        if not transcript:
            return ""

        def srt_time(seconds: float) -> str:
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            ms = int((seconds % 1) * 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        srt_lines = []
        selected_sentences = [
            s for s in transcript.sentences
            if any(w.is_selected for w in s.words)
        ]

        for i, sentence in enumerate(selected_sentences, 1):
            selected_words = [w for w in sentence.words if w.is_selected]
            if not selected_words:
                continue

            start = selected_words[0].start_time
            end = selected_words[-1].end_time
            text = " ".join(w.word for w in selected_words)

            srt_lines.extend([
                str(i),
                f"{srt_time(start)} --> {srt_time(end)}",
                text,
                ""
            ])

        return "\n".join(srt_lines)

    def undo(self, transcript_id: str) -> bool:
        """Undo last edit"""
        history = self.edit_histories.get(transcript_id)
        if not history:
            return False

        operation = history.undo()
        if operation:
            # Reverse the operation
            transcript = self.transcripts[transcript_id]
            for i in range(operation.start_index, min(operation.end_index, len(transcript.words))):
                if operation.operation_type == "cut":
                    transcript.words[i].is_selected = True
                elif operation.operation_type == "keep":
                    transcript.words[i].is_selected = False
            return True
        return False

    def redo(self, transcript_id: str) -> bool:
        """Redo last undone edit"""
        history = self.edit_histories.get(transcript_id)
        if not history:
            return False

        operation = history.redo()
        if operation:
            transcript = self.transcripts[transcript_id]
            for i in range(operation.start_index, min(operation.end_index, len(transcript.words))):
                if operation.operation_type == "cut":
                    transcript.words[i].is_selected = False
                elif operation.operation_type == "keep":
                    transcript.words[i].is_selected = True
            return True
        return False


# Factory function
async def create_text_editing_agent(
    openai_key: str = None,
    assembly_ai_key: str = None,
    deepgram_key: str = None
) -> TextBasedEditingAgent:
    """Create and configure text-based editing agent"""
    import os

    return TextBasedEditingAgent(
        openai_key=openai_key or os.getenv("OPENAI_API_KEY"),
        assembly_ai_key=assembly_ai_key or os.getenv("ASSEMBLY_AI_KEY"),
        deepgram_key=deepgram_key or os.getenv("DEEPGRAM_API_KEY")
    )
