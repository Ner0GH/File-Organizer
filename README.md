# File Organizer

Sorts files in a folder into subfolders by extension.

## Usage

```
py main.py <folder>
```

`<folder>` is a folder inside your home directory, so `Documents` means `~/Documents`. Add options at the end:

```
py main.py Documents -v
```

## Options

- `-v` shows skipped files
- `-n` does a dry run, showing what would move without moving anything

## Customization

A `config.json` file is created next to `main.py` the first time you run the program. Edit the `"extensions"` section to change which extensions go into which folders.

For example, to sort `.exe` files into an `Applications` folder, add this line (and keep commas between entries):

```json
".exe": "Applications"
```
