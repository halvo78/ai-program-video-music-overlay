# /process Command

Process video files with music overlay.

## Usage

```
/process <input_file> [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--audio` | Audio file to overlay | Required |
| `--quality` | Output quality (high/medium/low) | high |
| `--output` | Output file path | auto-generated |
| `--preview` | Preview before processing | false |

## Examples

```bash
# Basic processing
/process video.mp4 --audio music.mp3

# With quality setting
/process video.mp4 --audio music.mp3 --quality medium

# With custom output
/process video.mp4 --audio music.mp3 --output result.mp4

# Preview first
/process video.mp4 --audio music.mp3 --preview
```
