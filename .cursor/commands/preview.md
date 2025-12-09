# /preview Command

Preview video/audio files or processing results.

## Usage

```
/preview <file> [options]
```

## Options

| Option | Description |
|--------|-------------|
| `--start` | Start time (seconds) |
| `--duration` | Duration to preview (seconds) |
| `--frame` | Preview specific frame number |

## Examples

```bash
# Preview video file
/preview video.mp4

# Preview with time range
/preview video.mp4 --start 30 --duration 10

# Preview specific frame
/preview video.mp4 --frame 100
```
