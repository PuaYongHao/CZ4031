import java.util.ArrayList;

public class Node {

	private boolean isLeaf;
	private boolean isRoot;
	private ArrayList<Integer> keys;
	
	// Check parentnode, findSmallestKey, deleteNode
	
	// Constructor
	public Node() {
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
	
	// Get all keys in this node
	public ArrayList<Integer> getKeys() {
		return keys;
	}
	
	// Get key at certain index from this node
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
		for (i = 0; i < keys.size(); i++) {
			// If key is smaller than current element
			if (key < keys.get(i)) {
				// Insert the key to the front of this element
				keys.add(i, key);
				return i;
			}	
		}
		
		// Add key to the back since it is the largest value
		keys.add(key);
		return i;
	}
	
	// Delete all keys in this node
	public void deleteKeys() {
		keys = new ArrayList<Integer>();
	}
	
	// Delete key at certain index from this node
	public void deleteKeyAtIndex(int index) {
		keys.remove(index);
	}
	
	// Find smallest key
	public int findSmallestKey() {
		int key = -1;
		
		// If current node is  leaf
		if (this.getIsLeaf()) 
			key = this.getKeyAtIndex(0);
		
		return key;
	}
	
}
