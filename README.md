# UnbalancedVynilProject
A simulation of an unbalanced upright vinyl player, and corresponding controller using python.
The vinylDynamics.py folder holds most important information in the _UnbalancedVinyl()_ class, holding both the system model and the solver method, such that all requirements are packed into one class. The Example.ipynb creates an easy interface to interact with the system and apply and plot different controllers.

# To be added
- More accurate parameter estimates in the Example.ipynb folder
- A notch filter in the controller structure in Example.ipynb
- Some form of animation, in order to visually represent the progression
- Perhaps some frequency domain analysis and representation of the plant (although this is difficult because of the non-linearity)
