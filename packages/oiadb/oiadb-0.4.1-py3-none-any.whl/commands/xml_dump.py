"""
Module for XML dump functionality with accessibility support.
Provides a local server to dump XML representation of the current UI hierarchy.
Optimized for speed and compatibility with all Android versions including Android 14.
"""

import socket
import threading
import re
import json
import time
import hashlib
import lxml.etree as ET
from functools import lru_cache
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from difflib import SequenceMatcher

from .core import get_adb_instance

# Cache for XML dumps to improve performance
XML_CACHE = {}
# Cache timeout in seconds
CACHE_TIMEOUT = 1.0
# Cache for parsed XML to avoid repeated parsing
PARSED_XML_CACHE = {}

class XMLDumpHandler(BaseHTTPRequestHandler):
    """HTTP request handler for XML dump server."""
    
    def _set_headers(self, content_type="application/xml"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress log messages to improve performance."""
        pass
    
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
                if key in query_params and query_params[key]:
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

@lru_cache(maxsize=32)
def get_xml_dump(resource_id="", text_value="", content_desc="", class_name="", threshold=0.8, use_cache=True):
    """
    Get XML dump of the current UI hierarchy with optional filtering.
    Optimized for speed with caching and efficient XML parsing.
    
    Args:
        resource_id (str): Filter by resource ID
        text_value (str): Filter by text value
        content_desc (str): Filter by content description
        class_name (str): Filter by class name
        threshold (float): Similarity threshold for fuzzy matching
        use_cache (bool): Whether to use cached XML if available
    
    Returns:
        str: XML representation of the UI hierarchy
    """
    global XML_CACHE
    
    # Create a cache key based on parameters
    cache_key = f"xml_{resource_id}_{text_value}_{content_desc}_{class_name}_{threshold}"
    
    # Check if we have a recent cached version
    if use_cache and cache_key in XML_CACHE:
        cache_time, xml_content = XML_CACHE[cache_key]
        if time.time() - cache_time < CACHE_TIMEOUT:
            return xml_content
    
    adb = get_adb_instance()
    
    # Try multiple methods to get XML dump, starting with the fastest
    xml_content = ""
    
    # Method 1: Direct dump to stdout (fastest, works on most devices)
    try:
        xml_content = adb.run("shell uiautomator dump /dev/tty")
        if "<hierarchy" in xml_content and "</hierarchy>" in xml_content:
            # Extract XML content between hierarchy tags
            match = re.search(r'(<hierarchy.*</hierarchy>)', xml_content, re.DOTALL)
            if match:
                xml_content = match.group(1)
    except:
        pass
    
    # Method 2: Standard dump to file then read (works on all devices)
    if not xml_content or "<hierarchy" not in xml_content:
        try:
            dump_result = adb.run("shell uiautomator dump").strip()
            match = re.search(r'to: (.*\.xml)', dump_result)
            if match:
                xml_file_path = match.group(1)
                xml_content = adb.run(f"shell cat {xml_file_path}")
        except:
            pass
    
    # Method 3: Use accessibility service for Android 10+ (including Android 14)
    if not xml_content or "<hierarchy" not in xml_content:
        try:
            # Check if we're on Android 10 or higher
            sdk_version = get_android_sdk_version()
            if sdk_version >= 29:  # Android 10+
                # Use accessibility service to get XML
                xml_content = adb.run("shell settings put secure enabled_accessibility_services com.android.uiautomator.accessibility.AccessibilityService")
                xml_content = adb.run("shell am instrument -w -e class androidx.test.uiautomator.UiAutomatorAccessibilityDump com.android.uiautomator.test/androidx.test.runner.AndroidJUnitRunner")
                # Extract XML from output
                match = re.search(r'(<hierarchy.*</hierarchy>)', xml_content, re.DOTALL)
                if match:
                    xml_content = match.group(1)
        except:
            pass
    
    # Apply filters if provided
    if xml_content and any([resource_id, text_value, content_desc, class_name]):
        xml_content = filter_xml_content(
            xml_content, 
            resource_id, 
            text_value, 
            content_desc, 
            class_name, 
            threshold
        )
    
    # Cache the result
    if xml_content:
        XML_CACHE[cache_key] = (time.time(), xml_content)
    
    return xml_content

def get_android_sdk_version():
    """
    Get the Android SDK version of the connected device.
    
    Returns:
        int: Android SDK version (e.g., 29 for Android 10)
    """
    adb = get_adb_instance()
    try:
        output = adb.run("shell getprop ro.build.version.sdk").strip()
        return int(output)
    except:
        return 0  # Default to 0 if unable to determine

def filter_xml_content(xml_content, resource_id="", text_value="", content_desc="", class_name="", threshold=0.8):
    """
    Filter XML content based on provided criteria using efficient XML parsing.
    
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
    # If no filtering criteria, return original content
    if not any([resource_id, text_value, content_desc, class_name]):
        return xml_content
    
    try:
        # Parse XML using lxml for better performance
        root = ET.fromstring(xml_content)
        
        # Find all nodes
        nodes = root.findall(".//node")
        
        # Track nodes to remove
        nodes_to_remove = []
        
        for node in nodes:
            match_score = 0
            total_criteria = 0
            
            if resource_id:
                total_criteria += 1
                node_id = node.get('resource-id', '')
                if node_id == resource_id:
                    match_score += 1
                elif similarity_score(node_id, resource_id) >= threshold:
                    match_score += threshold
            
            if text_value:
                total_criteria += 1
                node_text = node.get('text', '')
                if node_text == text_value:
                    match_score += 1
                elif similarity_score(node_text, text_value) >= threshold:
                    match_score += threshold
            
            if content_desc:
                total_criteria += 1
                node_desc = node.get('content-desc', '')
                if node_desc == content_desc:
                    match_score += 1
                elif similarity_score(node_desc, content_desc) >= threshold:
                    match_score += threshold
            
            if class_name:
                total_criteria += 1
                node_class = node.get('class', '')
                if node_class == class_name:
                    match_score += 1
                elif similarity_score(node_class, class_name) >= threshold:
                    match_score += threshold
            
            # If node doesn't match criteria, mark for removal
            if total_criteria > 0 and match_score/total_criteria < threshold:
                nodes_to_remove.append(node)
        
        # Remove non-matching nodes
        for node in nodes_to_remove:
            parent = node.getparent()
            if parent is not None:
                parent.remove(node)
        
        # Convert back to string
        return ET.tostring(root, encoding='utf-8', pretty_print=True).decode('utf-8')
    
    except Exception as e:
        # Fallback to regex-based filtering if XML parsing fails
        return regex_filter_xml_content(xml_content, resource_id, text_value, content_desc, class_name, threshold)

def regex_filter_xml_content(xml_content, resource_id="", text_value="", content_desc="", class_name="", threshold=0.8):
    """
    Fallback method to filter XML content using regex when XML parsing fails.
    
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

@lru_cache(maxsize=1024)
def similarity_score(str1, str2):
    """
    Calculate similarity score between two strings using efficient algorithm.
    Cached for performance.
    
    Args:
        str1 (str): First string
        str2 (str): Second string
    
    Returns:
        float: Similarity score between 0 and 1
    """
    if not str1 and not str2:
        return 1.0  # Both strings are empty
    
    if not str1 or not str2:
        return 0.0  # One string is empty
    
    # Convert to lowercase for case-insensitive comparison
    str1 = str1.lower()
    str2 = str2.lower()
    
    # Quick check for exact match
    if str1 == str2:
        return 1.0
    
    # Check if one string contains the other
    if str1 in str2 or str2 in str1:
        return 0.9  # High similarity but not perfect
    
    # Use SequenceMatcher for more accurate similarity
    return SequenceMatcher(None, str1, str2).ratio()

@lru_cache(maxsize=32)
def find_elements_by_criteria(criteria_dict):
    """
    Find UI elements matching the given criteria using efficient XML parsing.
    Cached for performance.
    
    Args:
        criteria_dict (dict): Dictionary of criteria to match
    
    Returns:
        list: List of matching elements with their properties
    """
    # Convert criteria_dict to a hashable tuple for caching
    criteria_items = tuple(sorted(criteria_dict.items()))
    
    # Create a copy of the criteria dictionary
    criteria = dict(criteria_items)
    
    # Extract threshold if present
    threshold = float(criteria.pop('threshold', 0.8))
    
    # Get XML dump
    xml_content = get_xml_dump()
    
    # Use cached parsed XML if available
    xml_hash = hashlib.md5(xml_content.encode()).hexdigest()
    if xml_hash in PARSED_XML_CACHE:
        root = PARSED_XML_CACHE[xml_hash]
    else:
        try:
            root = ET.fromstring(xml_content)
            PARSED_XML_CACHE[xml_hash] = root
        except:
            # Fallback to regex-based parsing if XML parsing fails
            return regex_find_elements_by_criteria(criteria_dict)
    
    # Find all nodes
    nodes = root.findall(".//node")
    
    matching_elements = []
    for node in nodes:
        # Extract node properties
        element = {}
        for attr in node.attrib:
            element[attr] = node.get(attr)
        
        # Check if element matches all criteria
        matches = True
        for key, value in criteria.items():
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

def regex_find_elements_by_criteria(criteria_dict):
    """
    Fallback method to find elements using regex when XML parsing fails.
    
    Args:
        criteria_dict (dict): Dictionary of criteria to match
    
    Returns:
        list: List of matching elements with their properties
    """
    # Create a copy of the criteria dictionary
    criteria = dict(criteria_dict)
    
    # Extract threshold if present
    threshold = float(criteria.pop('threshold', 0.8))
    
    # Get XML dump
    xml_content = get_xml_dump()
    
    matching_elements = []
    node_pattern = r'<node[^>]*'
    
    for node_match in re.finditer(node_pattern, xml_content):
        node_str = node_match.group(0)
        
        # Extract node properties
        element = {}
        for prop in ['resource-id', 'class', 'text', 'content-desc', 'bounds', 'package', 'checkable', 'checked', 'clickable', 'enabled', 'focusable', 'focused', 'scrollable', 'long-clickable', 'password', 'selected']:
            prop_match = re.search(f'{prop}="([^"]*)"', node_str)
            if prop_match:
                element[prop] = prop_match.group(1)
        
        # Check if element matches all criteria
        matches = True
        for key, value in criteria.items():
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
    Enhanced to support Android 14 accessibility features.
    
    Args:
        node_id (str): Node identifier
    
    Returns:
        list: Available accessibility actions
    """
    adb = get_adb_instance()
    
    # Get Android version to determine available actions
    sdk_version = get_android_sdk_version()
    
    # Common accessibility actions
    common_actions = [
        {"name": "click", "description": "Click on the element"},
        {"name": "longClick", "description": "Long press on the element"},
        {"name": "scroll", "description": "Scroll from the element"},
        {"name": "setText", "description": "Set text on the element"}
    ]
    
    # Add Android 10+ actions
    if sdk_version >= 29:  # Android 10+
        common_actions.extend([
            {"name": "scrollForward", "description": "Scroll forward from the element"},
            {"name": "scrollBackward", "description": "Scroll backward from the element"}
        ])
    
    # Add Android 14 specific actions
    if sdk_version >= 34:  # Android 14
        common_actions.extend([
            {"name": "contextClick", "description": "Context click (right-click) on the element"},
            {"name": "showTooltip", "description": "Show tooltip for the element"},
            {"name": "dismiss", "description": "Dismiss the element (e.g., close dialog)"}
        ])
    
    # If no specific node is requested, return common actions
    if not node_id:
        return common_actions
    
    # Get specific node information
    elements = find_elements_by_criteria({'id': node_id})
    
    if not elements:
        return []
    
    element = elements[0]
    
    # Determine available actions based on node properties
    available_actions = []
    
    # All nodes support click
    available_actions.append({"name": "click", "description": "Click on the element"})
    
    # Long click is generally available
    available_actions.append({"name": "longClick", "description": "Long press on the element"})
    
    # Check if node is scrollable
    if element.get('scrollable') == 'true':
        available_actions.append({"name": "scroll", "description": "Scroll from the element"})
        
        # Add directional scrolling for Android 10+
        if sdk_version >= 29:
            available_actions.append({"name": "scrollForward", "description": "Scroll forward from the element"})
            available_actions.append({"name": "scrollBackward", "description": "Scroll backward from the element"})
    
    # Check if node can accept text input
    if element.get('class') == 'android.widget.EditText' or element.get('editable') == 'true':
        available_actions.append({"name": "setText", "description": "Set text on the element"})
    
    # Add Android 14 specific actions based on properties
    if sdk_version >= 34:
        if element.get('clickable') == 'true':
            available_actions.append({"name": "contextClick", "description": "Context click (right-click) on the element"})
        
        if element.get('content-desc'):
            available_actions.append({"name": "showTooltip", "description": "Show tooltip for the element"})
        
        if element.get('class') in ['android.widget.Dialog', 'android.app.Dialog'] or 'dialog' in element.get('resource-id', '').lower():
            available_actions.append({"name": "dismiss", "description": "Dismiss the element (e.g., close dialog)"})
    
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
    Enhanced to support more network interfaces.
    
    Returns:
        str: IP address of the device
    """
    adb = get_adb_instance()
    
    # Try multiple network interfaces
    interfaces = ['wlan0', 'eth0', 'eth1', 'rmnet0', 'rmnet_data0']
    
    for interface in interfaces:
        output = adb.run(f"shell ip addr show {interface} 2>/dev/null")
        ip_match = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', output)
        
        if ip_match:
            return ip_match.group(1)
    
    # Try alternative method for Android 10+
    output = adb.run("shell ip route")
    ip_match = re.search(r'src\s+(\d+\.\d+\.\d+\.\d+)', output)
    
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
    Enhanced to support Android 14 accessibility features.
    
    Args:
        action (str): Action to perform (click, longClick, scroll, setText, etc.)
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
    bounds = element.get('bounds', '')
    bounds_match = re.search(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
    if not bounds_match:
        return False
    
    x1, y1, x2, y2 = map(int, bounds_match.groups())
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    
    adb = get_adb_instance()
    sdk_version = get_android_sdk_version()
    
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
    
    elif action == "scrollForward" and sdk_version >= 29:
        # Scroll right
        end_x = center_x + 300
        if end_x > 2000:  # Avoid scrolling off screen
            end_x = 2000
        
        adb.run(f"shell input swipe {center_x} {center_y} {end_x} {center_y} 500")
        return True
    
    elif action == "scrollBackward" and sdk_version >= 29:
        # Scroll left
        end_x = center_x - 300
        if end_x < 0:  # Avoid scrolling off screen
            end_x = 0
        
        adb.run(f"shell input swipe {center_x} {center_y} {end_x} {center_y} 500")
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
    
    # Android 14 specific actions
    elif action == "contextClick" and sdk_version >= 34:
        # Simulate context click (long press + tap)
        adb.run(f"shell input swipe {center_x} {center_y} {center_x} {center_y} 500")
        return True
    
    elif action == "showTooltip" and sdk_version >= 34:
        # Simulate hover (not directly supported, use long press instead)
        adb.run(f"shell input swipe {center_x} {center_y} {center_x} {center_y} 300")
        return True
    
    elif action == "dismiss" and sdk_version >= 34:
        # Try to dismiss by pressing back button
        adb.run("shell input keyevent KEYCODE_BACK")
        return True
    
    return False

def clear_cache():
    """
    Clear all caches to force fresh data retrieval.
    
    Returns:
        bool: True if successful
    """
    global XML_CACHE, PARSED_XML_CACHE
    XML_CACHE = {}
    PARSED_XML_CACHE = {}
    
    # Clear LRU caches
    similarity_score.cache_clear()
    find_elements_by_criteria.cache_clear()
    get_xml_dump.cache_clear()
    
    return True
