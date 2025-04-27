"""
Protocol implementations for interacting with DeFi protocols.

This module provides convenient classes for interacting with popular 
DeFi protocols, enabling code like:

    to_addr = protocols.Uniswap._addresses['v2router']
    input_data = protocols.Uniswap.swapExactEthForToken(amount_out_min=aa, path=bb, to=cc, deadline=dd)
"""
from typing import Any, Dict, List, Union, Tuple
import json
from eth_abi import encode
from eth_utils import to_hex, to_bytes, to_checksum_address, to_int
from . import constants


class ProtocolBase:
    """Base class for all protocol implementations."""
    _addresses = {}
    _function_sigs = {}
    _function_types = {}
    _function_param_names = {}
    
    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()
    
    @classmethod
    def function(cls, name: str, **kwargs) -> str:
        """Generate function call data for the given function name."""
        name_lower = name.lower()
        
        # Check if the function exists
        if name_lower not in cls._function_sigs:
            raise ValueError(f"Function '{name}' not found in {cls.__name__}")
            
        # Get function signature
        func_sig = cls._function_sigs[name_lower]
        
        # Get function parameter types and names if available
        param_types = cls._function_types.get(name_lower, [])
        param_names = cls._function_param_names.get(name_lower, [])
        
        # Default basic encoding if no types defined
        if not param_types:
            # Simple concatenation (placeholder - not actual encoding)
            params = ''.join(f"{v}" for k, v in kwargs.items())
            return func_sig + params
        
        # Convert kwargs to positional args in the right order
        args = []
        
        # If param_names is defined, use named parameters
        if param_names and all(p in param_names for p in kwargs):
            # Map named parameters to positional order
            for i, param_name in enumerate(param_names):
                if param_name not in kwargs:
                    raise ValueError(f"Missing parameter '{param_name}' for function {name}")
                
                value = kwargs[param_name]
                param_type = param_types[i]
                
                # Type conversion based on Ethereum types
                if param_type.startswith('address'):
                    if isinstance(value, list):
                        value = [to_checksum_address(v) for v in value]
                    else:
                        value = to_checksum_address(value)
                elif param_type.startswith('uint') or param_type.startswith('int'):
                    if isinstance(value, str):
                        value = to_int(hexstr=value) if value.startswith('0x') else int(value)
                
                args.append(value)
        
        # Support legacy x1, x2, ... format
        elif all(f"x{i+1}" in kwargs for i in range(len(param_types))):
            for i, param_type in enumerate(param_types):
                key = f"x{i+1}"
                if key not in kwargs:
                    raise ValueError(f"Missing parameter {key} for function {name}")
                
                value = kwargs[key]
                # Type conversion based on Ethereum types
                if param_type.startswith('address'):
                    if isinstance(value, list):
                        value = [to_checksum_address(v) for v in value]
                    else:
                        value = to_checksum_address(value)
                elif param_type.startswith('uint') or param_type.startswith('int'):
                    if isinstance(value, str):
                        value = to_int(hexstr=value) if value.startswith('0x') else int(value)
                
                args.append(value)
        else:
            # If the parameter naming doesn't match either convention
            param_str = ", ".join(param_names) if param_names else f"x1, x2, ..., x{len(param_types)}"
            raise ValueError(f"Function {name} expects parameters: {param_str}")
        
        # ABI encode the parameters
        try:
            encoded_params = encode(param_types, args)
            return func_sig + to_hex(encoded_params)[2:]  # remove '0x' prefix
        except Exception as e:
            # Fallback for complex types
            return func_sig + json.dumps(args)

    @classmethod
    def __getattr__(cls, name: str):
        """Handle protocol function calls directly."""
        # Check if it's in addresses
        if name in cls._addresses:
            return cls._addresses[name]
            
        # Check if it's a function
        name_lower = name.lower()
        if name_lower in cls._function_sigs:
            # Return a function wrapper that will call the function method
            def function_wrapper(**kwargs):
                return cls.function(name, **kwargs)
            return function_wrapper
            
        # Try camelCase to lowercase conversion for functions
        if name[0].islower() and name.lower() in cls._function_sigs:
            def function_wrapper(**kwargs):
                return cls.function(name.lower(), **kwargs)
            return function_wrapper
            
        raise AttributeError(f"'{cls.__name__}' has no attribute '{name}'")


