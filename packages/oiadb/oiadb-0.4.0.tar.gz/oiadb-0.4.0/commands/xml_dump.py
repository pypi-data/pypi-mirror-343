"""
Module for XML dump functionality with accessibility support.
Provides a local server to dump XML representation of the current UI hierarchy.
"""

import socket
import threading
import re
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from .core import get_adb_instance

class XMLDumpHandler(BaseHTTPRequestHandler):
    """HTTP request handler for XML dump server."""
    
    def _set_headers(self, content_type="application/xml"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests to the server."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        if path == "/get_xml":
            # Extract parameters
            resource_id = query_params.get('id', [''])[0]
            text_value = query_params.get('value', [''])[0]
            content_desc = query_params.get('content_desc', [''])[0]
            class_name = query_params.get('class', [''])[0]
            threshold = float(query_params.get('threshold', ['0.8'])[0])
            
            # Get XML dump with optional filters
            xml_content = get_xml_dump(
                resource_id=resource_id,
                text_value=text_value,
                content_desc=content_desc,
                class_name=class_name,
                threshold=threshold
            )
            
            self._set_headers()
            self.wfile.write(xml_content.encode())
        
        elif path == "/find_elements":
            # Extract parameters for finding elements
            criteria = {}
            for key in query_params:
                criteria[key] = query_params[key][0]
            
            # Find elements matching criteria
            elements = find_elements_by_criteria(criteria)
            
            self._set_headers(content_type="application/json")
            self.wfile.write(json.dumps(elements).encode())
        
        elif path == "/accessibility_actions":
            # Get available accessibility actions
            node_id = query_params.get('node_id', [''])[0]
            actions = get_accessibility_actions(node_id)
            
            self._set_headers(content_type="application/json")
            self.wfile.write(json.dumps(actions).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

def get_xml_dump(resource_id="", text_value="", content_desc="", class_name="", threshold=0.8):
    """
    Get XML dump of the current UI hierarchy with optional filtering.
    
    Args:
        resource_id (str): Filter by resource ID
        text_value (str): Filter by text value
        content_desc (str): Filter by content description
        class_name (str): Filter by class name
        threshold (float): Similarity threshold for fuzzy matching
    
    Returns:
        str: XML representation of the UI hierarchy
    """
    adb = get_adb_instance()
    
    # Get raw XML dump
    xml_content = adb.run("uiautomator dump").strip()
    
    # Extract the file path from the output
    match = re.search(r'to: (.*\.xml)', xml_content)
    if match:
        xml_file_path = match.group(1)
        # Get the content of the XML file
        xml_content = adb.run(f"cat {xml_file_path}")
    else:
        # If no file path found, try to get XML directly
        xml_content = adb.run("uiautomator dump /dev/tty")
    
    # Apply filters if provided
    if any([resource_id, text_value, content_desc, class_name]):
        xml_content = filter_xml_content(
            xml_content, 
            resource_id, 
            text_value, 
            content_desc, 
            class_name, 
            threshold
        )
    
    return xml_content

def filter_xml_content(xml_content, resource_id="", text_value="", content_desc="", class_name="", threshold=0.8):
    """
    Filter XML content based on provided criteria.
    
    Args:
        xml_content (str): Original XML content
        resource_id (str): Filter by resource ID
        text_value (str): Filter by text value
        content_desc (str): Filter by content description
        class_name (str): Filter by class name
        threshold (float): Similarity threshold for fuzzy matching
    
    Returns:
        str: Filtered XML content
    """
    # Simple implementation - in a real scenario, this would use proper XML parsing
    # and more sophisticated filtering with fuzzy matching based on threshold
    
    filtered_lines = []
    for line in xml_content.splitlines():
        match_score = 0
        total_criteria = 0
        
        if resource_id:
            total_criteria += 1
            if f'resource-id="{resource_id}"' in line:
                match_score += 1
            elif 'resource-id="' in line:
                # Partial matching based on threshold
                actual_id = re.search(r'resource-id="([^"]*)"', line)
                if actual_id and similarity_score(actual_id.group(1), resource_id) >= threshold:
                    match_score += threshold
        
        if text_value:
            total_criteria += 1
            if f'text="{text_value}"' in line:
                match_score += 1
            elif 'text="' in line:
                # Partial matching based on threshold
                actual_text = re.search(r'text="([^"]*)"', line)
                if actual_text and similarity_score(actual_text.group(1), text_value) >= threshold:
                    match_score += threshold
        
        if content_desc:
            total_criteria += 1
            if f'content-desc="{content_desc}"' in line:
                match_score += 1
            elif 'content-desc="' in line:
                # Partial matching based on threshold
                actual_desc = re.search(r'content-desc="([^"]*)"', line)
                if actual_desc and similarity_score(actual_desc.group(1), content_desc) >= threshold:
                    match_score += threshold
        
        if class_name:
            total_criteria += 1
            if f'class="{class_name}"' in line:
                match_score += 1
            elif 'class="' in line:
                # Partial matching based on threshold
                actual_class = re.search(r'class="([^"]*)"', line)
                if actual_class and similarity_score(actual_class.group(1), class_name) >= threshold:
                    match_score += threshold
        
        # If no criteria specified or the line matches the criteria
        if total_criteria == 0 or (total_criteria > 0 and match_score/total_criteria >= threshold):
            filtered_lines.append(line)
    
    return "\n".join(filtered_lines)

def similarity_score(str1, str2):
    """
    Calculate similarity score between two strings.
    
    Args:
        str1 (str): First string
        str2 (str): Second string
    
    Returns:
        float: Similarity score between 0 and 1
    """
    # Simple implementation - in a real scenario, this would use more sophisticated
    # algorithms like Levenshtein distance or other string similarity metrics
    
    # Convert to lowercase for case-insensitive comparison
    str1 = str1.lower()
    str2 = str2.lower()
    
    # Check if one string contains the other
    if str1 in str2 or str2 in str1:
        return 0.9  # High similarity but not perfect
    
    # Count matching characters
    matches = sum(c1 == c2 for c1, c2 in zip(str1, str2))
    
    # Calculate similarity based on length of longer string
    max_length = max(len(str1), len(str2))
    if max_length == 0:
        return 1.0  # Both strings are empty
    
    return matches / max_length

def find_elements_by_criteria(criteria):
    """
    Find UI elements matching the given criteria.
    
    Args:
        criteria (dict): Dictionary of criteria to match
    
    Returns:
        list: List of matching elements with their properties
    """
    xml_content = get_xml_dump()
    
    # Parse XML to find matching elements
    # This is a simplified implementation - in a real scenario, this would use proper XML parsing
    
    matching_elements = []
    node_pattern = r'<node[^>]*'
    
    for node_match in re.finditer(node_pattern, xml_content):
        node_str = node_match.group(0)
        
        # Extract node properties
        element = {}
        for prop in ['resource-id', 'class', 'text', 'content-desc', 'bounds']:
            prop_match = re.search(f'{prop}="([^"]*)"', node_str)
            if prop_match:
                element[prop] = prop_match.group(1)
        
        # Check if element matches all criteria
        matches = True
        for key, value in criteria.items():
            if key == 'threshold':
                continue  # Skip threshold parameter
                
            threshold = float(criteria.get('threshold', 0.8))
            
            # Map API parameter names to XML attribute names
            xml_key = key
            if key == 'id':
                xml_key = 'resource-id'
            elif key == 'value':
                xml_key = 'text'
            elif key == 'content_desc':
                xml_key = 'content-desc'
            
            if xml_key in element:
                if not (element[xml_key] == value or 
                        similarity_score(element[xml_key], value) >= threshold):
                    matches = False
                    break
            else:
                matches = False
                break
        
        if matches:
            matching_elements.append(element)
    
    return matching_elements

def get_accessibility_actions(node_id):
    """
    Get available accessibility actions for a specific node.
    
    Args:
        node_id (str): Node identifier
    
    Returns:
        list: Available accessibility actions
    """
    adb = get_adb_instance()
    
    # This is a simplified implementation - in a real scenario, this would use
    # the Android accessibility API to get available actions
    
    # Common accessibility actions
    common_actions = [
        {"name": "click", "description": "Click on the element"},
        {"name": "longClick", "description": "Long press on the element"},
        {"name": "scroll", "description": "Scroll from the element"},
        {"name": "setText", "description": "Set text on the element"}
    ]
    
    # If no specific node is requested, return common actions
    if not node_id:
        return common_actions
    
    # Get specific node information
    xml_content = get_xml_dump()
    node_pattern = f'<node[^>]*resource-id="{node_id}"[^>]*'
    node_match = re.search(node_pattern, xml_content)
    
    if not node_match:
        return []
    
    node_str = node_match.group(0)
    
    # Determine available actions based on node properties
    available_actions = []
    
    # All nodes support click
    available_actions.append({"name": "click", "description": "Click on the element"})
    
    # Long click is generally available
    available_actions.append({"name": "longClick", "description": "Long press on the element"})
    
    # Check if node is scrollable
    if 'scrollable="true"' in node_str:
        available_actions.append({"name": "scroll", "description": "Scroll from the element"})
    
    # Check if node can accept text input
    if 'class="android.widget.EditText"' in node_str or 'editable="true"' in node_str:
        available_actions.append({"name": "setText", "description": "Set text on the element"})
    
    return available_actions

def start_xml_server(port=8000):
    """
    Start a local server to provide XML dump functionality.
    
    Args:
        port (int): Port number to listen on
    
    Returns:
        tuple: Server object and server thread
    """
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, XMLDumpHandler)
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    return httpd, server_thread

def stop_xml_server(server):
    """
    Stop the XML dump server.
    
    Args:
        server: Server object to stop
    """
    if server:
        server.shutdown()

def get_device_ip():
    """
    Get the IP address of the connected Android device.
    
    Returns:
        str: IP address of the device
    """
    adb = get_adb_instance()
    
    # Get IP address from device
    output = adb.run("shell ip addr show wlan0")
    ip_match = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', output)
    
    if ip_match:
        return ip_match.group(1)
    
    # Try alternative interface
    output = adb.run("shell ip addr show eth0")
    ip_match = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', output)
    
    if ip_match:
        return ip_match.group(1)
    
    return None

def setup_port_forwarding(device_port=8000, host_port=8000):
    """
    Set up port forwarding from device to host.
    
    Args:
        device_port (int): Port on the device
        host_port (int): Port on the host
    
    Returns:
        bool: True if successful, False otherwise
    """
    adb = get_adb_instance()
    
    # Set up port forwarding
    result = adb.run(f"forward tcp:{host_port} tcp:{device_port}")
    
    return "error" not in result.lower()

def perform_accessibility_action(action, node_criteria, value=None):
    """
    Perform an accessibility action on a node matching the criteria.
    
    Args:
        action (str): Action to perform (click, longClick, scroll, setText)
        node_criteria (dict): Criteria to identify the node
        value (str, optional): Value for setText action
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Find matching elements
    elements = find_elements_by_criteria(node_criteria)
    
    if not elements:
        return False
    
    # Use the first matching element
    element = elements[0]
    
    # Extract bounds
    bounds_match = re.search(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', element.get('bounds', ''))
    if not bounds_match:
        return False
    
    x1, y1, x2, y2 = map(int, bounds_match.groups())
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    
    adb = get_adb_instance()
    
    # Perform the requested action
    if action == "click":
        adb.run(f"shell input tap {center_x} {center_y}")
        return True
    
    elif action == "longClick":
        adb.run(f"shell input swipe {center_x} {center_y} {center_x} {center_y} 1000")
        return True
    
    elif action == "scroll":
        # Scroll down by default
        end_y = center_y + 300
        if end_y > 2000:  # Avoid scrolling off screen
            end_y = 2000
        
        adb.run(f"shell input swipe {center_x} {center_y} {center_x} {end_y} 500")
        return True
    
    elif action == "setText" and value is not None:
        # First tap to focus
        adb.run(f"shell input tap {center_x} {center_y}")
        time.sleep(0.5)
        
        # Clear existing text
        adb.run("shell input keyevent KEYCODE_CTRL_LEFT KEYCODE_A")
        time.sleep(0.2)
        
        # Input new text
        adb.run(f"shell input text '{value}'")
        return True
    
    return False
