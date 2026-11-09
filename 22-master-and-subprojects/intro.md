# Master and sub-projects

A master workflow calls **CRM in dev** and **billing in prod**. Each child publishes `last_batch`; the master reads both values. Then you deliberately create a project-call cycle and watch validation reject it.

The lesson uses local files only. Allow setup to display **Ready** before starting. No Docker or database is needed.
