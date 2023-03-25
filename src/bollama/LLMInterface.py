from additive_bo.data_init_selection.clustering import BOInitDataSelection
from additive_bo.bo.module import BoModule
from additive_bo.data.module import BOAdditivesDataModule
from additive_bo.surrogate_models.gp import GP
from additive_bo.gprotorch.kernels.fingerprint_kernels.tanimoto_kernel import TanimotoKernel
import ast
import torch
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning import Trainer

class LLMInterface(object):
    def __init__(self) -> None:        
        pass
            
    def initialize(self, design_space='additives', n_initial_points=10):
        initialization = BOInitDataSelection(init_method='believer-3', 
                                             metric='euclidean', 
                                             n_clusters=int(n_initial_points))
        if design_space == 'additives':
            self.data = BOAdditivesDataModule('data/additives_reactions.csv', 
                                              representation='fragprints', 
                                              featurize_column='Additive_Smiles', 
                                              init_sample_size=n_initial_points,
                                              init_selection_method=initialization)
            
            selected_additives = self.data.additives_reactions['Additive_Smiles'].values[self.data.train_indexes].tolist()
        return selected_additives
    

    def optimization_step(self, results_dict="{'CCc1ccc(cc1)C#C':1}"):
        # read dictionary
        # featurize and make arrays from init_data
          
        results_dict = ast.literal_eval(results_dict)
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
        }

        
        
        trainer =  Trainer(**trainer_config)
        trainer.fit(bo)

if __name__=="__main__":
    llm_interface = LLMInterface()
    initial_sample = llm_interface.initialize()
    llm_interface.optimization_step()