class Uniswap(ProtocolBase):
    """Uniswap protocol implementation."""
    
    # Addresses
    _addresses = {
        'v2factory': constants.Addresses.Uniswap.V2_FACTORY,
        'v2router': constants.DEXes.UNISWAP_V2_ROUTER_2,
        'v3factory': constants.Addresses.Uniswap.V3_FACTORY,
        'v3router': constants.DEXes.UNISWAP_V3_ROUTER,
        'universal_router': constants.DEXes.UNISWAP_UNIVERSAL_ROUTER,
        'universal_router_2': constants.DEXes.UNISWAP_UNIVERSAL_ROUTER_2,
        'v3positions': constants.DEXes.UNI_V3_POSITIONS,
    }
    
    # Function signatures - using lowercase keys internally
    _function_sigs = {
        # V2 Router functions
        'swapexactethfortoken': '0x7ff36ab5',  # swapExactETHForTokens(uint256,address[],address,uint256)
        'swapethfortokenssupportingfeeontransfertokens': '0xb6f9de95',  # swapETHForExactTokensSupportingFeeOnTransferTokens
        'swapexactethfortokens': '0x7ff36ab5',  # swapExactETHForTokens(uint256,address[],address,uint256)
        'swapethforexacttokens': '0xfb3bdb41',  # swapETHForExactTokens(uint256,address[],address,uint256)
        'swapexacttokensforeth': '0x18cbafe5',  # swapExactTokensForETH(uint256,uint256,address[],address,uint256)
        'swapexacttokensfortokens': '0x38ed1739',  # swapExactTokensForTokens(uint256,uint256,address[],address,uint256)
        'swaptokensforexacteth': '0x4a25d94a',  # swapTokensForExactETH(uint256,uint256,address[],address,uint256)
        'swaptokensforexacttokens': '0x8803dbee',  # swapTokensForExactTokens(uint256,uint256,address[],address,uint256)
        'addliquidity': '0xe8e33700',  # addLiquidity(address,address,uint256,uint256,uint256,uint256,address,uint256)
        'addliquidityeth': '0xf305d719',  # addLiquidityETH(address,uint256,uint256,uint256,address,uint256)
        'removeliquidity': '0xbaa2abde',  # removeLiquidity(address,address,uint256,uint256,uint256,address,uint256)
        'removeliquidityeth': '0x02751cec',  # removeLiquidityETH(address,uint256,uint256,uint256,address,uint256)
        
        # V3 Router functions
        'exactinput': '0xc04b8d59',  # exactInput((bytes,address,uint256,uint256,uint256))
        'exactoutput': '0xf28c0498',  # exactOutput((bytes,address,uint256,uint256,uint256))
        'exactinputsingle': '0x414bf389',  # exactInputSingle((address,address,uint24,address,uint256,uint256,uint256,uint160))
        'exactoutputsingle': '0xdb3e2198',  # exactOutputSingle((address,address,uint24,address,uint256,uint256,uint256,uint160))
    }
    
    # Function parameter types for ABI encoding
    _function_types = {
        'swapexactethfortoken': ['uint256', 'address[]', 'address', 'uint256'],
        'swapexactethfortokens': ['uint256', 'address[]', 'address', 'uint256'],
        'swapethforexacttokens': ['uint256', 'address[]', 'address', 'uint256'],
        'swapexacttokensforeth': ['uint256', 'uint256', 'address[]', 'address', 'uint256'],
        'swapexacttokensfortokens': ['uint256', 'uint256', 'address[]', 'address', 'uint256'],
        'swaptokensforexacteth': ['uint256', 'uint256', 'address[]', 'address', 'uint256'],
        'swaptokensforexacttokens': ['uint256', 'uint256', 'address[]', 'address', 'uint256'],
        'addliquidity': ['address', 'address', 'uint256', 'uint256', 'uint256', 'uint256', 'address', 'uint256'],
        'addliquidityeth': ['address', 'uint256', 'uint256', 'uint256', 'address', 'uint256'],
        'removeliquidity': ['address', 'address', 'uint256', 'uint256', 'uint256', 'address', 'uint256'],
        'removeliquidityeth': ['address', 'uint256', 'uint256', 'uint256', 'address', 'uint256'],
    }
    
    # Function parameter names for better usability
    _function_param_names = {
        'swapexactethfortoken': ['amount_out_min', 'path', 'to', 'deadline'],
        'swapexactethfortokens': ['amount_out_min', 'path', 'to', 'deadline'],
        'swapethforexacttokens': ['amount_out', 'path', 'to', 'deadline'],
        'swapexacttokensforeth': ['amount_in', 'amount_out_min', 'path', 'to', 'deadline'],
        'swapexacttokensfortokens': ['amount_in', 'amount_out_min', 'path', 'to', 'deadline'],
        'swaptokensforexacteth': ['amount_out', 'amount_in_max', 'path', 'to', 'deadline'],
        'swaptokensforexacttokens': ['amount_out', 'amount_in_max', 'path', 'to', 'deadline'],
        'addliquidity': ['token_a', 'token_b', 'amount_a_desired', 'amount_b_desired', 'amount_a_min', 'amount_b_min', 'to', 'deadline'],
        'addliquidityeth': ['token', 'amount_token_desired', 'amount_token_min', 'amount_eth_min', 'to', 'deadline'],
        'removeliquidity': ['token_a', 'token_b', 'liquidity', 'amount_a_min', 'amount_b_min', 'to', 'deadline'],
        'removeliquidityeth': ['token', 'liquidity', 'amount_token_min', 'amount_eth_min', 'to', 'deadline'],
    }


