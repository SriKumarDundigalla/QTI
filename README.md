# Algorithm 1

Here are the detailed steps of the `create_chunks_from_content` function with explanations of its loops and conditions:

### Step 1: Initialize Variables
- `all_chunks`: A list that will store the final content chunks.
- `current_chunk`: A string that temporarily accumulates content for the current chunk.
- `current_token_count`: An integer tracking the number of tokens in the `current_chunk`.

### Step 2: Iterate Through File Contents
- A for-loop iterates over each item in `file_contents`, a list of dictionaries where each dictionary contains the keys `content` (the text of the file) and `token_size` (the number of tokens in the text).

### Step 3: Process Each File Content
- For each `file_content` in the loop:
  - Retrieve the `content` and `token_size` from the dictionary.
  - Convert `token_size` to an integer to ensure it is in the correct format for arithmetic operations.

### Step 4: Check If Content Fits in the Current Chunk
- An if-statement checks whether adding the current file content's `token_size` to `current_token_count` would exceed `context_window_size`.
  - If **not exceeding**:
    - The file content is added to `current_chunk`.
    - `current_token_count` is incremented by the `token_size` of the current content.
  - If **exceeding**:
    - The `current_chunk` is appended to `all_chunks`, as it has reached or exceeded the `context_window_size`.
    - A new `current_chunk` is started with the current file content, and `current_token_count` is reset to the `token_size` of the current content.

### Step 5: Special Case for Large Content
- Within the else-block, there's a check to see if the `token_size` of the current content alone exceeds the `context_window_size`.
  - If so, the current content is directly appended to `all_chunks` as it cannot fit within any chunk without exceeding the limit.
  - A new `current_chunk` is started and initialized as an empty string, and `current_token_count` is reset to 0.

### Step 6: Finalize Last Chunk
- After the loop, there's a check if `current_chunk` contains any content (it may not have been added to `all_chunks` if the loop ended before reaching the `context_window_size` again).
  - If `current_chunk` is not empty, it is appended to `all_chunks`.

### Step 7: Return the Chunks
- The function returns `all_chunks`, the list containing all content chunks created.

## Flow Chart
![Flow Chart](https://github.com/SriKumarDundigalla/QTI/blob/AI-Algorithm-1/Algorithm%201%20Flow%20chart.png)
