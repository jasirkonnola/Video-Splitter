import subprocess
import sys
from pathlib import Path


def get_duration(video_path: str) -> float:
    """Return video duration in seconds using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path,
        ],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def split_in_half(video_path: str, reencode: bool = False) -> None:
    src = Path(video_path)
    duration = get_duration(video_path)
    mid = duration / 2

    part1 = src.with_name(f"{src.stem}_part1{src.suffix}")
    part2 = src.with_name(f"{src.stem}_part2{src.suffix}")

    # Fast mode copies streams (no quality loss, but the cut may be
    # off by a second or so). Re-encode mode is frame-accurate but slower.
    codec = ["-c:v", "libx264", "-c:a", "aac"] if reencode else ["-c", "copy"]

    # First half: 0 -> midpoint
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-t", str(mid), *codec, str(part1)],
        check=True,
    )

    # Second half: midpoint -> end
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(mid), "-i", str(src), *codec, str(part2)],
        check=True,
    )

    print(f"Saved:\n  {part1}\n  {part2}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_video.py <video_file> [--accurate]")
        sys.exit(1)

    split_in_half(sys.argv[1], reencode="--accurate" in sys.argv)
