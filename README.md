# Algorithm 3
The `create_chunks_from_content_greedy_HT` function is designed to iteratively adjust the size of content chunks to minimize the size difference between the largest and smallest chunks. It employs a Greedy approach combined with an iterative adjustment of the context window size to meet a target difference or to optimize the chunk sizes as much as possible within a given number of iterations. Here's a detailed breakdown of the steps and processes involved in this algorithm:

### Step 1: Initialize Variables
- `context_window_size` is set to the `initial_context_window_size`.
- `iteration` tracks the number of adjustments made to the context window size.
- `best_chunks` stores the best chunk configuration found so far, based on the smallest difference between the largest and smallest chunks (`best_diff`).
- `best_diff` is initialized to infinity to ensure any first calculated difference will be considered better.

### Step 2: Iterative Adjustment Loop
- The algorithm enters a loop that will continue until either the maximum number of iterations (`max_iterations`) is reached or the target difference between chunk sizes (`target_diff`) is achieved.

### Step 3: Prepare for Chunk Creation
- Within each iteration, the function prepares a list of content pieces (`remaining_contents`), sorted by `token_size` in descending order, for chunk creation.
- A new set of chunks (`chunks`) is initialized along with variables for constructing the current chunk (`current_chunk` and `current_token_count`).

### Step 4: Greedy Chunk Filling
- The function enters a nested loop to fill chunks with content pieces from `remaining_contents`:
  - It attempts to add the largest piece that fits within the remaining space of the `context_window_size`.
  - Upon successfully adding a piece, it is removed from `remaining_contents`, and the loop restarts to find the next largest piece that fits.
  - If no piece can be added without exceeding `context_window_size`, the current chunk is finalized and added to `chunks`, and a new chunk is started.
  - This process repeats until no more pieces can be added to any chunk.

### Step 5: Evaluate and Store Best Configuration
- After all possible chunks are created for the current iteration, the function evaluates this configuration:
  - It calculates the size difference between the largest and smallest chunks.
  - If this difference is less than `best_diff`, the current configuration is stored as the best found so far.
  - The loop breaks early if the target difference is met or if there are no remaining content pieces to adjust.

### Step 6: Adjust Context Window Size
- If the target difference has not been met, the `context_window_size` is decreased by 1, and the next iteration begins, aiming to find a better chunk configuration with the adjusted window size.

### Step 7: Return Best Chunks
- Once the loop concludes (either by meeting the target difference, exhausting `max_iterations`, or running out of content pieces to adjust), the function returns the best chunk configuration found (`best_chunks`).

This algorithm uniquely combines a Greedy approach for chunk filling with an iterative process for optimizing chunk sizes relative to each other, aiming to minimize the variance in chunk sizes within the constraints of the specified parameters.

![Alt text for the image](https://github.com/SriKumarDundigalla/QTI/blob/AI-Algorithm-3/Algorithm3.png)