class Sushiswap(ProtocolBase):
    """Sushiswap protocol implementation."""
    
    # Addresses
    _addresses = {
        'factory': constants.Addresses.Sushiswap.FACTORY,
        'router': '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F',  # SushiSwap Router
    }
    
    # Function signatures - Sushiswap uses the same ABI as Uniswap V2
    _function_sigs = {
        'swapexactethfortoken': '0x7ff36ab5',  # swapExactETHForTokens(uint256,address[],address,uint256)
        'swapethfortokenssupportingfeeontransfertokens': '0xb6f9de95',  # swapETHForExactTokensSupportingFeeOnTransferTokens
        'swapexactethfortokens': '0x7ff36ab5',  # swapExactETHForTokens(uint256,address[],address,uint256)
        'swapethforexacttokens': '0xfb3bdb41',  # swapETHForExactTokens(uint256,address[],address,uint256)
        'swapexacttokensforeth': '0x18cbafe5',  # swapExactTokensForETH(uint256,uint256,address[],address,uint256)
        'swapexacttokensfortokens': '0x38ed1739',  # swapExactTokensForTokens(uint256,uint256,address[],address,uint256)
        'swaptokensforexacteth': '0x4a25d94a',  # swapTokensForExactETH(uint256,uint256,address[],address,uint256)
        'swaptokensforexacttokens': '0x8803dbee',  # swapTokensForExactTokens(uint256,uint256,address[],address,uint256)
        'addliquidity': '0xe8e33700',  # addLiquidity(address,address,uint256,uint256,uint256,uint256,address,uint256)
        'addliquidityeth': '0xf305d719',  # addLiquidityETH(address,uint256,uint256,uint256,address,uint256)
        'removeliquidity': '0xbaa2abde',  # removeLiquidity(address,address,uint256,uint256,uint256,address,uint256)
        'removeliquidityeth': '0x02751cec',  # removeLiquidityETH(address,uint256,uint256,uint256,address,uint256)
    }
    
    # Function parameter types for ABI encoding
    _function_types = {
        'swapexactethfortoken': ['uint256', 'address[]', 'address', 'uint256'],
        'swapexactethfortokens': ['uint256', 'address[]', 'address', 'uint256'],
        'swapethforexacttokens': ['uint256', 'address[]', 'address', 'uint256'],
        'swapexacttokensforeth': ['uint256', 'uint256', 'address[]', 'address', 'uint256'],
        'swapexacttokensfortokens': ['uint256', 'uint256', 'address[]', 'address', 'uint256'],
        'swaptokensforexacteth': ['uint256', 'uint256', 'address[]', 'address', 'uint256'],
        'swaptokensforexacttokens': ['uint256', 'uint256', 'address[]', 'address', 'uint256'],
        'addliquidity': ['address', 'address', 'uint256', 'uint256', 'uint256', 'uint256', 'address', 'uint256'],
        'addliquidityeth': ['address', 'uint256', 'uint256', 'uint256', 'address', 'uint256'],
        'removeliquidity': ['address', 'address', 'uint256', 'uint256', 'uint256', 'address', 'uint256'],
        'removeliquidityeth': ['address', 'uint256', 'uint256', 'uint256', 'address', 'uint256'],
    }
    
    # Function parameter names for better usability - same as Uniswap
    _function_param_names = {
        'swapexactethfortoken': ['amount_out_min', 'path', 'to', 'deadline'],
        'swapexactethfortokens': ['amount_out_min', 'path', 'to', 'deadline'],
        'swapethforexacttokens': ['amount_out', 'path', 'to', 'deadline'],
        'swapexacttokensforeth': ['amount_in', 'amount_out_min', 'path', 'to', 'deadline'],
        'swapexacttokensfortokens': ['amount_in', 'amount_out_min', 'path', 'to', 'deadline'],
        'swaptokensforexacteth': ['amount_out', 'amount_in_max', 'path', 'to', 'deadline'],
        'swaptokensforexacttokens': ['amount_out', 'amount_in_max', 'path', 'to', 'deadline'],
        'addliquidity': ['token_a', 'token_b', 'amount_a_desired', 'amount_b_desired', 'amount_a_min', 'amount_b_min', 'to', 'deadline'],
        'addliquidityeth': ['token', 'amount_token_desired', 'amount_token_min', 'amount_eth_min', 'to', 'deadline'],
        'removeliquidity': ['token_a', 'token_b', 'liquidity', 'amount_a_min', 'amount_b_min', 'to', 'deadline'],
        'removeliquidityeth': ['token', 'liquidity', 'amount_token_min', 'amount_eth_min', 'to', 'deadline'],
    }


