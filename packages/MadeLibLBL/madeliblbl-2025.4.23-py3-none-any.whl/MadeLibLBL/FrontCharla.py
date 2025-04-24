import re

def transform_payload(payload_front):
    """
    Transforms the input payload structure into a simplified format for interactions,
    ignoring messages where 'role' is 'system'.

    Parameters
    ----------
    - payload_front (dict): The original payload dictionary containing conversation interactions.

    Returns
    -------
    - list of dict: A transformed list of dictionaries, where each dictionary represents an
                    interaction with keys:
                    - "role": The role of the speaker ("user" or "assistant").
                    - "content": A list containing a dictionary with the text of the interaction,
                                under the key "text".
    
    Example
    -------
    >>> payload_front = {
    ...     "inputs": [
    ...         [
    ...             {"role": "user", "content": "oi", "id_interaction": "...", "media": []},
    ...             {"role": "assistant", "content": "text here", "media": []},
    ...             {"role": "user", "content": "a parede", "id_interaction": "...", "media": []}
    ...         ]
    ...     ],
    ...     "parameters": {...}
    ... }
    >>> transform_payload(payload_front)
    [
        {'role': 'user', 'content': [{'text': 'oi'}]},
        {'role': 'assistant', 'content': [{'text': 'text here'}]},
        {'role': 'user', 'content': [{'text': 'a parede'}]}
    ]
    """

    # Extract the list of interactions from the payload
    interactions = payload_front.get("inputs", [[]])[0]

    # Transform and filter interactions
    transformed_payload = []
    for interaction in interactions:
        if interaction["role"] == "system":
            continue  # Ignore system messages

        transformed_entry = {
            "role": interaction["role"],
            "content": [{"text": interaction["content"]}]
        }
        transformed_payload.append(transformed_entry)

    return transformed_payload

def structure_to_conversation(structure):
    """Converts a structured conversation format into a flattened conversation history.
    
    Processes a list of message dictionaries containing roles and content, and transforms
    them into a formatted conversation string while tracking the last user input separately.

    Args
    ----
        structure (list): A list of message dictionaries where each contains:
            - role (str): Either 'user' or 'assistant'
            - content (list): List of content items where the first contains:
                - text (str): The message content
    
    Returns
    -------
        tuple: A tuple containing two elements:
            - str: The formatted conversation history with each message prefixed by **role**:
                   Example: "**user**: Hello\n**assistant**: Hi there"
            - str: The last user input in the structure (excluding the very last one if
                   it's a user message without a following assistant response)
    
    Note
    ----
        - The function skips adding the very last user message to the conversation history
          if it appears at the end of the structure (no following assistant response)
        - All messages are joined with newline characters
    
    Example
    -------
        >>> structure = [
        ...     {"role": "user", "content": [{"text": "Hello"}]},
        ...     {"role": "assistant", "content": [{"text": "Hi there"}]},
        ...     {"role": "user", "content": [{"text": "How are you?"}]}
        ... ]
        >>> structure_to_conversation(structure)
        ('**user**: Hello\\n**assistant**: Hi there', 'How are you?')
    """
    conversation_history = []
    user_last_input = ""

    for i, entry in enumerate(structure):
        role = entry["role"]
        text = entry["content"][0]["text"]
        
        if role == "user":
            user_last_input = text  # Store last user input
            if i == len(structure) - 1:
                break  # Skip adding last user input to conversation history
        
        conversation_history.append(f"**{role}**: {text}")
    
    return "\n".join(conversation_history), user_last_input

def conversation_to_structure(conversation_history, user_input):
    """Converts a formatted conversation string to a structured message format.
    
    Parses a conversation history string containing role-prefixed messages and combines it
    with the latest user input to create a list of message dictionaries in a standardized
    structure format.

    Args
    ----
        conversation_history (str): Formatted conversation string where each message is
                                   prefixed with **role**: (e.g., "**user**: Hello").
                                   Can be None or empty.
        user_input (str): The latest user input to be added to the structure.
                         Can be None or empty.

    Returns
    -------
        list: A list of message dictionaries where each contains:
            - role (str): Message originator ('user' or 'assistant')
            - content (list): List of content dictionaries with:
                - text (str): The message content

    Notes
    -----
        - Uses regex to parse the conversation history, looking for patterns like:
          "**user**: [message]" or "**assistant**: [message]"
        - Handles None/empty inputs gracefully
        - Strips whitespace from all message content
        - The user_input is always added as the last element when present

    Examples
    --------
        >>> conversation_to_structure(
        ...     "**user**: Hi\\n**assistant**: Hello!",
        ...     "How are you?"
        ... )
        [
            {'role': 'user', 'content': [{'text': 'Hi'}]},
            {'role': 'assistant', 'content': [{'text': 'Hello!'}]},
            {'role': 'user', 'content': [{'text': 'How are you?'}]}
        ]

        >>> conversation_to_structure(None, "Hello")
        [
            {'role': 'user', 'content': [{'text': 'Hello'}]}
        ]
    """
    structure = []
    
    # If there is history, process it first
    if conversation_history and isinstance(conversation_history, str):
        pattern = r'\*\*(user|assistant)\*\*:\s*(.*?)(?=\s*\*\*(user|assistant)\*\*:|$)'
        matches = re.findall(pattern, conversation_history, re.DOTALL)
        
        for match in matches:
            role = match[0]
            content = match[1].strip()
            structure.append({
                'role': role,
                'content': [{'text': content}]
            })
    
    # Add the last user input
    if user_input and isinstance(user_input, str):
        structure.append({
            'role': 'user',
            'content': [{'text': user_input.strip()}]
        })
    
    return structure

