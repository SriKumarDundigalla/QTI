# Algorithm 2

### Algorithm Steps:

1. **Initialization**:
   - `all_chunks`: A list to store the final content chunks.
   - `sorted_file_contents`: The input `file_contents` list is sorted in descending order based on `token_size`. This sorting ensures that larger contents are considered first for chunk creation.
   - `used_indices`: A set to keep track of indices of `file_contents` that have been added to chunks. This set is crucial for ensuring content is not duplicated across chunks.

2. **Outer Loop - Processing Each Chunk**:
   - Continues as long as there are contents in `sorted_file_contents` that have not been marked as used (i.e., their indices are not in `used_indices`).
   - Within this loop, a new chunk (`current_chunk`) is started with an empty string, and its token count (`current_token_count`) is set to 0.

3. **Inner Loop - Adding Content to the Current Chunk**:
   - Iterates over `sorted_file_contents`. For each item (represented by `i` and `file_content`), the loop checks if the item's index is in `used_indices`. If so, it skips to the next item, as this content has already been added to a chunk.
   - If the item's index is not in `used_indices`, the function checks if adding this item's content to `current_chunk` would exceed the `context_window_size`.
     - If adding the content does not exceed the limit, the content is appended to `current_chunk`, and its `token_size` is added to `current_token_count`. The item's index is then added to `used_indices`.
     - If adding the content would exceed the limit, the item is skipped for the current chunk but remains eligible for future chunks.

4. **Finalizing the Current Chunk**:
   - After attempting to add content from all eligible items to `current_chunk`, the function checks if `current_chunk` contains any content.
     - If it does, `current_chunk` is added to `all_chunks`.
     - If not (which could happen if remaining contents are too large to fit the current context window), the outer loop is terminated to prevent an infinite loop.

5. **Completion**:
   - Once the outer loop completes (either because all content has been used or no more content can fit within the context window size), the function returns `all_chunks`.

### Tracking Mechanism (`used_indices`):

- The `used_indices` set is critical for managing which contents have already been added to chunks. By recording indices of `sorted_file_contents` that have been used, the function efficiently skips over these contents in subsequent iterations, ensuring that each piece of content is only used once.
- This tracking allows the function to dynamically adjust which contents are considered for each new chunk based on the remaining space in the context window, optimizing the content distribution across chunks.

### Efficiency Considerations:

- Sorting `file_contents` at the start and using `used_indices` to track content usage are key strategies for efficiently organizing content into chunks. 
- The use of a set for `used_indices` ensures quick lookups (O(1) complexity) to check whether an index has already been used, contributing to the overall efficiency of the function.
