# test is not validate

Two commands, both look like they check your job before you run it. They check different things, and — this is the part that catches people — neither one ever opens a network connection.

In this lab you will scaffold a MySQL job with no `.env` file (so no credentials configured at all), run `hdrctl test`, then `hdrctl validate`, and watch both report success. Then you will run `hdrctl run` — the only command in the whole lab that actually tries to use those credentials.

Hydra ETL installs in the background while you read this.
