"""Test configurations for `backpack.core.extensions.secondorder`
that is shared among the following secondorder methods:
- Diagonal of Gauss Newton
- Diagonal of Hessian
- MC Approximation of Diagonal of Gauss Newton


Required entries:
    "module_fn" (callable): Contains a model constructed from `torch.nn` layers
    "input_fn" (callable): Used for specifying input function
    "target_fn" (callable): Fetches the groundtruth/target classes 
                            of regression/classification task
    "loss_function_fn" (callable): Loss function used in the model

Optional entries:
    "device" [list(torch.device)]: List of devices to run the test on.
    "id_prefix" (str): Prefix to be included in the test name.
    "seed" (int): seed for the random number for torch.rand
"""


import torch
from test.core.derivatives.utils import classification_targets, regression_targets

from torch.nn import (
    ReLU,
    Sigmoid,
    Tanh,
    LogSigmoid,
    LeakyReLU,
    Conv1d,
    Conv2d,
    Conv3d,
    ConvTranspose1d,
    ConvTranspose2d,
    ConvTranspose3d,
)

from test.extensions.automated_settings import (
    make_simple_act_setting,
    make_simple_cnn_setting,
)


SECONDORDER_SETTINGS = []

###############################################################################
#                                   examples                                  #
###############################################################################

example = {
    "input_fn": lambda: torch.rand(3, 10),
    "module_fn": lambda: torch.nn.Sequential(torch.nn.Linear(10, 5)),
    "loss_function_fn": lambda: torch.nn.CrossEntropyLoss(),
    "target_fn": lambda: classification_targets((3,), 5),
    "device": [torch.device("cpu")],
    "seed": 0,
    "id_prefix": "example",
}
SECONDORDER_SETTINGS.append(example)


SECONDORDER_SETTINGS += [
    # classification
    {
        "input_fn": lambda: torch.rand(3, 10),
        "module_fn": lambda: torch.nn.Sequential(
            torch.nn.Linear(10, 7), torch.nn.Linear(7, 5)
        ),
        "loss_function_fn": lambda: torch.nn.CrossEntropyLoss(reduction="mean"),
        "target_fn": lambda: classification_targets((3,), 5),
    },
    {
        "input_fn": lambda: torch.rand(3, 10),
        "module_fn": lambda: torch.nn.Sequential(
            torch.nn.Linear(10, 7), torch.nn.ReLU(), torch.nn.Linear(7, 5)
        ),
        "loss_function_fn": lambda: torch.nn.CrossEntropyLoss(reduction="sum"),
        "target_fn": lambda: classification_targets((3,), 5),
    },
    # Regression
    {
        "input_fn": lambda: torch.rand(3, 10),
        "module_fn": lambda: torch.nn.Sequential(
            torch.nn.Linear(10, 7), torch.nn.Sigmoid(), torch.nn.Linear(7, 5)
        ),
        "loss_function_fn": lambda: torch.nn.MSELoss(reduction="mean"),
        "target_fn": lambda: regression_targets((3, 5)),
    },
]

###############################################################################
#                         test setting: Activation Layers                     #
###############################################################################
activations = [ReLU, Sigmoid, Tanh, LeakyReLU, LogSigmoid]

for act in activations:
    for bias in [True, False]:
        SECONDORDER_SETTINGS.append(make_simple_act_setting(act, bias=bias))

###############################################################################
#                         test setting: Convolutional Layers                  #
"""
Syntax with default parameters: 
 - `torch.nn.ConvNd(in_channels, out_channels, 
    kernel_size, stride=1, padding=0, dilation=1, 
    groups=1, bias=True, padding_mode='zeros)`    

 - `torch.nn.ConvTransposeNd(in_channels, out_channels, 
    kernel_size, stride=1, padding=0, output_padding=0, 
    groups=1, bias=True, dilation=1, padding_mode='zeros)`

Note: There are 5 tests added to each `torch.nn.layers`. 
For `torch.nn.ConvTranspose2d` and `torch.nn.ConvTranspose3d`
only 3 tests are added because they are very memory intensive. 
"""
###############################################################################

