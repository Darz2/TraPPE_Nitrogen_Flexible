# TraPPE Nitrogen (flexible)

Force-field files and simulation inputs for a **flexible TraPPE model of nitrogen (N2)**, for both Monte Carlo and molecular dynamics.

Most TraPPE nitrogen implementations treat the molecule as rigid. This repository provides the flexible variant together with ready-to-run input decks, so the bond-stretching contribution can be included in thermodynamic and transport property calculations.

## Contents

- `MC/` — Monte Carlo input files (force-field definitions and simulation settings)
- `MD/` — molecular dynamics input files and run scripts

## Usage

Copy the relevant force-field files into your simulation working directory and adjust the state points (temperature, pressure, number of molecules) in the input file. The run scripts assume a SLURM cluster; edit the job headers for your own machine.

## License

MIT — see [LICENSE](LICENSE).
