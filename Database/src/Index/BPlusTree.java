package Index;

import Storage.Address;
import java.util.ArrayList;

public class BPlusTree {
	private static final int SIZE_POINTER = 8; // for 64 bits system; RAM use 64bit for addressing -> 2^6 = 6B
	private static final int SIZE_KEY = 4; // for int value
	int maxKeys; // Max number of keys per node
	int parentMinKeys; // Minimum number of key for non-leaf node, floor of (n/2)
	int leafMinKeys; // Minimum number of key for leaf node, floor of ((n+1)/2)
	Node root; // Root node
	int height; // to denote the depth of the tree
	int nodeCount; // to denote the number of node in the tree
	int deletedCount; // number of node deleted

	// Constructor for the BPlusTree
	// Take in blocksize so we can indicate how many keys there are by diving the
	// size
	public BPlusTree(int blockSize) {

		// Block --> store n number of key and n+1 number of pointer
		// max key = (blocksize - size of 1 pointer) / size of 1 key + size of 1
		// pointer)
		maxKeys = (blockSize - SIZE_POINTER) / (SIZE_KEY + SIZE_POINTER); // n
		parentMinKeys = (int) Math.floor(maxKeys / 2.0);
		leafMinKeys = (int) Math.floor((maxKeys + 1.0) / 2.0);
		System.out.println("init: blockSize = " + blockSize + ", maxKeys = " + maxKeys);
		System.out.println("MinKeys: parent=" + parentMinKeys + ", leaf=" + leafMinKeys);
		root = createFirst();
		nodeCount = 0;
		deletedCount = 0;
	}

	// to create first node
	public LeafNode createFirst() {
		LeafNode newRoot = new LeafNode();
		newRoot.setIsRoot(true);
		height = 1;
		nodeCount = 1;
		return newRoot;
	}

	// to insert a record into the tree
	public void insert(int key, Address address) {
		this.insertToLeaf(this.searchLeaf(key), key, address);
	}

	// to search for which leafnode the record should be stored at
	public LeafNode searchLeaf(int key) {
		// if root is a leaf, return root
		if (this.root.getIsLeaf()) {
			return (LeafNode) root;
		}
		// if root is not a leaf set, root = parent node
		ParentNode currentNode = (ParentNode) root;
		ArrayList<Integer> keys;
		// Transverse the tree to find the parent of the leafnode that the record should
		// be stored at
		while (!currentNode.getChildNodeAtIndex(0).getIsLeaf()) {

			keys = currentNode.getKeys();

			// iterate through the keys of currentNode
			for (int i = keys.size() - 1; i >= 0; i--) {

				if (keys.get(i) <= key) {

					currentNode = (ParentNode) currentNode.getChildNodeAtIndex(i + 1);
					break;
				}
				// if i is equal 0, means is smaller than every key
				if (i == 0) {
					currentNode = (ParentNode) currentNode.getChildNodeAtIndex(0);
					break;
				}
			}
		} // once the child is leaf, then stop

		// finding the leafnode by iterating the parent
		keys = currentNode.getKeys();
		for (int i = keys.size() - 1; i >= 0; i--) {

			if (keys.get(i) <= key)
				return (LeafNode) currentNode.getChildNodeAtIndex(i + 1);
		}

		return (LeafNode) currentNode.getChildNodeAtIndex(0);
	}

	// to insert record into leafnode
	public void insertToLeaf(LeafNode leaf, int key, Address address) {

		if (leaf.getKeys().size() < maxKeys)
			leaf.addRecord(key, address);

		else {// if leaf is full, need to split leaf, else just insert
			splitLeaf(leaf, key, address);
		}
	}

