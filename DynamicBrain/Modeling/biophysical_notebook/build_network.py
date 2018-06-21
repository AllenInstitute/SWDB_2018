from bmtk.builder.networks import NetworkBuilder


def build_cortical_network(output_dir='network/recurrent_network'):
    def distance_connection_handler(source, target, d_max, nsyn_min, nsyn_max):
        """ Connect cells that are less than d_max apart with a random number of synapses in the 
          interval [nsyn_min, nsyn_max)
        """
        sid = source['node_id']    # Get source id
        tid = target['node_id']    # Get target id
        
        # Avoid self-connections.
        if (sid == tid):
            return None
            
        # first calculate euclidean distance between cells
        src_positions = np.array([source['x'], source['y'], source['z']])
        trg_positions = np.array([target['x'], target['y'], target['z']])
        separation = np.sqrt(np.sum(src_positions - trg_positions)**2 )
            
        # drop the connection if nodes too far apart
        if separation >= d_max:
            return None

        # Add the number of synapses for every connection.
        tmp_nsyn = random.randint(nsyn_min, nsyn_max)
        return tmp_nsyn

    
    #### Step 1: Figure out what types, and number of, different cells to use in our network ####
    # Number of cell models desired
    N_Scnn1a = 2
    N_PV1 = 2
    N_LIF_exc = 2
    N_LIF_inh = 2
    
    # Define all the cell models in a dictionary (note dictionaries within a dictionary)
    biophysical_models = {
        'Scnn1a': { 
            'N': N_Scnn1a,               
            'ei': 'e', 
            'pop_name': 'Scnn1a', 
            'model_type': 'biophysical',
            'model_template': 'ctdb:Biophys1.hoc',
            'model_processing': 'aibs_perisomatic',       
            'morphology_file': 'Scnn1a-Tg3-Cre_Ai14_IVSCC_-177300.01.02.01_473845048_m.swc',
            'dynamics_params': '472363762_fit.json',
            'rotation_angle_zaxis': -3.646878266
        },    
        'PV1': {
            'N': N_PV1,
            'ei': 'i', 
            'pop_name': 'PV1',
            'model_type': 'biophysical',
            'model_template': 'ctdb:Biophys1.hoc',
            'model_processing': 'aibs_perisomatic',
            'dynamics_params': '472912177_fit.json',
            'morphology_file': 'Pvalb-IRES-Cre_Ai14_IVSCC_-176847.04.02.01_470522102_m.swc',
            'rotation_angle_zaxis': -2.539551891
        }
    }

    # Define all the cell models in a dictionary.
    LIF_models = {
        'LIF_exc': {
            'N': N_LIF_exc, 
            'ei': 'e', 
            'pop_name': 'LIF_exc',
            'model_type': 'point_process',
            'model_template': 'nrn:IntFire1',
            'dynamics_params': 'IntFire1_exc_1.json'
        },
        'LIF_inh': {
            'N': N_LIF_inh,
            'ei': 'i', 
            'pop_name': 'LIF_inh',
            'model_type': 'point_process',
            'model_template': 'nrn:IntFire1',
            'dynamics_params': 'IntFire1_inh_1.json'
        }
    }

    #### Step 2: Create NetworkBuidler object to build nodes and edges ####
    net = NetworkBuilder('Cortical')
    
    #### Step 3: Used add_nodes() method to add all our cells/cell-types
    for model in biophysical_models:
        # Build our biophysical cells
        params = biophysical_models[model]   
        n_cells = params.pop('N')
        
        # We'll randomly assign positions
        positions = generate_random_positions(n_cells)
        
        # Use add_nodes to create a set of N cells for each cell-type
        net.add_nodes(N=n_cells, # Specify the numer of cells belonging to this set of nodes 
                      x=positions[:,0], y=positions[:, 1], z=positions[:, 2],
                      rotation_angle_yaxis=np.random.uniform(0.0, 2*np.pi, n_cells),
                      
                      # The other parameters are shared by all cells of this set in the dictionary
                      **params)  # python shortcut for unrolling a dictionary

    for model in LIF_models:
        # Same thing as above but for our LIF type cells
        params = LIF_models[model].copy()

        # Number of cells for this model type
        n_cells = params.pop('N')
        
        # Precacluate positions, rotation angles for each N neurons in the population
        positions = generate_random_positions(n_cells)

        # Adds node populations
        net.add_nodes(N=n_cells ,
                      x=positions[:,0], y=positions[:, 1], z=positions[:, 2],
                      rotation_angle_yaxis=np.random.uniform(0.0, 2*np.pi, n_cells),
                      **params) 


    #### Step 4: Used add_edges() to set our connections between cells #### 
    cparameters = {'d_max': 160.0,    # Maximum separation between nodes where connection allowed 
                   'nsyn_min': 3,     # If connection exist, minimum number of synapses
                   'nsyn_max': 7}     # If connection exist, maximum number of synapses

    net.add_edges(source={'ei': 'i'}, # Select all inhibitory cells to apply this connection rule too
                  target={'ei': 'i', 'model_type': 'biophysical'},  # for the target cells we will use inhibitory biophysical cells
                  connection_rule=distance_connection_handler,
                  connection_params={'d_max': 160.0, 'nsyn_min': 3, 'nsyn_max': 7},
                  syn_weight=0.03, 
                  distance_range=[0.0, 1e+20],
                  target_sections=['somatic', 'basal'], 
                  delay=2.0,
                  dynamics_params='GABA_InhToInh.json', 
                  model_template='exp2syn')

    # inhibitory --> point-inhibitory
    net.add_edges(source={'ei': 'i'}, target={'ei': 'i', 'model_type': 'point_process'},
                  connection_rule=distance_connection_handler,
                  connection_params={'d_max': 160.0, 'nsyn_min': 3, 'nsyn_max': 7},
                  syn_weight=0.3, 
                  delay=2.0,
                  dynamics_params='instanteneousInh.json')

    # inhibiotry --> biophysical-excitatory
    net.add_edges(source={'ei': 'i'}, target={'ei': 'e', 'model_type': 'biophysical'},
                  connection_rule=distance_connection_handler,
                  connection_params={'d_max': 160.0, 'nsyn_min': 3, 'nsyn_max': 7},
                  syn_weight=0.3, 
                  distance_range=[0.0, 50.0],
                  target_sections=['somatic', 'basal', 'apical'], 
                  delay=2.0,
                  dynamics_params='GABA_InhToExc.json',
                  model_template='exp2syn')

    # inhibitory --> point-excitatory
    net.add_edges(source={'ei': 'i'}, target={'ei': 'e', 'model_type': 'point_process'},
                  connection_rule=distance_connection_handler,
                  connection_params={'d_max': 160.0, 'nsyn_min': 3, 'nsyn_max': 7},
                  syn_weight=0.4,
                  delay=2.0,
                  dynamics_params='instanteneousInh.json')

    # excitatory --> PV1 cells
    net.add_edges(source={'ei': 'e'}, target={'pop_name': 'PV1'},
                  connection_rule=distance_connection_handler,
                  connection_params={'d_max': 160.0, 'nsyn_min': 3, 'nsyn_max': 7},
                  syn_weight=0.05,
                  distance_range=[0.0, 1e+20],
                  target_sections=['somatic', 'basal'],
                  delay=2.0,
                  dynamics_params='AMPA_ExcToInh.json', 
                  model_template='exp2syn')
    
    # excitatory --> LIF_inh
    net.add_edges(source={'ei': 'e'}, target={'pop_name': 'LIF_inh'},
                  connection_rule=distance_connection_handler,
                  connection_params=cparameters,
                  syn_weight=0.2,
                  delay=2.0,
                  dynamics_params='instanteneousExc.json')

    # excitatory --> Scnn1a
    net.add_edges(source={'ei': 'e'}, target={'pop_name': 'Scnn1a'},
                  connection_rule=distance_connection_handler,
                  connection_params={'d_max': 160.0, 'nsyn_min': 3, 'nsyn_max': 7},
                  syn_weight=0.05,
                  distance_range=[30.0, 150.0], 
                  target_sections=['basal', 'apical'], 
                  delay=2.0,
                  dynamics_params='AMPA_ExcToExc.json',
                  model_template='exp2syn')

    # excitatory --> LIF_exc
    net.add_edges(source={'ei': 'e'}, target={'pop_name': 'LIF_exc'},
                  connection_rule=distance_connection_handler,
                  connection_params={'d_max': 160.0, 'nsyn_min': 3, 'nsyn_max': 7},
                  syn_weight=0.05, 
                  delay=2.0,
                  dynamics_params='instanteneousExc.json')

    
    #### Step 5: Build and save the network ####
    net.build()
    net.save(output_dir=output_dir)
    return net


