"""
Ordering module for SignalWire SWML output.

This module provides functionality to order SWML data according to a predefined
template, ensuring consistent output structure.
"""

from collections import OrderedDict
import yaml
from yaml.representer import SafeRepresenter

# Define the key order template for SWML data
KEY_ORDER = {
    "version": [],
    "sections": {
        "main": [
            {
                "ai": {
                    "prompt": {
                        "confidence": [],
                        "barge_confidence": [],
                        "top_p": [],
                        "temperature": [],
                        "frequency_penalty": [],
                        "presence_penalty": [],
                        "text": [],
                        "contexts": {
                            "default": {
                                "steps": [
                                    {
                                        "name": [],
                                        "text": [],
                                        "functions": [],
                                        "step_criteria": [],
                                        "valid_steps": [],
                                        "end": [],
                                        "skip_user_turn": []
                                    }
                                ]
                            }
                        }
                    },
                    "params": {
                        "direction": [],
                        "wait_for_user": [],
                        "end_of_speech_timeout": [],
                        "attention_timeout": [],
                        "inactivity_timeout": [],
                        "outbound_attention_timeout": [],
                        "background_file": [],
                        "background_file_loops": [],
                        "background_file_volume": [],
                        "local_tz": [],
                        "conscience": [],
                        "ai_volume": [],
                        "save_conversation": [],
                        "conversation_id": [],
                        "digit_timeout": [],
                        "digit_terminators": [],
                        "energy_level": [],
                        "swaig_allow_swml": [],
                        "ai_model": [],
                        "audible_debug": []
                    },
                    "post_prompt_url": [],
                    "post_prompt": {
                        "confidence": [],
                        "barge_confidence": [],
                        "top_p": [],
                        "temperature": [],
                        "frequency_penalty": [],
                        "presence_penalty": [],
                        "text": []
                    },
                    "languages": [
                        {
                            "name": [],
                            "code": [],
                            "voice": []
                        }
                    ],
                    "hints": [],
                    "pronounce": [
                        {
                            "replace": [],
                            "with": [],
                            "ignore_case": []
                        }
                    ],
                    "SWAIG": {
                        "defaults": {
                            "web_hook_url": [],
                            "meta_data_token": [],
                            "meta_data": {
                                "my_key": []
                            }
                        },
                        "native_functions": [],
                        "includes": [
                            {
                                "url": [],
                                "functions": []
                            }
                        ],
                        "functions": [
                            {
                                "function": [],
                                "meta_data_token": [],
                                "meta_data": {
                                    "my_key": []
                                },
                                "purpose": [],
                                "description": [],
                                "parameters": {
                                    "type": [],
                                    "properties": {
                                        "location": {
                                            "type": [],
                                            "description": []
                                        }
                                    }
                                },
                                "data_map": {
                                    "webhooks": [
                                        {
                                            "url": [],
                                            "method": [],
                                            "headers": {},
                                            "output": {
                                                "response": []
                                            }
                                        }
                                    ],
                                    "expressions": [
                                        {
                                            "string": [],
                                            "pattern": [],
                                            "output": {
                                                "response": [],
                                                "action": []
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        ]
    }
}

def order_data(data, key_order=None):
    """
    Order data based on the provided key_order map.
    
    Args:
        data (dict): The data to order
        key_order (dict, optional): The key order template. Defaults to KEY_ORDER.
    
    Returns:
        OrderedDict: The ordered data
    """
    if key_order is None:
        key_order = KEY_ORDER
    
    if isinstance(data, dict):
        ordered = OrderedDict()
        # First include keys that are in the key_order
        for key, sub_order in key_order.items():
            if key in data:
                ordered[key] = order_data(data[key], sub_order)
        # Then include any keys that are not in key_order (to preserve all data)
        for key in data:
            if key not in key_order:
                ordered[key] = data[key]
        return ordered
    elif isinstance(data, list):
        if key_order and len(key_order) > 0:
            return [order_data(item, key_order[0]) for item in data]
        return data
    else:
        return data


def get_ordered_dict(data):
    """
    Get an ordered dictionary from the provided data.
    
    Args:
        data (dict): The data to order
    
    Returns:
        OrderedDict: The ordered data
    """
    return order_data(data)


# Custom YAML representation for OrderedDict
class OrderedYAMLDumper(yaml.SafeDumper):
    """
    A custom YAML dumper that preserves the order of keys in OrderedDict objects
    without adding explicit tags or type information.
    """
    pass

# Add a representer for OrderedDict to the custom dumper
def _represent_ordered_dict(dumper, data):
    """
    Represent an OrderedDict as a standard YAML mapping without any OrderedDict tags.
    """
    return dumper.represent_mapping('tag:yaml.org,2002:map', data.items())

OrderedYAMLDumper.add_representer(OrderedDict, _represent_ordered_dict)

class BlockStyleDumper(OrderedYAMLDumper):
    def represent_scalar(self, tag, value, style=None):
        if isinstance(value, str) and '\\n' in value:
            style = '|'
        return super().represent_scalar(tag, value, style)

def ordered_to_dict(obj):
    if isinstance(obj, OrderedDict):
        return {k: ordered_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, dict):
        return {k: ordered_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [ordered_to_dict(i) for i in obj]
    elif isinstance(obj, tuple):
        return tuple(ordered_to_dict(i) for i in obj)
    elif isinstance(obj, set):
        return set(ordered_to_dict(i) for i in obj)
    else:
        return obj

def dump_yaml(data, **kwargs):
    default_kwargs = {
        'default_flow_style': False,
        'sort_keys': False,
        'indent': 2
    }
    default_kwargs.update(kwargs)
    data = ordered_to_dict(data)
#    print("DEBUG: Top-level type before dump:", type(data))
#    print("DEBUG: Type of data['sections']:", type(data.get('sections')))
    return yaml.dump(data, Dumper=BlockStyleDumper, **default_kwargs) 