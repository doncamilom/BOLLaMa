from additive_bo.data_init_selection.clustering import BOInitDataSelection
from additive_bo.bo.module import BoModule
from additive_bo.data.module import BOAdditivesDataModule
from additive_bo.surrogate_models.gp import GP

class LLMInterface(object):
    def __init__(self) -> None:        
        pass
        
        # self.optimization = BoModule(model=)
    
    def initialize(self, design_space='additives', n_initial_points=10):
        assert n_initial_points
        initialization = BOInitDataSelection(init_method='believer-3', metric='euclidean', n_clusters=int(n_initial_points))
        if design_space == 'additives':
            self.data = BOAdditivesDataModule('data/additives_reactions.csv', 
                                              representation='fragprints', 
                                              featurize_column='Additive_Smiles', 
                                              init_sample_size=n_initial_points,
                                              init_selection_method=initialization)
        return self.data.additives_reactions['Additive_Smiles'].values[self.data.train_indexes].tolist()
    

    def optimization_step(self, results_dict):
        # featurize and make arrays from init_data
        x = None
        y = None
        surrogate_model = GP(x, y)
        BoModule(data=self.data, model=surrogate_model)


llm_interface = LLMInterface()
initial_sample = llm_interface.initialize()
print(initial_sample)