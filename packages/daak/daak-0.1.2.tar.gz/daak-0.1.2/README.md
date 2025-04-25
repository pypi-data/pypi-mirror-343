# daak

In the Tausug language, daak means to command or order.  daak is a small pure python library that can execute a 
subprocess and grab the stdout and stderr asynchronously.

It has limited support for handling input, mostly for when a sudo password is expected.

## Installation

Through pip

```bash
pip install daak
```

## Usage

The main class to use is called `Run`

```python
import asyncio

from daak.process import Run

def which(prog: str):
    return Run("which", args=[prog]).run(throw=False) 

async def main():
    _, process = await which("poetry")
    print(process.returncode)

if __name__ == "__main__":
    with asyncio.Runner() as runner:
        runner.run(main())
```