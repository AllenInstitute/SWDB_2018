from bmtk.simulator import pointnet

#import json
#%matplotlib inline



#import set_weights as wf

# Some functions in modelingSDK for faster reading of the config files
configure = pointnet.Config.from_json('config.json')

# Reads and loads the config file
net = pointnet.PointNetwork.from_config(configure)

# This will not be required for future versions (will be optional). Allows users to have different
# weight functions. Here we will just use the weight as is. See set_weights.py if interested of another example.
#net.add_weight_function(wf.wmax)

# Create network for NEST. Can just give the configure and graph - also possible for biophysical networks.
sim = pointnet.PointSimulator.from_config(configure, net)
sim.run()
print 'done'
