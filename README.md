# comicwalker-dl

A python tool to download free manga/comics from [ComicWalker](https://comic-walker.com/).

The downloaded images are untouched from the source, they are not modified in any way.

## Requirements
- python3
- [`requests`](https://docs.python-requests.org/)

## Usage

```
usage: walker.py [-h] [-v] cid

positional arguments:
  cid            content id, chapter URL, or series URL

options:
  -h, --help     show this help message and exit
  -v, --verbose  log more
```

all downloaded chapters are saved to `downloaded_chapters/{title}/{chapter}`

### Examples

#### Raw CID

`./walker.py KDCW_AM05000042010001_68`

#### Chapter page

`./walker.py https://comic-walker.com/viewer/?tw=2&dlcl=ja&cid=KDCW_AM05000042010002_68`

#### Series page

`./walker.py https://comic-walker.com/contents/detail/KDCW_AM05000042010000_68/`

---

feel free to modify the code as you wish.
