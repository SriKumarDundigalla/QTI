# Summary of MapReduce

MapReduce is a programming model and an associated implementation for processing and generating large data sets with a parallel, distributed algorithm on a cluster. The model is a simple way to parallelize computation across huge datasets using key-value pairs. It consists of two steps, Map and Reduce, where the Map function processes input data to produce intermediate key-value pairs, and the Reduce function processes these pairs to output the final result.

## Learning Outcomes

1. **Understanding MapReduce Concept:** Grasping the basic principles and components of the MapReduce model.

2. **MapReduce Algorithms:** Learning about designing and implementing algorithms using the MapReduce model.

3. **Data Processing with MapReduce:** Understanding data processing and handling large-scale data using MapReduce.

## Mapping of LO's to questions

| Learning Outcome | Corresponding Question Numbers |
|------------------|--------------------------------|
| Understanding MapReduce Concept | 1, 6, 11 |
| MapReduce Algorithms | 3, 7, 12 |
| Data Processing with MapReduce | 2, 5, 10 |

## Multiple Choice Questions and Answers

**1. What is MapReduce primarily used for?**
   A) Real-time data processing
   B) Large-scale data processing
   C) Web development
   D) Mobile app development
   **Answer: B) Large-scale data processing**

**2. Which of the following is a characteristic of MapReduce?**
   A) Low fault tolerance
   B) Real-time processing
   C) High scalability
   D) Sequential data processing
   **Answer: C) High scalability**

**3. In MapReduce, what is a 'Reducer'?**
   A) A function that splits data into smaller chunks
   B) A function that combines the output of the Map function
   C) A tool to distribute tasks across nodes
   D) A data storage component
   **Answer: B) A function that combines the output of the Map function**

**4. What does the 'Map' step in MapReduce do?**
   A) Reduces the data size
   B) Sorts the data
   C) Processes each data piece individually
   D) Combines the results
   **Answer: C) Processes each data piece individually**

**5. In the context of MapReduce, what is meant by 'shuffling'?**
   A) Discarding unnecessary data
   B) Sorting and transferring the output of the Map function to the Reducers
   C) Splitting data into smaller chunks for the Map function
   D) Encrypting data for secure processing
   **Answer: B) Sorting and transferring the output of the Map function to the Reducers**

**6. Which programming language is commonly used for writing MapReduce programs?**
   A) Python
   B) Java
   C) C#
   D) JavaScript
   **Answer: B) Java**

**7. What is the role of Hadoop in MapReduce?**
   A) It is a database system
   B) It provides a distributed file system and a framework for MapReduce operations
   C) It is a programming language
   D) It is a web server
   **Answer: B) It provides a distributed file system and a framework for MapReduce operations**

**8. How does MapReduce handle failure?**
   A) By restarting the entire process
   B) Through manual intervention
   C) By re-executing failed tasks on any available node
   D) By skipping the failed tasks
   **Answer: C) By re-executing failed tasks on any available node**

**9. In MapReduce, what is the importance of the 'key-value' pair?**
   A) It is used for sorting data only
   B) It is a format for storing data in the file system
   C) It organizes the output of the Map function for processing by the Reduce function
   D) It encrypts data for security
   **Answer: C) It organizes the output of the Map function for processing by the Reduce function**

**10. Can MapReduce be used for tasks other than processing large data sets?**
   A) No, it is exclusively for large data sets
   B) Yes, but it is not efficient
   C) Yes, it can be adapted for various types of data processing tasks
   D) No, it is only for data storage
   **Answer: C) Yes, it can be adapted for various types of data processing tasks**

**11. What is the main advantage of using MapReduce for large-scale data processing?**
   A) It requires less storage space
   B) It processes data sequentially for accuracy
   C) It is cheaper than traditional methods
   D) It can process data in parallel, reducing the processing time
   **Answer: D) It can process data in parallel, reducing the processing time**

**12. In MapReduce, how is data typically input and output?**
   A) Through a database
   B) As files in a distributed file system
   C) Via direct user input
   D) Through an API
   **Answer: B) As files in a distributed file system**

