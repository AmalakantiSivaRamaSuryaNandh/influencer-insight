# Sample dataset

`influencers.csv` contains 24 fictional profiles created for learning and testing.
It does not contain live Instagram data and should not be treated as a real-world
endorsement or performance claim.

## Columns

- `username`: fictional public handle
- `display_name`: display label shown in the interface
- `bio`: text searched by the NLP pipeline
- `category`: expected discovery category
- `followers`, `likes`, `comments`, `shares`: non-negative sample metrics

To replace the sample data, keep the same column names and provide at least one
complete row. The application validates the file before using it.
