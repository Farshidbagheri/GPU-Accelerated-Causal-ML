"""Bounded CPU smoke test of original VTDNet architecture (NOT its paper metrics).

Check out author's source separately. The only runtime source edit replaces
hard-coded .cuda() with .to(x.device) to make the forward/loss pass possible on
CPU. Third-party source is not vendored. wandb is stubbed because no logging
is performed in this smoke test. No causal effect is evaluated.
"""
import argparse, json, sys, types
from pathlib import Path
import numpy as np
import torch

def check(upstream:Path)->dict:
    torch.set_num_threads(2)
    torch.manual_seed(2026)
    source=(upstream/"VTD_modules.py").read_text(encoding="utf8")
    source=source.replace(".cuda()",".to(x.device)")
    stub=types.ModuleType("wandb")
    stub.log=lambda *args,**kwargs:None
    sys.modules["wandb"]=stub
    sys.path.insert(0,str(upstream))
    module=types.ModuleType("vtd_cpu_smoke")
    exec(compile(source,str(upstream/"VTD_modules.py"),"exec"),module.__dict__)
    model=module.VTD(30,32,32,1,3,4,6).to("cpu")
    b,t=4,6
    x=torch.randn(b,t,30);delta=torch.ones(b,t,1)
    treatments=torch.randint(0,2,(b,t,3)).float()
    active=torch.full((b,),t,dtype=torch.long)
    model.train()
    outputs=model(x,delta,treatments,active)
    assert tuple(outputs[0].shape)==(b,t,30)
    assert tuple(outputs[3].shape)==(b,t,3)
    assert tuple(outputs[4].shape)==(b,t,1)
    loss_and_parts=module.loss_function(x,outputs[0],outputs[1],outputs[2],
                  treatments,outputs[3],torch.randn(b,t,1),outputs[4],active,1.)
    loss=loss_and_parts[0]
    assert torch.isfinite(loss).item()
    loss.backward()
    num_grads=sum(int(p.grad is not None and bool(torch.isfinite(p.grad).all()))
                  for p in model.parameters())
    assert num_grads>0
    # Verify whether author's attention mixes patients in the batch (same
    # target patient with vs without a second patient).
    model.eval()
    z=torch.randn(t,2,32); a=torch.rand(t,2,3)
    full,_=model.attention(z,a)
    solo,_=model.attention(z[:,:1,:],a[:,:1,:])
    batch_effect=float((full[:,:1,:]-solo).abs().max())
    return {
      "upstream":"Throwfox/VTDNet",
      "pinned_commit":"3770f32e0479dab16a97fc11849dfaa1fc717153",
      "source_edited_only_for_CPU_device_placement":True,
      "torch_runtime":torch.__version__,
      "synthetic_random_input_shape":list(x.shape),
      "architecture":"VTDNet reduced-size (hidden=32, latent=32, sequence=6); original model classes",
      "forward_pass_success":True,
      "backpropagation_success":True,
      "loss_is_finite":True,
      "gradient_parameter_tensors":num_grads,
      "batch_member_dependency_max_abs_output_change":round(batch_effect,7),
      "batch_dependency_interpretation":"Attention computes softmax over the batch axis; review batch-composition sensitivity before clinical inference.",
      "synthetic_generator_reproduced":False,
      "original_training_pipeline_reproduced":False,
      "ITE_PEHE_reproduced":False,
      "paper_results_reproduced":False,
      "gpu_used":False,
      "warnings":[
         "Only an architecture forward/backward compatibility test, no fitted causal model.",
         "Native training/evaluation scripts have mismatched data schema, signatures and mandatory CUDA calls.",
         "Hidden-confounder identification is not established by this test."
      ]
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--upstream",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    result=check(args.upstream)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":main()
