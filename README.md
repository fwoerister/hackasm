# Hackasm - HACK Assembly to Machine Code Converter

## Introduction

`hackasm` is an assembler that translates HACK assembly source files into HACK machine language. The HACK architecture
is a simplified computer model designed by Noam Nisan and Shimon Schocken, as described in their book _The Elements of
Computing Systems_. This architecture is intended to provide a clear and concise understanding of how computers
function, making it an excellent learning tool.

## Features

- Converts HACK assembly (.asm) files to HACK machine code (.hack) files.
- Designed to work with assembly code for the HACK computer, as per _The Elements of Computing Systems_ curriculum.
- Easy to use with a simple command-line interface.

## Requirements

- A valid HACK assembly file with an `.asm` extension.

## Installation

You can install `hackasm` by using the python package manager pip.

```shell
python3 -m venv .venv
. .venv/bin/activate
pip install --editable .
```

## Usage

To assemble a HACK assembly file into machine code, run the `hackasm` script with the `.asm` file as the argument:

```shell
$ hackasm Add.asm
```

## Contact

Florian Wörister | florian _[dot]_ woerister _[at]_ univie _[dot]_ ac _[dot]_ at