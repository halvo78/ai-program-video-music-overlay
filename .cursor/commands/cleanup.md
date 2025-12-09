# /cleanup Command

Clean up temporary files and output directory.

## Usage

```
/cleanup [target] [options]
```

## Targets

| Target | Description |
|--------|-------------|
| `temp` | Clean temporary files |
| `output` | Clean output directory |
| `all` | Clean both (default) |

## Options

| Option | Description |
|--------|-------------|
| `--older-than` | Remove files older than N days |
| `--dry-run` | Show what would be deleted |

## Examples

```bash
# Clean all temporary and output files
/cleanup

# Clean only temp files
/cleanup temp

# Clean files older than 7 days
/cleanup --older-than 7

# Dry run to see what would be deleted
/cleanup --dry-run
```
