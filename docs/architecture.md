# Initial pipeline architecture

Status: initial Version 1 design with Day 5 implementation updates. Data
preparation, searches, timing, benchmark output, and the interactive menu are
implemented. `main.py` routes menu sessions to `src/cli.py` and full benchmark
runs to `src/benchmark.py`. Final written analysis remains planned.
The PNG shows the full target architecture.

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

Interactive searches branch directly from measured results to terminal display;
they do not export CSVs. `--benchmark` follows the full CSV/metadata export branch.
Each menu search reloads the selected CSV, so file corrections are visible on
the next attempt. Input errors re-prompt; file/data errors return to the menu.

## Module responsibilities

| Module | Input | Output / responsibility | Day |
| --- | --- | --- | --- |
| `main.py` | Action/generation flags and benchmark timing settings | Default interactive search; explicit preview/generation/benchmark routing | 5 delivered |
| `src/cli.py` | Dataset-size option, integer target, search mode | Load/prepare/time selected searches, display measured records, recover input/file errors, handle quit/EOF/Ctrl+C | 5 delivered |
| `src/data_generator.py` | Size and documented generation settings | Integer data and required stored CSV datasets | 2 delivered |
| `src/data_loader.py` | CSV path and optional expected size | Validated integer list or a clear loading failure | 2 delivered |
| `src/data_processor.py` | Loaded list and optional expected size | Validated original-order list and independently sorted copy | 2 delivered |
| `src/linear_search.py` | Original-order list and target | First matching index or `-1` | 3 delivered |
| `src/binary_search.py` | Ascending sorted list and target | Any matching index or `-1` | 3 delivered |
| `src/performance_timer.py` | Search function, prepared input, target, repetition settings | Index, median seconds/search, and per-batch samples | 4 delivered |
| `src/results_manager.py` | Validated benchmark records | Exact CSV schema in `results/` | 4 delivered |
| `src/benchmark.py` | Dataset/output directories and timing settings | Both algorithms, four cases per size, separate sort measurements, CSV and metadata export | 4 delivered |

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
  datasets at the pipeline boundary: both searches return `-1` for empty input.
- Validation and sorting stay outside the search functions. The pipeline
  integration test passes the original-order list to linear search and the
  sorted copy to binary search for all three required sizes. Binary search
  does not detect unsorted input at runtime; sorted order is a precondition.
- Linear search returns the first duplicate; binary search may return any
  matching duplicate. Neither function modifies its input.
- Storage and terminal output stay outside the search functions and timed
  region. Use project-relative locations rather than machine-specific paths.
- CSV records have `algorithm,dataset_size,target,found,index,execution_time`.
  The time unit is seconds per search, summarized as the median batch mean.
  A metadata sidecar maps each record to its case and samples; sorting times
  are stored separately. See [benchmark methodology](benchmark_methodology.md).
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
