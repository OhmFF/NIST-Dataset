# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 18:55:19 2023
For reference only
@author: Pakpoom Limtong
"""
"""
input parameters
Vu = Unhydrated phase fractions
Vcsh = Resolved hydrated phase fractions
Vcp = Resolved pore fractions
Vcp_p = Capillary pore from Powers
wc = water-to-cement ratio
phi1 = solid C-S-H 
phi2 = unresolved capillary pore 
f0 = Powers'degree of hydration
f1 = Powers'capillary pore
D0 = bulk diffusivity in pore solution = 1.72e-9 m^2/s
D1 = diffusivity of real C-S-H = 0.001D0
D2 = diffusivity of unresolved capillary pore = 1.0D0
De = effective diffusivity of the effective composite
"""
segment = np.load("your segmented image.npy")
def prop_table(labeled_img):
    props = ps.metrics.regionprops_3D(labeled_img)
    metrics = ['label', 'volume', 'sphericity']
    from loguru import logger
    d = {}
    for i, k in enumerate(metrics):
        logger.trace('Processing {k}')
        try:
            d[k] = np.array([r[k] for r in props])
        except ValueError: 
            logger.error(f'Error encountered evaluating {k} so skipping it')
    df = pd.DataFrame(d)
    return df

pore = (segment == -5)
thk = ps.filters.local_thickness(pore, sizes = 25, mode ="hybrid", divs = 2)
thk = (thk >= 3) #Tentative value for spherical voids
all_labels = measure.label(thk)
df = prop_table(all_labels)
im = np.zeros(shape = all_labels.shape)
#This size and sphericity are tentative value from trials and errors
for cluster in df[((df['volume'] >= 1000)&(df['sphericity']>= 0.7)) | \
              (df['volume']>= 3000)]['label'].values.tolist(): 
    x = (all_labels == cluster)
    im = np.logical_or(im, x)
air = 10*im #Assign node type of air void as 5
airvoid_isolated = segment + air #superimpose to the original segmented image
ps.io.to_vtk(airvoid_isolated , 'output') #export to vtk for 3D visualization
np.save('output.npy',airvoid_isolated) #save np array for later use
