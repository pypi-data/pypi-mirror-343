use_wandb=False
local_mode=True
trust_remote_code_SentenceTransformer=False



# import os
# WandbToken=os.getenv('WandbToken')
# HFToken=os.getenv('HFToken')
# GitHubToken=os.getenv('GitHubToken')



WandbToken=''
HFToken=''
GitHubToken=''


def SetTokens(t_wandb,t_hf, t_github):
    global WandbToken
    global HFToken
    global GitHubToken
    WandbToken=t_wandb
    HFToken=t_hf
    GitHubToken=t_github