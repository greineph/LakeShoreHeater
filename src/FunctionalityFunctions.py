# this file exists to avoid circular imports
import src.AbstractFunctionality as abstractF
import src.HeaterFunctionality as heaterF


functions = {"Basic": {"load": abstractF.load_gui_elements,
                       "extract": abstractF.extract_data,
                       "create": abstractF.create_instance},
             "Heater": {"load": heaterF.load_gui_elements,
                        "extract": heaterF.extract_data,
                        "create": heaterF.create_instance},
             }
