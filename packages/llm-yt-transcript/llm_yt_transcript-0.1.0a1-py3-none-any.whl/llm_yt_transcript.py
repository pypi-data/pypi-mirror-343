import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
import os

import llm


def get_log_args() -> list[str]:
    """
    Get log arguments for yt-dlp
    """
    log_mode = os.getenv("LLM_YT_LOG", default="default")

    match log_mode.lower():
        case "verbose":
            return ["--verbose"]
        case "quiet":
            return ["--quiet"]
        case "default":
            return []
        case _:
            raise ValueError(f"Unknown log mode: {log_mode}")


def download_subtitles(url, path, sub_format, sub_lang) -> Path:
    """
    https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#subtitle-options
    """
    # yt-dlpのコマンドを構築
    command = [
        "yt-dlp",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-lang",
        sub_lang,
        "--sub-format",
        sub_format,  # 'ass/srt/ttml'
        "--path",
        path,
        "--output",
        "transcript.%(ext)s",
        url,
    ] + get_log_args()

    # コマンドを実行
    subprocess.run(command, check=True)

    out = (
        Path(path) / f"transcript.{sub_lang}.{sub_format}"
    )  # i cannot change this format template...

    if not out.exists():
        raise NameError(f"no such file: {out}")

    return out


def list_subtitles(url):
    """
    https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#subtitle-options
    """
    # yt-dlpのコマンドを構築
    command = ["yt-dlp", "--skip-download", "--list-subs", url] + get_log_args()

    # コマンドを実行
    subprocess.run(command, check=True)


@dataclass
class Subtitle:
    begin_time: str
    end_time: str
    begin_seconds: float
    end_seconds: float
    text: str


class TtmlParser:
    def __init__(self, ttml_content):
        self.ttml_content = ttml_content
        self.subtitles = self.parse_ttml(ttml_content)

    def parse_ttml(self, ttml_content):
        """
        Parse TTML (Timed Text Markup Language) content and extract subtitles with timing information.

        Args:
            ttml_content (str): The TTML content as a string

        Returns:
            list: A list of Subtitle objects containing begin time, end time, and text for each subtitle
        """
        # Define the namespaces used in the TTML file
        namespaces = {
            "ttml": "http://www.w3.org/ns/ttml",
            "tts": "http://www.w3.org/ns/ttml#styling",
            "ttp": "http://www.w3.org/ns/ttml#parameter",
        }

        # Parse the XML content
        try:
            root = ET.fromstring(ttml_content)
        except ET.ParseError as e:
            print(f"Error parsing TTML content: {e}")
            return []

        # Convert time format (HH:MM:SS.mmm) to seconds
        def time_to_seconds(time_str):
            time_pattern = r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})"
            match = re.match(time_pattern, time_str)
            if match:
                hours, minutes, seconds, milliseconds = map(int, match.groups())
                return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
            return 0

        # Find all paragraph elements and extract subtitles
        _subtitles = []

        # The path uses namespaces to find the p elements in the TTML body
        for p in root.findall(".//ttml:body//ttml:p", namespaces):
            begin = p.get("begin")
            end = p.get("end")
            text = p.text or ""

            # Some TTML files might have nested spans
            for span in p.findall(".//ttml:span", namespaces):
                if span.text:
                    text += span.text

            if begin and end:
                subtitle = Subtitle(
                    begin_time=begin,
                    end_time=end,
                    begin_seconds=time_to_seconds(begin),
                    end_seconds=time_to_seconds(end),
                    text=text,
                )
                _subtitles.append(subtitle)

        # Sort subtitles by begin time
        _subtitles.sort(key=lambda x: x.begin_seconds)

        return _subtitles

    def to_text(self, sep="\n"):
        """
        Extract just the text content from TTML, joining all subtitles into a single string.

        Args:
            ttml_content (str): The TTML content as a string

        Returns:
            str: The combined text of all subtitles
        """
        text = sep.join(subtitle.text for subtitle in self.subtitles)
        return text

    def to_srt(self, output_file=None):
        """
        Convert TTML to SRT format.

        Args:
            ttml_content (str): The TTML content as a string
            output_file (str, optional): Path to output SRT file. If None, returns the SRT content as a string.

        Returns:
            str: The SRT content if output_file is None, otherwise None
        """
        srt_content = []

        for i, subtitle in enumerate(self.subtitles, 1):
            # Convert time from seconds to SRT format (HH:MM:SS,mmm)
            def format_time(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                seconds = seconds % 60
                return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace(".", ",")

            begin_formatted = format_time(subtitle.begin_seconds)
            end_formatted = format_time(subtitle.end_seconds)

            srt_content.append(
                f"{i}\n{begin_formatted} --> {end_formatted}\n{subtitle.text}\n"
            )

        srt_output = "\n".join(srt_content)

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(srt_output)
            return None
        else:
            return srt_output


@llm.hookimpl
def register_fragment_loaders(register):
    register("ytt", yt_transcript_loader)


def yt_transcript_loader(argument: str) -> list[llm.Fragment]:
    """
    Load Youtube transcript

    Args:
        argument:

    Returns:
        List of Fragment objects, one for each tnrascript for a video
    """

    if argument.startswith(("http://", "https://")):
        sub_lang = "en"  # default
        video_url = argument
    else:
        sub_lang, *rest = argument.split(":")
        video_url = ":".join(rest)

    with tempfile.TemporaryDirectory() as td:
        out = download_subtitles(
            url=video_url, path=td, sub_format="ttml", sub_lang=sub_lang
        )

        ttml = out.read_text()

    parser = TtmlParser(ttml)

    return [llm.Fragment(parser.to_text(), argument)]
