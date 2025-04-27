import json
import matplotlib.pyplot as plt

from .independent import *
from .layers import PosEnc, Block
from ._utils import call_model_jit, loss_fn, time_it, BatchTrain
from .debug import debug_state

rng = jax.random.PRNGKey(0)

class Model(nn.Module):
    num_heads: int
    attention_dim: int
    vocab_size: int
    num_blocks: int
    ff_dim: int
    dropout_rate: float
    dtype: jnp.dtype = jnp.float32


    def setup(self):
        self.emb = nn.Embed(num_embeddings=self.vocab_size,features=self.attention_dim, embedding_init=nn.initializers.normal(stddev=0.02),dtype=self.dtype)
        self.pos_enc = PosEnc(self.attention_dim)
        self.blocks = [Block(num_heads=self.num_heads,attention_dim=self.attention_dim,ff_dim=self.ff_dim,dropout_rate=self.dropout_rate,dtype=self.dtype)for i in range(self.num_blocks)]
    
    def __call__(self,x,mask,training=True):
        mask = self.process_mask(mask)
        x = x.astype(jnp.int32)
        x = self.emb(x)
        x = self.pos_enc(x)
        for i in self.blocks:
            x = i(x,mask,training)
        return x @ self.emb.embedding.T


    def process_mask(self,mask):
        _, seq_len = mask.shape

        # Create causal mask (lower triangular matrix)
        causal_mask = jnp.tril(jnp.ones((seq_len, seq_len)))

        # Reshape padding mask and apply to causal mask
        mask = mask[:, None, :]  # (batch_size, 1, seq_len)
        mask_sq = causal_mask[None, :, :] * mask  # (batch_size, seq_len, seq_len)
        mask_sq = jnp.transpose(mask_sq, (0, 2, 1)) * mask
        mask_sq = jnp.transpose(mask_sq, (0, 2, 1))

        return mask_sq


class ModelManager():
    @debug_state.trace_func
    def __init__(self,num_heads,attention_dim,vocab_size,num_blocks,ff_dim,dropout_rate,dtype = None) -> None:
        self.key = jax.random.PRNGKey(0)
        self.model_struct = Model(num_heads,attention_dim,vocab_size,num_blocks,ff_dim,dropout_rate,dtype)
        self.params = self.model_struct.init(self.key,jax.random.normal(self.key,(2, 11)),jnp.ones((2,11))) 
        if dtype is not None:
            self.params = convert_tree(dtype,self.params)
        
        self.optimizer = None

        self.data = {
            "num_heads":num_heads,
            "attention_dim":attention_dim,
            "vocab_size":vocab_size,
            "num_blocks":num_blocks,
            "ff_dim":ff_dim,
            "dropout_rate":dropout_rate
        }


    def __call__(self,input,mask):
        return self.model_struct.apply(self.params,input,mask,rngs={"dropout": self.key_bruh},training=False)
    
    def jax_call(self,input,mask):
        rngs = rngs={"dropout": self.key}
        return call_model_jit(self.model_struct,self.params,input,mask,rngs)
    

    @property
    def trainable_variables(self):
        return self.params
    
    @property
    def key_bruh(self):
        self.key, subkey = jax.random.split(self.key)
        return subkey
    
    @debug_state.trace_func
    def training_setup(self,optimizer,lr,lrf,batches,epochs,state_path="",opt_state_dtype=None):
        self.optimizer = Optimizer(optimizer,lr,lrf,batches,epochs,self.params)
        self.optimizer.load(state_path,opt_state_dtype)
        self.grad_fn = jax.value_and_grad(loss_fn)
        return self.optimizer.lr_schedule
    
    @debug_state.trace_func
    def train_batch(self,x,mask,y):
        key = self.key_bruh
        (loss, self.params, self.optimizer.state), first_time = time_it(BatchTrain,self.params,self.grad_fn,self.model_struct,x,mask,y,key,self.optimizer.optimizer,self.optimizer.state)
        return loss , [first_time,0,0]
    
    @debug_state.trace_func
    def save_model(self,name,opt_state=True):
        os.makedirs(name, exist_ok=True)
        with open(os.path.join(name, "good_stuff.pkl"), "wb") as f:
            f.write(flax.serialization.to_bytes(self.trainable_variables))

        with open(os.path.join(name, "understanding_good_stuff.json"),"w") as f:
            json.dump(self.data, f, indent=2)
        
        if (opt_state) and (self.optimizer is not None):
            with open(os.path.join(name, "make_stuff_better.pkl"), "wb") as f:
                f.write(flax.serialization.to_bytes(self.optimizer.state))

    @debug_state.trace_func
    def batch_it(self, x, mask, y, batch_size, x_eq_y=True):
        dataset = Flax_ds(x_eq_y)
        dataset.load_data(x,mask,y)
        dataset.batch_it_(batch_size=batch_size)
        return dataset

    @debug_state.trace_func
    def train(self,x,mask,y,epochs,batch_size,optimizer,lr,lrf,val_x=None,val_mask=None,val_y=None,val_step=100,updates_in=1,avg_mem=1500,state_path=None):
        pass # I don't want to expose the training stuff... So... I hope you understand :D
    
    
    @debug_state.trace_func
    def summary(self):
        def count_params(params):
            total = 0
            for value in params.values():
                if isinstance(value, dict):
                    total += count_params(value)
                elif hasattr(value, 'size'):
                    total += value.size
            return total
        
        for i in list(self.trainable_variables['params'].keys()):
            print(f"{i} :{count_params(self.trainable_variables['params'].get(i, {})):,}")
        print("-------------------")
        print(f"Total :{count_params(self.trainable_variables['params']):,}")
    
    @debug_state.trace_func
    def change_precision(self,dtype):
        self.params = jax.tree_util.tree_map(lambda x: x.astype(dtype),self.params)

    @property
    def precision(self):
        type_tree = jax.tree_util.tree_map(lambda x: x.dtype,self.model)
        types = jax.tree_util.tree_leaves(type_tree)
        if len(set(types)) == 1:
            print(f"Model dtype:{types[0]}")
        else:
            print("Model contrains mixed dtypes")



### Test stuff for now ok?
### Bruh your forgot to get the better predict from googel collab ;-;

@debug_state.trace_func
def plot(losses, num_points=100, chop_off=100):
    if chop_off >= len(losses):
        raise ValueError("chop_off is greater than or equal to the length of losses")
    
    smoothed_losses = np.cumsum(losses) / (np.arange(len(losses)) + 1)
    
    interval = max(len(losses) // num_points, 1)
    sampled_losses = smoothed_losses[::interval][chop_off:]
    sampled_batches = np.arange(len(losses))[::interval][chop_off:]

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(sampled_batches, sampled_losses, marker='o', linestyle='-')
    plt.xlabel('Batch')
    plt.ylabel('Loss')
    plt.title('Smoothed Loss over Batches')
    plt.show()