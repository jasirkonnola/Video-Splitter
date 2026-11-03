# Video Splitter

A small Python script that splits a video into two equal halves and saves each half as its own file. It uses [FFmpeg](https://ffmpeg.org/) under the hood.

## Features

- Splits any FFmpeg-supported video (MP4, MKV, MOV, AVI, etc.) at the exact midpoint
- **Fast mode:** copies streams without re-encoding (no quality loss, cut may be off by a second or so)
- **Accurate mode:** re-encodes for a frame-accurate cut (slower)
- Saves output next to the original file

## Requirements

- Python 3.8 or newer
- FFmpeg and ffprobe available on your PATH

### Installing FFmpeg

**Windows**

```powershell
winget install Gyan.FFmpeg
```

Close and reopen PowerShell afterwards. To refresh PATH in an already-open window:

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

**macOS**

```bash
brew install ffmpeg
```

**Linux (Debian/Ubuntu)**

```bash
sudo apt install ffmpeg
```

Verify the install:

```bash
ffmpeg -version
ffprobe -version
```

## Usage

```bash
python split_video.py <video_file> [--accurate]
```

| Option       | Description                                                      |
| ------------ | ---------------------------------------------------------------- |
| `--accurate` | Re-encode (H.264 + AAC) for an exact cut. Slower, but precise.   |
| *(none)*     | Fast stream copy. Cut may be off by about a second.              |

### Examples

```bash
# Fast split
python split_video.py lecture.mp4

# Frame-accurate split
python split_video.py lecture.mp4 --accurate
```

### Output

For an input named `lecture.mp4`, the script creates:

```
lecture_part1.mp4   # first half
lecture_part2.mp4   # second half
```

## How it works

1. `ffprobe` reads the total duration of the video.
2. The midpoint is calculated (`duration / 2`).
3. `ffmpeg` writes the first half (`0` to midpoint) and the second half (midpoint to end).

## Tips

- **Speed up re-encoding on NVIDIA GPUs:** change `"libx264"` to `"h264_nvenc"` in the script.
- **Long videos:** `--accurate` can take several minutes. FFmpeg prints a lot of progress text, which is normal.
- **Spaces in file names:** wrap the path in quotes, e.g. `python split_video.py "my lecture.mp4"`.

## Troubleshooting

| Problem | Fix |
| ------- | --- |
| `FileNotFoundError: [WinError 2]` | FFmpeg/ffprobe is not on PATH. Install it, then restart the terminal or refresh PATH (see above). |
| `ffmpeg is not recognized` | Same as above. Alternatively, copy `ffmpeg.exe` and `ffprobe.exe` into the script's folder. |
| Output has a few seconds of frozen video at the start of part 2 | You used fast mode. Re-run with `--accurate`. |
| Output files already exist | The script overwrites them (`-y`). Move or rename them first if you want to keep them. |

## License

Free to use and modify.
