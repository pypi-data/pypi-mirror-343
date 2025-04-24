# pycatchrs

pycatchrs is a "clone" of the original [catch22 features](https://github.com/DynamicsAndNeuralSystems/catch22), providing an updated implementation with enhanced memory safety and significant improvements in computation speed. It uses a Rust backend for efficient and safe execution.

This implementation has been rigorously tested by computing all the features on all the time series across the entire UCR Archive (128 datasets), yielding the same results as the original catch22.

## Installation

### Prerequisites

-   Python 3.10 or later

### From Source

To install pycatchrs from source, follow these steps:
```bash
    $ git clone https://github.com/albertoazzari/pycatch/
    $ cd pycatch
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install maturin
    $ maturin develop --release
```