	// to split a full leafnode
	public void splitLeaf(LeafNode old, int key, Address address) {
		// temp values
		int tempKeys[] = new int[maxKeys + 1];
		Address tempAddresses[] = new Address[maxKeys + 1];
		LeafNode leaf2 = new LeafNode(); // new node
		int i;

		// getting full and sorted lists of keys and addresses
		for (i = 0; i < maxKeys; i++) {

			tempKeys[i] = old.getKeyAtIndex(i);
			tempAddresses[i] = old.getRecordAtIndex(i);
		}

		for (i = maxKeys - 1; i >= 0; i--) {

			if (tempKeys[i] <= key) {

				i++;
				tempKeys[i] = key;
				tempAddresses[i] = address;
				break;
			}

			tempKeys[i + 1] = tempKeys[i];
			tempAddresses[i + 1] = tempAddresses[i];
		}

		// clearing old leafnode values
		old.deleteRecords();

		// putting the keys and addresses into the two leafnodes
		for (i = 0; i < leafMinKeys; i++)
			old.addRecord(tempKeys[i], tempAddresses[i]);

		for (i = leafMinKeys; i < maxKeys + 1; i++)
			leaf2.addRecord(tempKeys[i], tempAddresses[i]);

		// setting old leafnode to point to new leafnode and new leafnode to point to
		// next leafnode
		leaf2.setNext(old.getNext());
		old.setNext(leaf2);

		// setting parents for new leafnode
		if (old.getIsRoot()) {

			ParentNode newRoot = new ParentNode();
			old.setIsRoot(false);
			newRoot.setIsRoot(true);
			newRoot.addChildNode(old);
			newRoot.addChildNode(leaf2);
			root = newRoot;
			height++;
		}

		else if (old.getParentNode().getKeys().size() < maxKeys)
			old.getParentNode().addChildNode(leaf2);

		else
			splitParent(old.getParentNode(), leaf2);

		// updating nodeCount
		nodeCount++;
	}

	// to split a full parent node
	public void splitParent(ParentNode parent, Node child) {

		Node children[] = new Node[maxKeys + 2];
		int tempKeys[] = new int[maxKeys + 2];
		int smallestKey = child.findSmallestKey();
		ParentNode parent2 = new ParentNode();

		// getting full and sorted lists of keys and children
		for (int i = 0; i < maxKeys + 1; i++) {

			children[i] = parent.getChildNodeAtIndex(i);
			tempKeys[i] = children[i].findSmallestKey();
		}

		for (int i = maxKeys; i >= 0; i--) {

			if (tempKeys[i] <= smallestKey) {

				i++;
				tempKeys[i] = smallestKey;
				children[i] = child;
				break;
			}

			tempKeys[i + 1] = tempKeys[i];
			children[i + 1] = children[i];
		}

		// clearing old parent values
		parent.deleteChildNodes();

		// Splitting the key into the two parents
		// (because number of pointer now is n + 2) (number of pointer = n/2 + 1) (then
		// partion left to be more so + 1 more)
		for (int i = 0; i < parentMinKeys + 2; i++)
			parent.addChildNode(children[i]);

		for (int i = parentMinKeys + 2; i < maxKeys + 2; i++)
			parent2.addChildNode(children[i]);

		// setting parent for the new parentnode
		if (parent.getIsRoot()) {

			ParentNode newRoot = new ParentNode();
			parent.setIsRoot(false);
			newRoot.setIsRoot(true);
			newRoot.addChildNode(parent);
			newRoot.addChildNode(parent2);
			root = newRoot;
			height++;
		}

		else if (parent.getParentNode().getKeys().size() < maxKeys)
			parent.getParentNode().addChildNode(parent2);

		else
			splitParent(parent.getParentNode(), parent2);

		// updating nodeCount
		nodeCount++;
	}

	// to delete all records of a certain key
	public void deleteKey(int key) {

		ArrayList<Integer> keys;
		LeafNode leaf;
		int count = 0;

		// while there are still records with given key value
		while (getRecordsWithKey(key).size() != 0) {

			// leaf = searchLeaf(key);
			leaf = getLeafNodeWithKey(key);
			keys = leaf.getKeys();
			// System.out.println("Still have keys to delete: " + keys);

			// delete one record and update tree
			for (int i = 0; i < keys.size(); i++) {

				if (keys.get(i) == key) {

					leaf.deleteRecordAtIndex(i);
					count++;

					// if leafnode is not root then update tree
					if (!leaf.getIsRoot())
						resetLeaf(leaf);

					break;
				}
			}
			// System.out.println(keys);
		}
		System.out.println("No more keys to delete...... ");
		System.out.println("number of 1000s deleted: " + count);
		nodeCount -= deletedCount;
		treeStats();
	}

