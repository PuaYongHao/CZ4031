package Index;

import java.util.ArrayList;

public class ParentNode extends Node {

	// Child node could be leaf node or parent node
	private ArrayList<Node> childNodes;
	
	// Constructor
	public ParentNode() {
		super();
		childNodes = new ArrayList<Node>();
	}
	
    // Get all child nodes
    public ArrayList<Node> getChildNodes() {
        return childNodes;
    }

    // Get child node at given index in this parent node
    public Node getChild(int index) {
        return childNodes.get(index);
    }
    
    // Add child node to the appropriate position
    public int addChildNode(Node childNode) {
    	// If parent node is empty
    	if (childNodes.size() == 0) {
    		childNodes.add(childNode);
    		// Set parent node of the child node to be current node
    		// This is possible as a reference to the object is passed
    		childNode.setParentNode(this);
    		return 0;
    	}
    	
    	int	key = childNode.findSmallestKey();
    	int currentSmallest = this.findSmallestKey();
    	int i;
    
    	// Index.Node that is going to be added has smaller key value
    	if (key < currentSmallest) {
    		// The leftmost child node key value is added
    		this.addKey(currentSmallest);
    		// Add the node to be the leftmost child node
    		this.childNodes.add(0, childNode);
    		i = 0;
    	}
    	else {
    		i = this.addKey(key);
    		// Pointer is key+1
    		this.childNodes.add(++i, childNode);
    	}
    	
    	childNode.setParentNode(this);
    	return i;
    }
    
    // Add child node at first index and reset the keys
    public void addChildNodeAtFirstIndex(Node childNode) {
    	this.childNodes.add(0, childNode);
    	childNode.setParentNode(this);
    	// Reset the keys
    	deleteKeys();
    	tallyKeysWithChildNodes();
    }
    
    // Delete a child node and reset the keys
    public void deleteChildNode(Node childNode) {
    	this.childNodes.remove(childNode);
    	// Reset the keys
    	deleteKeys();
    	tallyKeysWithChildNodes();
    }
    
    // Reset the keys according to the child nodes
    private void tallyKeysWithChildNodes() {
        for (int i = 0; i < this.childNodes.size(); i++) {
        	// The leftmost child node key value is not added
            if (i != 0)
                this.addKey(this.childNodes.get(i).findSmallestKey());
        }
    }
    
    // NEED TO REVIEW WITH OTHERS
    // Delete all child nodes
    public void deleteChildNodes() {
    	// Make sure keys and child nodes are always tally
    	deleteKeys();
    	childNodes = new ArrayList<Node>();
    }
    
    // Get the child node before
    public Node getBefore(Node node) {
    	// If it is not the first child node
        if (childNodes.indexOf(node) != 0)
            return childNodes.get(childNodes.indexOf(node) - 1);
        return null;
    }

    // Get the child node after
    public Node getAfter(Node node) {
    	// If it is not the last child node
        if (childNodes.indexOf(node) != childNodes.size() - 1)
            return childNodes.get(childNodes.indexOf(node) + 1);
        return null;
    }

	// NEED TO REVIEW WITH OTHERS
	@Override
	// Traverse the child node to find the smallest key
	public int findSmallestKey() {
		int key;
		// If child node is leaf node
		if (this.getChild(0).getIsLeaf())
			key = this.getChild(0).findSmallestKey();
		else {
			// Make a copy of child node
			ParentNode childNode = (ParentNode) this.getChild(0);
			// Traverse if the node is not leaf node
			while (!childNode.getIsLeaf())
				childNode = (ParentNode) childNode.getChild(0);
		}
		key = childNode.getKeyAtIndex(0);
		return key;
	}
	
	// NEED TO REVIEW WITH OTHERS
	// Delete current leaf node
	public void deleteNode() {
		super.deleteNode();
		this.childNodes = new ArrayList<Node>();
	}
    
}
