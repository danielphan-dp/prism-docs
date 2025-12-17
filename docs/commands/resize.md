# resize

Resize PDF pages.

## Synopsis

```
prism-docs resize <input> [options]
```

## Options

```
-o, --output PATH      Output file path
--size SIZE            Target size: A4, Letter, Legal, A3, etc.
--width N              Custom width (points)
--height N             Custom height (points)
--fit MODE             Fit mode: contain, cover, stretch (default: contain)
```

## Examples

```shell
# Resize to A4
prism-docs resize document.pdf --size A4

# Resize to Letter
prism-docs resize document.pdf --size Letter --fit stretch

# Custom dimensions
prism-docs resize document.pdf --width 612 --height 792 -o resized.pdf
```

## Notes

Standard sizes in points:

- A4: 595 x 842
- Letter: 612 x 792
- Legal: 612 x 1008

## See Also

- [crop](crop.md) - Crop margins
