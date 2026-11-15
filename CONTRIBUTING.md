# Contributing

Thank you for helping the library grow. Everything here is released under **CC0** (see
[LICENSE](LICENSE)); by contributing you agree to release your contribution the same way.

## A new definition, or a fix

1. **Start from the closest existing definition**, or from *New* in Signal Visor's Protocol
   workspace, which fills in a valid skeleton and validates as you type. Name the folder and the
   file after the `id`: `remotes/<id>/<id>.json` or `sensors/<id>/<id>.json`.
2. **`status: draft`.** A definition becomes `verified` only once a real capture proves it in the
   application's test suite; say in the pull request what you checked it against.
3. **`description` describes the protocol** — modulation, coding, what each pulse length means,
   why a flag such as `invert` is needed. Not how you found it, and no file names or paths.
4. **Check it:**

   ```
   pip install jsonschema==4.23.0
   python tools/validate.py
   ```

5. **Open a pull request** with: where the timing came from (a datasheet, your own measurement,
   another project), the device it was checked on, and — if you can share one under CC0 — a sample
   capture in `<group>/<id>/samples/`.

A fix to an existing definition is welcome the same way. Keep the `id`: that is what lets a
corrected file replace the shipped one in everybody's own folder.

## Rules for samples

| Rule | Reason |
|---|---|
| Your own devices only, released under CC0 | Keeps the library's licensing uniform |
| No rolling-code captures from cars, alarms or garage systems | Such a collection does not belong in a public repository |
| No readings from other people's meters | Water, gas and heat consumption is personal data |
| Nothing that identifies a household | A device serial number is fine; a file named after an address is not |

Rolling-code protocols (KeeLoq, Somfy RTS) may be described — recognition and the frame layout
only. Nothing here decrypts them, and contributions that would help to are not accepted.

## Data only

A definition contains no scripts and no expressions. Anything the format cannot express needs a
new primitive in the application and a higher `schema` number — open an issue describing the
protocol rather than working around it inside a definition.
