# /status Command

Check system status and health.

## Usage

```
/status [component]
```

## Components

| Component | Description |
|-----------|-------------|
| `all` | Full system status (default) |
| `processing` | Media processing status |
| `storage` | Storage and disk usage |
| `memory` | Memory usage and limits |
| `formats` | Supported format status |

## Examples

```bash
# Full status
/status

# Processing status only
/status processing

# Storage status
/status storage
```

## Output

### Processing Status

```
╔══════════════════════════════════════════════════════════════╗
║                    PROCESSING STATUS                         ║
╠══════════════════════════════════════════════════════════════╣
║  Active Jobs:        0                                       ║
║  Queue Length:        0                                       ║
║  Processing Mode:     Safe                                   ║
║  Output Directory:   ./output                               ║
╚══════════════════════════════════════════════════════════════╝
```

### Storage Status

```
╔══════════════════════════════════════════════════════════════╗
║                    STORAGE STATUS                            ║
╠══════════════════════════════════════════════════════════════╣
║  Disk Usage:         45.2 GB / 500 GB (9.0%)                  ║
║  Output Directory:   2.1 GB                                  ║
║  Temp Directory:     0.5 GB                                  ║
║  Available Space:    454.8 GB                                ║
╚══════════════════════════════════════════════════════════════╝
```
