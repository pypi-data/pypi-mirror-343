import jax
import flax
import jax.numpy as jnp
import numpy as np
import optax
import flax.serialization
import flax.linen as nn
import time
import os
import json
from huggingface_hub import hf_hub_download
from functools import partial

def get_first(pytree):
    return jax.tree_util.tree_map(lambda x: x[0], pytree)

def convert_tree(dtype,pytree):
    return jax.tree_util.tree_map(lambda x: x.astype(dtype),pytree)