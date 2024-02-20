# Algorithm 2

The `create_chunks_from_content_greedy` function follows a specific series of steps to create content chunks using a Greedy approach. Here's a breakdown of the steps involved in this algorithm:

### 1. Initialize Variables
- `all_chunks`: A list to store the finalized content chunks.
- `current_chunk`: A string to accumulate content for the current chunk being built.
- `current_token_count`: An integer to track the total token count of the current chunk.

### 2. Sort Content by Token Size
- The input `file_contents` is sorted in descending order of `token_size`. This prioritization allows the algorithm to consider larger content pieces first, attempting to fit the largest possible pieces into each chunk under the context window limit.

### 3. Iterate Through Sorted Content
- The function iterates over each content piece in `sorted_file_contents`.

### 4. Check for New Chunk Necessity
- For each content piece, it checks if adding its `token_size` to `current_token_count` would exceed the `context_window_size`.
  - If it would exceed, and `current_chunk` is not empty, the current chunk is added to `all_chunks`, and both `current_chunk` and `current_token_count` are reset to start a new chunk.
  - This step ensures that each chunk does not exceed the specified `context_window_size`.

### 5. Add Content to Chunk
- If the current content piece fits within the remaining space of the `context_window_size` (including after possibly starting a new chunk), it is added to `current_chunk`, and its `token_size` is added to `current_token_count`.
  - A newline character is appended after each content piece for readability, ensuring that pieces start on new lines within the chunk.

### 6. Finalize Last Chunk
- After iterating through all content pieces, if there is any content accumulated in `current_chunk` that has not yet been added to `all_chunks`, it is added as the last chunk.

### 7. Return Result
- The function returns `all_chunks`, the list of content chunks created through this process.

### Greedy Approach Characteristics
- **Local Optimality**: At each step, the algorithm greedily adds the largest piece of content that fits within the remaining space of the current chunk or starts a new chunk if necessary.
- **No Backtracking**: Once a piece of content is placed in a chunk, the algorithm does not reconsider or rearrange past decisions, even if a different arrangement might have allowed for a more optimal use of space.
- **Efficiency**: The algorithm is designed for efficiency, making a single pass through the sorted content and making immediate decisions based on the current state.


