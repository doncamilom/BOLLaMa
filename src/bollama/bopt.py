import ast
import numpy as np
from additive_bo.data_init_selection.clustering import BOInitDataSelection
from additive_bo.bo.module import BoModule
from additive_bo.data.module import BOAdditivesDataModule
from additive_bo.surrogate_models.gp import GP
from additive_bo.gprotorch.kernels.fingerprint_kernels.tanimoto_kernel import TanimotoKernel
import ast
import torch
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning import Trainer
from pytorch_lightning import seed_everything

seed_everything(1, workers=True)


class LLMInterface:
    def __init__(self):
        self.design_space = ["a","v", "c","d","E","f","G","h","Z"]
        self.data_list = {}

    def initialize(self, n):
        # try:
        initialization = BOInitDataSelection(init_method='believer-3', 
                                            metric='euclidean', 
                                            n_clusters=int(n), 
                                            seed=0)
        self.data = BOAdditivesDataModule('../data/additives_reactions.csv', 
                                            representation='fragprints', 
                                            featurize_column='Additive_Smiles', 
                                            init_sample_size=n,
                                            init_selection_method=initialization)
        
        return self.data.additives_reactions['Additive_Smiles'].values[self.data.train_indexes].tolist()
        # except:
        #     return "Error. Please check your input, it should be a single number."

    def optimization_step(self, d: dict):
        results_dict = ast.literal_eval(d)
        inputs, _ = zip(*results_dict.items())

        self.data.additives_reactions.loc[self.data.additives_reactions['Additive_Smiles'].isin(inputs), 'UV210_Prod AreaAbs'] = self.data.additives_reactions.loc[self.data.additives_reactions['Additive_Smiles'].isin(inputs), 'Additive_Smiles'].map(results_dict)        
        train_x = torch.stack(self.data.additives_reactions['x'].tolist())
        train_y = torch.stack(self.data.additives_reactions['y'].tolist())

        surrogate_model = GP(train_x, train_y, kernel=TanimotoKernel())
        bo = BoModule(data=self.data, model=surrogate_model)
        
        trainer_config = {
            "logger": WandbLogger(project="additives-report"),
            "log_every_n_steps": 1,
            # "min_epochs": 0,
            # "max_steps": -1,
            "accelerator": "cpu",
            "devices": 1,
            "num_sanity_val_steps": 0,
            "max_epochs": 1,
            "deterministic": True
  
        }

        
        
        trainer =  Trainer(**trainer_config)
        trainer.fit(bo)

        trained_model = trainer.model
        return trained_model.gimme_suggestion()
    
# if __name__=='__main__':
#     llm = LLMInterface()
#     llm.initialize(10)
#     llm.optimization_step(d="{'c1nnc2n1CCCC2C(=O)O': 0}")
