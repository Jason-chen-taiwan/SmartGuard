# SmartGuard

SmartGuard is a comprehensive smart contract analysis tool that integrates multiple security analysis tools to help developers identify vulnerabilities and potential issues in their Solidity smart contracts.

## Features

- Multiple Analysis Tools Support:

  - Slither: Static analysis framework
  - Static Analysis: Custom AST-based analysis
  - Echidna: Fuzzing/property-based testing
  - Securify2: Security scanner
  - ConFuzzius: Fuzzing tool
  - Etainter: Taint analysis
  - Mythril: Security analysis tool

- Flexible Version Support:

  - Supports Solidity versions from 0.4.25 to 0.8.25
  - Automatic version compatibility checking

- User-Friendly Interface:
  - Web-based interface
  - Easy file upload
  - Configurable analysis parameters
  - Downloadable reports in Markdown format

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/SmartGuard.git
cd SmartGuard
```

2. Run the installation script:

```bash
chmod +x install.sh
./install.sh
```

This will install all required dependencies including:

- Docker and required containers
- Rust and Cargo
- Python dependencies

## Requirements

- Ubuntu/Linux environment
- Docker
- Python 3.x
- Web browser

## Usage

1. Start the application:

```bash
python src/__main__.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Select your analysis options:

   - Upload your Solidity contract file
   - Choose the Solidity version
   - Select the analysis tool
   - Configure tool-specific parameters
   - Run the analysis

4. View and download the analysis results

## Tool-Specific Parameters

### Slither

- Compilation options
- Detection configurations
- Output formatting options

### Echidna

- Test mode selection
- Timeout settings
- Test limits configuration

### Securify2

- Pattern selection
- Severity filters
- Blockchain integration

### ConFuzzius

- Algorithm parameters
- Environmental settings
- Data dependency options

### Etainter

- Taint analysis configuration
- Memory limits
- Analysis type selection

### Mythril

- Analysis modes
- Transaction depth
- Solver timeout

## License

[Add your license information here]

## Contributors

[Add contributor information here]

## Acknowledgments

This project integrates several open-source security analysis tools:

- [Slither](https://github.com/crytic/slither)
- [Echidna](https://github.com/crytic/echidna)
- [Securify2](https://github.com/eth-sri/securify2)
- [ConFuzzius](https://github.com/christoftorres/ConFuzzius)
- [Etainter](https://github.com/eth-sri/etainter)
- [Mythril](https://github.com/ConsenSys/mythril)
