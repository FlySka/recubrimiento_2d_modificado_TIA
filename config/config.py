'''
clase de configuracion
'''
from os import cpu_count
from config.parser import parse_args
from tomli import load as load_toml

class Config:
    def __init__(self, path_config: str = 'config/init.toml'):
        self.path_config = path_config
        config, args = self.load()
        self.config2properties(config, args)
    
    def load(self):
        '''
        carga el archivo de configuracion

        :return: dict
        '''
        args = parse_args()
        with open(self.path_config, "rb") as f:
            config = load_toml(f)
        return config, args

    def config2properties(self, config: dict, args: dict) -> "Config":
        '''
        logica que transforma las configuraciones en parametros utiles

        :param config: diccionario de congiuracion en init.ini
        :param args: diccionario con parseados
        :return: None
        '''
        # parseados
        self.name = args.name
        self.log = args.log
        if args.n_jobs >= 1:
            self.n_jobs = args.n_jobs
        else:
            self.n_jobs = cpu_count() // 2 - 2

        # desde init.toml
        self.type_algorithm = config['CoatingMod2D']['type_algorithm']
        self.space_width = config['CoatingMod2D']['space_width']
        self.num_blocks = config['CoatingMod2D']['num_blocks']

        # genetico
        if self.type_algorithm == 'genetic':
            self.type_stop = config['GeneticAlgorithm']['type_stop']
        self.num_generations = config['GeneticAlgorithm']['num_generations']
        self.generations = config['GeneticAlgorithm']['num_generations']
        self.compute_time = config['GeneticAlgorithm']['compute_time']
        self.population_size = config['GeneticAlgorithm']['population_size']

        self.K = config['GeneticAlgorithm']['K']
        # self.area_factor = config['GeneticAlgorithm']['area_factor']
        self.gen_to_final_judgment = config['GeneticAlgorithm']['gen_to_final_judgment']
        self.survivors = config['GeneticAlgorithm']['survivors']
        self.mutation_rate = config['GeneticAlgorithm']['mutation_rate']
        self.per_children_choose = config['GeneticAlgorithm']['per_children_choose']

        # simulated_annealing
        if self.type_algorithm == 'simulated_annealing':
            self.type_stop = config['SimulatedAnnealing']['type_stop']
        self.iterations = config['SimulatedAnnealing']['num_iterations']
        self.compute_time = config['SimulatedAnnealing']['compute_time']
        self.T_init = config['SimulatedAnnealing']['T_init']
        self.T_end = config['SimulatedAnnealing']['T_end']
        self.type_update = config['SimulatedAnnealing']['type_update']
        self.k = config['SimulatedAnnealing']['k']

