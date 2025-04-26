# React Flow with Dagre.js - Tree Layout Example

A demonstration of integrating [dagre.js](https://github.com/dagrejs/dagre) with [React Flow](https://reactflow.dev/) to create simple tree layouts.

## Overview

This repository contains an example implementation of a tree layout visualization using React Flow and dagre.js. It demonstrates how to create hierarchical node structures with automatic layout positioning.

## Features

- **Automatic Tree Layout**: Uses dagre.js to automatically position nodes in a tree structure
- **Interactive Graph**: Nodes and edges can be interacted with (selected, dragged, etc.)
- **Customizable**: Easily customizable node and edge styles
- **Responsive**: Works well on different screen sizes

## Technologies Used

- **React**: Frontend library
- **React Flow**: Library for building node-based editors and interactive diagrams
- **dagre.js**: JavaScript library for graph layout, particularly directed graphs
- **CodeSandbox**: Development environment

## Use Cases

This example is useful for visualizing:

- Organizational charts
- Decision trees
- Hierarchical data structures
- Network topologies
- Dependency graphs

## Important Notes

This example demonstrates **static** layouting. If the nodes or edges in the graph change, the layout won't automatically recalculate. For dynamic layouting that updates when the graph changes, you would need to implement additional logic or refer to more advanced examples.

## Alternatives

If you're looking for more advanced layouting libraries, consider:

- [d3-hierarchy](https://github.com/d3/d3-hierarchy)
- [elkjs](https://github.com/kieler/elkjs)

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/shaneholloman/reactflow-test.git
   cd reactflow-test
   ```

2. Install dependencies:

   ```sh
   npm install
   # or
   yarn
   ```

3. Start the development server:

   ```sh
   npm start
   # or
   yarn start
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Usage

The example demonstrates:

1. How to set up a React Flow component
2. How to integrate dagre.js for automatic layout
3. How to style nodes and edges
4. How to handle user interactions

## License

This project is available under the MIT License. See the LICENSE file for more information.

## Acknowledgements

- [React Flow](https://reactflow.dev/) for the interactive diagram library
- [dagre.js](https://github.com/dagrejs/dagre) for the graph layout algorithm
- [CodeSandbox](https://codesandbox.io/) for the development environment
