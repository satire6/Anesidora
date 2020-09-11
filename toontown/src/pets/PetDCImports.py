"""This file allows us to conditionally import pet-related modules for the DC
"""

if hasattr(base, 'wantPets') and base.wantPets:
    import DistributedPet
