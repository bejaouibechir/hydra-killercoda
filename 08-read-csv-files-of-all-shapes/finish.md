# Same data, different CSV formats

You read the same rows from three files and verified identical output data.

| Input | Source settings |
| --- | --- |
| Comma, UTF-8 | `connection: {}` |
| Semicolon, UTF-8 | `delimiter: ";"` |
| Semicolon, Latin-1 | `delimiter: ";"` and `encoding: latin-1` |

A wrong separator may produce a successful job with incorrect columns. A wrong encoding can cause a decoding error; some other encoding mismatches can instead produce garbled text. Check both the column structure and the values.

All three destinations write comma-separated UTF-8. No transformation is needed to change the input separator or encoding.

Corrected source manifests are available in `/root/lab/csv-shapes/solutions/`.
