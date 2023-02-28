package Index;

import java.util.ArrayList;

public abstract class Node {

	private boolean isLeaf;
	private boolean isRoot;
	private ParentNode parentNode;
	private ArrayList<Integer> keys;
	
	// Constructor
	public Node() {
		keys = new ArrayList<Integer>();
		isLeaf = false;
		isRoot = false;
	}
	
	// Get if it is a leaf node
	public boolean getIsLeaf() {
		return isLeaf;
	}
	
	// Set if it is a leaf node
	public void setIsLeaf(boolean isLeaf) {
		this.isLeaf = isLeaf;
	}
	
	// Get if it is a root node
	public boolean getIsRoot() {
		return isRoot;
	}
	
	// Set if it is a root node
	public void setIsRoot(boolean isRoot) {
		this.isRoot = isRoot;
	}
	
    // Get parent node of this node 
    public ParentNode getParentNode() {
        return parentNode;
    }

    // Set parent node of this node 
    public void setParentNode(ParentNode parentNode) {
    	this.parentNode = parentNode;
    }
	
	// Get all keys in this node
	public ArrayList<Integer> getKeys() {
		return keys;
	}
	
	// Get key at given index from this node
	public int getKeyAtIndex(int index) {
		return keys.get(index);
	}
	
	// Add key in ascending order to the node and return index
	public int addKey(int key) {
		// If node is empty
		if (this.keys.size() == 0) {
			this.keys.add(key);
			return 0;
		}

		int i;
		// Start from first element
		for (i = 0; i < this.keys.size(); i++) {
			// If key is smaller than current element
			if (key < this.keys.get(i)) {
				// Insert the key to the front of this element
				this.keys.add(i, key);
				return i;
			}	
		}
		
		// Add key to the back since it is the largest value
		this.keys.add(key);
		return i;
	}
	
	// Delete all keys in this node
	public void deleteKeys() {
		keys = new ArrayList<Integer>();
	}
	
	// Delete key at given index from this node
	public void deleteKeyAtIndex(int index) {
		keys.remove(index);
	}
	
	// Find smallest key
	public abstract int findSmallestKey();
	
	// Delete node
	public void deleteNode() {
		// If there exist a parent node
		if (this.getParentNode() != null) {
			// Delete current leaf node from the parent node and reset its keys
			this.getParentNode().deleteChildNode(this);
			this.setParentNode(null);
		}
		isLeaf = false;
		isRoot = false;
		keys = new ArrayList<Integer>();
	}
	
}
