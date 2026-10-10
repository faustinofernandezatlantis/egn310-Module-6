# Contact Directory (BST vs Linear Scan)

A Streamlit application that manages a contact directory using a custom Binary Search Tree (BST) implementation.

## Features
- **Binary Search Tree Storage**: Contacts are stored and sorted alphabetically by name.
- **Ordered Listing**: In-order traversal (`O(n)`) renders contacts in sorted alphabetical order.
- **Search & Benchmark**: Compares BST lookup (`O(log n)`) against a Linear Scan (`O(n)`) in real-time milliseconds.
- **Delete & Insert**: Full support for node deletion (including the two-child case).

## Live Demo
🔗 **Deployed Application:** [https://faustino-fernandez-eng310-bst.streamlit.app/]

## How to Run Locally
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
