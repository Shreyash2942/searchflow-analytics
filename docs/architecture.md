# Initial pipeline architecture

Status: initial Version 1 design with Day 2 implementation updates. Dataset
generation, loading, validation, and preparation are implemented. `main.py`
runs those stages; search, timing, result collection, and the interactive
search menu remain planned. The PNG shows the full target architecture.

![Planned pipeline](../diagrams/pipeline_architecture.png)

## Data flow

```text
CLI selections: dataset size, target, algorithm(s)
                      |
Generate integers -> Save CSV (or use an existing dataset)
                      |
                  Load CSV
                      |
      Validate integers, nonempty data, expected count
                      |
              Prepare search inputs
                /             \
       Original order      Sorted copy
              |                |
       Timed linear       Timed binary
          search             search
                \             /
           Collect search results and timings
                      |
         Save results/performance_results.csv
                  /          \
           CLI display    Written analysis
```

The CLI orchestrates the pipeline and displays results; it is not a data
preprocessing stage. Timing wraps each search call. It does not start after
search completes, and it excludes data generation/loading, sorting, display,
and CSV writes. Analyze sorting cost separately when discussing one-time
versus repeated searches.

## Module responsibilities

| Module | Input | Output / responsibility | Day |
| --- | --- | --- | --- |
| `main.py` | `--generate` flag now; user search selections later | Load/validate/preview datasets, optionally regenerate them, handle data/file errors; search menu planned | 2 delivered; 5 planned |
| `src/data_generator.py` | Size and documented generation settings | Integer data and required stored CSV datasets | 2 delivered |
| `src/data_loader.py` | CSV path and optional expected size | Validated integer list or a clear loading failure | 2 delivered |
| `src/data_processor.py` | Loaded list and optional expected size | Validated original-order list and independently sorted copy | 2 delivered |
| `src/linear_search.py` | Original-order list and target | Matching index or `-1` | 3 |
| `src/binary_search.py` | Sorted list and target | Matching index or `-1` | 3 |
| `src/performance_timer.py` | Search function, input, target, repetition settings | Search result and measured time | 4 |
| `src/results_manager.py` | Benchmark records | CSV headers and rows in `results/` | 4 |

## Contracts and boundaries

- Required dataset sizes are 100, 1,000, and 10,000. The loader and processor
  must prevent invalid or empty data from reaching the interactive search flow.
- The binary-search branch receives a sorted copy. Sorting must not mutate
  the original list used by linear search.
- Both algorithms return an index or `-1`. Found status derives from that
  return value. Index zero is a successful match, not a false result.
- An index belongs to the particular input list. Linear and binary search
  can find the same value at different indexes because their list order differs.
- Algorithm-level empty-list behavior is distinct from rejecting empty CSV
  datasets at the pipeline boundary.
- Storage and terminal output stay outside the search functions and timed
  region. Use project-relative locations rather than machine-specific paths.
- CSV records have `algorithm,dataset_size,target,found,index,execution_time`.
  Benchmark settings and units must be documented when Day 4 is implemented.
- Tests belong in `tests/`. Use standard-library `unittest` so application
  setup does not require a separate test framework.

## Diagram maintenance

The checked-in PNG is a design artifact; users do not need graphics packages
to run the application. `diagrams/render_architecture.py` is the editable
diagram source. To regenerate it, optionally install Pillow in a development
environment, then run the script from the repository root:

```powershell
.\.venv\Scripts\python.exe -m pip install Pillow
.\.venv\Scripts\python.exe diagrams/render_architecture.py
```

This optional documentation tool is separate from runtime requirements.