	// Update leaf to fit the "balance tree criteria" ((n+1)/2) [leafMinKeys]
	public void resetLeaf(LeafNode node) {

		// if no need to change node, reset parent and finish
		if (node.getKeys().size() >= leafMinKeys) {

			resetParent(node.getParentNode());
			return;
		}

		// get the leafnode before and after of the currentNode
		LeafNode before = (LeafNode) node.getParentNode().getBefore(node);
		LeafNode after = (LeafNode) node.getParentNode().getAfter(node);
		int needed = leafMinKeys - node.getKeys().size();
		int bExtra = 0;
		int aExtra = 0;
		ParentNode parentToReset;

		// getting number of keys that before and after nodes can spare
		if (before != null) {
			bExtra += before.getKeys().size() - leafMinKeys;
		}

		if (after != null) {
			aExtra += after.getKeys().size() - leafMinKeys;
		}

		// if need to merge
		if (needed > aExtra + bExtra) {

			// if node has both before and after nodes
			if (before != null && after != null) {

				// insert as many records as possible into before node
				for (int i = 0; i < maxKeys - (bExtra + leafMinKeys); i++)
					before.addRecord(node.getKeyAtIndex(i), node.getRecordAtIndex(i));

				// insert the rest into after node
				for (int i = maxKeys - (bExtra + leafMinKeys); i < node.getKeys().size(); i++)
					after.addRecord(node.getKeyAtIndex(i), node.getRecordAtIndex(i));
			}

			// if node only has after node
			else if (before == null) {

				for (int i = 0; i < node.getKeys().size(); i++)
					after.addRecord(node.getKeyAtIndex(i), node.getRecordAtIndex(i));
			}

			// if node only has before node
			else {

				for (int i = 0; i < node.getKeys().size(); i++)
					before.addRecord(node.getKeyAtIndex(i), node.getRecordAtIndex(i));
			}

			// have to copy parent to reset after deleting leafnode
			parentToReset = node.getParentNode();

			// have to look for before node if it is not from the same parent
			if (before == null) {

				if (!parentToReset.getIsRoot())
					before = searchLeaf(parentToReset.findSmallestKey() - 1);
			}

			// change before to point to after
			before.setNext(node.getNext());

			// delete node
			node.deleteNode();
			deletedCount++;
		}

		// if able to borrow keys
		else {

			if (before != null && after != null) {

				// take the last few keys from before node that can be spared
				for (int i = 0; i < bExtra; i++) {

					node.addRecord(before.getKeyAtIndex(before.getKeys().size() - 1 - i),
							before.getRecordAtIndex(before.getKeys().size() - 1 - i));
					before.deleteRecordAtIndex(before.getKeys().size() - 1 - i);
				}

				// take the rest from after node
				for (int i = bExtra, j = 0; i < needed; i++, j++) {

					node.addRecord(after.getKeyAtIndex(j), after.getRecordAtIndex(j));
					after.deleteKeyAtIndex(j);
				}
			}

			else if (before == null) {

				// take all from after node
				for (int i = 0; i < needed; i++) {

					node.addRecord(after.getKeyAtIndex(i), after.getRecordAtIndex(i));
					after.deleteRecordAtIndex(i);
				}
			}

			else {

				// take all from before node
				for (int i = 0; i < needed; i++) {

					node.addRecord(before.getKeyAtIndex(before.getKeys().size() - 1 - i),
							before.getRecordAtIndex(before.getKeys().size() - 1 - i));
					before.deleteRecordAtIndex(before.getKeys().size() - 1 - i);
				}
			}

			parentToReset = node.getParentNode();
		}

		// update parents
		resetParent(parentToReset);
	}

