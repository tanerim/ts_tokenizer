# Command line

## Files and standard input

```bash
ts-tokenizer input.txt
cat input.txt | ts-tokenizer
zcat input.txt.gz | ts-tokenizer
```

To use the filename argument, standard input must be a terminal. When standard
input is redirected, the CLI reads it instead of the filename argument. Empty
standard input produces an error and exit status 1.

## Options

| Option | Meaning | Default |
| --- | --- | --- |
| `-o`, `--output` | `tokenized`, `lines`, `tagged`, `tagged_lines` | `tokenized` |
| `-n`, `--num-workers` | Worker count for file processing | CPU count minus one |
| `-v`, `--verbose` | Accepted for compatibility; has no effect | Disabled |
| `-V`, `--version` | Display package version | — |
| `-h`, `--help` | Display help | — |

File processing uses multiple processes. Piped text is processed directly.
Specify `-n 1` on a single-CPU system for file processing.
Input files are read as UTF-8.

```bash
ts-tokenizer -n 2 -o tagged input.txt
cat input.txt | ts-tokenizer -o lines
```

## Pipelines

Count token frequencies:

```bash
cat input.txt | ts-tokenizer | sort | uniq -c | sort -n
```

Count tag frequencies:

```bash
cat input.txt | ts-tokenizer -o tagged | cut -f2 | sort | uniq -c
```

The CLI uses string format names; `OutputFormat` is for the Python API.
See [Output formats](Output-Formats) and [Token tags](Token-Tags).
