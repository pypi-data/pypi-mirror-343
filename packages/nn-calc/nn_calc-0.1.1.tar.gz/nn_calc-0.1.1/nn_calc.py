import click
from typing import List, Dict


def calculate_conv_params(kernel: int, in_ch: int, out_ch: int) -> int:
    """(kernel² × in_ch × out_ch) + out_ch (bias)."""
    return kernel * kernel * in_ch * out_ch + out_ch


def calculate_rnn_params(input_size: int, hidden_size: int) -> int:
    """RNN: input→hidden + hidden→hidden + bias."""
    return input_size * hidden_size + hidden_size * hidden_size + hidden_size


def calculate_gru_params(input_size: int, hidden_size: int) -> int:
    """GRU: 3 gates each with RNN params."""
    base = calculate_rnn_params(input_size, hidden_size)
    return 3 * base


def calculate_lstm_params(input_size: int, hidden_size: int) -> int:
    """LSTM: 4 gates each with RNN params."""
    base = calculate_rnn_params(input_size, hidden_size)
    return 4 * base


def extend_list(vals: List[int], length: int, default: int) -> List[int]:
    if not vals:
        return [default] * length
    if len(vals) < length:
        vals = vals + [vals[-1]] * (length - len(vals))
    return vals[:length]


def build_encoder(
    in_chs: List[int],
    out_chs: List[int],
    kernels: List[int],
    strides: List[int],
    pads: List[int],
) -> List[Dict]:
    return [
        {
            "layer": i + 1,
            "type": "Conv2d",
            "in_channels": in_chs[i],
            "out_channels": out_chs[i],
            "kernel_size": kernels[i],
            "stride": strides[i],
            "padding": pads[i],
            "params": calculate_conv_params(kernels[i], in_chs[i], out_chs[i]),
        }
        for i in range(len(in_chs))
    ]


def build_decoder(
    in_chs: List[int],
    out_chs: List[int],
    kernels: List[int],
    strides: List[int],
    pads: List[int],
) -> List[Dict]:
    rev_ins = out_chs[::-1]
    rev_outs = in_chs[::-1]
    rev_k = kernels[::-1]
    rev_s = strides[::-1]
    rev_p = pads[::-1]
    return [
        {
            "layer": i + 1,
            "type": "ConvTranspose2d",
            "in_channels": rev_ins[i],
            "out_channels": rev_outs[i],
            "kernel_size": rev_k[i],
            "stride": rev_s[i],
            "padding": rev_p[i],
            "params": calculate_conv_params(rev_k[i], rev_ins[i], rev_outs[i]),
        }
        for i in range(len(rev_ins))
    ]


def print_block(block: List[Dict], name: str) -> None:
    click.echo(f"\n{name}:")
    for L in block:
        click.echo(
            f"  Layer {L['layer']} ─ {L['type']} "
            f"(in={L['in_channels']}, out={L['out_channels']}, "
            f"k={L['kernel_size']}, s={L['stride']}, p={L['padding']}) "
            f"→ {L['params']} params"
        )


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--model",
    type=click.Choice(["cnn", "rnn", "gru", "lstm"], case_sensitive=False),
    default="cnn",
    show_default=True,
    help="Type of network to compute parameters for.",
)
@click.option("-n", "--num-layers", type=int, default=3, show_default=True,
              help="Number of layers (CNN) or RNN layers (recurrent).")
@click.option("--stride", type=int, default=1, show_default=True,
              help="Default stride for each conv layer.")
@click.option("--kernel-size", type=int, default=3, show_default=True,
              help="Default kernel size for each conv layer.")
@click.option("--padding", type=int, default=1, show_default=True,
              help="Default padding for each conv layer.")
@click.option("--in-channels", type=int, default=3, show_default=True,
              help="CNN: input channels for first layer; RNN: input size.")
@click.option("--out-channels", type=int, default=64, show_default=True,
              help="CNN: output channels for each layer; RNN: hidden size.")
@click.option("-S", "--strides", type=int, multiple=True,
              help="CNN: per-layer strides (e.g. -S 1 2 2).")
@click.option("-K", "--kernel-sizes", type=int, multiple=True,
              help="CNN: per-layer kernel sizes.")
@click.option("-P", "--paddings", type=int, multiple=True,
              help="CNN: per-layer paddings.")
def main(
    model, num_layers, stride, kernel_size, padding,
    in_channels, out_channels, strides, kernel_sizes, paddings
):
    """
    Calculate parameter counts for CNN encoder/decoder OR RNN/GRU/LSTM layers.
    """
    if model.lower() == "cnn":
        S = extend_list(list(strides), num_layers, stride)
        K = extend_list(list(kernel_sizes), num_layers, kernel_size)
        P = extend_list(list(paddings), num_layers, padding)
        # encoder channels
        EC_out = extend_list([], num_layers, out_channels)
        EC_in = [in_channels] + EC_out[:-1]
        enc = build_encoder(EC_in, EC_out, K, S, P)
        dec = build_decoder(EC_in, EC_out, K, S, P)
        print_block(enc, "Encoder Configuration")
        print_block(dec, "Decoder Configuration")
    else:
        # recurrent
        results = []
        for i in range(1, num_layers + 1):
            if model.lower() == "rnn":
                params = calculate_rnn_params(in_channels, out_channels)
                typename = "RNN"
            elif model.lower() == "gru":
                params = calculate_gru_params(in_channels, out_channels)
                typename = "GRU"
            else:  # lstm
                params = calculate_lstm_params(in_channels, out_channels)
                typename = "LSTM"
            results.append((i, typename, in_channels, out_channels, params))
            # for stacked layers, next input = hidden
            in_channels = out_channels
        click.echo(f"\n{typename} stack ({num_layers} layers):")
        for layer_idx, tname, inp, hid, p in results:
            click.echo(
                f"  Layer {layer_idx} ─ {tname} "
                f"(input_size={inp}, hidden_size={hid}) → {p} params"
            )


if __name__ == "__main__":
    main()
