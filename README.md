# Algorithm 3

The `create_chunks_from_content_greedy_HT` function aims to dynamically adjust the context window size to balance the sizes of content chunks, utilizing a Greedy approach to select content for each chunk. Here's a step-by-step flow of how the algorithm works:

### Initialization
1. **Set Initial Conditions**: Initialize variables like `context_window_size` to the `initial_context_window_size`, set `iteration` to 0, and prepare empty lists for `best_chunks` and tracking the `best_diff` (difference between the largest and smallest chunk sizes).

### Iterative Adjustment Loop
2. **Start Iterative Process**: Begin a loop that will run up to `max_iterations` times, aiming to find the best chunk configuration that minimizes the size difference (`diff`) between the largest and smallest chunks.

### Chunk Creation Process
3. **Sort and Prepare Content**: Sort `file_contents` in descending order by `token_size` to prioritize larger content pieces. This sorting is done at the beginning of each iteration to reassess the content order as the context window size adjusts.
4. **Create Chunks with Current Window Size**: 
   - Initialize a new set of chunks (`chunks`) and reset `current_chunk` and `current_token_count` for accumulating content.
   - Use a nested loop to iterate through `remaining_contents`, attempting to add content to the current chunk without exceeding the `context_window_size`.
   - If a piece of content fits, add it to `current_chunk`, update `current_token_count`, and remove this piece from `remaining_contents`. Break the inner loop to re-evaluate the best next piece to add.

### Evaluating and Adjusting Chunks
5. **Evaluate Created Chunks**:
   - Once no more content can be added to the current chunk or `remaining_contents` is empty, evaluate the set of created chunks.
   - Calculate the size difference (`diff`) between the largest and smallest chunks.
   - If this `diff` is less than `best_diff`, update `best_chunks` and `best_diff` with the current configuration.

### Dynamic Adjustment
6. **Adjust Context Window Size**:
   - If the size difference (`diff`) is within the `target_diff` or there are no more contents to try adjusting, conclude the adjustment process.
   - Otherwise, decrement `context_window_size` to try a smaller window size in the next iteration, aiming to find a better balance between chunk sizes.

### Conclusion
7. **Finalize and Return Best Chunks**:
   - After completing all iterations or achieving the target size difference, return `best_chunks` as the optimal set of content chunks based on the dynamic adjustments.

### Greedy Selection Within Each Iteration
- The Greedy aspect of this algorithm manifests in how content is selected for each chunk: prioritizing the inclusion of the largest piece that fits within the remaining space of the current context window size, and then immediately removing it from further consideration.
- This Greedy choice is made within the context of the current iteration's window size, without foresight into how future adjustments to the window size or selections might affect overall optimality.

### Dynamic Window Adjustment
- The unique feature of this algorithm is its iterative adjustment of the context window size based on the observed size differences between chunks, aiming to minimize these differences and achieve a more balanced chunk configuration.



