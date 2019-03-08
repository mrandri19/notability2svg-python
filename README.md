# Appunti

Ho unzippato il file `.note`

```console
➜  Notability unzip Nota\ 7\ mar\ 2019.note
Archive:  Nota 7 mar 2019.note
  inflating: Nota 7 mar 2019/thumbnail
   creating: Nota 7 mar 2019/Assets/
  inflating: Nota 7 mar 2019/Session.plist
  inflating: Nota 7 mar 2019/thumb3x.png
  inflating: Nota 7 mar 2019/Recordings/library.plist
  inflating: Nota 7 mar 2019/thumb2x.png
  inflating: Nota 7 mar 2019/thumbnail2x
  inflating: Nota 7 mar 2019/metadata.plist
   creating: Nota 7 mar 2019/Images/
   creating: Nota 7 mar 2019/HandwritingIndex/
  inflating: Nota 7 mar 2019/thumb6x.png
  inflating: Nota 7 mar 2019/thumb.png
```

- `thumbnail2x`
- `thumbnail`
  File .plist

- `thumb6x.png`
- `thumb3x.png`
- `thumb2x.png`
- `thumb.png`
  Png anteprima

- `Assets/`
  Boh, inutile

- `Session.plist`
  La roba e' qua

- `Recordings/library.plist`
  Boh, inutile

- `metadata.plist`
  Boh, metadati

- `Images/`
  Suppongo contenga le immagini

- `HandwritingIndex/`
  Boh, inutile

## `Session.plist`

```bash
rm -f program.prof noname.svg && time python main.py Lezione\ 1-2\ MMP/Session.plist.xml && snakeviz program.prof
```
