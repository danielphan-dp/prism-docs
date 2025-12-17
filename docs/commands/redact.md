# redact

Redact regions in PDF pages.

## Synopsis

```
prism-docs redact <input> [options]
```

## Options

```
-o, --output PATH      Output file path
--regions SPEC         Regions to redact: "page:x1,y1,x2,y2;..."
--color COLOR          Redaction color (default: black)
```

## Examples

```shell
# Redact single region
prism-docs redact document.pdf --regions "1:100,100,200,200"

# Redact multiple regions
prism-docs redact document.pdf --regions "1:50,50,150,100;2:100,200,300,250"

# Custom color
prism-docs redact document.pdf --regions "1:0,0,100,50" --color white
```

## Notes

Regions are specified as `page:x1,y1,x2,y2` where coordinates are in points from bottom-left.

## See Also

- [flatten](flatten.md) - Flatten annotations
