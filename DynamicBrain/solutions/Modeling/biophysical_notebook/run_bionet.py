from bmtk.simulator import bionet


conf = bionet.Config.from_json('config.json', validate=True)
conf.build_env()
graph = bionet.BioNetwork.from_config(conf)
sim = bionet.BioSimulator.from_config(conf, network=graph)
sim.run()
