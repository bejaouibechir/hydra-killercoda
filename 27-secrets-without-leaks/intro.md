# Secrets without leaks

A small PostgreSQL database is available inside this lab. Its password is generated at setup and placed in a private project file. You will run the same job using three secret sources:

1. The ignored project file .hydra/secrets.
2. An environment variable named DB_PASSWORD.
3. A file outside the project selected by --secrets-file.

The job writes a two-row CSV snapshot. You will inspect git status at each stage. The helper checks only this lab's files and local database output. Wait for Ready before pressing Check.