	public void resetParent(ParentNode parent) {

		// if node is root
		if (parent.getIsRoot()) {

			// if root has at least 2 children, reset and return
			if (parent.getChildNodes().size() > 1) {

				// lazy man's reset
				Node child = parent.getChildNodeAtIndex(0);
				parent.deleteChildNode(child);
				parent.addChildNode(child);
				return;
			}

			// if root has 1 child, delete root level
			else {

				parent.getChildNodeAtIndex(0).setIsRoot(true);
				root = parent.getChildNodeAtIndex(0);
				parent.deleteNode();
				deletedCount++;
				height--;
				return;
			}
		}

		ParentNode before = (ParentNode) parent.getParentNode().getBefore(parent);
		ParentNode after = (ParentNode) parent.getParentNode().getAfter(parent);
		int needed = parentMinKeys - parent.getKeys().size();
		int bExtra = 0;
		int aExtra = 0;
		ParentNode parentToReset;

		if (before != null) {
			bExtra += before.getKeys().size() - parentMinKeys;
		}

		if (after != null) {
			aExtra += after.getKeys().size() - parentMinKeys;
		}

		// if need to merge
		if (needed > aExtra + bExtra) {

			// if node has both before and after nodes
			if (before != null && after != null) {

				// insert as many records as possible into before node
				for (int i = 0; i < maxKeys - (bExtra + parentMinKeys) + 1 && i < parent.getChildNodes().size(); i++)
					before.addChildNode(parent.getChildNodeAtIndex(i));

				// insert the rest into after node
				for (int i = maxKeys - (bExtra + parentMinKeys) + 1; i < parent.getChildNodes().size(); i++)
					after.addChildNode(parent.getChildNodeAtIndex(i));
			}

			// if node only has after node
			else if (before == null) {

				for (int i = 0; i < parent.getChildNodes().size(); i++)
					after.addChildNode(parent.getChildNodeAtIndex(i));
			}

			// if node only has before node
			else {

				for (int i = 0; i < parent.getChildNodes().size(); i++)
					before.addChildNode(parent.getChildNodeAtIndex(i));
			}

			// delete after merging
			parentToReset = parent.getParentNode();
			parent.deleteNode();
			deletedCount++;
		}

		// if able to borrow keys
		else {

			if (before != null && after != null) {

				// take the last few keys from before node that can be spared
				for (int i = 0; i < bExtra && i < needed; i++) {

					parent.addChildNodeAtFirstIndex(before.getChildNodeAtIndex(before.getChildNodes().size() - 1));
					before.deleteChildNode(before.getChildNodeAtIndex(before.getChildNodes().size() - 1));
				}

				// take the rest from after node
				for (int i = bExtra; i < needed; i++) {

					parent.addChildNode(after.getChildNodeAtIndex(0));
					after.deleteChildNode(after.getChildNodeAtIndex(0));
				}
			}

			else if (before == null) {

				// take all from after node
				for (int i = 0; i < needed; i++) {

					parent.addChildNode(after.getChildNodeAtIndex(0));
					after.deleteChildNode(after.getChildNodeAtIndex(0));
				}
			}

			else {

				// take all from before node
				for (int i = 0; i < needed; i++) {

					parent.addChildNodeAtFirstIndex(before.getChildNodeAtIndex(before.getChildNodes().size() - 1 - i));
					before.deleteChildNode(before.getChildNodeAtIndex(before.getChildNodes().size() - 1 - i));
				}
			}

			parentToReset = parent.getParentNode();
		}

		resetParent(parentToReset);
	}

	// Get Records with a target key (e.g. numVote = 500)
	public ArrayList<Address> getRecordsWithKey(int key) {
		ArrayList<Address> result = new ArrayList<>();
		int nonLeafAccess = 0; // count internal node accesses
		int leafNodeAccess = 0; // count leaf node accesses
		Node curNode = root;
		ParentNode parentNode;
		// search for leaf node
		while (!curNode.getIsLeaf()) {
			nonLeafAccess++;
			parentNode = (ParentNode) curNode;
			// System.out.println("Current index node: "+ curNode.getKeys());
			for (int i = 0; i < parentNode.getKeys().size(); i++) {
				if (key <= parentNode.getKeyAtIndex(i)) {
					// System.out.println("target "+ key +" is <= "+ parentNode.getKeyAtIndex(i));
					curNode = parentNode.getChildNodeAtIndex(i);
					break;
				}
				if (i == parentNode.getKeys().size() - 1) {
					// System.out.println("target "+key+" is larger than all of the keys, following
					// last pointer");
					curNode = parentNode.getChildNodeAtIndex(i + 1);
					break;
				}
			}
		}
		// find all leaf node keys index with the target key
		LeafNode curLeaf = (LeafNode) curNode;
		boolean done = false;
		while (!done && curLeaf != null) {
			leafNodeAccess++;
			for (int i = 0; i < curLeaf.getKeys().size(); i++) {
				if (curLeaf.getKeyAtIndex(i) == key) {
					// found leaf node key index with the target key
					result.add(curLeaf.getRecordAtIndex(i));
					continue;
				}
				// break if current leaf node key is larger than what we are searching for
				if (curLeaf.getKeyAtIndex(i) > key) {
					done = true;
					break;
				}
			}
			if (!done) {
				// if end of leaf node but key index is still smaller or equal to target key
				// go to next leaf node and continue scanning
				if (curLeaf.getNext() != null) {
					curLeaf = curLeaf.getNext();
				} else {
					break;
				}
			}
		}
		// System.out.println("Normal search method ====================");
		System.out.println(
				"Number of index node access (internal node + leaf node): " + (nonLeafAccess + leafNodeAccess));
		return result;
	}