SECONDORDER_SETTINGS += [
    # Conv1d
    make_simple_cnn_setting((3, 3, 7), Conv1d, (3, 2, 2)),
    # test dilation & stride
    make_simple_cnn_setting((3, 2, 7), Conv1d, (2, 3, 2, 2, 0, 2)),
    # test stride & padding
    make_simple_cnn_setting((3, 3, 7), Conv1d, (3, 2, 2, 2, 1)),
    # test stride & padding & dilation
    make_simple_cnn_setting((3, 3, 8), Conv1d, (3, 6, 2, 4, 2, 3)),
    # test bias
    make_simple_cnn_setting((3, 3, 7), Conv1d, (3, 2, 2, 4, 2, 1, 1, False)),
    # Conv2d
    make_simple_cnn_setting((3, 3, 7, 7), Conv2d, (3, 2, 2)),
    make_simple_cnn_setting((3, 2, 7, 7), Conv2d, (2, 3, 2, 2, 0, 2)),
    make_simple_cnn_setting((3, 3, 7, 7), Conv2d, (3, 2, 2, 2, 1)),
    make_simple_cnn_setting((3, 3, 8, 8), Conv2d, (3, 6, 2, 4, 2, 3)),
    make_simple_cnn_setting((3, 3, 7, 7), Conv2d, (3, 2, 2, 4, 2, 1, 1, False)),
    # Conv3d
    make_simple_cnn_setting((3, 3, 2, 7, 7), Conv3d, (3, 2, 2)),
    make_simple_cnn_setting((3, 2, 3, 7, 7), Conv3d, (2, 3, 2, 2, 0, 2)),
    make_simple_cnn_setting((3, 3, 2, 7, 7), Conv3d, (3, 2, 2, 3, 2)),
    make_simple_cnn_setting((3, 3, 4, 8, 8), Conv3d, (3, 6, 2, 4, 2, 3)),
    make_simple_cnn_setting((3, 3, 2, 7, 7), Conv3d, (3, 2, 2, 4, 2, 1, 1, False)),
    # ConvTranspose1d
    make_simple_cnn_setting((3, 3, 7), ConvTranspose1d, (3, 2, 2)),
    # test dilation & stride
    make_simple_cnn_setting((3, 2, 7), ConvTranspose1d, (2, 3, 2, 2, 0, 0, 1, True, 2)),
    # test stride & padding
    make_simple_cnn_setting((3, 3, 7), ConvTranspose1d, (3, 2, 2, 2, 1)),
    # test stride & padding & dilation
    make_simple_cnn_setting((3, 3, 8), ConvTranspose1d, (3, 6, 2, 4, 2, 0, 1, True, 3)),
    # test bias
    make_simple_cnn_setting((3, 3, 7), ConvTranspose1d, (3, 2, 2, 4, 2, 0, 1, False)),
    # ConvTranspose2d
    make_simple_cnn_setting((3, 3, 7, 7), ConvTranspose2d, (3, 2, 2)),
    make_simple_cnn_setting(
        (3, 2, 9, 9), ConvTranspose2d, (2, 4, 2, 1, 0, 0, 1, True, 2)
    ),
    make_simple_cnn_setting((3, 3, 7, 7), ConvTranspose2d, (3, 2, 2, 2, 1)),
    make_simple_cnn_setting(
        (3, 3, 7, 7), ConvTranspose2d, (3, 2, 2, 4, 2, 0, 1, False)
    ),
    # ConvTranspose3d
    make_simple_cnn_setting((3, 3, 2, 7, 7), ConvTranspose3d, (3, 2, 2)),
    make_simple_cnn_setting(
        (3, 2, 3, 5, 5), ConvTranspose3d, (2, 3, 2, 2, 2, 0, 1, True, 2)
    ),
    make_simple_cnn_setting(
        (3, 3, 2, 7, 7), ConvTranspose3d, (3, 2, 2, 4, 2, 0, 1, False)
    ),
]