def build_input_network(net, output_dir='network/source_input'):
    def select_source_cells(sources, target, N_syn=10):
        """ Note here that "sources" are given (not "source"). So the iterations occur through every target 
         with all sources as potential inputs. Faster than before and better if will have common rules.
        """

        target_id = target.node_id
        source_ids = [s.node_id for s in sources]
        
        nsyns_ret = [N_syn]*len(source_ids)
        return nsyns_ret
        

    filter_models = {
        'inputFilter': {
            'N': 25, 
            'ei': 'e', 
            'pop_name': 'input_filter', 
            'model_type': 'virtual'
        }
    }

    inputNetwork = NetworkBuilder("inputNetwork")
    inputNetwork.add_nodes(**filter_models['inputFilter'])

    inputNetwork.add_edges(target=net.nodes(pop_name='Scnn1a'),
                           iterator='all_to_one',
                           connection_rule=select_source_cells,
                           syn_weight=0.0007, 
                           distance_range=[0.0, 150.0],
                           target_sections=['basal', 'apical'],
                           delay=2.0,
                           dynamics_params='AMPA_ExcToExc.json',
                           model_template='exp2syn')

    inputNetwork.add_edges(target=net.nodes(pop_name='LIF_exc'),
                           iterator='all_to_one',
                           connection_rule=select_source_cells,
                           syn_weight=0.07,
                           delay=2.0,
                           dynamics_params='instanteneousExc.json')

    inputNetwork.add_edges(target=net.nodes(pop_name='PV1'),
                           iterator='all_to_one',
                           connection_rule=select_source_cells,
                           syn_weight=0.002, 
                           distance_range=[0.0, 1.0e+20],
                           target_sections=['basal', 'somatic'],
                           delay=2.0,
                           dynamics_params='AMPA_ExcToInh.json',
                           model_template='exp2syn')

    inputNetwork.add_edges(target=net.nodes(pop_name='LIF_inh'),
                           iterator='all_to_one',
                           connection_rule=select_source_cells,
                           syn_weight=0.01,
                           delay=2.0,
                           dynamics_params='instanteneousExc.json')

    inputNetwork.build()
    inputNetwork.save(output_dir=output_dir)


if __name__ == '__main__':
    net = build_cortical_network()
    build_input_network(net)
