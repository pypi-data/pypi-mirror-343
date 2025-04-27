from .request_utils import *
from abstract_utilities import *
import types      
def make_request(url,
                 data=None,
                 headers=None,
                 get_post=None,
                 endpoint=None,
                 status_code=False,
                 retry_after=False,
                 raw_response=False,
                 response_result=None,
                 load_nested_json=True,
                 auth=None,*args,**kwargs):
    data =data or {}
    response = None
    endpoint = endpoint or ''
    values = get_values_js(url=url,
                           endpoint=endpoint,
                           data=json.dumps(data),
                           headers=headers)
    
    get_post = str(get_post or ('POST' if data == None else 'GET')).upper() or 'POST'
    if get_post == 'POST':
        response = requests.post(**values)
    elif get_post == 'GET':
        response = requests.get(**values)
    else:
        raise ValueError(f"Unsupported HTTP method: {values.get('method')}")
    
    got_response = get_response(response,
                                raw_response=raw_response,
                                response_result=response_result,
                                load_nested_json=load_nested_json)
    
    got_status_code,got_retry_after = False,False
    if status_code or retry_after:
        if status_code:
            got_status_code = get_status_code(response)
        if retry_after:
            got_retry_after = get_retry_after(response)
        if got_status_code != False and got_retry_after == False :
            return got_response, got_status_code
        elif got_retry_after != False and got_status_code ==  False:
            return got_response,  got_retry_after
        return got_response, got_status_code, got_retry_after
    return got_response

def postRequest(url, data=None, **kwargs):
    """
    Make a POST request.
    
    Args:
        url (str): Base URL.
        data (dict, optional): Data to send in the request body.
        **kwargs: Additional arguments passed to make_request.
    
    Returns:
        Same as make_request.
    """
    return make_request(url, data=data, get_post='POST', **kwargs)

def getRequest(url, data=None, **kwargs):
    """
    Make a GET request.
    
    Args:
        url (str): Base URL.
        data (dict, optional): Query parameters (if any).
        **kwargs: Additional arguments passed to make_request.
    
    Returns:
        Same as make_request.
    """
    return make_request(url, data=data, get_post='GET', **kwargs)

def getRpcData(method=None,
               params=None,
               jsonrpc=None,
               id=None):
    return {
            "jsonrpc": jsonrpc or "2.0",
            "id": 0,
            "method": method,
            "params": params,
        }
def rpcRequest(url: str, method: str, params: Any = None, jsonrpc: str = "2.0", 
               id: Optional[int] = 0, headers: Optional[dict] = None, **kwargs) -> Any:
    """
    Make a JSON-RPC request (via POST by default).
    
    Args:
        url: Base URL for the JSON-RPC server.
        method: JSON-RPC method name.
        params: JSON-RPC parameters (list or dict).
        jsonrpc: JSON-RPC version. Defaults to "2.0".
        id: JSON-RPC request ID. Defaults to 0.
        headers: Request headers (adds Content-Type: application/json if not set).
        **kwargs: Additional arguments passed to make_request (e.g., endpoint, status_code).
    
    Returns:
        Same as make_request.
    """
    headers = headers or {}
    headers.setdefault('Content-Type', 'application/json')
    data = getRpcData(method=method, params=params, jsonrpc=jsonrpc, id=id)
    return make_request(url, data=data, get_post='POST', headers=headers, **kwargs)

def rpcRequest(url: str, method: str, params: Any = None, jsonrpc: str = "2.0", 
               id: Optional[int] = 0, headers: Optional[dict] = None, **kwargs) -> Any:
    """
    Make a JSON-RPC request (via POST by default).
    
    Args:
        url: Base URL for the JSON-RPC server.
        method: JSON-RPC method name.
        params: JSON-RPC parameters (list or dict).
        jsonrpc: JSON-RPC version. Defaults to "2.0".
        id: JSON-RPC request ID. Defaults to 0.
        headers: Request headers (adds Content-Type: application/json if not set).
        **kwargs: Additional arguments passed to make_request (e.g., endpoint, status_code).
    
    Returns:
        Same as make_request.
    """
    headers = headers or {}
    headers.setdefault('Content-Type', 'application/json')
    data = getRpcData(method=method, params=params, jsonrpc=jsonrpc, id=id)
    return make_request(url, data=data, get_post='POST', headers=headers, **kwargs)