	// this method is to return the first leaf node that contains the target key
	public LeafNode getLeafNodeWithKey(int key) {
		Node curNode = root;
		ParentNode parentNode;
		// search for leaf node
		while (!curNode.getIsLeaf()) {
			parentNode = (ParentNode) curNode;
			for (int i = 0; i < parentNode.getKeys().size(); i++) {
				if (key <= parentNode.getKeyAtIndex(i)) {
					curNode = parentNode.getChildNodeAtIndex(i);
					break;
				}
				if (i == parentNode.getKeys().size() - 1) {
					curNode = parentNode.getChildNodeAtIndex(i + 1);
					break;
				}
			}
		}
		// find the FIRST leaf node keys index with the target key
		LeafNode curLeaf = (LeafNode) curNode;
		boolean done = false;
		while (!done && curLeaf != null) {
			for (int i = 0; i < curLeaf.getKeys().size(); i++) {
				// found same key, immediately return
				if (curLeaf.getKeyAtIndex(i) == key) {
					return curLeaf;
				}
				// break if current leaf node key is larger than what we are searching for
				if (curLeaf.getKeyAtIndex(i) > key) {
					done = true;
					break;
				}
			}
			if (!done) {
				// if end of leaf node but key index is still smaller or equal to target key
				// go to next leaf node and continue scanning
				if (curLeaf.getNext() != null) {
					curLeaf = curLeaf.getNext();
				} else {
					break;
				}
			}
		}
		// no result found
		return null;
	}

	// print the current stats of the B+ tree
	public void treeStats() {

		ArrayList<Integer> rootKeys = new ArrayList<Integer>();
		ArrayList<Integer> firstKeys = new ArrayList<Integer>();
		ParentNode rootCopy = (ParentNode) root;
		Node first = rootCopy.getChildNodeAtIndex(0);

		for (int i = 0; i < root.getKeys().size(); i++) {

			rootKeys.add(root.getKeyAtIndex(i));
		}

		for (int i = 0; i < first.getKeys().size(); i++) {

			firstKeys.add(first.getKeyAtIndex(i));
		}

		System.out.println("The parameter n of the B+ tree: " + maxKeys);
		System.out.println("The number of nodes of the B+ tree: " + nodeCount);
		System.out.println("The number of levels of the B+ tree: " + height);
		System.out.println("The content of the root node (only the keys): " + rootKeys);
	}

	// called from MainApp
	// used for experiment 4 ranged query 30k to 40k
	public ArrayList<Address> getRecordsWithKeyInRange(int min, int max) {
		ArrayList<Address> result = new ArrayList<>();
		int nonLeafAccess = 0;
		int leafNodeAccess = 0;
		Node curNode = root;
		ParentNode parentNode;
		// search for leaf node
		while (!curNode.getIsLeaf()) {
			nonLeafAccess++;
			parentNode = (ParentNode) curNode;
			for (int i = 0; i < parentNode.getKeys().size(); i++) {
				if (min <= parentNode.getKeyAtIndex(i)) {
					curNode = parentNode.getChildNodeAtIndex(i);
					break;
				}
				if (i == parentNode.getKeys().size() - 1) {
					curNode = parentNode.getChildNodeAtIndex(i + 1);
					break;
				}
			}
		}
		// find all leaf node keys index with the target key
		// instead of just target key, we select values that are >= 30k and <=40k
		LeafNode curLeaf = (LeafNode) curNode;
		boolean done = false;
		while (!done && curLeaf != null) {
			leafNodeAccess++;
			for (int i = 0; i < curLeaf.getKeys().size(); i++) {
				if (curLeaf.getKeyAtIndex(i) >= min && curLeaf.getKeyAtIndex(i) <= max) {
					result.add(curLeaf.getRecordAtIndex(i));
					continue;
				}
				// if current leaf node key value is more than max, for example 40001, we break
				// and return
				if (curLeaf.getKeyAtIndex(i) > max) {
					done = true;
					break;
				}
			}
			if (!done) {
				// go to next leaf node if leaf node is still within range (e.g. 30k to 40k)
				if (curLeaf.getNext() != null) {
					curLeaf = (LeafNode) curLeaf.getNext();
				} else {
					break;
				}
			}
		}
		System.out.println(
				"Number of index node access (internal node + leaf node): " + (nonLeafAccess + leafNodeAccess));
		return result;
	}

}
