from .common_imports import *

class PosEnc(nn.Module):
    dim : int
    dtype: jnp.dtype = jnp.bfloat16

    @nn.compact
    def __call__(self, x):
        batch_size, sequence_length, _ = x.shape  

        # Compute div term once (avoiding repeated `exp` calls)
        div_term = jnp.exp(-jnp.arange(0, self.dim, 2) * (jnp.log(10000.0) / self.dim)).astype(self.dtype)

        # Compute positions in one step (efficiently broadcasting)
        position = jnp.arange(sequence_length)[:, None] * div_term  # (seq_len, emb_dim/2)

        # Directly compute sine & cosine, then interleave them
        pos_enc = jnp.zeros((sequence_length, self.dim),dtype=self.dtype)
        pos_enc = pos_enc.at[:, 0::2].set(jnp.sin(position)).astype(self.dtype)
        pos_enc = pos_enc.at[:, 1::2].set(jnp.cos(position)).astype(self.dtype)

        # Expand for batch & return
        return x + pos_enc[None, :, :]

class Attention(nn.Module):
    num_heads: int
    d_model: int
    dtype: jnp.dtype = jnp.bfloat16

    def setup(self):
        assert self.d_model % self.num_heads == 0, "d_model must be divisible by num_heads"
        self.depth = self.d_model // self.num_heads
        self.qkv_dense = nn.Dense(features=3 * self.d_model, kernel_init=nn.initializers.normal(stddev=0.02),dtype=self.dtype)
        self.out_dense = nn.Dense(features=self.d_model, kernel_init=nn.initializers.normal(stddev=0.02),dtype=self.dtype)

    def __call__(self, x, mask):
        batch_size, seq_len, _ = x.shape
        qkv = self.qkv_dense(x)  # (batch, seq_len, 3 * d_model)
        qkv = qkv.reshape(batch_size, seq_len, 3, self.num_heads, self.depth)
        qkv = jnp.transpose(qkv, (2, 0, 3, 1, 4))  # (3, batch, num_heads, seq_len, depth)
        Q, K, V = qkv  # Unpacking (batch, num_heads, seq_len, depth)

        # Scaled Dot-Product Attention
        logits = jnp.einsum("bhqd,bhkd->bhqk", Q, K) / jnp.sqrt(self.depth)

        if mask is not None:
            mask = mask[:, None, :]  # Expand for broadcasting (batch, 1, seq_len, seq_len)
            logits = jnp.where(mask, logits, -1e9)

        attn_weights = jax.nn.softmax(logits, axis=-1)
        attn_output = jnp.einsum("bhqk,bhkd->bhqd", attn_weights, V)

        # Concatenate heads
        attn_output = jnp.transpose(attn_output, (0, 2, 1, 3))  # (batch, seq_len, num_heads, depth)
        concat_output = attn_output.reshape(batch_size, seq_len, self.d_model)  # (batch, seq_len, d_model)

        return self.out_dense(concat_output)


class Block(nn.Module):
    num_heads : int
    attention_dim : int
    ff_dim : int
    dropout_rate : float
    dtype: jnp.dtype = jnp.bfloat16

    @nn.compact
    def __call__(self, x_inp, mask, train: bool):
        x = nn.LayerNorm(dtype=self.dtype)(x_inp)  
        x = Attention(self.num_heads, self.attention_dim,dtype=self.dtype)(x, mask)
        x = nn.Dropout(self.dropout_rate)(x, deterministic=not train)
        x_inp = x + x_inp

        # Pre-LN before FFN
        x = nn.LayerNorm(dtype=self.dtype)(x_inp)  
        x = nn.Dense(self.ff_dim, kernel_init=nn.initializers.normal(stddev=0.02),dtype=self.dtype)(x)
        x = nn.gelu(x)
        x = nn.Dense(self.attention_dim, kernel_init=nn.initializers.normal(stddev=0.02),dtype=self.dtype)(x)
        return x + x_inp