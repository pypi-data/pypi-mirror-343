# Neural Network calculator

Neural Network calculator reads your hyperparameter choices (kernel size, stride, channels, etc.) and outputs:

- Encoder block: detailed Conv2d specs + parameter counts

- Decoder block: mirrored ConvTranspose2d specs + parameter counts

- Recurrent stacks: per-layer (input_size, hidden_size, params) for RNN/GRU/LSTM

## Features:

- Multi-layer CNN mode

   - Global defaults or per-layer overrides for stride, kernel size, padding

   - Automatic channel-chaining in encoder → mirrored decoder block


- Recurrent mode

   - RNN: single-gate formula

   - GRU: 3× single-gate formula

   - LSTM: 4× single-gate formula

   - Stacked layers automatically chain hidden sizes

- User-friendly CLI with automatic help pages & type-safe options

- Subcommand support, lazy loading, file arguments, and more via Click


## Usage:

### Example


### bash command

```
nn_calc -h
```

### output

```
  Calculate parameter counts for CNN encoder/decoder OR RNN/GRU/LSTM layers.

Options:
  --model [cnn|rnn|gru|lstm]  Type of network to compute parameters for.
                              [default: cnn]
  -n, --num-layers INTEGER    Number of layers (CNN) or RNN layers
                              (recurrent).  [default: 3]
  --stride INTEGER            Default stride for each conv layer.  [default:
                              1]
  --kernel-size INTEGER       Default kernel size for each conv layer.
                              [default: 3]
  --padding INTEGER           Default padding for each conv layer.  [default:
                              1]
  --in-channels INTEGER       CNN: input channels for first layer; RNN: input
                              size.  [default: 3]
  --out-channels INTEGER      CNN: output channels for each layer; RNN: hidden
                              size.  [default: 64]
  -S, --strides INTEGER       CNN: per-layer strides (e.g. -S 1 2 2).
  -K, --kernel-sizes INTEGER  CNN: per-layer kernel sizes.
  -P, --paddings INTEGER      CNN: per-layer paddings.
  -h, --help                  Show this message and exit.

```

## Requirements:

- Python >= 3.7
- click>=8.0

## Installation:

### Pip

```shell
pip install nn_calc
```

### git repository

```
https://github.com/pssv7/nn-calc.git
```

## Usage

```shell
nn_calc (OPTIONAL)
```