class OneInch(ProtocolBase):
    """1inch protocol implementation."""
    
    # Addresses
    _addresses = {
        'router_v4': constants.DEXes.AGGREGATION_ROUTER_V4,
        'router_v5': constants.DEXes.AGGREGATION_ROUTER_V5,
        'router_v2': constants.DEXes.ONEINCH_ROUTER_2,
        'settlement': constants.DEXes.ONEINCH_SETTLEMENT,
    }
    
    # Function signatures
    _function_sigs = {
        'swap': '0x7c025200',  # swap(address,(address,address,address,address,uint256,uint256,uint256,bytes),bytes)
        'unoswap': '0x2e95b6c8',  # unoswap(address,uint256,uint256,bytes[])
        'clipperswap': '0x84bd6d29',  # clipperSwap(address,address,address,uint256,uint256,uint256,bytes32,bytes32)
    }
    
    # Function parameter types
    _function_types = {
        'swap': ['address', 'tuple', 'bytes'],
        'unoswap': ['address', 'uint256', 'uint256', 'bytes[]'],
        'clipperswap': ['address', 'address', 'address', 'uint256', 'uint256', 'uint256', 'bytes32', 'bytes32'],
    }
    
    # Function parameter names
    _function_param_names = {
        'swap': ['recipient', 'desc', 'data'],
        'unoswap': ['src_token', 'amount', 'min_return', 'parts'],
        'clipperswap': ['src_token', 'dst_token', 'recipient', 'amount', 'min_return', 'fee', 'signature', 'auxiliary_data'],
    }


class Curve(ProtocolBase):
    """Curve protocol implementation."""
    
    # Addresses - note that Curve has many pools with different addresses
    _addresses = {
        'compound_swap': constants.DEXes.CURVE_FI_COMPOUND_SWAP,
        'dai_usdc_usdt_pool': constants.DEXes.CURVE_FI_DAI_USDC_USDT_POOL,
        'usdt_swap': constants.DEXes.CURVE_FI_USDT_SWAP,
        'y_swap': constants.DEXes.CURVE_FI_Y_SWAP,
    }
    
    # Function signatures
    _function_sigs = {
        'exchange': '0x3df02124',  # exchange(int128,int128,uint256,uint256)
        'exchange_underlying': '0xa6417ed6',  # exchange_underlying(int128,int128,uint256,uint256)
        'add_liquidity': '0x0b4c7e4d',  # add_liquidity(uint256[2],uint256)
        'remove_liquidity': '0x5b36389c',  # remove_liquidity(uint256,uint256[2])
    }
    
    # Function parameter types
    _function_types = {
        'exchange': ['int128', 'int128', 'uint256', 'uint256'],
        'exchange_underlying': ['int128', 'int128', 'uint256', 'uint256'],
        'add_liquidity': ['uint256[2]', 'uint256'],
        'remove_liquidity': ['uint256', 'uint256[2]'],
    }
    
    # Function parameter names
    _function_param_names = {
        'exchange': ['i', 'j', 'dx', 'min_dy'],
        'exchange_underlying': ['i', 'j', 'dx', 'min_dy'],
        'add_liquidity': ['amounts', 'min_mint_amount'],
        'remove_liquidity': ['amount', 'min_amounts'],
    }


# Protocol class wrapper for direct method access
class ProtocolProxy:
    """Proxy class to directly access protocol methods."""
    
    def __init__(self, protocol_class):
        self._protocol_class = protocol_class
        
    def __getattr__(self, name):
        """
        Forward attribute access to the protocol class.
        This handles both standard attributes and dynamically generated functions.
        """
        try:
            # First try regular attribute access
            return getattr(self._protocol_class, name)
        except AttributeError:
            # Then try the protocol's __getattr__ method for dynamic function access
            if hasattr(self._protocol_class, '__getattr__'):
                try:
                    return self._protocol_class.__getattr__(name)
                except AttributeError:
                    pass
            # If all else fails, raise the attribute error
            raise AttributeError(f"'{self._protocol_class.__name__}' has no attribute '{name}'")


# Protocols class to provide direct access to protocol classes
class Protocols:
    """
    Container class for protocol implementations.
    
    This class provides access to all protocol implementations through a consistent interface.
    """
    def __init__(self):
        # Create proxies for direct method access
        self.Uniswap = ProtocolProxy(Uniswap)
        self.Sushiswap = ProtocolProxy(Sushiswap)
        self.OneInch = ProtocolProxy(OneInch)
        self.Curve = ProtocolProxy(Curve)

# Export the protocols namespace
protocols = Protocols() 