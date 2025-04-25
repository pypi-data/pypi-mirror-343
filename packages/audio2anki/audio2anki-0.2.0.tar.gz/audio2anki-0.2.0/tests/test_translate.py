"""Tests for translation module."""

import os
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import deepl
import pytest
from rich.progress import Progress

from audio2anki.exceptions import Audio2AnkiError
from audio2anki.transcribe import TranscriptionSegment, load_transcript, save_transcript
from audio2anki.translate import (
    TranslationItem,
    TranslationProvider,
    TranslationResponse,
    translate_segments,
)
from audio2anki.types import LanguageCode


@pytest.mark.parametrize(
    "input_text,expected_translation",
    [
        ("u4f60u597d", "Hello"),
        ("u8c22u8c22", "Thank you"),
    ],
)
def test_translate_with_openai(tmp_path: Path, input_text: str, expected_translation: str) -> None:
    """Test basic translation with OpenAI."""
    segment = TranscriptionSegment(start=0.0, end=1.0, text=input_text, translation=None)

    # Create temporary files for input and output
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("OPENAI_API_KEY", "test-key")
        input_file = tmp_path / "input.json"
        output_file = tmp_path / "output.json"

        # Save segment to input file
        save_transcript([segment], input_file)

        # Create a mock response
        mock_response = TranslationResponse(
            items=[
                TranslationItem(
                    start=0.0,
                    end=1.0,
                    text=input_text,
                    translation=expected_translation,
                    pronunciation=None,
                )
            ]
        )

        # Patch the translate_with_openai_sync function to return our mock response
        with patch("audio2anki.translate.translate_with_openai_sync", return_value=mock_response):
            with Progress() as progress:
                task_id = progress.add_task("Translating", total=1)

                # Translate segment
                translate_segments(
                    input_file,
                    output_file,
                    task_id,
                    progress,
                    source_language=LanguageCode("en"),
                    target_language=LanguageCode("en"),
                )

                # Load the result and verify
                result = load_transcript(output_file)
                assert len(result) == 1
                assert result[0].translation == expected_translation


def test_translate_with_deepl(tmp_path: Path) -> None:
    """Test translation using DeepL."""
    segment = TranscriptionSegment(start=0.0, end=1.0, text="Bonjour", translation=None)

    # Create temporary files for input and output
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("DEEPL_API_TOKEN", "test-key")
        mp.setenv("OPENAI_API_KEY", "test-key")
        input_file = tmp_path / "input.json"
        output_file = tmp_path / "output.json"

        # Save segment to input file
        save_transcript([segment], input_file)

        # Mock for translate_with_deepl function
        def mock_translate_deepl(
            text: str,
            source_lang: LanguageCode,
            target_lang: LanguageCode,
            translator: deepl.Translator,
            model: Any = None,
        ) -> tuple[str, str | None]:
            return "Hello", None  # Return translation and pronunciation

        # Mock for translate_single_segment
        def mock_single_segment(
            segment: TranscriptionSegment,
            source_lang: LanguageCode,
            target_lang: LanguageCode,
            translator: deepl.Translator,
            use_deepl: bool,
            model: Any = None,
        ) -> tuple[TranscriptionSegment, TranscriptionSegment | None, bool]:
            translated = TranscriptionSegment(
                start=segment.start,
                end=segment.end,
                text="Hello",  # The translation
                translation="Hello",
            )
            return translated, None, True  # translated segment, reading segment, success

        with (
            # Patch the DeepL translator to succeed
            patch("deepl.Translator", return_value=MagicMock()),
            # Patch translate_with_deepl
            patch("audio2anki.translate.translate_with_deepl", side_effect=mock_translate_deepl),
            # Patch translate_single_segment
            patch("audio2anki.translate.translate_single_segment", side_effect=mock_single_segment),
        ):
            with Progress() as progress:
                task_id = progress.add_task("Translating", total=1)

                # Translate segment using DeepL
                translate_segments(
                    input_file,
                    output_file,
                    task_id,
                    progress,
                    source_language=LanguageCode("en"),
                    target_language=LanguageCode("es"),
                    translation_provider=TranslationProvider.DEEPL,
                )

                # Load the result and verify
                result = load_transcript(output_file)
                assert len(result) == 1
                assert result[0].translation is not None


def test_deepl_failure_raises_error(tmp_path: Path) -> None:
    """Test that DeepL failure raises Audio2AnkiError (no fallback to OpenAI)."""
    segment = TranscriptionSegment(start=0.0, end=1.0, text="Hola", translation=None)
    input_file = tmp_path / "input.json"
    output_file = tmp_path / "output.json"
    save_transcript([segment], input_file)

    with (
        patch.dict(os.environ, {"DEEPL_API_TOKEN": "test-key", "OPENAI_API_KEY": "test-key"}),
        patch("deepl.Translator") as mock_deepl,
        patch("audio2anki.translate.translate_with_openai_sync"),
    ):
        mock_deepl.side_effect = Exception("DeepL error")
        with Progress() as progress:
            task_id = progress.add_task("Translating", total=1)
            with pytest.raises(Audio2AnkiError):
                translate_segments(
                    input_file,
                    output_file,
                    task_id,
                    progress,
                    source_language=LanguageCode("en"),
                    target_language=LanguageCode("es"),
                    translation_provider=TranslationProvider.DEEPL,
                )


def test_no_api_keys_raises_error(tmp_path: Path) -> None:
    """Test that missing API keys raise appropriate errors."""
    with pytest.MonkeyPatch.context() as mp:
        mp.delenv("OPENAI_API_KEY", raising=False)
        input_file = tmp_path / "input.json"
        output_file = tmp_path / "output.json"

        # Create an empty input file
        save_transcript([], input_file)

        with Progress() as progress:
            task_id = progress.add_task("test", total=1)
            with pytest.raises(ValueError) as exc:
                translate_segments(
                    input_file,
                    output_file,
                    task_id,
                    progress,
                    source_language=LanguageCode("en"),
                    target_language=LanguageCode("es"),
                )
                assert "OPENAI_API_KEY environment variable is required" in str(exc.value)
