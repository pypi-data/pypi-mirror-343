from dataclasses import dataclass
from dataclasses import field
from typing import List
from numpy import dtype
from pandaprosumer.element.element_toolbox import enforce_types

@enforce_types
@dataclass
class ChillerElementData:
    """
    Represents the parameters of a chiller in SenergyNets.

    Attributes:
        name (str): The name of the chiller.
        input (List[tuple]): A list of tuples defining the necessary and instance properties.
    """
    name: str = "sn_chiller"
    input: List[tuple] = field(default_factory=lambda: [

        # Necessary properties
        ('name', dtype(object)),
        ('in_service', bool),

        # @tecnalia: TODO: clean this up according to the "datasheet" values defined before

        # Instance properties
        ("cp_water", "f8"),
        ("t_sh", "f8"),
        ("t_sc", "f8"),
        ("pp_cond", "f8"),
        ("pp_evap", "f8"),
        ("w_cond_pump", "f8"),
        ("w_evap_pump", "f8"),
        ("plf_cc", "f8"),
        ("eng_eff", "f8"),
        ("n_ref", dtype(object))

    ])