def transform_payload(payload_front):
    """
    Transforms the input payload structure into a simplified format for interactions,
    ignoring messages where 'role' is 'system'.

    Parameters
    ----------
    - payload_front (dict): The original payload dictionary containing conversation interactions.

    Returns
    -------
    - list of dict: A transformed list of dictionaries, where each dictionary represents an
                    interaction with keys:
                    - "role": The role of the speaker ("user" or "assistant").
                    - "content": A list containing a dictionary with the text of the interaction,
                                under the key "text".
    
    Example
    -------
    >>> payload_front = {
    ...     "inputs": [
    ...         [
    ...             {"role": "user", "content": "oi", "id_interaction": "...", "media": []},
    ...             {"role": "assistant", "content": "text here", "media": []},
    ...             {"role": "user", "content": "a parede", "id_interaction": "...", "media": []}
    ...         ]
    ...     ],
    ...     "parameters": {...}
    ... }
    >>> transform_payload(payload_front)
    [
        {'role': 'user', 'content': [{'text': 'oi'}]},
        {'role': 'assistant', 'content': [{'text': 'text here'}]},
        {'role': 'user', 'content': [{'text': 'a parede'}]}
    ]
    """

    # Extract the list of interactions from the payload
    interactions = payload_front.get("inputs", [[]])[0]

    # Transform and filter interactions
    transformed_payload = []
    for interaction in interactions:
        if interaction["role"] == "system":
            continue  # Ignore system messages

        transformed_entry = {
            "role": interaction["role"],
            "content": [{"text": interaction["content"]}]
        }
        transformed_payload.append(transformed_entry)

    return transformed_payload

def structure_to_conversation(structure):
    """Converts a structured conversation format into a flattened conversation history.
    
    Processes a list of message dictionaries containing roles and content, and transforms
    them into a formatted conversation string while tracking the last user input separately.

    Args
    ----
        structure (list): A list of message dictionaries where each contains:
            - role (str): Either 'user' or 'assistant'
            - content (list): List of content items where the first contains:
                - text (str): The message content
    
    Returns
    -------
        tuple: A tuple containing two elements:
            - str: The formatted conversation history with each message prefixed by **role**:
                   Example: "**user**: Hello\n**assistant**: Hi there"
            - str: The last user input in the structure (excluding the very last one if
                   it's a user message without a following assistant response)
    
    Note
    ----
        - The function skips adding the very last user message to the conversation history
          if it appears at the end of the structure (no following assistant response)
        - All messages are joined with newline characters
    
    Example
    -------
        >>> structure = [
        ...     {"role": "user", "content": [{"text": "Hello"}]},
        ...     {"role": "assistant", "content": [{"text": "Hi there"}]},
        ...     {"role": "user", "content": [{"text": "How are you?"}]}
        ... ]
        >>> structure_to_conversation(structure)
        ('**user**: Hello\\n**assistant**: Hi there', 'How are you?')
    """
    conversation_history = []
    user_last_input = ""

    for i, entry in enumerate(structure):
        role = entry["role"]
        text = entry["content"][0]["text"]
        
        if role == "user":
            user_last_input = text  # Store last user input
            if i == len(structure) - 1:
                break  # Skip adding last user input to conversation history
        
        conversation_history.append(f"**{role}**: {text}")
    
    return "\n".join(conversation_history), user_last_input

def conversation_to_structure(conversation_history, user_input):
    """Converts a formatted conversation string to a structured message format.
    
    Parses a conversation history string containing role-prefixed messages and combines it
    with the latest user input to create a list of message dictionaries in a standardized
    structure format.

    Args
    ----
        conversation_history (str): Formatted conversation string where each message is
                                   prefixed with **role**: (e.g., "**user**: Hello").
                                   Can be None or empty.
        user_input (str): The latest user input to be added to the structure.
                         Can be None or empty.

    Returns
    -------
        list: A list of message dictionaries where each contains:
            - role (str): Message originator ('user' or 'assistant')
            - content (list): List of content dictionaries with:
                - text (str): The message content

    Notes
    -----
        - Uses regex to parse the conversation history, looking for patterns like:
          "**user**: [message]" or "**assistant**: [message]"
        - Handles None/empty inputs gracefully
        - Strips whitespace from all message content
        - The user_input is always added as the last element when present

    Examples
    --------
        >>> conversation_to_structure(
        ...     "**user**: Hi\\n**assistant**: Hello!",
        ...     "How are you?"
        ... )
        [
            {'role': 'user', 'content': [{'text': 'Hi'}]},
            {'role': 'assistant', 'content': [{'text': 'Hello!'}]},
            {'role': 'user', 'content': [{'text': 'How are you?'}]}
        ]

        >>> conversation_to_structure(None, "Hello")
        [
            {'role': 'user', 'content': [{'text': 'Hello'}]}
        ]
    """
    structure = []
    
    # If there is history, process it first
    if conversation_history and isinstance(conversation_history, str):
        pattern = r'\*\*(user|assistant)\*\*:\s*(.*?)(?=\s*\*\*(user|assistant)\*\*:|$)'
        matches = re.findall(pattern, conversation_history, re.DOTALL)
        
        for match in matches:
            role = match[0]
            content = match[1].strip()
            structure.append({
                'role': role,
                'content': [{'text': content}]
            })
    
    # Add the last user input
    if user_input and isinstance(user_input, str):
        structure.append({
            'role': 'user',
            'content': [{'text': user_input.strip()}]
        })
    
    return structure