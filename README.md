# Algoritm 1
### Step 1: Initialize Variables
- `context_window_size` is set by converting `context_window_str` to an integer. This variable determines the maximum token size for each chunk.
- `all_chunks` is initialized as an empty list. This list will eventually contain all the content chunks that are created.
- `current_chunk` is initialized as an empty string. It temporarily holds the content being aggregated into the current chunk.
- `current_token_count` is set to 0. It keeps track of the number of tokens in `current_chunk`.

### Step 2: Iterate Over File Contents
- The function iterates over each item in `file_contents` using a `for` loop. Each item (`file_content`) represents a single file's content and associated metadata (like token size).

### Step 3: Process Each File's Content
- For each `file_content`, the function retrieves `content` (the actual text of the file) and `token_size` (the number of tokens in the file's content, converted to an integer for safety).

### Step 4: Check If Current Content Fits in the Current Chunk
- The function checks if adding the current file's `content` to `current_chunk` would cause the total number of tokens (`current_token_count + token_size`) to exceed `context_window_size`.
  - If not, the file's `content` is appended to `current_chunk`, and `current_token_count` is updated accordingly.
  - If yes, the function proceeds to the next steps to handle the overflow.

### Step 5: Handle Overflow and Start a New Chunk
- When the addition of the current file's `content` would exceed the `context_window_size`, the current state of `current_chunk` (before adding the new content) is appended to `all_chunks`. This marks the completion of the current chunk.
- Afterward, `current_chunk` is reset to contain just the current file's `content`, and `current_token_count` is reset to the current file's `token_size`.
- There's a special condition checked here: if the `token_size` of the current content itself exceeds the `context_window_size`, it is directly appended to `all_chunks` as its own chunk, and `current_chunk` and `current_token_count` are reset for the next iteration.

### Step 6: Finalize Remaining Content
- After iterating through all file contents, there might be content in `current_chunk` that hasn't been added to `all_chunks` yet (because it didn't trigger the overflow condition). The function checks if `current_chunk` is not empty and appends any remaining content to `all_chunks`.

### Step 7: Return the List of Chunks
- Finally, the function returns `all_chunks`, which now contains all the content chunks that have been created.

## Flow Chart



<img src="https://github.com/SriKumarDundigalla/QTI/blob/main/Algorithm1_Flow_Chart.png" alt="Image Description" style="width: 1000px; height: 1000px;"> 


